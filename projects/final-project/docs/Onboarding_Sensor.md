---
title: "Onboarding de un sensor Sentinel-IT"
author: "Daniel Alarcon"
date: "2026-06-15"
tags: ["onboarding", "sensor", "sentinel-agent", "provisioning", "mtls", "systemd", "signing", "aws"]
---

# Onboarding de un sensor

## 1. Propósito y alcance

Esta guía describe el **alta end-to-end de un sensor** `sentinel-agent` en un host Linux: desde un servidor recién aprovisionado hasta un sensor que conecta por mTLS a AWS IoT Core, publica su **System Profile** a PI-5 y ejecuta comandos de mitigación firmados (Ed25519) bajo systemd.

Cubre: requisitos del host, la **invariante de identidad**, el provisioning de identidad mTLS (manual y fleet), la distribución y rotación de la clave de firma, la configuración de `sentinel.local.yml`, el despliegue con systemd y la verificación de la primera puesta en marcha.

No describe la **arquitectura interna** del sensor ni el diseño del subsistema Discovery — eso vive en [diseno_agente_discovery.md](diseno_agente_discovery.md) y en el [README del paquete](../sentinel-agent/README.md). Tampoco cubre el coordinador PI-5, que tiene su propia guía en [Configuration_and_Deployment.md](Configuration_and_Deployment.md).

## 2. Requisitos del host

| Componente | Requisito | Notas |
|------------|-----------|-------|
| Sistema operativo | Linux (Debian/Ubuntu base recomendado) | El sensor lee logs y ejecuta verbos de firewall; pensado para Linux |
| Python | `python3` (3.10+) + `pip` | El instalador lo instala vía `apt-get` si falta |
| Dependencias Python | `pyyaml`, `AWSIoTPythonSDK`, `cryptography` | En [`sentinel-agent/requirements.txt`](../sentinel-agent/requirements.txt) |
| Firewall | `iptables` o `nftables` | El executor aplica los verbos de bloqueo; el instalador avisa si falta |
| Privilegios | **root** (default) | Necesario para leer `/var/log/*` y manipular el firewall. `executor.run_as` permite de-escalar |
| Reloj | **NTP activo y sincronizado** | La firma valida `iat`/`exp` con un *skew* de 5 s; sin NTP, los comandos legítimos se rechazan |
| Red saliente | **8883/TCP** hacia `*.iot.eu-north-1.amazonaws.com` | MQTT sobre TLS (mTLS) con AWS IoT Core. Debe estar permitido en el firewall perimetral |

> **NTP no es opcional.** Si el reloj del sensor se desvía más de 5 s respecto al de PI-5, la verificación de firma rechaza los comandos por ventana de validez (`iat`/`exp`) aunque la firma sea criptográficamente correcta. Asegúrate de que `systemd-timesyncd`, `chrony` o `ntpd` está activo **antes** de poner el sensor en producción.

## 3. La invariante de identidad

El alta de un sensor gira en torno a una única invariante. **Todos estos valores tienen que ser idénticos:**

```text
device_id  ==  ThingName (AWS IoT)  ==  client_id MQTT  ==  <device_id> en seguridad/<device_id>/...  ==  campo "sensor" de cada mensaje
```

Es decir: el `device_id` que pones en [`sentinel.local.yml`](../sentinel-agent/sentinel.local.example.yml) tiene que coincidir **exactamente** con el `ThingName` del objeto creado en AWS IoT, con el `client_id` con el que el sensor abre la conexión MQTT, con el sufijo del topic de comandos `seguridad/<device_id>/comando` y con el campo `sensor` que viaja en cada mensaje.

**Por qué es crítica.** La [runtime policy del sensor](../sentinel-agent/provisioning/runtime-policy.json) autoriza la conexión usando `${iot:Connection.Thing.ThingName}` y PI-5 enruta los comandos al topic `seguridad/<device_id>/comando`. Si el `device_id` del sensor no coincide con su `ThingName`:

- El sensor **conecta y recibe eventos / telemetría** (los topics de subida usan comodines `seguridad/*`),
- pero PI-5 publica las órdenes en `seguridad/<ThingName>/comando`, un topic al que el sensor mal configurado **no está suscrito**.

Resultado: un sensor aparentemente sano que **nunca recibe comandos**. Es el fallo silencioso más frecuente del alta. Verifícalo antes que nada (ver §8).

## 4. Provisioning de identidad mTLS

El sensor se autentica contra AWS IoT Core con un certificado X.509 propio (mTLS). Hay dos modos de obtenerlo: **manual** (el default hoy) y **fleet provisioning** (cuando la flota crezca).

### 4.1 Modo MANUAL (≤ 5 sensores, recomendado hoy)

Es el procedimiento por defecto mientras la flota sea pequeña. Crea un certificado permanente por sensor y lo coloca en disco.

1. **Crear el Thing.** En la consola de AWS IoT (cuenta `582997418897`, región `eu-north-1`), crea un *Thing* cuyo **`ThingName` sea exactamente el `device_id`** que vas a usar (p. ej. `web-prod-01`). Respeta la invariante de §3.
2. **Generar el certificado X.509.** Al crear el Thing, genera un certificado y descarga los tres ficheros:
   - `device.cert.pem` — certificado del dispositivo,
   - `device.private.key` — clave privada (no la regenera nadie; guárdala bien),
   - `root-CA.crt` — raíz de Amazon (la misma para todos los dispositivos).
3. **Adjuntar la runtime policy del sensor.** Asocia al certificado la política de los sensores, [`sentinel-agent/provisioning/runtime-policy.json`](../sentinel-agent/provisioning/runtime-policy.json): autoriza la conexión con `${iot:Connection.Thing.ThingName}` **y acota cada sensor a `seguridad/<su device_id>/*`** (un sensor no puede tocar los topics de otro). Como usa la variable de conexión, **una sola policy vale para todos los sensores** siempre que se respete la invariante. (No la confundas con [`PI-5/Policy.json`](../PI-5/Policy.json), la policy —más amplia— del coordinador/dashboard, que sí necesita todo `seguridad/*`.) Recuerda **adjuntar el certificado al Thing** (no solo la policy al certificado): si el certificado no está vinculado al Thing, `${iot:Connection.Thing.ThingName}` queda vacío y la conexión se deniega (ver §9).
4. **Colocar los certificados en el host.** Copia los tres ficheros a `/etc/sentinel/certs/` con estos nombres (los que espera la plantilla de config):

   ```text
   /etc/sentinel/certs/
   ├── device.cert.pem
   ├── device.private.key      # chmod 600
   └── root-CA.crt
   ```

Estos ficheros **no se suben nunca a git**. Trátalos como secretos.

### 4.2 Modo FLEET (cuando la flota crezca)

Cuando el número de sensores supere la decena, el alta manual deja de escalar. La alternativa es **AWS IoT Fleet Provisioning**: cada sensor arranca con un **certificado *claim*** compartido (de privilegio mínimo) y, en el primer arranque, intercambia ese claim por su certificado permanente, que AWS genera al vuelo.

Las plantillas que sostienen este flujo viven en [`sentinel-agent/provisioning/`](../sentinel-agent/provisioning/):

- `provisioning-template.json` — plantilla de provisioning (define cómo se crea el Thing y se adjunta la policy a partir de los parámetros del claim),
- `claim-policy.json` — política mínima del certificado *claim* (solo lo justo para arrancar el intercambio),
- `runtime-policy.json` — política que hereda el certificado permanente una vez aprovisionado (equivalente fleet de la runtime policy de §4.1),
- `README.md` — procedimiento detallado de Fleet Provisioning.

La idea es que el **primer arranque auto-aprovisione**: el sensor presenta el claim, recibe su certificado permanente con `ThingName == device_id` y lo persiste en `/etc/sentinel/certs/`.

> **Aclaración honesta.** Hoy el **código del sensor asume un certificado permanente ya colocado en disco** (§4.1). El *bootstrap por claim* —que el propio sensor negocie su certificado en el primer arranque— **se incorporará cuando se adopte Fleet Provisioning** (Fase 5 del [diseño Discovery](diseno_agente_discovery.md)). Las plantillas de `provisioning/` ya están listas, pero el sensor todavía no las consume por sí mismo: por ahora, usa el modo manual.

## 5. Distribución de la clave de firma Ed25519

El sensor **solo verifica** las firmas de los comandos; nunca firma. Necesita la **clave pública** Ed25519 de PI-5 para validar cada orden antes de ejecutarla.

1. Copia la clave pública de PI-5 al host:

   ```text
   /etc/sentinel/sentinel_pi5_signing.pub
   ```

2. Apunta `signing.public_key_path` a esa ruta en `sentinel.local.yml` (ver §6).

Si la clave pública falta o la ruta es incorrecta, el sensor **no arranca** (no puede verificar nada, así que falla en seguro en lugar de ejecutar a ciegas).

### 5.1 Rotación sin downtime (clave *current* + *next*)

La clave de firma se rota sin parar el servicio gracias al esquema **doble clave** (la actual y la siguiente). El sensor acepta comandos firmados con **cualquiera de las dos** mientras dura la transición. El generador de claves está en [`scripts/generate_signing_keys.py`](../scripts/generate_signing_keys.py) y soporta los flags `--next` y `--promote`.

Procedimiento (lado sensor):

1. **PI-5 genera el par `next`** con `python scripts/generate_signing_keys.py --next` (no toca la clave actual; produce `sentinel_pi5_signing.next.pub`).
2. **Distribuye la `.next.pub`** a cada sensor, en `/etc/sentinel/sentinel_pi5_signing.next.pub`, y descomenta / añade en su `sentinel.local.yml`:

   ```yaml
   signing:
     public_key_path: "/etc/sentinel/sentinel_pi5_signing.pub"
     next_public_key_path: "/etc/sentinel/sentinel_pi5_signing.next.pub"
   ```

3. **Reinicia los sensores.** Ahora cada sensor acepta comandos firmados con la clave **actual O la next** — ventana de transición sin rechazos.
4. **PI-5 promociona** la `next` a actual con `python scripts/generate_signing_keys.py --promote`. Esto sobreescribe el par canónico (`.key`/`.pub`) con la clave `next` y elimina el par `.next`. **`PI-5/config.yml` no se toca:** `signing.private_key_path` sigue apuntando al `.key` estable (que ahora contiene la clave nueva), así que un restart de PI-5 nunca queda apuntando a un fichero inexistente.
5. **Reinicia PI-5 (coordinador *y* dashboard)** para que recarguen el `.key`. Ahora PI-5 firma con la clave nueva, que los sensores ya aceptan (es su `next`) → cero downtime. (Hasta este reinicio, PI-5 sigue firmando con la clave vieja desde memoria; los sensores también la aceptan.)
6. **Limpia los sensores:** copia la nueva `.pub` (ya la actual) a `signing.public_key_path`, retira `signing.next_public_key_path` y reinicia. **La nueva `.pub` debe estar físicamente en `public_key_path` antes del reinicio:** el sensor carga las claves una sola vez al arrancar y **no las recarga en caliente**.

El procedimiento completo (incluido el lado PI-5) está documentado también en la cabecera de [`scripts/generate_signing_keys.py`](../scripts/generate_signing_keys.py).

## 6. Configuración de `sentinel.local.yml`

Cada sensor tiene su propio fichero de configuración. Parte de la plantilla versionada y rellénala:

```bash
cp sentinel.local.example.yml sentinel.local.yml
```

La plantilla comentada vive en [`sentinel-agent/sentinel.local.example.yml`](../sentinel-agent/sentinel.local.example.yml). Campos a rellenar:

| Sección | Campo | Qué poner |
|---------|-------|-----------|
| (raíz) | `device_id` | **El identificador único** del sensor. Debe respetar la invariante de §3 |
| `aws` | `endpoint` | `aj4wsdnimoej8-ats.iot.eu-north-1.amazonaws.com` (fijo para el proyecto) |
| `aws` | `cert_path` / `key_path` / `root_ca` | Rutas a los certs de §4 (`/etc/sentinel/certs/...`) |
| `signing` | `public_key_path` | Clave pública de PI-5 (`/etc/sentinel/sentinel_pi5_signing.pub`) |
| `signing` | `next_public_key_path` | **Solo durante una rotación** (§5.1). Comentado el resto del tiempo |
| `executor` | `run_as` | `null` = root (default). Un usuario aquí de-escala la ejecución |
| `discovery` | `rediscovery_interval` | `0` = solo snapshot al arranque (default). `>0` activa el perfil vivo (Fase 3) |
| `detectors` | `thresholds` | Umbrales de detección; opcionales (sobreescriben los defaults) |
| `logging` | `file_path` / `level` | Log local del sensor |

Ejemplo mínimo coherente con las rutas de despliegue de esta guía:

```yaml
device_id: "web-prod-01"

aws:
  endpoint: "aj4wsdnimoej8-ats.iot.eu-north-1.amazonaws.com"
  cert_path: "/etc/sentinel/certs/device.cert.pem"
  key_path:  "/etc/sentinel/certs/device.private.key"
  root_ca:   "/etc/sentinel/certs/root-CA.crt"

signing:
  public_key_path: "/etc/sentinel/sentinel_pi5_signing.pub"

executor:
  run_as: null
```

## 7. Despliegue con systemd

El sensor se ejecuta como servicio de systemd. La unit canónica está en [`sentinel-agent/deploy/sentinel-agent.service`](../sentinel-agent/deploy/sentinel-agent.service); su `ExecStart` es `/usr/bin/python3 -m sentinel_agent --config /etc/sentinel/sentinel.local.yml` (systemd exige la ruta absoluta del intérprete) y su `WorkingDirectory` es `/opt/sentinel-agent`, donde debe estar desplegado el paquete `sentinel_agent/`.

Lo más cómodo es dejar que el **instalador** lo haga todo (ver §7.1). Si prefieres hacerlo a mano:

```bash
# 1. Desplegar el paquete donde lo busca la unit (WorkingDirectory=/opt/sentinel-agent)
sudo mkdir -p /opt/sentinel-agent
sudo cp -r sentinel-agent/sentinel_agent /opt/sentinel-agent/

# 2. Instalar la unit
sudo cp sentinel-agent/deploy/sentinel-agent.service /etc/systemd/system/

# 3. Recargar systemd para que la lea
sudo systemctl daemon-reload

# 4. Habilitar (arranque automático) y arrancar
#    (arranca SOLO si los certs, la clave de firma y sentinel.local.yml ya están)
sudo systemctl enable sentinel-agent.service
sudo systemctl start sentinel-agent.service

# 5. Ver el estado y los logs en vivo
sudo systemctl status sentinel-agent.service
sudo journalctl -u sentinel-agent -f
```

La unit fija `WorkingDirectory=/opt/sentinel-agent` (sin el paquete ahí, el arranque falla con `ModuleNotFoundError`), `Restart=on-failure`, `RestartSec=10` y dirige stdout/stderr al journal. Si arrancas el servicio sin los prerequisitos (certs, clave de firma, config), entrará en bucle de reinicio cada 10 s hasta que los coloques.

### 7.1 Instalador `install.sh`

El script [`sentinel-agent/scripts/install.sh`](../sentinel-agent/scripts/install.sh) automatiza el alta: comprueba root, instala dependencias del sistema y de Python, **despliega el paquete `sentinel_agent/` en `/opt/sentinel-agent`** (el `WorkingDirectory` de la unit), crea `/etc/sentinel/` y `/etc/sentinel/certs/`, **avisa** si faltan los certificados mTLS, la clave pública de firma o el `sentinel.local.yml` (no los genera — han de colocarse a mano según §4 y §5), copia el `sentinel.local.yml` si se le proporciona, e instala + habilita la unit. **Solo arranca el servicio si los prerequisitos están presentes**; si falta alguno, lo deja habilitado sin arrancar (para evitar el crash-loop) y lo arrancas tú con `sudo systemctl start sentinel-agent` al colocarlos.

```bash
cd sentinel-agent
sudo ./scripts/install.sh
```

## 8. Verificación / primera puesta en marcha

Recorre este checklist tras instalar. Si algún paso falla, salta a §9.

```text
[ ] El reloj está sincronizado por NTP:
       timedatectl status   → "System clock synchronized: yes"
[ ] El discovery imprime el System Profile sin errores (sin MQTT):
       python3 -m sentinel_agent --discover-only --device <device_id>
       (imprime el System Profile en JSON; --discover-only NO toca MQTT ni lee
        --config, así que el device_id se pasa con --device)
[ ] El servicio está activo:
       sudo systemctl status sentinel-agent  → "active (running)"
[ ] El sensor conectó a AWS IoT (sin errores de mTLS en el journal):
       sudo journalctl -u sentinel-agent -n 50 --no-pager
[ ] El System Profile del sensor aparece en PI-5 (dashboard / logs del coordinador).
[ ] Un comando de prueba firmado desde PI-5 se ejecuta en el sensor
       y el sensor publica su respuesta (eco con log_id) en seguridad/<device_id>/respuesta.
[ ] El device_id coincide con el ThingName y con el campo 'sensor' de los mensajes
       (la invariante de §3 — verifícalo aunque todo lo demás funcione).
```

> El flag `--discover-only` ejecuta el descubrimiento, imprime el perfil y sale **sin tocar MQTT**. Es la forma más rápida de comprobar que el sensor "ve" bien el host antes de conectarlo, y es útil además para preparar el provisioning.

## 9. Resolución de problemas frecuentes

| Síntoma | Causa raíz | Solución |
|---------|------------|----------|
| `Connect` denegado / desconexión inmediata tras el TLS handshake | El **certificado no está adjunto al Thing** → `${iot:Connection.Thing.ThingName}` queda vacío → la runtime policy no autoriza la conexión | En AWS IoT, adjunta el certificado al Thing correcto (no solo la policy al certificado). Reintenta |
| El sensor conecta y publica perfil/telemetría, **pero nunca recibe comandos** | `device_id` ≠ `ThingName`: PI-5 publica en `seguridad/<ThingName>/comando`, un topic al que el sensor no está suscrito (viola la invariante de §3) | Corrige `device_id` en `sentinel.local.yml` para que sea idéntico al `ThingName`, o recrea el Thing con el `ThingName` correcto. Reinicia el servicio |
| El servicio **no arranca**; el journal menciona la clave de firma | Falta `/etc/sentinel/sentinel_pi5_signing.pub` o la ruta de `signing.public_key_path` es incorrecta. El sensor falla en seguro en vez de ejecutar sin poder verificar | Copia la clave pública de PI-5 a `/etc/sentinel/` (§5) y corrige la ruta en la config |
| Los comandos llegan pero se rechazan por firma aunque PI-5 firme bien | Reloj desincronizado: `iat`/`exp` fuera de la ventana de 5 s, **o** PI-5 ya rotó a una clave nueva que el sensor no conoce | Activa/sincroniza NTP (§2). Si hay rotación en curso, distribuye la `.next.pub` y pon `next_public_key_path` (§5.1) |
| Comando firmado correctamente pero rechazado con `rejected_local_policy` | La **denylist local** del executor bloqueó un verbo destructivo (`rm`, `mkfs`, `dd`, `shutdown`…) por defensa en profundidad, independientemente de la firma | Es el comportamiento esperado. Revisa por qué PI-5 emitió ese comando; no se debe desactivar la barrera local |

---

**Enlaces útiles**

- Paquete del sensor: [`sentinel-agent/README.md`](../sentinel-agent/README.md)
- Plantilla de configuración: [`sentinel-agent/sentinel.local.example.yml`](../sentinel-agent/sentinel.local.example.yml)
- Entry point: [`sentinel-agent/sentinel_agent/__main__.py`](../sentinel-agent/sentinel_agent/__main__.py)
- Unit systemd: [`sentinel-agent/deploy/sentinel-agent.service`](../sentinel-agent/deploy/sentinel-agent.service)
- Instalador: [`sentinel-agent/scripts/install.sh`](../sentinel-agent/scripts/install.sh)
- Plantillas Fleet Provisioning: [`sentinel-agent/provisioning/`](../sentinel-agent/provisioning/)
- Runtime policy del sensor (aislada por device): [`sentinel-agent/provisioning/runtime-policy.json`](../sentinel-agent/provisioning/runtime-policy.json)
- Runtime policy del coordinador PI-5 (amplia): [`PI-5/Policy.json`](../PI-5/Policy.json)
- Generador/rotador de la clave de firma: [`scripts/generate_signing_keys.py`](../scripts/generate_signing_keys.py)
- Diseño del subsistema Discovery: [diseno_agente_discovery.md](diseno_agente_discovery.md)
