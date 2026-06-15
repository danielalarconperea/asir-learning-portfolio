import sqlite3
import os
import yaml
from tools.pending_ai_events import init_pending_ai_events_schema

# Rutas base y configuracion
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yml')


def _resolve_db_path() -> str:
    """Carga la ruta de la base de datos desde el archivo de configuracion."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
        return os.path.join(BASE_DIR, config['database']['db_path'])
    except Exception as e:
        print(f"[ERROR] Error al cargar configuracion, usando ruta por defecto: {e}")
        return os.path.join(BASE_DIR, "soc_data.db")


def init_schema(db_path: str) -> None:
    """
    Crea (o migra) el esquema completo del SOC en la base de datos indicada.

    Es la UNICA fuente de verdad del esquema: los tests deben llamar a esta
    funcion sobre una BD temporal en vez de duplicar los CREATE TABLE a mano
    (la duplicacion ya provoco drift: tests sin la columna revert_command).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Esquema de la tabla 'logs' para almacenar incidentes y decisiones del agente IA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo TEXT,
            servicio TEXT,
            log_original TEXT,
            ip_origen TEXT,
            nivel_gravedad TEXT,
            veredicto_ia TEXT,
            accion_tomada TEXT,
            estado_mitigacion TEXT,
            status TEXT DEFAULT 'LOGGED',
            pending_command TEXT,
            rationale TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            revert_command TEXT
        )
    ''')

    # Migración para bases de datos existentes: intentar añadir las nuevas columnas
    try:
        cursor.execute('ALTER TABLE logs ADD COLUMN estado_mitigacion TEXT')
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE logs ADD COLUMN status TEXT DEFAULT 'LOGGED'")
        cursor.execute("ALTER TABLE logs ADD COLUMN pending_command TEXT")
        cursor.execute("ALTER TABLE logs ADD COLUMN rationale TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE logs ADD COLUMN revert_command TEXT")
    except sqlite3.OperationalError:
        pass

    # Tabla de auditoria append-only para el Policy Engine.
    # Cierra el hueco "sin trazabilidad ordenada" del doc futuras_mejoras.md
    # (mapeo con NIST SP 800-53 AU-2 e ISO 27001 A.12.4).
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            device TEXT,
            command TEXT,
            classification TEXT,
            decision_reason TEXT,
            related_log_id INTEGER,
            FOREIGN KEY (related_log_id) REFERENCES logs(id)
        )
    ''')

    # Triggers anti-modificacion: la integridad del log de auditoria depende de
    # que nadie pueda editarlo a posteriori desde la aplicacion.
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS audit_log_no_update
        BEFORE UPDATE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only');
        END
    ''')
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS audit_log_no_delete
        BEFORE DELETE ON audit_log
        BEGIN
            SELECT RAISE(ABORT, 'audit_log is append-only');
        END
    ''')

    # Perfil del sistema descubierto por cada sensor (agente Discovery).
    # Un device = una fila (PK device). Se guarda el JSON crudo del perfil mas
    # campos desnormalizados para consulta rapida desde el dashboard/contexto.
    # Tabla aparte: NO se tocan columnas de 'logs' (el dashboard la lee por
    # indice posicional). Ver docs/diseno_agente_discovery.md.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_profiles (
            device TEXT PRIMARY KEY,
            schema_version INTEGER,
            profile_version INTEGER,
            profile_hash TEXT,
            os_id TEXT,
            os_version TEXT,
            firewall TEXT,
            web_server TEXT,
            db_engine TEXT,
            raw_profile_json TEXT,
            discovered_at TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Enriquecimientos LLM del perfil (Fase 4). Tabla SEPARADA de device_profiles:
    # el perfil determinista no se contamina. Sin triggers anti-update (status SÍ
    # debe poder mutar: PENDING_REVIEW -> PROMOTED/DISCARDED/SUPERSEDED).
    # Ver docs/diseno_agente_discovery.md §12.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_enrichments (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            device            TEXT NOT NULL,
            profile_hash      TEXT,
            profile_version   INTEGER,
            enrichment_json   TEXT NOT NULL,
            discarded_json    TEXT,
            model_used        TEXT,
            ai_mode           TEXT,
            confidence        TEXT,
            status            TEXT NOT NULL DEFAULT 'PENDING_REVIEW',
            promoted_item_ids TEXT,
            created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
            reviewed_at       DATETIME
        )
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_enrich_device_status
            ON device_enrichments (device, status)
    ''')

    conn.commit()
    conn.close()

    init_pending_ai_events_schema(db_path)


if __name__ == "__main__":
    DB_PATH = _resolve_db_path()
    init_schema(DB_PATH)
    print(f"[INFO] Base de datos preparada en: {DB_PATH}")
