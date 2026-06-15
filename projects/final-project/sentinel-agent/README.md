# sentinel-agent — sensor genérico de Sentinel-IT

Sensor auto-configurable de Sentinel-IT. Se despliega en cualquier servidor Linux, **se autodescubre**
(servicios, puertos, logs y formatos, servidor web, BD, firewall, capacidades),
publica un **System Profile** a PI-5 y ejecuta comandos de mitigación firmados
(Ed25519) con una **barrera local** que rechaza verbos destructivos.

Diseño completo: [`docs/diseno_agente_discovery.md`](../docs/diseno_agente_discovery.md).
Alta paso a paso: [`docs/Onboarding_Sensor.md`](../docs/Onboarding_Sensor.md).

## Estructura

```
sentinel_agent/
├── discovery/        # probes stdlib degradables (os, services, stack, log, firewall, caps, users, surface)
├── profile_builder.py# ensambla el System Profile + profile_hash/profile_version
├── parsers.py        # línea de log -> observación (sshd, nginx/apache, vsftpd)
├── detectors.py      # ventana deslizante (fuerza bruta) + patrones (SQLi/XSS)
├── executor.py       # firma + denylist local + ejecución (root por defecto) + eco log_id
├── transport.py      # MQTT a AWS IoT Core (cola de publicación)
├── monitor.py        # orquestador
├── config.py         # carga sentinel.local.yml
└── signing.py        # verificación Ed25519 (byte-idéntica a PI-5)
```

## Uso

```bash
pip install -r requirements.txt

# Ver qué descubre el sensor en este host (sin MQTT) — útil para provisioning:
python -m sentinel_agent --discover-only --device web-prod-01

# Arrancar el sensor:
cp sentinel.local.example.yml sentinel.local.yml   # y rellenar
python -m sentinel_agent --config sentinel.local.yml
```

## Provisioning de un sensor nuevo

1. Crear un Thing + certificado X.509 en AWS IoT con `client_id == device_id`
   (la política de PI-5 ya usa `${iot:Connection.Thing.ThingName}`).
2. Copiar los certs y la **clave pública** Ed25519 de PI-5 (`*.pub`) al host.
3. Rellenar `sentinel.local.yml`. **`device_id` debe coincidir** con el sufijo
   de su topic de comando (`seguridad/<device_id>/comando`) o el sensor recibe
   eventos pero nunca comandos.

## Seguridad

- **Ejecución como root por defecto** (`executor.run_as` para de-escalar).
- **Denylist local dura**: rechaza `rm`, `mkfs`, `dd`, `shutdown`, etc. aunque
  la firma sea válida (`status: rejected_local_policy`). Defensa en profundidad
  junto a la firma (que valida origen, no contenido) y al Policy Engine de PI-5.

## Tests

```bash
python -m pytest    # 94 tests offline (parsers, detectores, denylist, firma+rotación, perfil)
```
