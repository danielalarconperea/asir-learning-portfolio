---
title: "Changelog — Sentinel-IT"
author: "Daniel Alarcon"
date: "2026-05-19"
tags: ["changelog", "releases", "history"]
---

# Changelog

Registro de todos los cambios significativos del proyecto. Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2026-06-15] — Agente Discovery, Fase 5: escalado de flota

Quinta y última fase del [agente Discovery](diseno_agente_discovery.md): preparar el sistema para desplegar muchos sensores sin tocar AWS por nodo. Incluye la rotación de la clave de firma sin downtime, la migración de la política de PI-4 a `${...ThingName}`, las plantillas de Fleet Provisioning, la guía de onboarding con instalador, y la retirada del monolito del TFG. Pasó por una **revisión adversarial** (cripto, políticas IoT, retirada del monolito y docs/operaciones) que destapó y corrigió un defecto **alto** de procedimiento en la rotación y varios de aislamiento de red y robustez del despliegue.

### Añadido
- **Rotación de la clave de firma Ed25519 sin downtime** (`sentinel-agent/sentinel_agent/signing.py`): el sensor verifica contra un **set de claves** (`current` + opcional `next`); `verify_payload` acepta si **cualquiera** valida (el payload no lleva `kid`, así que se prueban todas — Ed25519 verify es barato). `load_public_keys([...])` carga el set (ignora rutas vacías) y `load_public_key` se conserva como compat. Campo `signing.next_public_key_path` (opcional) en `config.py` y `sentinel.local.example.yml`; `monitor.py` carga current+next al arranque.
- **`scripts/generate_signing_keys.py`**: modos `--next` (genera el par `next` sin tocar el actual) y `--promote` (asciende el `next` a actual con `os.replace` atómico), con un procedimiento de rotación en el que **PI-5 nunca repunta a `.next.key`** (siempre apunta al `.key` estable).
- **Plantillas IaC de Fleet Provisioning by Claim** (`sentinel-agent/provisioning/`): `provisioning-template.json`, `claim-policy.json` (mínima, solo topics de provisioning), `runtime-policy.json` (**aislada por device**: `seguridad/${...ThingName}/*`) y un README con los comandos AWS CLI y la seguridad del claim cert compartido.
- **Guía de onboarding** (`docs/Onboarding_Sensor.md`): alta end-to-end de un sensor (provisioning manual y fleet, distribución y rotación de la clave de firma, despliegue systemd, checklist de verificación). **Instalador** `sentinel-agent/scripts/install.sh` y **unit** `sentinel-agent/deploy/sentinel-agent.service`. Indexada en `docs/README.md`.

### Cambiado
- **Política AWS IoT de PI-4** (`PI-4/Agente de monitorizacion/Policy v2.json`) migrada a `${iot:Connection.Thing.ThingName}` (alineada con la de PI-5); corregido el typo `Pi4-felix`→`Pi4-Felix` en `PI-5/Policy.json`.
- **Monolito `agente_monitor3.py` retirado**: eliminados los 7 artefactos solo-legado (el sensor, su Dockerfile/systemd/setup, su `config.yml` desincronizado, la copia muerta de `aws_connector.py` y su `requirements.txt`). Se conservan `signing.py`, `sentinel_pi5_signing.pub` y `Policy v2.json` (atados a código vivo) con un README de deprecación. Docs actualizados (`funcionamiento_mqtt.md`, `Testing_Guide.md`, `Configuration_and_Deployment.md`, `diseno_agente_discovery.md` y la ficha histórica de PI-4) para reflejar que el sensor vigente es `sentinel-agent`.

### Corregido (revisión adversarial)
- **🔴 Procedimiento de rotación (alto):** el orden documentado original dejaba `PI-5/config.yml` apuntando al `.next.key` justo antes de que `--promote` lo borrara → un restart de PI-5 lanzaba `FileNotFoundError` y PI-5 dejaba de firmar (rechazo total de comandos a toda la flota). Reescrito para que PI-5 apunte **siempre** al `.key` estable; `--promote` intercambia el contenido bajo esa ruta y un reinicio de PI-5 lo recarga.
- **Aislamiento de red (medio):** la `runtime-policy.json` de los sensores concedía `seguridad/*` (toda la flota). Acotada a `seguridad/${...ThingName}/*` (un sensor no puede publicar ni leer los topics de otro) y retirado `iot:RetainPublish` (no usado por el sensor). La `claim-policy.json` se afinó a mínimo privilegio exacto (Publish solo en topics base; Subscribe/Receive solo en `accepted`/`rejected`).
- **Despliegue (medio):** `install.sh` ya no arranca el servicio si faltan certs/clave/config (evitaba un crash-loop con `Restart=on-failure`): solo `enable`, dejando el `start` al operador. Corregido el comando de verificación de la guía (`--discover-only --device <id>`, que no lee `--config`), el `ExecStart` con ruta absoluta y el paso de despliegue del paquete a `/opt/sentinel-agent`.

10 tests nuevos (rotación current+next, transición del set, orden firma-antes-de-ventana, atomicidad de carga, campo `next` en config); 290 en total (196 PI-5 + 94 sensor).

---

## [2026-06-15] — Agente Discovery, Fase 4: enriquecedor LLM offline (+ fix transversal del Policy Engine)

Cuarta fase del [agente Discovery](diseno_agente_discovery.md): un normalizador LLM **offline** que enriquece el perfil determinista con sugerencias validadas, sin meter no-determinismo en la ruta caliente. Pasó por una **revisión adversarial** que, además de hallazgos propios de la fase, destapó un bug **transversal de seguridad** en el Policy Engine.

### 🔴 Corregido — seguridad alta (transversal a todas las fases)
- **El Policy Engine no trataba el salto de línea como separador de comandos.** `cat /etc/passwd\nsystemctl restart sshd` se clasificaba `SAFE_READ` y se **auto-ejecutaba sin HITL** (shlex fusiona el LF como espacio). Ahora `classify` divide por saltos de línea/retorno de carro fuera de comillas y clasifica cada tramo: `SAFE_READ` solo si TODOS lo son, si no `max(HIGH, …)`. Afectaba a cualquier comando del agente IA en caliente.

### Añadido
- **`PI-5/src/tools/profile_enricher.py`** — orquestador offline: dualidad de modelo (`AI_MODE`/`AI_MODEL`, override opcional `ENRICH_MODE`/`ENRICH_MODEL`) **sin mutar el entorno global**; `litellm` one-shot con `response_format` por proveedor; distinción `ProviderError` (reintentable) vs `HallucinationError`. Salida validada en dos capas (JSON Schema estricto + cross-check contra el perfil), `confidence = min(LLM, respaldo)` (recovery capada a medium), y **sanitización por `policy_engine`** que rechaza destructivos, ejecución por intérprete y saltos de línea.
- **`enrichment_schema.py`** (esquema draft-07, `additionalProperties:false`) y **`enrichment_crosscheck.py`** (funciones puras: cada sugerencia debe apuntar a servicios/puertos/logs/capabilities reales; rutas normalizadas anti-traversal y bajo allowlist).
- **Tabla `device_enrichments`** (separada de `device_profiles`; estados PENDING_REVIEW/PROMOTED/DISCARDED/SUPERSEDED) + helpers en `db_tools`; al llegar un perfil nuevo, los pendientes pasan a SUPERSEDED.
- **CLI `scripts/enrich_profile.py`** (`--generate`/`--list`/`--show`/`--promote`/`--discard`, override `--mode`/`--model`) con `promote_override` (append atómico a `recommendations/<device>.json`, guard anti-stale por hash y re-clasificación de seguridad). Endpoints opcionales `/api/enrich/*` (auth fail-closed, imports perezosos).
- `jsonschema` en `requirements.txt`; bloque `ENRICH_*` en `.env.example`.

### Invariantes garantizados (con tests)
- La **ruta caliente del triage no lee `device_enrichments` ni importa `profile_enricher`** (sigue 100% determinista). **Nada se auto-aplica**: las sugerencias quedan en PENDING_REVIEW y solo el operador las promueve; un override promovido vuelve a pasar por `policy_engine` + HITL.

### Otros fixes de la revisión
- `sanitize_and_classify` rechaza ejecución por intérprete (`sh -c`/`bash -c`/`curl|bash`) y saltos de línea; `_path_known` normaliza el path traversal (`/var/log/../../etc/shadow`) y estrecha `/etc`; promoción re-clasifica; guard anti-stale exige ambos hashes; `_sanitize_prose` escapa HTML (XSS latente).

45 tests nuevos; 280 en total (196 PI-5 + 84 sensor).

---

## [2026-06-15] — Agente Discovery, Fase 3: perfil vivo + verbos de firewall

Tercera fase del [agente Discovery](diseno_agente_discovery.md): el sensor mantiene su perfil al día sin intervención y el Policy Engine clasifica con precisión los firewalls modernos. Pasó por una **revisión adversarial** (concurrencia + gating) que destapó y corrigió 8 defectos antes de cerrar la fase.

### Añadido
- **Sensor — perfil vivo** (`sentinel-agent/sentinel_agent/monitor.py`): re-descubrimiento periódico (config `discovery.rediscovery_interval`, opt-in) y bajo demanda (acción firmada `redescubrir`) que **republica el perfil solo si cambia el hash**. Cuando cambia *qué se vigila* (`log_sources`), **restart controlado del conjunto de tailers**: Event de generación independiente, snapshot por hilo, `join` acotado, **debounce + cap por hora** (anti-flapping) y conservación de los contadores de detección. Parámetros nuevos opcionales en `sentinel.local.yml` (`tailer_join_timeout`, `restart_min_interval`, `restart_cap_per_hour`).
- **Policy Engine — verbos de firewall** (`PI-5/src/tools/policy_engine.py`): `_classify_bounded_write` pasa a ser un dispatcher con clasificación por subcomando de **nft**, **firewall-cmd** y **ufw** (lectura→SAFE_READ; regla contra IP→LOW; flush/reset/panic→CRITICAL/HIGH), preservando que lo desconocido caiga a LOW (nunca DENY). El cuerpo de iptables queda intacto.

### Corregido (revisión adversarial)
- **🔴 Seguridad alta:** `firewall-cmd --direct --passthrough ipv4 -F` se auto-ejecutaba como `SAFE_READ` (colaba un `iptables -F` crudo como lectura). Ahora `--direct`/`--passthrough` delegan el cuerpo en el clasificador de iptables → CRITICAL/HIGH y pasan por HITL.
- **Concurrencia (sensor):** (a) carrera de shutdown — `run()` no marcaba `_stop`, lo que permitía revivir tailers tras cerrar MQTT y colgar `_pub_queue.join()`; ahora hay guard de shutdown en el coordinador, en `_publish_event` y en `transport.publish`. (b) el arranque de tailers de boot ocurría fuera del lock (un `redescubrir` temprano duplicaba la generación); ahora boot arranca bajo `_discovery_lock`. (c) `journalctl` bloqueado en `readline` quedaba huérfano en cada restart; ahora se registra el `Popen` y se hace `terminate()` al parar la generación.
- **Gating (firewall):** `firewall-cmd --lockdown-on`/`--load-zone-defaults` y reglas que abren el firewall (`accept 0.0.0.0/0`, IP solo en comentario) ya no caen a LOW; `firewall-cmd --` y `ufw --force` (sin acción real) → HIGH.
- **Hash inestable:** `_canonical_material` excluye también `exe` (volátil: `(deleted)` tras `apt upgrade`) y ordena `services`, evitando republicaciones espurias.

37 tests nuevos (firewall, firma de log_sources, restart, debounce/cap, guards de shutdown, terminación de journalctl, hash estable); 233 en total. Limitaciones conocidas documentadas en el diseño §12.1.

---

## [2026-06-14] — Agente Discovery, Fase 2: recomendaciones de mitigación deshardcodeadas

Segunda fase del [agente Discovery](diseno_agente_discovery.md): las mitigaciones que propone el agente IA dejan de estar clavadas al honeypot y se adaptan al sistema real de cada device descubierto.

### Añadido
- **`PI-5/src/recommendations/generic.json`** — manual genérico (36 entradas) por familia de ataque (ssh/ftp brute force, sqli, xss, web brute force, session hijacking, defacement, db compromise, port scan, recon). Solo contiene mitigaciones **parametrizables desde el perfil**: cada entrada lleva `requires` (capacidades), `applies_if` (condiciones del perfil), `placeholders` y **plantillas por gestor de firewall** (iptables/ufw/nftables/firewalld). Redactado y revisado en seguridad por un panel multi-agente.
- **`PI-5/src/recommendations/Pi4-Felix.json`** — override del honeypot (lo que era `recommendations.json`): mitigaciones específicas del sitio (restic+S3, `cerrar_sesion_admin.php`, doble bloqueo 80/8080, restauración de BD). Es el mecanismo de **overrides por device**.
- **`PI-5/src/tools/mitigation_manual.py`** — motor que: selecciona entradas por familia/keyword, **filtra por `requires` (capabilities) y `applies_if` (perfil)**, elige la plantilla del **firewall activo** (con fallback), **sustituye placeholders** desde el perfil (con validación: puertos 1-65535, rutas por allowlist, `web_unit` por enum), **fusiona los overrides** del device, y ante 0 coincidencias o perfil ausente devuelve **acciones genéricas seguras — nunca el manual del honeypot**. `{ip}`/`{nombre_usuario}` se dejan literales para el LLM. 17 tests (incluido el de que el honeypot nunca se filtra a otro device).

### Cambiado
- **`consultar_manual_mitigacion(query, device)`** ahora delega en el motor y recibe el `device`. Estado de módulo `set_active_device` seteado por el triage worker como fallback fiable si el LLM no pasa el device. Prompt del triage ajustado: las recomendaciones ya vienen filtradas y parametrizadas, el agente solo rellena la IP.
- Eliminado `PI-5/src/recommendations.json` (su contenido vive ahora en el override `Pi4-Felix.json`).

---

## [2026-06-14] — Agente Discovery, Fase 1: sensor genérico auto-configurable

Primera fase del [agente Discovery](diseno_agente_discovery.md): generalizar el sensor (hoy cableado al honeypot `Pi4-Felix`) a un sensor que se autodescubre en cualquier servidor y alimenta el contexto del sistema al agente IA de PI-5.

### Añadido
- **Paquete nuevo `sentinel-agent/`** (sensor genérico, reemplaza al monolito `agente_monitor3.py`, que queda como legado):
  - `discovery/` — probes con `stdlib` + utilidades Linux, degradables: OS/arch/virt, servicios y puertos (`ss`), stack web/BD (por proceso, no por puerto), fuentes de log y formato, firewall (gestor **activo**, no solo binarios), capacidades (`command -v`), usuarios (`getent`), superficie expuesta.
  - `profile_builder.py` — ensambla el **System Profile** y calcula `profile_hash` sobre las secciones materiales (excluye `discovered_at`/PIDs) + `profile_version` incremental.
  - `parsers.py` (sshd/nginx/apache/vsftpd), `detectors.py` (ventana deslizante para fuerza bruta + patrones SQLi/XSS, umbrales configurables), `executor.py` (firma + **denylist local dura** + ejecución root por defecto + eco de `log_id`), `monitor.py` (orquestador), `transport.py` (MQTT), `config.py`, `signing.py` (verificación Ed25519 byte-idéntica a PI-5).
  - CLI `python -m sentinel_agent` con `--discover-only` para inspeccionar el perfil sin desplegar. 61 tests offline.
- **PI-5 — ingesta del perfil e inyección de contexto** (todo aditivo, sin tocar transporte/firma/esquema de `logs`):
  - Tabla `device_profiles` (un device = una fila) en `database.init_schema`.
  - `upsert_device_profile` (deduplica por `profile_hash`) y `get_device_profile` en `db_tools`.
  - Rama `/perfil` en `process_event` (+ fallback telemetría `tipo=PERFIL_SISTEMA`): el perfil se **persiste, no va al LLM** ni crea fila en `logs`. Suscripción `seguridad/+/perfil`.
  - `profile_context.py`: render del bloque de contexto, cacheado por `profile_version`.
  - Inyección **por evento** del bloque `### CONTEXTO DEL SISTEMA OBJETIVO` en `_run_agent_event` (solo triage; la sesión ADK es única y compartida).
  - Prompt del triage ajustado para usar el firewall/rutas/herramientas reales del sistema descubierto en vez de asumir el honeypot. 12 tests nuevos (109 en total en PI-5).

### Seguridad
- La denylist local del sensor rechaza verbos destructivos (`rm`, `mkfs`, `dd`, `shutdown`…) aunque la firma sea válida (`status: rejected_local_policy`): defensa en profundidad junto a la firma (origen) y al Policy Engine de PI-5. La ejecución sigue siendo **root por defecto** (decisión del proyecto); `run_as` permite de-escalar.

---

## [2026-06-13] — Correlación log_id, backpressure real, hardening y saneamiento del repo

Primera jornada de la etapa post-TFG. Cierra varios de los hallazgos del análisis en profundidad del proyecto (fiabilidad del round-trip HITL, pérdida silenciosa de eventos, bypasses del Policy Engine y autenticación fail-open).

### Añadido
- **Correlación comando↔respuesta por `log_id`**: el dashboard adjunta el id de la fila al payload firmado (approve y revert), `agente_monitor3.py` lo devuelve en `seguridad/<device>/respuesta` y el coordinador llama a `mark_mitigation_result(log_id)` (hasta hoy código muerto) para actualizar **exactamente esa fila**. Se elimina la dependencia de la heurística "última fila del dispositivo" para el round-trip del dashboard; el feedback con `registro_directo: true` indica al feedback_agent que no duplique el registro.
- **Tests nuevos** (`test_hitl_approve.py`, `test_coordinator_routing.py`, `test_policy_engine_hardening.py`): 32 tests que cubren el endpoint `/api/mitigate/approve` (incluido el gate CRITICAL), la auth fail-closed, el routing del coordinador, el spill por backpressure y los bypasses del clasificador. Total de la suite offline: 97.
- **`conftest.py` + `pytest.ini`**: `pytest` a secas ya es seguro — los 8 scripts manuales/E2E que conectan a AWS real al importarse viven ahora en `tests/manual/` y quedan excluidos de la colección.
- **`database.init_schema(db_path)`**: el esquema deja de ser un script con efectos al importar; es la única fuente de verdad reutilizada por los tests (elimina el drift de esquemas duplicados a mano).
- **`.env.example` y `requirements-dev.txt`** en PI-5.

### Cambiado
- **Backpressure real en las colas**: `call_soon_threadsafe(put_nowait)` capturaba `QueueFull` en el hilo equivocado (código muerto) y los eventos por encima de 100 se perdían en silencio. Ahora el put se ejecuta dentro del loop y, si la cola está llena, el evento se persiste en `pending_ai_events` (`error_reason='queue_full'`) y el retry worker lo reprocesa.
- **Observabilidad de reconexión MQTT**: `AWSMqttClient` registra `on_connection_interrupted/resumed`, `is_alive()` refleja el estado real notificado por el SDK (antes solo miraba `_binding`, inútil tras una caída de red) y se re-suscriben los topics si AWS no conserva la sesión.
- **Autenticación del dashboard fail-closed**: sin `DASHBOARD_PASSWORD`/`DASHBOARD_PASSWORD_HASH` se deniega todo acceso (antes se permitía todo en "modo dev" — un .env mal desplegado dejaba el HITL abierto).
- **Gate CRITICAL en `/revert`**: un revert clasificado CRITICAL exige `confirm_critical`, igual que approve (antes solo se auditaba).
- **Policy Engine endurecido**: constructos de ejecución embebidos en comillas (`awk system()`, `$(...)`, backticks, `<(...)`) ya no se clasifican `SAFE_READ` (escalan a HIGH → HITL); `tcpdump -z/-w` y `find -execdir/-ok/-okdir` escalan a HIGH. Las lecturas legítimas (pipelines de `cat|grep|awk '{print}'`) siguen fluyendo sin fricción.
- **PI-4 `on_accion`**: la rama `else` publica siempre a `TOPIC_RESPUESTAS` (antes mandaba confirmaciones a topics legacy que nadie escucha). El Dockerfile de PI-4 ejecuta `agente_monitor3.py` (apuntaba al agente viejo).
- **`get_mqtt_client` del dashboard**: el bucle de conexión queda dentro del lock (dos requests concurrentes podían crear dos clientes con el mismo client_id y AWS los desconectaba mutuamente en bucle).
- **Higiene de secretos**: la contraseña root de MySQL sale de `recommendations.json` (ahora `mysql --defaults-extra-file=/home/lopex/.my.cnf`; hay que crear ese fichero en PI-4 y **rotar la contraseña**, que estuvo en el repo público). `ssh_run.py`/`scp_upload.py` leen `PI_PASSWORD` del entorno; `scp_upload.py` se destrackea de git (la credencial vivía en el historial). `.env` alineado al modelo documentado `gemini-3-flash-preview` (estaba en `gemini-2.5-pro`, probable causa del 429 por tope de gasto).
- **Logging tolerante**: coordinador y dashboard arrancan aunque la ruta del fichero de log no exista (p. ej. desarrollo en Windows) — siguen con consola.

### Corregido
- `.gitignore` contradictorio: se eliminan las entradas `PI-4/` y `.gitignore` (ambos trackeados). La entrada `PI-4/` ocultaba en silencio archivos nuevos del sensor: `signing.py` (¡el verificador Ed25519!), `sentinel_pi5_signing.pub`, `requirements.txt` y `Policy v2.json` no estaban versionados, y `test_signing.py` era irreproducible en un clon limpio.
- Eliminados duplicados y restos: `docs/MQTT_Resilience-DANIEL.md` (copia byte a byte), `PI-5/TFG_Technical_Reference.md` (idéntico al archivado), `agente_monitor.py` (versión obsoleta del agente del sensor).

### Validado (sin cambio)
- El `PRAGMA busy_timeout` que proponía el informe semanal **no es necesario**: el parámetro `timeout=` de `sqlite3.connect()` que ya usan todas las conexiones es exactamente el busy timeout.

---

## [2026-05-28] — Resiliencia ante Gemini 429 (commit `5dbfd12`)

Implementación completa de [plan_implementacion_resiliencia_gemini_429.md](plan_implementacion_resiliencia_gemini_429.md) tras el incidente del 2026-05-28 (`429 RESOURCE_EXHAUSTED` por tope de gasto mensual).

### Añadido
- **Tabla `pending_ai_events`** (`tools/pending_ai_events.py`): los eventos que el modelo remoto no pudo procesar se persisten en vez de perderse.
- **Worker de reintentos** (`_pending_ai_retry_worker` en `main_coordinator.py`): reprocesa eventos vencidos con backoff 60/300/900/3600s.
- **Contador en el dashboard** de eventos pendientes de IA.
- **Purga desde SOC Manager** (opción 5→3) que limpia también `pending_ai_events`.
- Tests `test_pending_ai_events.py` y `test_soc_manager_script.py`.

### Cambiado
- `AI_MODEL` fijado explícitamente a `gemini-3-flash-preview` (sin alias movibles) en `config.yml` y `soc_manager.sh`.

Commits intermedios sin entrada propia: `db258f1` (permisos de ejecución autónoma), `f981308` (corrección de parámetros), `6c844e4` (fallo de ruta), `c7eabab` (mitigación XSS), `e883ea0` (recomendaciones).

---

## [2026-05-27] - Revert editable con rollback explicito

Correccion del flujo de **REVERTIR** en el dashboard del API 5. El comportamiento anterior podia construir comandos comentados (`# REVERT: ...`) o un fallback generico de `iptables -D`, lo que daba la sensacion de revertir sin garantizar que se estuviera deshaciendo el comando real ejecutado por PI-5.

### Anadido
- **Campo `revert_command` en `logs`**: almacena el rollback explicito de una mitigacion cuando el agente o PI-5 pueden conocerlo con seguridad.
- **Parametro opcional `revert_command` en `request_mitigation_approval`**: triage y feedback pueden adjuntar el comando exacto que revierte la mitigacion propuesta.
- **Helper `tools/revert_commands.py`**: deriva solo inversiones conservadoras conocidas (`iptables -A/-I` a `-D`, `ufw delete`, `systemctl/service start|stop|enable|disable`).
- **Tests `test_revert_commands.py`**: cubren inversiones derivables y aseguran que un comando desconocido no genera rollback inventado.

### Cambiado
- El modal de revert usa un `<textarea>` editable y envia el comando elegido al backend.
- `/revert/<id>` prioriza el comando editado por el operador, despues `revert_command`, y solo al final una derivacion segura desde `pending_command`.
- Tras aprobar o revertir, `pending_command` se actualiza con el comando real enviado para que **VER COMANDO** muestre lo ultimo despachado.
- Las instrucciones de los agentes especifican que deben dejar `revert_command` vacio cuando no exista rollback seguro sin estado previo.

### Corregido
- Ya no se publica un comentario como comando de reversión.
- Ya no se inventa `sudo iptables -D INPUT -s <ip> -j DROP` para comandos que no eran ese bloqueo concreto.

---

## [2026-05-20] — Procesamiento Inmediato con asyncio.Queue

Reemplazo completo del sistema de microbatching con doble trigger por un sistema de colas asíncronas para eliminar delays artificiales y usar la API recomendada `runner.run_async()`.

### ✨ Añadido
- **Workers asíncronos**: Implementación de `_worker()` utilizando `runner.run_async()` de Google ADK.
- **Puente Thread-Safe**: Método `_enqueue_from_thread` con `call_soon_threadsafe` para pasar eventos del hilo de callbacks de `awscrt` al event loop de asyncio.
- **Backpressure**: Configuración de `queue.max_size` en `config.yml` con límite de 100 eventos para proteger la memoria de la PI-5.

### 🔧 Cambiado
- **Eliminación de Microbatches**: Se elimina la clase `LogBatchQueue`, los dispatchers periódicos y las esperas artificiales. El primer evento se procesa a los 0ms de llegar.
- **Loop de Eventos**: El entry point de `main_coordinator.py` ahora corre sobre `asyncio.run(main())`.

### 📁 Archivos modificados hoy
| Archivo | Tipo de cambio |
|---------|---------------|
| `PI-5/config.yml` | Sección `queue` de backpressure en lugar de `batch` |
| `PI-5/src/main_coordinator.py` | Migración de threading/LogBatchQueue a asyncio/Queue |
| `PI-5/tests/test_agent_flow.py` | Ajustes en comentarios del test de flujo |
| `docs/*` | Actualización de toda la documentación técnica sobre el flujo de colas y latencia |

---

## [2026-05-19] — Firma Ed25519, Reconexión MQTT, Rediseño Dashboard

Jornada intensiva de desarrollo: **4 commits en `main`**, más la rama `feature/policy-engine`. Resumen por área funcional.

### ✨ Añadido

#### Firma criptográfica Ed25519 (`97ba24b`)
- **Módulo `PI-5/src/tools/signing.py`**: firma de comandos PI-5 → PI-4 con campos `iat`, `exp`, `nonce` y `sig` (base64 Ed25519 sobre JSON canónico).
- **Script `scripts/generate_signing_keys.py`**: genera par de claves Ed25519 (`.key` privada en PI-5, `.pub` pública en PI-4).
- **Integración en `main_coordinator.py`**: todo payload publicado a `seguridad/{device}/comando` se firma antes del envío.
- **Integración en `dashboard_soc.py`**: los endpoints `/api/mitigate/approve` y `/revert/<id>` firman el payload antes del publish MQTT.
- **Sección `signing` en `config.yml`**: paths de claves y TTL configurable.
- **Tests**: 7 tests de firma + 8 tests del normalizador de feedback — todos verdes.

#### Normalización del feedback del sensor (`97ba24b`)
- `feedback_agent.py` ahora normaliza los tres shapes posibles de respuesta de PI-4 (v3, rejected_signature, legacy plano) a un dict canónico de 5 campos (`sensor`, `command`, `status`, `output`, `exitcode`).

#### Catálogo de recomendaciones ampliado (`97ba24b`)
- `recommendations.json`: nuevas entradas para bloqueo/desbloqueo de IP en HTTP+8080 (proxy + servidor real) y restauración vía restic.

#### Detección de conexiones MQTT zombie (`c00d61a`)
- **`AWSMqttClient.is_alive()`**: comprueba el handle nativo `_binding` del SDK awscrt para detectar conexiones donde el objeto Python existe pero el socket TCP/TLS está muerto.
- **`AWSMqttClient.disconnect()`**: desconexión limpia con cleanup del handle para permitir reconexión.
- **Mensajes de error descriptivos en `publish()`**: si `publish_future.result()` falla con excepción vacía, se reemplaza por `"PUBACK timeout or connection lost"`.

### 🐛 Corregido

#### DNS crash-loop en Docker (`3b5eb3b`)
- **Problema**: el contenedor Docker arrancaba antes de que el resolver DNS del host estuviera listo, provocando `AWS_IO_DNS_QUERY_FAILED` en bucle infinito.
- **Causa raíz**: `main_coordinator.py` intentaba una única conexión MQTT al arrancar — si el DNS fallaba, el proceso moría y Docker lo reiniciaba en bucle.
- **Solución**: 
  - `main_coordinator.py`: retry con backoff exponencial (6 intentos, delay inicial 2s, max 8s).
  - `docker-compose.yml`: configuración DNS explícita (`dns: [8.8.8.8, 1.1.1.1]`) como fallback.
  - `soc_manager.sh`: verificación de conectividad DNS antes de `docker compose up`.

#### Conexión MQTT zombie en dashboard → 502 en HITL (`c00d61a`)
- **Problema**: `POST /api/mitigate/approve` devolvía `502 Bad Gateway` con el mensaje `[ERROR] Publish HITL fallo, no se actualiza DB:` (error vacío).
- **Causa raíz**: la conexión MQTT del dashboard (`Dashboard-SOC-Pi5`) moría tras un corte transitorio de red/DNS. El objeto `self.connection` de Python seguía no siendo `None`, pero el socket TLS subyacente estaba muerto. El check `getattr(mqtt_client, 'connection', None) is not None` en `get_mqtt_client()` devolvía `True` → se intentaba publicar en un cliente muerto → `publish_future.result()` fallaba con excepción vacía → 502.
- **Solución**: 
  - `AWSMqttClient.is_alive()`: health check real a nivel de SDK.
  - `get_mqtt_client()`: detecta zombie, llama `disconnect()`, reconecta con backoff.
  - `publish()`: pre-check con `is_alive()` + wrapper de excepciones con mensajes descriptivos.
  - Todos los endpoints del dashboard migrados de `getattr()` a `is_alive()`.

#### Arreglos varios de Docker (`923c33d`)
- `docker-compose.yml`: ajustes de volúmenes y configuración.
- `dashboard_soc.py`: correcciones en la serialización de logs y manejo de columnas faltantes.
- `agente_monitor3.py` (PI-4): mejoras en el agente de monitorización.

### 🔧 Cambiado

#### Eliminación del sistema INTRUSION-COMMAND-INJECTION (`97ba24b`)
- La detección reactiva de inyección de comandos (caché de despachos `record_dispatch` / `match_feedback` en `policy_engine.py`) fue reemplazada por la firma Ed25519 proactiva. La garantía de autenticidad pasa de ser *a posteriori* (detectar después) a ser *a priori* (verificar antes de ejecutar).

### 📁 Archivos modificados hoy

| Archivo | Tipo de cambio |
|---------|---------------|
| `PI-5/src/aws_connector.py` | Añadidos `is_alive()`, `disconnect()`, mejora en `publish()` |
| `PI-5/src/dashboard_soc.py` | Reconexión MQTT, firma de payloads, checks `is_alive()` |
| `PI-5/src/main_coordinator.py` | Retry DNS, firma de comandos, normalización feedback |
| `PI-5/src/tools/signing.py` | **Nuevo** — módulo de firma Ed25519 |
| `PI-5/src/tools/policy_engine.py` | Eliminada caché de despachos, simplificación |
| `PI-5/src/agents/feedback_agent/feedback_agent.py` | Normalización de feedback |
| `PI-5/src/agents/triage_agent/triage_agent.py` | Integración con firma |
| `PI-5/src/recommendations.json` | Nuevas recomendaciones de mitigación |
| `PI-5/config.yml` | Sección `signing` |
| `PI-5/docker-compose.yml` | DNS explícito, ajustes de volúmenes |
| `PI-5/requirements.txt` | Dependencia `cryptography` |
| `PI-4/Agente de monitorizacion/agente_monitor3.py` | Mejoras en monitorización |
| `scripts/generate_signing_keys.py` | **Nuevo** — generador de claves |
| `PI-5/tests/test_signing.py` | **Nuevo** — tests de firma |
| `PI-5/tests/test_feedback_normalizer.py` | **Nuevo** — tests de normalización |
| `docs/Configuration_and_Deployment.md` | Sección 8: firma Ed25519 |

---

## Convenciones

- Cada entrada incluye el hash corto del commit entre paréntesis.
- Los bugs documentan: **Problema** (síntoma visible), **Causa raíz** (por qué ocurría) y **Solución** (qué se hizo).
- Los archivos **nuevos** se marcan explícitamente.
