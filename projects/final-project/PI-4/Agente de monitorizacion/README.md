# PI-4 — Agente de monitorización (legado retirado)

> **Estado (Fase 5, 2026-06-15):** el sensor monolítico **`agente_monitor3.py`**
> (artefacto del TFG, cableado al honeypot `Pi4-Felix`, con su servicio systemd ya
> sin levantar) ha sido **retirado**. El sensor vigente es el paquete genérico
> auto-configurable [`sentinel-agent/`](../../sentinel-agent/README.md), y
> `Pi4-Felix` pasa a ser **un device configurado más** (`sentinel.local.yml` con
> `device_id=Pi4-Felix`), no un caso especial.

## Qué se retiró

Se eliminaron del repositorio los artefactos que **solo** servían para arrancar el
monolito (su historia y autoría quedan en el `git log`, no se reescriben):

`agente_monitor3.py`, `Dockerfile`, `soc-sensor.service`, `setup.sh`,
`config.yml` (desincronizado y que el propio monolito ignoraba), `aws_connector.py`
(copia muerta; el vivo es `PI-5/src/aws_connector.py`) y `requirements.txt`.

## Qué permanece aquí (y por qué)

| Fichero | Por qué se conserva |
|---|---|
| `signing.py` | Verificador Ed25519 que **sigue vivo** como contrato criptográfico: lo carga `PI-5/tests/test_signing.py` para validar end-to-end el firmante de PI-5. No es el verificador del sensor genérico (ese vive en `sentinel-agent/sentinel_agent/signing.py`). |
| `sentinel_pi5_signing.pub` | Clave **pública** Ed25519 de PI-5 (commiteable). La escribe `scripts/generate_signing_keys.py` y se distribuye a cada sensor. |
| `Policy v2.json` | Política AWS IoT del device, **migrada en la Fase 5** a `${iot:Connection.Thing.ThingName}`. Copia local *source-of-truth* (no se aplica sola). |

## Para desplegar un sensor hoy

Ver [`docs/Onboarding_Sensor.md`](../../docs/Onboarding_Sensor.md) y el diseño en
[`docs/diseno_agente_discovery.md`](../../docs/diseno_agente_discovery.md).
