# PI-4 — `firma-iot` (política IoT + firma de comandos)

> **Estado (Fase 5, 2026-06-15):** esta carpeta se llamaba `Agente de monitorización`
> y alojaba el sensor monolítico `agente_monitor3.py` (artefacto del TFG, cableado al
> honeypot `Pi4-Felix`, con su servicio systemd ya sin levantar). Ese monolito fue
> **retirado** y la carpeta se renombró a **`firma-iot`** para reflejar lo que realmente
> queda: la **política AWS IoT** del device y el **contrato de firma Ed25519** de los
> comandos. El sensor vigente es el paquete genérico
> [`sentinel-agent/`](../../sentinel-agent/README.md), y `Pi4-Felix` pasa a ser **un
> device configurado más** (`sentinel.local.yml` con `device_id=Pi4-Felix`).

## Contenido

| Fichero | Qué es |
|---|---|
| `Policy.json` | Política AWS IoT del device PI-4, **migrada en la Fase 5** a `${iot:Connection.Thing.ThingName}`. Copia local *source-of-truth* (no se aplica sola; se pega en la consola de AWS IoT). |
| `signing.py` | Verificador Ed25519 (clave pública) — **contrato criptográfico vivo**: lo carga `PI-5/tests/test_signing.py` para validar end-to-end al firmante de PI-5. No es el verificador del sensor genérico (ese vive en `sentinel-agent/sentinel_agent/signing.py`). |
| `sentinel_pi5_signing.pub` | Clave **pública** Ed25519 de PI-5 (commiteable). La escribe `scripts/generate_signing_keys.py` y se distribuye a cada sensor. |

## Qué se retiró con el monolito

Se eliminaron del repositorio los artefactos que **solo** servían para arrancar el
monolito (su historia y autoría quedan en el `git log`, no se reescriben):
`agente_monitor3.py`, `Dockerfile`, `soc-sensor.service`, `setup.sh`, `config.yml`
(desincronizado), `aws_connector.py` (copia muerta; el vivo es
`PI-5/src/aws_connector.py`) y `requirements.txt`.

## Para desplegar un sensor hoy

Ver [`docs/Onboarding_Sensor.md`](../../docs/Onboarding_Sensor.md) y el diseño en
[`docs/diseno_agente_discovery.md`](../../docs/diseno_agente_discovery.md).
