# provisioning — plantillas IaC para AWS IoT Fleet Provisioning by Claim

Plantillas de infraestructura (IaC) para registrar sensores de Sentinel-IT en
**AWS IoT Core** mediante **Fleet Provisioning by Claim**. Son la **fuente de
verdad local** del provisioning de flota: viven versionadas en el repo, pero
**no se aplican solas** — el operador las crea/pega en la consola de AWS IoT o
las sube vía AWS CLI (ver [Comandos de referencia](#comandos-de-referencia-aws-cli)).

> **Estado:** estas plantillas están **listas para activar**, pero el modo Fleet
> **todavía no está en uso**. Hoy el provisioning es **manual** (Thing + cert por
> objetivo) hasta ~5 sensores; ver
> [`docs/diseno_agente_discovery.md`](../../docs/diseno_agente_discovery.md)
> sección 10.5 (decisión "Provisioning manual vs Fleet"). El **código de
> auto-provisioning del sensor** (bootstrap por claim cert) se incorporará cuando
> se adopte el modo Fleet; **a día de hoy el sensor asume un cert permanente ya
> presente en disco** (`/etc/sentinel/certs/`, ver
> [`../sentinel.local.example.yml`](../sentinel.local.example.yml)).

- **Región AWS:** `eu-north-1`
- **Cuenta:** `582997418897`
- **Endpoint IoT:** `aj4wsdnimoej8-ats.iot.eu-north-1.amazonaws.com`
- **Namespace de topics de la aplicación:** `seguridad/*`
- **Nombre del provisioning template:** `SentinelFleetProvisioning`

## Los tres JSON y cómo se relacionan

| Fichero | Qué es | Quién lo usa |
|---|---|---|
| [`claim-policy.json`](claim-policy.json) | Política IoT **mínima** adjunta al **claim certificate** (la identidad temporal y **compartida** del bootstrap). Solo permite los topics reservados de provisioning. | El **claim cert** durante el arranque de un sensor nuevo. |
| [`provisioning-template.json`](provisioning-template.json) | El **provisioning template** del servicio. Define los recursos que AWS crea al consumir el claim: el **Thing**, el **certificado permanente** del sensor y la **política de runtime** que se le adjunta. | AWS IoT, cuando un sensor reclama (claim) su identidad. |
| [`runtime-policy.json`](runtime-policy.json) | La política **permanente** (`SentinelSensorRuntimePolicy`) que el template adjunta a cada sensor provisionado. Le da acceso **solo a `seguridad/<su device_id>/*`** (aislamiento por dispositivo vía `${iot:Connection.Thing.ThingName}`): un sensor no puede publicar ni leer los topics de otro. Más estricta que la policy del coordinador ([`PI-5/Policy.json`](../../PI-5/Policy.json)), que sí necesita el namespace completo `seguridad/*`. | El **cert permanente** de cada sensor en operación normal. |

Flujo (cuando el modo Fleet esté activo):

```
                  claim cert (compartido)  ──conecta con──►  claim-policy.json
                        │                                     (solo $aws/.../provisioning)
                        │  publica en $aws/certificates/create/json
                        ▼
            AWS IoT crea un cert permanente nuevo
                        │
                        │  publica en $aws/provisioning-templates/SentinelFleetProvisioning/provision/json
                        ▼
            provisioning-template.json se ejecuta
                        │
                        ├─►  crea Thing (ThingName == device_id)
                        ├─►  activa el cert permanente nuevo
                        └─►  adjunta runtime-policy.json (SentinelSensorRuntimePolicy)
                        │
                        ▼
            el sensor descarta el claim cert y opera con su cert permanente
            (Connect a client/<device_id>, Pub/Sub en seguridad/<device_id>/*)
```

## Invariante crítica: `ThingName == device_id`

**`device_id == ThingName == client_id MQTT == campo "sensor" del payload`.**

El template **debe** nombrar el Thing igual que el `device_id` del sensor
(parámetro `ThingName`). La política de runtime usa
`${iot:Connection.Thing.ThingName}` en `iot:Connect`, así que el `client_id`
MQTT del sensor tiene que coincidir con el `ThingName` o **la conexión se
rechaza**.

Y aún conectando: si el Thing se nombra distinto del `device_id`, el cert
conecta pero **los comandos de PI-5 nunca llegan**, porque PI-5 publica en
`seguridad/<device_id>/comando` y el sensor se suscribe usando su `device_id`.
Mismatch silencioso = sensor que ve eventos pero **nunca ejecuta mitigaciones**.

> Por eso `SerialNumber` (identificador físico/inventario) y `ThingName`
> (`= device_id`) son **parámetros separados** del template: el `device_id` lo
> elige el operador para casar con `sentinel.local.yml`, no se deriva del serial.

## Seguridad del claim cert compartido

El **claim certificate es compartido entre todos los sensores**. Si se filtra,
**cualquiera puede provisionar Things** en la cuenta. Mitigaciones obligatorias:

1. **Mínimo privilegio** — `claim-policy.json` solo permite los topics
   `$aws/certificates/create/json` y
   `$aws/provisioning-templates/SentinelFleetProvisioning/provision/json`
   (+ `accepted`/`rejected`). **No toca `seguridad/*`**: el claim no tiene acceso
   a la aplicación. El `client_id` del claim se restringe al patrón
   `sentinel-claim-*` (ver nota de diseño abajo).
2. **Pre-provisioning hook (Lambda)** — adjunta al template una Lambda que
   valide el `SerialNumber` contra una **allowlist** (p. ej. una tabla DynamoDB
   de seriales autorizados) y **rechace** los desconocidos antes de crear nada.
   Se configura con `--pre-provisioning-hook` al crear el template (campo
   `provisioningHook` / `DeviceConfiguration`). No va en el JSON del template
   (el formato no admite comentarios ni referencias a la Lambda inline).
3. **El claim cert NO se commitea** — igual que cualquier `*.pem`/`*.key`, el
   `.gitignore` del repo lo excluye. Solo se versionan **estas plantillas**.

> **Nota de diseño — `client_id` del claim:** se restringe a
> `client/sentinel-claim-*` en lugar de `client/*`. El claim cert es uno solo y
> compartido; acotar el prefijo del `client_id` evita que ese cert pueda
> conectarse suplantando el `client_id` de un sensor ya provisionado
> (`client/<device_id>`) y reduce la superficie si se filtra. El bootstrap del
> sensor debe generar un `client_id` con ese prefijo (p. ej.
> `sentinel-claim-<serial>`).

## Comandos de referencia (AWS CLI)

> Ejecutar con credenciales de la cuenta `582997418897` y `--region eu-north-1`.
> Estos comandos **activan** las plantillas en AWS; el repo solo las guarda.

```bash
# 1) Crear la política de runtime (la que el template adjunta a cada sensor).
aws iot create-policy \
  --region eu-north-1 \
  --policy-name SentinelSensorRuntimePolicy \
  --policy-document file://runtime-policy.json

# 2) Crear la política del claim (mínima, para el bootstrap).
aws iot create-policy \
  --region eu-north-1 \
  --policy-name SentinelClaimPolicy \
  --policy-document file://claim-policy.json

# 3) Crear el provisioning template (modo claim). Requiere un rol IAM que
#    AWS IoT asume para registrar Things; --pre-provisioning-hook es opcional
#    pero RECOMENDADO (valida el SerialNumber contra la allowlist).
aws iot create-provisioning-template \
  --region eu-north-1 \
  --provisioning-template-name SentinelFleetProvisioning \
  --provisioning-role-arn arn:aws:iam::582997418897:role/<rol-provisioning-iot> \
  --template-body file://provisioning-template.json \
  --enabled
  # --pre-provisioning-hook targetArn=arn:aws:lambda:eu-north-1:582997418897:function:<lambda-allowlist>

# 4) Crear el CLAIM certificate y guardarlo (NO commitear los .pem/.key).
aws iot create-keys-and-certificate \
  --region eu-north-1 \
  --set-as-active \
  --certificate-pem-outfile claim.cert.pem \
  --public-key-outfile claim.public.key \
  --private-key-outfile claim.private.key

# 5) Adjuntar la claim-policy al claim cert (usar el certificateArn del paso 4).
aws iot attach-policy \
  --region eu-north-1 \
  --policy-name SentinelClaimPolicy \
  --target arn:aws:iot:eu-north-1:582997418897:cert/<certificateId-del-claim>
```

El claim cert (`claim.*.pem`/`claim.private.key`) se distribuye con la imagen
base del sensor; cada host lo usa **solo una vez** para reclamar su identidad y
luego opera con su cert permanente.

## Provisioning manual hoy (sin Fleet)

Mientras la flota sea pequeña (~5 sensores), el provisioning es manual y **no
usa estas plantillas**: se crea un Thing + cert por objetivo, se adjunta
`SentinelSensorRuntimePolicy` (cuyo documento es exactamente
[`runtime-policy.json`](runtime-policy.json)) y se fija el `device_id` en
`sentinel.local.yml`. Como la policy ya usa `${iot:Connection.Thing.ThingName}`,
**no hay que editar la política por cada sensor**. El paso a paso end-to-end está
en la guía de onboarding.

## Guía relacionada

- [`docs/Onboarding_Sensor.md`](../../docs/Onboarding_Sensor.md) — guía
  operativa de alta de un sensor (manual hoy; bootstrap por claim cuando se
  active el modo Fleet).
- [`docs/diseno_agente_discovery.md`](../../docs/diseno_agente_discovery.md) —
  diseño del agente; sección 10.5 (provisioning manual vs Fleet).
- [`../README.md`](../README.md) — sensor genérico `sentinel-agent`.
- [`../../PI-5/Policy.json`](../../PI-5/Policy.json) — política de runtime
  canónica del proyecto (patrón replicado en `runtime-policy.json`).
