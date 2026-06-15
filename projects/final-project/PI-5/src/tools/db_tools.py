import os
import sqlite3
import yaml
import logging
import time

# Calculo de rutas y carga de configuracion global
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yml')

try:
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    DB_PATH = os.path.join(BASE_DIR, config['database']['db_path'])
    
    # Parametros de retencion para la limpieza automatica
    _RETENTION_MAX_DAYS = config.get('retention', {}).get('max_days', 30)
    _RETENTION_PURGE_ON_INSERT = config.get('retention', {}).get('purge_on_insert', True)
except Exception:
    DB_PATH = os.path.join(BASE_DIR, "soc_data.db")
    _RETENTION_MAX_DAYS = 30
    _RETENTION_PURGE_ON_INSERT = True

logger = logging.getLogger("CoordinatorSOC")

def rotate_old_logs() -> dict:
    """
    Elimina registros antiguos de baja prioridad (Solo Registro) segun la politica de retencion.
    """
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')
        cursor = conn.cursor()

        # Conteo previo de registros a eliminar
        cursor.execute(
            """
            SELECT COUNT(*) FROM logs
            WHERE accion_tomada = 'Solo Registro'
              AND timestamp <= datetime('now', ?)
            """,
            (f"-{_RETENTION_MAX_DAYS} days",)
        )
        count_before = cursor.fetchone()[0]

        if count_before == 0:
            conn.close()
            return {"status": "ok", "purged": 0}

        # Ejecucion de la limpieza
        cursor.execute(
            """
            DELETE FROM logs
            WHERE accion_tomada = 'Solo Registro'
              AND timestamp <= datetime('now', ?)
            """,
            (f"-{_RETENTION_MAX_DAYS} days",)
        )
        conn.commit()
        conn.close()

        logger.info(f"[INFO] Limpieza de base de datos: {count_before} registros eliminados.")
        return {"status": "ok", "purged": count_before}

    except Exception as e:
        logger.error(f"[ERROR] Error en la rotacion de logs: {e}")
        return {"status": "error", "message": str(e)}

def register_alert(device: str, attack_vector: str, source_ip: str, severity: str, verdict: str, raw_log: str) -> dict:
    """
    Registra un incidente de seguridad en la base de datos local.
    
    Args:
        device: Nombre del dispositivo de origen.
        attack_vector: Etiqueta estricta del protocolo o servicio atacado (ej. SSH, NGINX-HTTP, MYSQL, PORT-SCAN).
        source_ip: IP asociada a la amenaza (MUST strictly be a valid IPv4/IPv6 address).
        severity: Nivel (Baja, Media, Alta, Critica).
        verdict: Resumen conciso del razonamiento logico del agente (chain-of-thought summary).
        raw_log: Texto original literal del log analizado.
    """
    if _RETENTION_PURGE_ON_INSERT:
        rotate_old_logs()

    # Politica de reintentos para manejar bloqueos en SQLite
    for attempt in range(5):
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH, timeout=15.0, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL;')
            conn.execute('PRAGMA synchronous=NORMAL;')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs (dispositivo, servicio, log_original, ip_origen, nivel_gravedad, veredicto_ia, accion_tomada)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (device, attack_vector, raw_log, source_ip, severity, verdict, "Solo Registro"))
            conn.commit()
            logger.info(f"[INFO] Alerta registrada para IP: {source_ip}")
            return {"status": "success", "message": "Log guardado correctamente. NO LLAMAR a register_alert de nuevo. Procede con block_ip si es necesario."}
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() or "readonly" in str(e).lower():
                logger.warning(f"[WARNING] Base de datos ocupada, reintento {attempt+1}/5...")
                time.sleep(2)
            else:
                logger.error(f"[ERROR] Error de base de datos: {e}")
                return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"[ERROR] Error no contemplado en registro: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if conn:
                conn.close()
    return {"status": "error", "message": "Database timeout after retries"}

def mark_mitigation_result(log_id: int, mitigation_status: str, command_result: str) -> dict:
    """
    Actualiza estado_mitigacion en la fila concreta identificada por log_id.

    A diferencia de update_alert_status (que escribe en la fila mas reciente del
    dispositivo y depende de que el feedback_agent procese el batch), este
    metodo es la via rapida del round-trip HITL: el coordinador lo invoca en
    cuanto llega una respuesta de PI-4 que correlaciona con un dispatch
    conocido, para que el dashboard vea el resultado en el siguiente poll
    (1 segundo) en lugar de esperar el flush del batch (15 s) y la latencia
    del LLM.

    Args:
        log_id: ID exacto de la fila en logs.
        mitigation_status: 'EXITO' o 'FALLO'.
        command_result: salida literal de la terminal en PI-4.
    """
    for attempt in range(5):
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH, timeout=15.0, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            cursor.execute(
                '''
                UPDATE logs
                SET estado_mitigacion = CASE
                    WHEN estado_mitigacion IS NULL OR estado_mitigacion = '' THEN ?
                    ELSE estado_mitigacion || ?
                END
                WHERE id = ?
                ''',
                (
                    f"[{mitigation_status}] {command_result}",
                    f"\n[{mitigation_status}] {command_result}",
                    log_id,
                ),
            )
            rowcount = cursor.rowcount
            conn.commit()
            if rowcount > 0:
                logger.info(
                    f"[INFO] Round-trip OK: log_id={log_id} -> {mitigation_status}"
                )
                return {"status": "success", "rowcount": rowcount}
            return {"status": "warning", "message": f"No row with id={log_id}"}
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < 4:
                time.sleep(1)
                continue
            logger.error(f"[ERROR] mark_mitigation_result: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"[ERROR] mark_mitigation_result: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if conn:
                conn.close()
    return {"status": "error", "message": "Database timeout after retries"}


def upsert_device_profile(
    device: str,
    profile: dict,
    db_path: str = None,
) -> dict:
    """
    Inserta o actualiza el System Profile de un device. Deduplica por
    profile_hash: si el hash no cambió respecto a lo almacenado, NO reescribe
    (evita churn). Devuelve {status, changed}.

    `profile` es el dict del perfil tal cual lo publica el sensor en
    seguridad/<device>/perfil. No va al LLM: solo se persiste aquí.
    """
    import json as _json
    path = db_path or DB_PATH
    new_hash = profile.get("profile_hash")
    # Defensa anti-stale: un perfil sin profile_hash se almacenaría con NULL y
    # dejaría a los enriquecimientos sin ancla de verificación (el guard de
    # promote_override no podría comparar). Lo rechazamos en origen.
    if not new_hash:
        logger.error(f"[PROFILE] Perfil de '{device}' sin profile_hash; descartado (defensa anti-stale).")
        return {"status": "error", "changed": False, "message": "perfil sin profile_hash; descartado"}
    for attempt in range(5):
        conn = None
        try:
            conn = sqlite3.connect(path, timeout=15.0, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL;')
            cur = conn.cursor()
            row = cur.execute(
                "SELECT profile_hash FROM device_profiles WHERE device = ?", (device,)
            ).fetchone()
            if row and row[0] and row[0] == new_hash:
                conn.close()
                return {"status": "success", "changed": False}

            fw = (profile.get("firewall") or {}).get("active_manager")
            web = (profile.get("web_server") or {}).get("engine") if profile.get("web_server") else None
            dbe = (profile.get("db_engine") or {}).get("engine") if profile.get("db_engine") else None
            host = profile.get("host") or {}
            cur.execute(
                """
                INSERT INTO device_profiles
                    (device, schema_version, profile_version, profile_hash,
                     os_id, os_version, firewall, web_server, db_engine,
                     raw_profile_json, discovered_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(device) DO UPDATE SET
                    schema_version=excluded.schema_version,
                    profile_version=excluded.profile_version,
                    profile_hash=excluded.profile_hash,
                    os_id=excluded.os_id,
                    os_version=excluded.os_version,
                    firewall=excluded.firewall,
                    web_server=excluded.web_server,
                    db_engine=excluded.db_engine,
                    raw_profile_json=excluded.raw_profile_json,
                    discovered_at=excluded.discovered_at,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (device, profile.get("schema_version"), profile.get("profile_version"),
                 new_hash, host.get("os_id"), host.get("os_version"), fw, web, dbe,
                 _json.dumps(profile, ensure_ascii=False), profile.get("discovered_at")),
            )
            conn.commit()
            conn.close()
            logger.info(f"[PROFILE] Perfil de '{device}' actualizado (v{profile.get('profile_version')}).")
            # Perfil nuevo -> los enriquecimientos pendientes quedan obsoletos.
            try:
                superseded = supersede_pending_enrichments(device, path)
                if superseded:
                    logger.info(f"[PROFILE] {superseded} enriquecimiento(s) de '{device}' marcados SUPERSEDED.")
            except Exception as e:  # noqa: BLE001 — no romper el upsert por esto
                logger.error(f"[PROFILE] Error superseding enrichments: {e}")
            return {"status": "success", "changed": True}
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < 4:
                time.sleep(1)
                continue
            logger.error(f"[ERROR] upsert_device_profile: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"[ERROR] upsert_device_profile: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if conn:
                conn.close()
    return {"status": "error", "message": "Database timeout after retries"}


def save_enrichment(device, profile_hash, profile_version, payload, discarded,
                    model_used=None, ai_mode=None, confidence=None, db_path=None) -> int:
    """Inserta un enriquecimiento (ya validado) con status PENDING_REVIEW. Devuelve su id."""
    import json as _json
    path = db_path or DB_PATH
    for attempt in range(5):
        conn = None
        try:
            conn = sqlite3.connect(path, timeout=15.0, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL;')
            cur = conn.execute(
                """
                INSERT INTO device_enrichments
                    (device, profile_hash, profile_version, enrichment_json, discarded_json,
                     model_used, ai_mode, confidence, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_REVIEW')
                """,
                (device, profile_hash, profile_version,
                 _json.dumps(payload, ensure_ascii=False),
                 _json.dumps(discarded or [], ensure_ascii=False),
                 model_used, ai_mode, confidence),
            )
            conn.commit()
            return int(cur.lastrowid)
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < 4:
                time.sleep(1)
                continue
            logger.error(f"[ERROR] save_enrichment: {e}")
            raise
        finally:
            if conn:
                conn.close()
    raise RuntimeError("Database timeout after retries")


def _row_to_enrichment(row) -> dict:
    import json as _json
    return {
        "id": row[0], "device": row[1], "profile_hash": row[2], "profile_version": row[3],
        "enrichment": _json.loads(row[4]) if row[4] else {},
        "discarded": _json.loads(row[5]) if row[5] else [],
        "model_used": row[6], "ai_mode": row[7], "confidence": row[8], "status": row[9],
        "promoted_item_ids": _json.loads(row[10]) if row[10] else [],
        "created_at": row[11], "reviewed_at": row[12],
    }


_ENRICH_COLS = ("id, device, profile_hash, profile_version, enrichment_json, discarded_json, "
                "model_used, ai_mode, confidence, status, promoted_item_ids, created_at, reviewed_at")


def list_enrichments(device, status=None, db_path=None) -> list:
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(path, timeout=10.0, check_same_thread=False)
        if status:
            rows = conn.execute(
                f"SELECT {_ENRICH_COLS} FROM device_enrichments WHERE device=? AND status=? ORDER BY id DESC",
                (device, status)).fetchall()
        else:
            rows = conn.execute(
                f"SELECT {_ENRICH_COLS} FROM device_enrichments WHERE device=? ORDER BY id DESC",
                (device,)).fetchall()
        conn.close()
        return [_row_to_enrichment(r) for r in rows]
    except Exception as e:
        logger.error(f"[ERROR] list_enrichments: {e}")
        return []


def get_enrichment(enrichment_id, db_path=None) -> dict:
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(path, timeout=10.0, check_same_thread=False)
        row = conn.execute(
            f"SELECT {_ENRICH_COLS} FROM device_enrichments WHERE id=?", (enrichment_id,)).fetchone()
        conn.close()
        return _row_to_enrichment(row) if row else {}
    except Exception as e:
        logger.error(f"[ERROR] get_enrichment: {e}")
        return {}


def set_enrichment_status(enrichment_id, status, promoted_item_ids=None, db_path=None) -> dict:
    import json as _json
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')
        conn.execute(
            "UPDATE device_enrichments SET status=?, reviewed_at=CURRENT_TIMESTAMP, "
            "promoted_item_ids=? WHERE id=?",
            (status, _json.dumps(promoted_item_ids) if promoted_item_ids is not None else None, enrichment_id))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        logger.error(f"[ERROR] set_enrichment_status: {e}")
        return {"status": "error", "message": str(e)}


def supersede_pending_enrichments(device, db_path=None) -> int:
    """Marca SUPERSEDED los PENDING_REVIEW del device (al llegar un perfil nuevo)."""
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')
        cur = conn.execute(
            "UPDATE device_enrichments SET status='SUPERSEDED', reviewed_at=CURRENT_TIMESTAMP "
            "WHERE device=? AND status='PENDING_REVIEW'", (device,))
        n = cur.rowcount
        conn.commit()
        conn.close()
        return int(n)
    except Exception as e:
        logger.error(f"[ERROR] supersede_pending_enrichments: {e}")
        return 0


def get_device_profile(device: str, db_path: str = None) -> dict:
    """Devuelve el perfil completo (dict) de un device, o {} si no hay."""
    import json as _json
    path = db_path or DB_PATH
    try:
        conn = sqlite3.connect(path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')
        row = conn.execute(
            "SELECT raw_profile_json, profile_version FROM device_profiles WHERE device = ?",
            (device,),
        ).fetchone()
        conn.close()
        if not row or not row[0]:
            return {}
        return _json.loads(row[0])
    except Exception as e:
        logger.error(f"[ERROR] get_device_profile: {e}")
        return {}


def update_alert_status(device: str, command_result: str, mitigation_status: str) -> dict:
    """
    Actualiza el estado de mitigación del último evento registrado para un dispositivo, 
    permitiendo a los agentes tener feedback sobre si sus defensas funcionaron.
    
    Args:
        device: Nombre del dispositivo origen (ej. 'Pi4-Sensor-01').
        command_result: Salida literal devuelta por la terminal.
        mitigation_status: 'EXITO' si funcionó, 'FALLO' si el sistema devolvió un error.
    """
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL;')
        cursor = conn.cursor()
        
        # Actualizamos la fila más reciente (ID más alto) correspondiente a este dispositivo
        cursor.execute('''
            UPDATE logs 
            SET estado_mitigacion = CASE 
                WHEN estado_mitigacion IS NULL THEN ?
                ELSE estado_mitigacion || ? 
            END
            WHERE id = (
                SELECT id FROM logs 
                WHERE dispositivo = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            )
        ''', (f"[{mitigation_status}] {command_result}", f"\n[{mitigation_status}] {command_result}", device))
        
        rowcount = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rowcount > 0:
            logger.info(f"[INFO] Feedback registrado en DB (Dispositivo: {device} | Status: {mitigation_status})")
            return {"status": "success", "message": "Feedback escrito exitosamente en la base de datos."}
        else:
            return {"status": "warning", "message": "No se encontraron alertas previas para este dispositivo."}
    except Exception as e:
        logger.error(f"[ERROR] Error al actualizar status de alerta: {e}")
        return {"status": "error", "message": str(e)}
