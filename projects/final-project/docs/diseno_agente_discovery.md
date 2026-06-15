---
title: "Diseño — Agente Discovery (sensor auto-configurable)"
author: "Daniel Alarcon"
date: "2026-06-13"
status: "FASES 1-5 IMPLEMENTADAS (Fase 5: Fleet como plantillas+guia; bootstrap por claim diferido)"
tags: ["discovery", "sensor", "pi4", "pi5", "system-profile", "design"]
---

# Agente Discovery — Diseño

> **Estado (2026-06-15):** las **Fases 1-5 están implementadas y testeadas** (287 tests: 196 PI-5 + 91 sensor). Fase 1: sensor genérico `sentinel-agent/` + ingesta del perfil + contexto al triage. Fase 2: manual genérico + overrides por device + motor `mitigation_manual`. Fase 3: perfil vivo + verbos de firewall en el Policy Engine. Fase 4: **enriquecedor LLM offline** (`profile_enricher`) que propone notas/fuentes de log/borradores de mitigación validados contra el perfil, fuera de la ruta caliente, honrando la dualidad de modelo api/local. Fase 5: **escalado de flota** — política de PI-4 migrada a `${...ThingName}`, **rotación de la clave de firma Ed25519 sin downtime** (set current+next en el sensor), Fleet Provisioning entregado como **plantillas IaC** (`sentinel-agent/provisioning/`) + **guía de onboarding** (`docs/Onboarding_Sensor.md`) + instalador/systemd, y retirada del monolito `agente_monitor3.py`. El bootstrap por claim en el sensor se incorporará cuando la flota lo requiera ([§10](#10-seguridad).5). Cada fase pasó por revisión adversarial; la de Fase 4 destapó un bug **transversal de seguridad alta** (salto de línea no tratado como separador en el Policy Engine → auto-ejecución sin HITL), ya corregido. Ver [§12 Plan por fases](#12-plan-por-fases), [§12.1 Limitaciones conocidas](#121-limitaciones-conocidas-de-la-fase-3) y el CHANGELOG.

## 1. Propósito

Hoy el sensor de PI-4 (`agente_monitor3.py`) está **cableado a un honeypot concreto**: rutas de log fijas, regexes por servicio, umbrales en código, `client_id` literal `Pi4-Felix` y ejecución de comandos como root sin filtro local. No se puede desplegar tal cual en otro servidor.

El objetivo es convertir ese sensor en un **agente Discovery genérico**: un agente que, al desplegarse en *cualquier* servidor Linux, **descubre solo** cómo funciona ese sistema (servicios, puertos, logs y sus formatos, servidor web, base de datos, firewall, OS, capacidades) y **pasa ese contexto al agente IA de PI-5** para que el triage y las mitigaciones se adapten al sistema real en vez de asumir el honeypot.

Este documento es la **propuesta de diseño** (no hay código todavía). Recoge la arquitectura recomendada, el esquema del *System Profile*, el contrato de mensajes, los cambios necesarios en cada componente, el plan por fases y las decisiones abiertas con su recomendación.

> **Qué NO cubre:** la implementación. Cada fase del [§12 Plan por fases](#12-plan-por-fases) se documentará y validará al construirla.

### Decisiones tomadas (2026-06-14)

Decisiones de alcance, acordadas antes de implementar, que condicionan el plan:

1. **Objetivo: servidores reales desde el principio.** No es un ejercicio de laboratorio: el sensor se desplegará en servidores de producción. → El **provisioning serio** y la **denylist local dura** son obligatorios desde la Fase 1.
2. **Ejecución como root (configurable).** Los comandos de mitigación se siguen ejecutando **como root** por defecto, como hoy — se descarta el de-escalado a usuario sin privilegios. La defensa añadida es la **denylist local dura** (rechaza verbos destructivos aunque la firma sea válida), que **no** cambia el privilegio de ejecución, solo añade una segunda barrera de contenido junto a la firma (que solo valida origen). `run_as` queda como opción de config para quien quiera de-escalar, pero el default es root.
3. **Visión completa directa (sin paralelo).** El monolito `agente_monitor3.py` fue un artefacto del TFG y **su servicio no está ni levantado**; no merece la pena mantenerlo en paralelo. El sensor genérico `sentinel-agent/` **es** el sensor desde el día uno, planteado ya a nivel completo, y el honeypot `Pi4-Felix` pasa a ser **simplemente un device configurado** (`sentinel.local.yml` con `device_id=Pi4-Felix`), no un caso especial. El monolito queda como legado/referencia y se retira cuando convenga.
4. **Recomendaciones: reestructurar ya.** `recommendations.json` se separa en manual genérico + overrides por device de forma temprana (Fase 2), porque es lo que de verdad deshardcodea a la IA del honeypot.

Estas decisiones están reflejadas en el [§12 Plan por fases](#12-plan-por-fases) y en el [§13](#13-decisiones-resueltas-y-de-implementación).

---

## 2. El problema: tres capas hardcodeadas

El sensor actual ata el sistema a este honeypot en tres capas independientes. Las tres hay que volverlas dinámicas:

| Capa | Dónde vive hoy | Qué está hardcodeado |
|------|----------------|----------------------|
| **Qué vigila** | `agente_monitor3.py:45-79` (retirado en Fase 5) | Rutas fijas `/var/log/vsftpd.log`, `/var/log/apache2/access.log`, JSON propietario de la app web; regexes `regex_ftp/apache/ssh`; umbrales `UMBRAL_*`/`VENTANA_*`/`INTERVALO_ENVIO` |
| **Qué sabe la IA del objetivo** | [recommendations.json](../PI-5/src/recommendations.json), [triage_agent.py:40](../PI-5/src/agents/triage_agent/triage_agent.py#L40) | Mitigaciones clavadas a `/home/lopex`, `/var/www/html/sentinelti.com`, puertos 80/8080, `restic`, `mysql`, `cerrar_sesion_admin.php`; el prompt asume "Bash terminal on the target IoT device" y firewall `iptables` |
| **Identidad y ejecución** | `agente_monitor3.py:29-42` (retirado en Fase 5), [Policy.json](../PI-4/Policy.json) | `client_id`, endpoint y certs fijos; ejecución con `subprocess.run(shell=True)` **como root, sin allowlist local**; política AWS IoT con client IDs literales |

> **Nota:** el `config.yml` de PI-4 existe pero **está desincronizado y `agente_monitor3.py` lo ignora** (declara `client_id` `Pi4-Felix-Sensor`, topics legacy y `/var/log/auth.log`, ninguno usado por el código real). No tomarlo como fuente de verdad.

---

## 3. La buena noticia: el contrato MQTT y la firma NO se tocan

El acoplamiento real **no está en el transporte**. El contrato entre sensor y coordinador es estrecho y estable, y un sensor genérico funciona sin tocar PI-5 siempre que lo respete al pie de la letra:

- **4 topics por dispositivo** `seguridad/<device>/{evento,telemetria,respuesta,comando}`. PI-5 enruta **solo por el sufijo** del topic (`/respuesta` → feedback_agent; el resto → triage_agent) y saca el `<device>` de `data['dispositivo'] || data['sensor']` ([main_coordinator.py:394](../PI-5/src/main_coordinator.py#L394), [:408](../PI-5/src/main_coordinator.py#L408)). PI-5 **no inspecciona el contenido para enrutar**.
- **Eco obligatorio de `log_id`** en las respuestas: PI-5 lo adjunta al comando firmado y el sensor lo devuelve, para correlación exacta comando↔respuesta (round-trip rápido del dashboard). Sin eco, se cae al fallback frágil de "última fila del dispositivo".
- **Firma Ed25519 con canonicalización byte-idéntica**: `json.dumps(sort_keys=True, separators=(",",":"))` excluyendo `sig`. Debe ser idéntica en ambos lados o **todo comando se rechaza**.

**Conclusión de diseño:** preservamos transporte + firma intactos. El trabajo está en (1) parametrizar el sensor, (2) añadir **un** tipo de mensaje nuevo —el perfil del sistema—, (3) persistirlo en PI-5 y (4) inyectarlo en el contexto del LLM. Detalle completo del contrato actual en [PI4_Referencia_Tecnica.md](PI4_Referencia_Tecnica.md) y [funcionamiento_mqtt.md](funcionamiento_mqtt.md).

---

## 4. Enfoque recomendado: "A+" (bootstrap + perfil vivo deduplicado)

Se evaluaron tres enfoques. El recomendado es **A+**: la base conservadora del enfoque *bootstrap* (cambios aditivos y de bajo riesgo en el cerebro de PI-5) con el injerto valioso del *perfil vivo* (re-descubrimiento periódico deduplicado por hash y topic dedicado), dejando la generación por LLM como herramienta **offline opcional** de fase tardía.

| Enfoque | Idea | Esfuerzo | Riesgo | Veredicto |
|---------|------|----------|--------|-----------|
| **A — Bootstrap** | Discovery una vez al arranque → perfil estático; PI-5 lo inyecta por evento | Medio | Bajo | **Base ganadora** (desplegable ya) |
| **B — Perfil vivo** | Re-descubrimiento continuo, monitorización reconfigurada en caliente, multi-tenant | Alto | Concurrencia en el sensor | Se toma lo barato y valioso (hash, re-descubrir, topic `/perfil`); se descarta la reconfiguración en caliente |
| **C — Agéntico (LLM)** | Un agente ADK en PI-5 interpreta los hechos y genera perfil + recomendaciones | Alto | No-determinismo, alucinación | Reservado como **enriquecedor offline** (Fase 4), nunca en la ruta caliente |

**Por qué A es la base, no C ni B puro:**

- **No C como base** — para un SOC auditable, que el perfil sea output de un LLM es peligroso: dos ejecuciones del mismo inventario dan perfiles distintos, y si el triage razona sobre un perfil alucinado propone comandos para un sistema que no existe. Un discovery determinista cubre el ~95% de los casos. La buena idea de C (usar el LLM para configuraciones raras frágiles de codificar a mano) se conserva como capacidad opcional offline.
- **No B puro** — B es la mejor arquitectura a largo plazo, pero su coste se concentra en lo más arriesgado de mantener para un solo desarrollador: **reconfigurar los tailers de log en caliente** (abrir/cerrar sin perder ni duplicar líneas) y elegir bien qué campos son "materiales" para el hash. Un bug ahí pierde eventos en silencio. En A+ un cambio de perfil que altere *qué se vigila* se aplica con **restart controlado** del proceso de monitorización, no con malabares de locks.
- **A es la base** — no reescribe el cerebro de PI-5 (triage, feedback, policy_engine, dashboard intactos), no toca transporte ni firma, no toca el esquema posicional de la tabla `logs` que lee el dashboard, conserva el eco de `log_id`, y aun así resuelve el problema central: **el perfil descubierto llega al LLM**. Es reversible: si el discovery falla, degrada a `unknown` y PI-5 sigue como hoy.

A+ entrega ~90% del valor de B con el riesgo y esfuerzo de A.

---

## 5. Arquitectura del sensor (`sentinel-agent/`)

**Paquete genérico nuevo, planteado a nivel completo desde el principio** (decisión §1.3). Es *el* sensor: el monolito `agente_monitor3.py` queda como legado (su servicio no corre) y el honeypot `Pi4-Felix` se configura como un device más (`sentinel.local.yml`). Vive en un directorio propio de primer nivel `sentinel-agent/` para señalar que es genérico, no atado a la Pi del honeypot. **Todo con `stdlib` de Python + utilidades base de Linux** — sin osquery/Wazuh/Filebeat (mala dependencia en ARM, duplican a PI-5; solo sirven de inspiración para el esquema de *facts*).

```
sentinel_agent/
├── discovery/            # probes independientes y degradables
│   ├── os_probe.py        # os-release + os.uname + systemd-detect-virt + geteuid
│   ├── services_probe.py  # ss -H -tlnp/-ulnp (puerto→proceso→binario); systemctl -o json; fallback /proc/net/tcp
│   ├── stack_probe.py     # cruza proceso de ss con `command -v` + nginx -V/apache2ctl -V/mysqld --version; detecta reverse-proxy 80→8080
│   ├── log_probe.py       # deriva rutas+formato DESDE la config del servicio y logrotate.d; journalctl -o json para systemd
│   ├── firewall_probe.py  # gestor ACTIVO: ufw status / firewall-cmd / nft list ruleset / iptables -S (+ backend nft vs legacy)
│   ├── caps_probe.py      # command -v restic/fail2ban/mysql/docker/php + gestor de paquetes (dpkg-query/rpm/apk)
│   ├── users_probe.py     # getent passwd/group sudo|wheel, sudoers.d
│   └── surface_probe.py   # binds no-loopback cruzados con el firewall
├── profile_builder.py    # ensambla el System Profile, calcula profile_hash + profile_version
├── monitor.py            # lee sentinel.local.yml: tailers (FileTailer / JournalTailer) + detectores declarativos
├── parsers/              # parsers en Python por tipo de servicio (sshd_auth, nginx_access, apache_clf, vsftpd, app_json)
├── executor.py           # verifica firma Ed25519 (reusado) + denylist LOCAL + usuario de-escalado
└── transport.py          # cliente MQTT + cola de publicación + firma (reusados); deriva los 4 topics de un device_id
```

**Principios:**

- **Probes degradables.** Cada probe va en `try/except` con timeout; un fallo degrada *su* sección a `unknown`/`[]` sin tumbar el snapshot. Si falta `ss`/`systemctl` o no hay root, cae a fallback (`/proc/net/tcp`) y marca la sección en `degraded`.
- **Fuentes estructuradas sobre parseo de texto.** `os-release` (no `lsb_release`), `os.uname` (no shell), `ss -H` (no `netstat`), `systemctl -o json`, `journalctl -o json`. `command -v` (no `which`).
- **Rutas y formatos de log desde la config real del servicio** (`nginx -V`, `apache2ctl -V`, `my.cnf`, `logrotate.d`), no rutas `/var/log` fijas.
- **Identificación por proceso, no por puerto.** El puerto 80 puede ser un proxy (el caso 80→8080 del honeypot). Se resuelve puerto→proceso→binario→versión.
- **Firewall: gestor ACTIVO, no solo binarios.** En Debian 11+/RHEL 8+ `iptables` suele ser `iptables-nft` conviviendo con `ufw`/`firewalld`; reglas crudas pueden romperse al recargar.
- **Detectores declarativos, parsers en Python (decisión [§13](#13-decisiones-abiertas-y-recomendación)).** Los umbrales/ventanas/listas de patrones (SQLi/XSS) van en `sentinel.local.yml`; los parsers de formatos raros van en Python seleccionados por `log_source.parser`.
- **Reuso del contrato:** la verificación Ed25519 ([signing.py](../sentinel-agent/sentinel_agent/signing.py), el verificador con clave pública) se porta al paquete genérico **idéntica byte a byte** en la canonicalización; el cliente MQTT y la cola de publicación se reescriben limpios en el paquete (el patrón del monolito sirve de referencia).
- **Ejecución como root** (decisión §1.2): `executor.py` mantiene `shell=True` como root por defecto; `run_as` opcional en config para de-escalar. La barrera nueva es la **denylist local**, no el privilegio.

**Ciclo:** snapshot al arranque → publica el perfil a `seguridad/<device>/perfil` → arranca monitorización. Re-descubrimiento periódico (p. ej. 600 s) y on-demand vía comando firmado `{accion:"redescubrir"}`; **republica solo si `profile_hash` cambia**. Un cambio en *qué vigilar* se aplica con **restart controlado** del proceso, no reconfigurando tailers en caliente.

---

## 6. Arquitectura del coordinador (PI-5) — cambios aditivos

Sin tocar el routing por sufijo, la firma ni el esquema posicional de `logs`:

1. **BD** ([database.py](../PI-5/src/database.py) `init_schema`): nueva tabla `device_profiles` con `CREATE TABLE IF NOT EXISTS`. **No** se añaden columnas a `logs` (el dashboard la lee por índice posicional `row[8]..row[13]`).
2. **`db_tools.py`**: `upsert_device_profile(device, profile_json, schema_version, profile_version, profile_hash, discovered_at)` que **salta el write si el hash no cambió**, y `get_device_profile(device) -> dict`.
3. **`process_event`** ([main_coordinator.py:~408](../PI-5/src/main_coordinator.py#L408), **antes** de enrutar al triage): rama para el sufijo `/perfil` → `upsert` en un executor thread y `return` (no consume cuota de Gemini, no crea fila en `logs`). Red de seguridad: telemetría con `tipo == "PERFIL_SISTEMA"` desviada al mismo upsert. Añadir la suscripción `seguridad/+/perfil` en [main:~514](../PI-5/src/main_coordinator.py#L514) + `topic_subscribe_perfil` en `config.yml`.
4. **`profile_context.py`** (nuevo): `get_profile(device)` cacheado e invalidado por `profile_version` + `render_profile_block(profile)` → bloque compacto de contexto.
5. **`_run_agent_event`** ([main_coordinator.py:195-197](../PI-5/src/main_coordinator.py#L195)): solo en `queue_type=='triage'`, anteponer el bloque `### CONTEXTO DEL SISTEMA OBJETIVO` al `raw_log`. **Clave:** la sesión ADK es **única y compartida** entre dispositivos ([main:470-472](../PI-5/src/main_coordinator.py#L470)) → el contexto **no puede vivir en el estado de sesión**; se inyecta **por evento** desde BD con caché.
6. **`triage_agent.py`** ([:40](../PI-5/src/agents/triage_agent/triage_agent.py#L40)): cambiar `"executed in a Bash terminal on the target IoT device"` por una referencia al bloque de contexto (host Linux genérico si ausente), eligiendo firewall/paquetes/rutas según ese bloque.
7. **`consultar_manual_mitigacion`** ([iot_tools.py:315-350](../PI-5/src/tools/iot_tools.py#L315)): aceptar `device`, leer su perfil y filtrar por firewall/capabilities reales. Ante 0 coincidencias, devolver un **manual genérico parametrizado**, no el del honeypot (hoy [:339](../PI-5/src/tools/iot_tools.py#L339) devuelve todo el manual, contaminando cualquier decisión con rutas de `/home/lopex`).

---

## 7. El System Profile (esquema)

Snapshot estructurado, determinista y versionado. Cada bloque proviene de un probe y degrada independiente sin romper.

```jsonc
{
  "tipo": "PERFIL_SISTEMA",
  "schema_version": 1,
  "sensor": "web-prod-01",          // == sufijo del topic y campo de routing
  "dispositivo": "web-prod-01",     // alias (PI-5 lee dispositivo||sensor)
  "profile_version": 7,             // incremental por cambio material (invalida caché en PI-5)
  "profile_hash": "sha256:ab12...", // hash de SECCIONES MATERIALES (dedupe de upsert/republicación)
  "agent_version": "sentinel-agent/0.1.0",
  "discovered_at": "2026-06-13T10:22:31Z",   // NO entra en el hash
  "trigger": "boot",                // boot | on_demand | periodic
  "host": {"hostname":"...","os_id":"debian","os_version":"12","pretty_name":"...",
           "kernel":"6.1.0","arch":"aarch64","virt":"none","init":"systemd","is_root":true},
  "package_manager": "apt",         // apt | dnf | apk | pacman | unknown
  "firewall": {"active_manager":"nftables","active":true,"backend":"iptables-nft",
               "managers_present":["nft","iptables"]},
  "web_server": {"engine":"nginx","version":"1.22.1","config_paths":["/etc/nginx/nginx.conf"],
                 "docroots":["/var/www/html"],"reverse_proxy_to":[8080]},
  "db_engine": {"engine":"mysql","version":"8.0","config_path":"/etc/mysql/my.cnf",
                "listen":[{"port":3306,"bind":"127.0.0.1"}]},
  "services": [{"unit":"ssh.service","port":22,"bind":"0.0.0.0","proc":"sshd",
                "exe":"/usr/sbin/sshd","active":true}],
  "log_sources": [
    {"id":"ssh","service":"ssh","source":"journald","unit":"ssh.service","path":null,
     "format":"journald-json","parser":"sshd_auth","detectors":["ssh_bruteforce"]},
    {"id":"web_access","service":"nginx","source":"file","unit":null,
     "path":"/var/log/nginx/access.log","format":"combined","parser":"nginx_access",
     "detectors":["web_bruteforce","sqli","xss"]}
  ],
  "capabilities": {"restic":false,"fail2ban":true,"docker":false,"mysql_client":true,"php":false},
  "users": {"sudoers":["admin"],"sudo_group":"sudo","recent_logins":[]},
  "surface": {"exposed_ports":[22,80],"loopback_only":[3306],"internet_facing":true},
  "degraded": ["ss_no_root"]        // [] si discovery corrió completo
}
```

**Reglas:**

- `sensor`/`dispositivo` **deben coincidir** con el sufijo del topic `/comando` o el sensor recibe eventos pero **nunca** comandos.
- `profile_hash` se calcula **solo** sobre `host`, `package_manager`, `firewall`, `web_server`, `db_engine`, `services`, `log_sources`, `capabilities`. Excluye `discovered_at`, `profile_version`, `trigger`, PIDs y `since` para no republicar cada ciclo.
- Cabe holgadamente bajo el límite de ~128 KB de AWS IoT; si crece, truncar `services`/`users` a lo expuesto.

---

## 8. Contrato de mensajes definitivo

Único cambio de transporte: **añadir el topic `/perfil`**. Todo lo demás se conserva.

| Quién | Topic | Cambio |
|-------|-------|--------|
| Sensor **publica** | `/evento`, `/telemetria`, `/respuesta` | Sin cambios |
| Sensor **publica** | `/perfil` | **NUEVO** — payload = System Profile JSON |
| Sensor **escucha** | `/comando` | Sin cambios (firmado) |
| PI-5 **suscribe** | `seguridad/+/{telemetria,evento,respuesta}` | Existentes |
| PI-5 **suscribe** | `seguridad/+/perfil` | **NUEVO** ([main:514-516](../PI-5/src/main_coordinator.py#L514) + `config.yml`) |
| PI-5 **publica** | `seguridad/{device}/comando` | Sin cambios |

- **Fallback de cero coste:** el mismo JSON por `/telemetria` con `tipo == "PERFIL_SISTEMA"`, detectado en `process_event` y desviado al upsert antes del LLM.
- **Respuesta** — nuevo valor `status: "rejected_local_policy"` cuando la barrera local rechaza un comando (firma válida pero verbo destructivo).
- **Comando** — nuevas acciones firmadas, gratis por el canal seguro: `{accion:"redescubrir"}` y, opcional, `{accion:"configurar_monitorizacion", fuentes:[...]}`.
- **Versionado en tres niveles:** `schema_version` (forma del JSON; PI-5 migra/ignora campos nuevos), `profile_version` (incremental por device, invalida la caché), `profile_hash` (sha256 de secciones materiales, dedupe).
- **AWS IoT:** los topics ya son wildcard `seguridad/*` → `/perfil` no requiere cambio de política. Sí: añadir el `client_id` del sensor nuevo (o migrar a `${iot:Connection.Thing.ThingName}`, ver [§10](#10-seguridad)).

---

## 9. Inyección de contexto al LLM

El perfil llega al triage **por evento** (no vía `instruction` estático ni session-state, porque la sesión ADK es única y compartida). En `_run_agent_event`, antes de armar el mensaje:

```python
profile = profile_context.get_profile(device)
ctx = profile_context.render_profile_block(profile) if profile else ""
message = f"Nuevo {event_type} proveniente del dispositivo '{device}':\n{ctx}\n{raw_log}"
```

Donde `render_profile_block` produce un bloque compacto:

```
### CONTEXTO DEL SISTEMA OBJETIVO (device=web-prod-01)
OS: Debian 12 (aarch64)
Web: nginx 1.22 (proxy 443->127.0.0.1:8080), config /etc/nginx/nginx.conf
BD: mysql 8.0 (127.0.0.1:3306)
Firewall ACTIVO: nftables (backend iptables-nft) — usa `nft`/`firewall-cmd`, NO reglas iptables-legacy crudas
Capacidades: restic=NO, fail2ban=SI, package_manager=apt
Puertos expuestos: 443, 22
```

Con esto el triage elige el firewall correcto y rutas reales en vez de asumir `apache`+`iptables`. Coste: tokens extra por evento, mitigable cacheando el bloque renderizado por device (invalidado por `profile_version`). Complemento: `consultar_manual_mitigacion` filtra recomendaciones por el perfil (no proponer `restic` si `capabilities.restic == false`; usar `ufw deny` si el gestor activo es `ufw`).

---

## 10. Seguridad

> El riesgo central: un sensor genérico en un **servidor de producción ajeno no es un honeypot de juguete**. Ejecutar con `shell=True` como root con la firma como única barrera es agresivo fuera del honeypot.

1. **Denylist local DURA (obligatoria desde Fase 1 — objetivo: servidores reales).** La firma Ed25519 autentica **origen** (viene de PI-5), no **contenido** (que sea seguro). El Policy Engine vive **solo en PI-5**. Si PI-5 se compromete, la clave se filtra o el LLM alucina algo destructivo y un humano lo aprueba por error, el sensor lo ejecuta como root. El `executor.py` debe **rechazar verbos destructivos** (`rm -rf`, `mkfs`, `dd`, `shutdown`, `reboot`, `wipefs`, `userdel`) **aunque la firma sea válida** (→ `status:"rejected_local_policy"`). Defensa en profundidad: dos capas independientes (PI-5 remoto + sensor local) deben fallar para ejecutar algo destructivo. Idealmente, portar `classify()` del [policy_engine](../PI-5/src/tools/policy_engine.py) como barrera local.
2. **Ejecución como root (decisión del proyecto).** Los comandos siguen corriendo **como root** por defecto, igual que hoy — se prioriza que las mitigaciones (iptables/nft, systemctl, restauración de backups) funcionen sin fricción. La defensa no es el de-escalado de privilegios sino la **denylist local** del punto 1, que actúa con root igualmente. `executor.py` expone `run_as` en config por si en algún objetivo concreto se quiere de-escalar, pero el default es root. El perfil sigue listando capacidades para que el LLM elija el binario correcto, no para acotar un `sudoers`.
3. **Mapeo de capacidades del firewall.** El perfil reporta el gestor activo; el bloque de contexto le dice al LLM qué herramienta usar. Mejora opcional: el Policy Engine selecciona catálogos de verbos por firewall del perfil (hoy `nft`/`firewalld` caen a `LOW` por "verbo desconocido").
4. **No confiar la salida del LLM para algo estructural** (aplica a la Fase 4). Si un LLM produce el perfil o el catálogo, validar **siempre** contra JSON Schema + cross-check con los hechos crudos + marca de `confidence`; nunca dispara comandos sin pasar por `policy_engine` + HITL.
5. **Provisioning de identidad.** Manual hasta ~5 sensores: por objetivo, crear Thing + cert X.509 + adjuntar policy y fijar `device_id` en `sentinel.local.yml` (== sufijo del topic `/comando` == campo `sensor`). Como [PI-5/Policy.json](../PI-5/Policy.json) **ya usa** `${iot:Connection.Thing.ThingName}`, con `client_id == ThingName` **no hay que editar la política por cada sensor**. Fleet Provisioning (claim cert + provisioning template) solo cuando la flota crezca.
6. **El perfil no va firmado en v1** (es informativo, no ejecutable). Aceptable, pero registrar `last_profile_hash` para detectar perfiles incoherentes/forjados. Un sensor comprometido podría enviar un perfil falso para sesgar el triage, pero como el triage solo **propone** y todo pasa por HITL + policy_engine + firma, el blast radius es limitado. A futuro: firmar el perfil con clave del propio sensor.
7. **Rotación de la clave Ed25519** (deuda pre-existente que el server real agrava). Soportar un set de claves públicas válidas en el sensor (`current`+`next`) para rotar sin downtime.
8. **Superficie de red.** El canal de control es **solo MQTT saliente sobre mTLS**; el sensor **nunca** abre un listener entrante.

---

## 11. Qué modificar en todo (resumen por componente)

| Componente | Archivos | Cambio |
|------------|----------|--------|
| Sensor — discovery | `sentinel-agent/sentinel_agent/discovery/*.py`, `profile_builder.py` (paquete genérico **nuevo**) | Probes stdlib degradables; ensamblado del perfil con `profile_hash`/`profile_version` |
| Sensor — monitorización | `sentinel-agent/sentinel_agent/monitor.py`, `parsers/*.py`, `sentinel.local.yml` | Detectores declarativos en vez de rutas/regexes/umbrales fijos; 4 topics desde un `device_id`. El monolito `agente_monitor3.py` queda como legado |
| Sensor — identidad/ejecución | `sentinel-agent/sentinel_agent/executor.py`, `sentinel.local.yml` | Config en vez de constantes; **denylist local dura** (ejecución sigue siendo root por defecto) |
| PI-5 — ingesta perfil | [main_coordinator.py](../PI-5/src/main_coordinator.py), `config.yml` | Rama `/perfil` en `process_event` + suscripción `seguridad/+/perfil` |
| PI-5 — BD | [database.py](../PI-5/src/database.py) | Tabla `device_profiles` (sin tocar `logs`) |
| PI-5 — tools | [db_tools.py](../PI-5/src/tools/db_tools.py), `profile_context.py` (nuevo) | `upsert/get_device_profile`; render del bloque de contexto cacheado |
| PI-5 — inyección | [main_coordinator.py:195](../PI-5/src/main_coordinator.py#L195) | Anteponer el bloque de contexto por evento (solo triage) |
| Agente triage | [triage_agent.py:40](../PI-5/src/agents/triage_agent/triage_agent.py#L40) | Prompt depende del bloque de contexto, no asume honeypot |
| Recomendaciones | [iot_tools.py:315](../PI-5/src/tools/iot_tools.py#L315), [recommendations.json](../PI-5/src/recommendations.json) | Filtrar por perfil; separar manual genérico + overrides por device |
| Policy Engine (opcional) | [policy_engine.py:91-132](../PI-5/src/tools/policy_engine.py#L91) | Catálogos de verbos por firewall del perfil |
| Firma | [signing.py](../PI-5/src/tools/signing.py) (PI-5 y PI-4) | **Sin cambios** funcionales; a futuro, set de claves para rotación |
| Política AWS IoT | [Policy.json](../PI-4/Policy.json), [Policy.json](../PI-5/Policy.json) | Migrar PI-4 a `${...ThingName}`; corregir literal `Pi4-felix`→`Pi4-Felix` en Policy.json:10 |
| Documentación | `docs/`, CHANGELOG | Este doc; contrato de 4 topics; guía de provisioning |

---

## 12. Plan por fases

Reordenado según las [decisiones tomadas](#decisiones-tomadas-2026-06-14): el sensor genérico es *el* sensor desde el principio (sin paralelo), la ejecución sigue siendo root con denylist local como barrera, y la reestructuración de recomendaciones sube a la Fase 2.

| Fase | Objetivo | Entregables | Esfuerzo |
|------|----------|-------------|----------|
| **1. Sensor genérico + discovery + contexto** ✅ **HECHA (2026-06-14)** | Un sensor genérico desplegable en un servidor real que descubre el sistema, envía el perfil y ejecuta comandos con barrera local; el triage recibe el contexto y deja de asumir el honeypot | **Sensor (paquete genérico `sentinel-agent/`):** `discovery/` (probes), `profile_builder` (con `profile_hash`/`profile_version`), `monitor.py` que lee `sentinel.local.yml`, `parsers.py`, `transport.py` (MQTT) + `signing.py` (verificación Ed25519 portada), y `executor.py` con **denylist local DURA** (ejecución root por defecto). **PI-5:** tabla `device_profiles`, `upsert/get`, rama `/perfil` + suscripción, `profile_context.render_profile_block`, inyección por evento en `_run_agent_event`, ajuste del prompt de triage. Tests: 61 del sensor + 12 en PI-5. _Pendiente operativo: provisioning real del primer sensor (Thing/cert)._ | Alto |
| **2. Recomendaciones deshardcodeadas** ✅ **HECHA (2026-06-14)** | Que las mitigaciones se adapten al sistema real, no al honeypot | `recommendations/generic.json` (36 entradas por familia, con placeholders, `requires`/`applies_if` y plantillas por firewall) + `recommendations/Pi4-Felix.json` (override del honeypot). Motor `tools/mitigation_manual.py`: filtra por capabilities/firewall del perfil, sustituye placeholders, fusiona overrides y **nunca** devuelve el honeypot a otro device. `consultar_manual_mitigacion(query, device)` delega; prompt del triage ajustado. 17 tests del motor | Medio |
| **3. Perfil vivo** ✅ **HECHA (2026-06-15)** | Mantener el perfil al día sin intervención | Loop de re-descubrimiento (periódico + acción firmada `redescubrir`) que **republica solo si cambia el hash** (estabilizado excluyendo `pid`/`exe`/orden de `services`); **restart controlado de tailers** solo cuando cambia `log_sources` (Event de generación + debounce + cap, sin reconfiguración en caliente; mata el `journalctl` al parar). Policy Engine: clasificación por subcomando de **nft/firewall-cmd/ufw**. Revisión adversarial → 8 fixes (incl. `firewall-cmd --direct --passthrough` que auto-ejecutaba `iptables -F`). 37 tests nuevos | Medio |
| **4. Enriquecimiento LLM offline** ✅ **HECHA (2026-06-15)** | Normalizar configs raras sin no-determinismo en la ruta caliente | `tools/profile_enricher.py` (offline, dualidad api/local con override `ENRICH_*`) + `enrichment_schema`/`enrichment_crosscheck` + tabla `device_enrichments` + CLI `scripts/enrich_profile.py` (`--generate`/`--list`/`--show`/`--promote`/`--discard`) + endpoints `/api/enrich`. Salida validada contra JSON Schema estricto + cross-check contra el perfil + `confidence` + sanitización por `policy_engine`; **nada se auto-aplica** (PENDING_REVIEW → el operador promueve a `recommendations/<device>.json` y vuelve a pasar por HITL). Revisión adversarial → 7 fixes (incl. el transversal del salto de línea). 45 tests nuevos | Medio |
| **5. Escalado de flota** ✅ **HECHA (2026-06-15)** | Desplegar muchos sensores sin tocar AWS por nodo | Política de PI-4 migrada a `${...ThingName}` (+ typo `Pi4-felix`→`Pi4-Felix` en `Policy.json`); **rotación de la clave Ed25519 sin downtime** (set current+next en `sentinel-agent/signing.py`, modos `--next`/`--promote` en `generate_signing_keys.py`); Fleet Provisioning entregado como **plantillas IaC** (`sentinel-agent/provisioning/`: template + claim policy + runtime policy) + **guía de onboarding** (`docs/Onboarding_Sensor.md`) + instalador y unit systemd; monolito `agente_monitor3.py` retirado (la política IoT del device queda en `PI-4/Policy.json` y la clave pública de firma en `PI-5/`). El **bootstrap por claim en el sensor** se difiere a cuando la flota crezca (§10.5). 7 tests nuevos del sensor | Alto |

---

### 12.1 Limitaciones conocidas de la Fase 3

Recogidas de la revisión adversarial; se dejan fuera a propósito (no son bloqueantes) y se documentan para una Fase 3.1:

- **Rotación de logs (logrotate):** `tail_file` abre el fichero y hace seek-al-final una vez; no detecta rotación de inode ni truncado. Mitigación operativa: configurar logrotate con `copytruncate`. El re-descubrimiento periódico reabre los ficheros y acota la ceguera al intervalo.
- **Ventana de transición en el restart:** la nueva generación de tailers reabre con seek-al-final, así que se prioriza **no duplicar** sobre no perder: se pierden las pocas líneas escritas en la sub-ventana del reinicio (duplicar inflaría los contadores de fuerza bruta). El `DetectorEngine` conserva los contadores previos.
- **Restart del conjunto completo:** aunque solo cambie una fuente, se reinician todos los tailers. El restart por diferencia se descarta ahora por requerir estado por-tailer.
- **Divergencia por cap de restarts:** si el debounce o el cap suprimen un restart, PI-5 recibió el perfil nuevo pero el sensor sigue vigilando el set viejo hasta el siguiente ciclo. Se registra con un *warning*.
- **IPv6 en el Policy Engine:** la detección de "IP concreta" (`_has_ip`) es solo IPv4; las reglas de firewall con IPv6 caen a HIGH (fail-safe, van igualmente a HITL).
- **Bloqueo del hilo de red en `redescubrir`:** un `redescubrir` que provoque un restart bloquea el hilo de callbacks MQTT durante el `join` de los tailers (pocos segundos). Aceptable; mitigable lanzándolo en un hilo aparte.

## 13. Decisiones (resueltas y de implementación)

**Decididas el 2026-06-14** (ver [§1](#decisiones-tomadas-2026-06-14)):

| Decisión | Resolución |
|----------|------------|
| 🟢 Alcance del objetivo | **Servidores reales desde el principio** → provisioning serio + denylist local obligatorios en Fase 1 |
| 🟢 Privilegio de ejecución | **Root por defecto** (configurable con `run_as`); la barrera añadida es la denylist local, no el de-escalado |
| 🟢 Estrategia de migración | **Visión completa directa**: el sensor genérico es *el* sensor; `agente_monitor3.py` queda como legado (servicio no levantado); `Pi4-Felix` es un device configurado |
| 🟢 Recomendaciones | **Manual genérico + overrides por device** (Fase 2); el honeypot pasa a ser el override de `Pi4-Felix` |

**Resueltas por recomendación del diseño** (modificables si surge motivo):

| Decisión | Resolución |
|----------|------------|
| Topic `/perfil` dedicado vs telemetría con `tipo` | **Topic dedicado `/perfil`** (routing trivial `topic.endswith('/perfil')`, no contamina triage). Fallback por telemetría como red de seguridad de cero coste |
| Contexto por evento vs session-state ADK por device | **Por evento, sí o sí.** La sesión ADK es única y compartida; session-state mezclaría contextos |
| Re-descubrimiento ya en Fase 1 o más tarde | **Snapshot al arranque en Fase 1**; periódico + dedupe en Fase 3. Pero diseñar `profile_hash`/`profile_version` desde Fase 1. **No** reconfiguración en caliente: restart controlado |
| Provisioning manual vs Fleet | **Manual hasta ~5 sensores** (la policy ya usa ThingName, no se edita por nodo); Fleet en Fase 5 si la flota crece |
| Detectores YAML vs Python | **Híbrido:** parsers en Python seleccionados por `log_source.parser`; umbrales/ventanas/patrones en YAML |

---

## 14. Flujo end-to-end (con discovery)

```
Arranque del sensor
   │  snapshot de discovery (probes)
   ▼
Publica System Profile ──► seguridad/<device>/perfil ──► PI-5 process_event
   │                                                         │ upsert device_profiles (dedupe por hash)
   ▼                                                         ▼  (NO va al LLM, NO crea fila en logs)
Monitorización (tailers según perfil)
   │  detecta ataque
   ▼
Evento ──► seguridad/<device>/evento ──► triage_queue
                                            │ _run_agent_event antepone CONTEXTO DEL SISTEMA del device
                                            ▼
                        Triage Agent razona sobre OS/firewall/web REALES
                                            │ consultar_manual_mitigacion(device) filtrado por capabilities
                                            ▼
                        Propone comando con el firewall correcto ──► request_mitigation_approval
                                            │ policy_engine clasifica ──► HITL (dashboard)
                                            ▼  al aprobar: PI-5 firma (con log_id) ──► seguridad/<device>/comando
Sensor verifica firma + denylist LOCAL ──► ejecuta de-escalado ──► respuesta (eco log_id) ──► mark_mitigation_result
```

---

*Diseño derivado de un análisis multi-agente del repositorio (investigación de técnicas de auto-descubrimiento + mapeo del contrato actual + panel de 3 enfoques + síntesis). Pendiente de implementación por fases.*
