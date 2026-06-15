---
title: "Guía de Testing - Sentinel-IT (PI-5)"
author: "Daniel Alarcon"
date: "2026-05-17"
tags: ["testing", "unittest", "e2e", "mocks", "adk", "policy-engine"]
---

# Guía de Testing

## 1. Propósito

Este documento describe el conjunto de tests del coordinador SOC: qué cubre cada uno, qué necesita para correr (BD, red, AWS IoT, coordinator vivo, etc.) y cómo se invocan. Pensado para que cualquier persona sepa qué probar tras tocar una pieza concreta del sistema.

No describe la lógica que validan los tests — para eso ir al doc del componente correspondiente.

## 2. Mapa de tests

Desde 2026-06-13 la suite está dividida en dos mundos físicamente separados:

- **`PI-5/tests/`** — tests automatizados **offline** (196 tests). Sin red, sin Gemini, sin hardware. Es lo que ejecuta `pytest` a secas (hay `pytest.ini` + `conftest.py` en `PI-5/`).
- **`PI-5/tests/manual/`** — scripts manuales y E2E que requieren AWS IoT real (mTLS), Gemini y/o el coordinador corriendo. **Excluidos de la colección de pytest** (varios conectan a AWS en código de nivel de módulo); se lanzan uno a uno a mano.

```
PI-5/tests/
├── test_policy_engine.py            ← unitario ← motor de políticas (36 tests)
├── test_policy_engine_hardening.py  ← unitario ← bypasses por contenido entrecomillado
├── test_signing.py                  ← unitario ← contrato Ed25519 PI-5 ↔ PI-4
├── test_feedback_normalizer.py      ← unitario ← normalizador de feedback del coordinador
├── test_coordinator_routing.py      ← unitario ← routing, round-trip log_id, backpressure
├── test_hitl_approve.py             ← unitario ← /api/mitigate/approve, gate CRITICAL, auth fail-closed
├── test_dashboard_api.py            ← unitario ← /api/data, /, /revert
├── test_pending_ai_events.py        ← unitario ← persistencia ante 429 de Gemini
├── test_revert_commands.py          ← unitario ← derivación de rollbacks
├── test_soc_manager_script.py       ← unitario ← invariantes de soc_manager.sh
├── aws_mqtt.txt                     ← notas sueltas sobre conexión MQTT
└── manual/
    ├── test_adk.py                  ← integ.   ← triage_agent vivo con Gemini (online IA)
    ├── test_feedback_loop.py        ← integ.   ← tools + BD real data/soc_data.db
    ├── test_flexible_command.py     ← E2E      ← MQTT real, mock de Pi4 local
    ├── test_agent_flow.py           ← E2E      ← MQTT real + coordinator vivo + BD real
    ├── test_pi4_simulation.py       ← manual   ← se hace pasar por Pi4 desde otra máquina
    ├── test_local.py                ← humo     ← publica un log de prueba (topics legacy)
    ├── test_mqtt.py                 ← humo     ← conexión MQTT básica (topics legacy)
    └── test_publish_pi.py           ← humo     ← publish manual
```

| Tipo | Sin red | Necesita Gemini | Necesita coordinator vivo | Modifica BD real |
|------|---------|-----------------|--------------------------|------------------|
| `tests/*.py` (todos) | ✓ (BD temporal/mocks) | — | — | — |
| `manual/test_feedback_loop.py` | ✓ | — | — | ✓ (data/soc_data.db) |
| `manual/test_adk.py` | — (Gemini) | ✓ | — | — |
| `manual/test_flexible_command.py` | — (AWS IoT) | — | ✗ (lo para temporalmente) | — |
| `manual/test_agent_flow.py` | — (AWS IoT) | ✓ (vía coord.) | ✓ | ✓ |
| `manual/test_pi4_simulation.py` | — (AWS IoT) | ✓ (vía coord.) | ✓ | ✓ |
| `manual/test_local.py` / `test_mqtt.py` | — (AWS IoT) | — | opcional | — |

## 3. `test_policy_engine.py` — Unitarios del motor

**Lo que cubre:**

- Clasificación de comandos en `SAFE_READ` / `LOW` / `HIGH` / `CRITICAL`.
- Reglas de escalado (intérpretes con `-c`, pipelines, redirecciones, metacaracteres, wildcards en paths sensibles, encadenamiento `;` con verbo destructivo).
- Verbos desconocidos caen a `LOW` (nunca DENY automático).
- `request_mitigation_approval` despacha solo `SAFE_READ` directo y deja `LOW`/`HIGH`/`CRITICAL` en HITL.
- Inmutabilidad del `audit_log` (triggers anti-UPDATE/DELETE).

**Cómo correrlo:**

```bash
cd PI-5
python -m unittest tests.test_policy_engine -v
```

Crea una BD temporal con `tempfile`, ejecuta los tests, y la borra. No toca `data/soc_data.db`. Sin red, sin API keys, sin AWS.

**Cuándo correrlo:** después de tocar `policy_engine.py`, `iot_tools.py`, `database.py` o cualquier prompt de los agentes que mencione niveles de riesgo.

## 4. `test_feedback_loop.py` — Ciclo agentes + BD (sin red)

**Lo que cubre:**

- `register_alert` → inserción correcta en `logs`.
- `update_alert_status` → concatenación en `estado_mitigacion`.
- Que los tools publican lo esperado (interceptado con un `MockIotClient`).

**Cómo correrlo:**

```bash
cd PI-5
python tests/test_feedback_loop.py
```

Usa un mock del cliente MQTT (`MockIotClient`) que almacena las publicaciones en una lista en lugar de mandarlas a AWS. La BD que usa es `PI-5/data/soc_data.db` real — los registros que crea quedan ahí. Si quieres una BD limpia, copia el `.db` o usa `sqlite3 ... "DELETE FROM logs WHERE veredicto_ia LIKE '%test%'"` antes de correr.

**Cuándo correrlo:** después de tocar `db_tools.py`, el esquema en `database.py`, o cualquier llamada a tools en los agentes.

## 5. `test_dashboard_api.py` — Smoke del dashboard

**Lo que cubre:**

- `/api/data` devuelve 200 + JSON con los campos esperados.
- `/` (página principal) renderiza con el header "Sentinel-IT".
- Autenticación HTTP Basic funciona (credenciales `admin:testpass` set por env).

**Cómo correrlo:**

```bash
cd PI-5
python -m unittest tests.test_dashboard_api -v
```

Mockea `AWSMqttClient` y las funciones de acceso a BD (`get_logs`, `get_db_stats`) con `unittest.mock.patch`. No abre red ni toca SQLite real.

**Cuándo correrlo:** después de tocar `dashboard_soc.py` (rutas, serialización, auth) o `templates/index.html` (que el smoke test sepa que la string "Sentinel-IT" sigue presente).

## 6. `test_adk.py` — Agente con LLM real

**Lo que cubre:**

- El `triage_agent` se construye correctamente con sus tools.
- Procesa un log de SQL Injection y emite tool calls coherentes.
- Verbose de cada `function_call` y `function_response` para depuración.

**Cómo correrlo:**

```bash
cd PI-5
python tests/test_adk.py
```

Necesita `GEMINI_API_KEY` en `.env`. Inyecta un `MockIotClient` así que aunque la IA llame `execute_diagnostic_command`, el comando no sale a AWS — se imprime por pantalla. Permite ver el chain-of-thought del agente sin gastar mucho coste.

**Cuándo correrlo:** después de tocar el `instruction` de `triage_agent.py`, añadir/quitar tools o cambiar el modelo (`AI_MODEL`).

## 7. `test_flexible_command.py` — Ciclo MQTT real con mock de Pi-4

**Lo que cubre:**

- Conecta a AWS IoT con el `client_id` del coordinador para "hacerse pasar" por él (asume coordinator parado).
- Publica un log → recibe el comando que emite el agente → simula la ejecución y publica la respuesta.
- Verifica que el feedback se procesa.

**Cómo correrlo:**

```bash
# 1. Parar el coordinator si está corriendo (es exclusivo: usa el mismo client_id).
docker stop soc-coordinator-pi5

# 2. Lanzar el test.
cd PI-5
python tests/test_flexible_command.py

# 3. Reiniciar el coordinator.
docker start soc-coordinator-pi5
```

**Cuándo correrlo:** después de cambios en el esquema MQTT (topics, payloads), en `aws_connector.py` o en la subscription routing del coordinator.

## 8. `test_agent_flow.py` — E2E completo

**Lo que cubre:**

- El flujo entero con el coordinator corriendo en otra terminal/container.
- Se hace pasar por Pi-4 usando el `client_id` `Dashboard-SOC-Pi5` (paralelo, no en conflicto).
- Caso A: publica evento → captura comando → responde `success` → verifica `[EXITO]` en BD.
- Caso B: publica evento → captura comando → responde `error` → verifica `[FALLO]` + opcionalmente comando alternativo.

**Cómo correrlo:**

```bash
# Terminal 1: coordinator vivo
docker compose -f PI-5/docker-compose.yml up

# Terminal 2: el test
cd PI-5
python tests/test_agent_flow.py
```

Cada escenario tiene una ventana de espera (`TRIAGE_WAIT_SECONDS=45`, `FEEDBACK_WAIT_SECONDS=45`) que cubre el tiempo de procesamiento asíncrono e inferencia del modelo Gemini.

**Cuándo correrlo:** validación full-stack tras cualquier cambio mayor (coordinator, agentes, Policy Engine, MQTT, BD). Es el test más cercano a producción y el que más coste tiene (Gemini se invoca dos veces).

**Pi-4 real:** este test asume que la Pi-4 NO está conectada al broker en ese momento. Si está conectada, habría carrera porque ambas publican en los mismos topics. Si tienes una Pi-4 viva, desconecta su servicio antes (`sudo systemctl stop sentinel-agent` o equivalente).

## 9. `test_pi4_simulation.py` — Pi-4 manual desde otro host

Variante interactiva de `test_agent_flow.py`. Se conecta a AWS, escucha en `seguridad/acciones/...`, publica un log de SQL Injection y espera comandos ad infinitum. Pensado para correr desde una máquina **distinta** del coordinador (otra terminal, otro PC) y comprobar manualmente el flujo en el dashboard.

> Nota: este test usa topics antiguos (`seguridad/acciones/...`, `seguridad/<dev>/logs`) que ya no encajan con el esquema actual (`seguridad/<dev>/{telemetria,evento,comando,respuesta}`). Está pendiente de actualizar al esquema nuevo descrito en [funcionamiento_mqtt.md](funcionamiento_mqtt.md). Sirve solo como referencia, no como test válido a día de hoy.

## 10. `test_local.py` — Humo MQTT

Publica un único log de fuerza bruta SSH en `seguridad/logs/Pi5-Simulador/ssh` y termina. Lo usaba la primera versión del proyecto cuando los topics eran `seguridad/logs/...`. Útil como ejemplo mínimo de cómo conectar al broker, pero su topic ya no encaja con el esquema actual.

> Pendiente de actualizar igual que `test_pi4_simulation.py`.

## 11. Cómo ejecutar todos los unitarios offline

```bash
cd PI-5
python -m pytest          # 196 tests, ~8 s, sin red. pytest.ini excluye tests/manual/

# El sensor genérico tiene su propia suite (94 tests offline):
cd ../sentinel-agent && python -m pytest    # parsers, detectores, denylist, firma+rotación, perfil
```

Para desarrollo se necesitan además las dependencias de `requirements-dev.txt` (`pip install -r requirements.txt -r requirements-dev.txt`).

> ⚠️ **No usar `unittest discover` sobre `tests/manual/`**: varios de esos scripts (`test_local.py`, `test_mqtt.py`) conectan a AWS IoT en código de nivel de módulo — importarlos ya abre sockets. Por eso viven en una carpeta excluida de la colección.

## 12. Tests pendientes

Áreas que no tienen cobertura automatizada todavía:

- **Revert end-to-end completo:** existe cobertura unitaria para la derivación de rollback (`test_revert_commands.py`), el endpoint (`test_dashboard_api.py`, `test_hitl_approve.py`) y la correlación log_id (`test_coordinator_routing.py`), pero falta una prueba E2E con MQTT real que confirme ejecución en PI-4 y feedback de `estado_mitigacion`.
- **`aws_connector.py`:** las ramas de error (`is_alive` zombie, PUBACK timeout, re-suscripción tras `session_present=False`) son testables con dobles de `awsiot` y no lo están.
- **CI:** los 196 tests offline no se ejecutan automáticamente en ningún commit (no hay GitHub Actions).

Estas mejoras quedan registradas en [futuras_mejoras.md](futuras_mejoras.md) (si se añaden) o como issues.

## 13. Archivos involucrados

Ver el mapa completo de la sección 2. Infraestructura de la suite:

```
PI-5/
├── conftest.py           # añade src/ al sys.path para todos los tests
├── pytest.ini            # testpaths=tests, excluye tests/manual/
├── requirements-dev.txt  # pytest, pytest-cov
└── tests/                # offline (pytest) + tests/manual/ (a mano)
```
