"""
Cross-check de la salida del enriquecedor contra el perfil DETERMINISTA.

Funciones puras (sin LLM ni BD): comprueban que cada sugerencia del LLM apunta a
algo que EXISTE de verdad en el inventario del device. Lo no respaldado se
descarta (DISCARD) o baja de confianza (downgrade). Reutiliza el motor de Fase 2
(mitigation_manual) para que un override aceptado se comporte igual que en caliente.

Ver docs/diseno_agente_discovery.md §12 (Fase 4).
"""

from __future__ import annotations

import posixpath
import re
from typing import List, Tuple

from tools import mitigation_manual as mm

LOG_PATH_PREFIXES = ("/var/log/", "/var/www/", "/etc/")
_WEB_DETECTORS = {"sqli", "xss", "web_bruteforce"}
_ABS_PATH_RE = re.compile(r"/[\w./-]+")


def facts(profile: dict) -> dict:
    """Índice plano de los hechos crudos del perfil, para los chequeos."""
    services = profile.get("services") or []
    log_sources = profile.get("log_sources") or []
    web = profile.get("web_server") or {}
    return {
        "services_procs": {(s.get("proc") or "").lower() for s in services if s.get("proc")},
        "services_units": {(s.get("unit") or "") for s in services if s.get("unit")},
        "service_ports": {s.get("port") for s in services if s.get("port")},
        "log_paths": {ls.get("path") for ls in log_sources if ls.get("path")},
        "log_units": {ls.get("unit") for ls in log_sources if ls.get("unit")},
        "log_ids": {ls.get("id") for ls in log_sources if ls.get("id")},
        "caps_true": {k for k, v in (profile.get("capabilities") or {}).items() if v},
        "web_engine": web.get("engine"),
        "web_docroots": set(web.get("docroots") or []),
        "web_configs": set(web.get("config_paths") or []),
        "db_engine": (profile.get("db_engine") or {}).get("engine"),
        "os_id": (profile.get("host") or {}).get("os_id"),
        "fw": (profile.get("firewall") or {}).get("active_manager"),
    }


def extract_abs_paths(cmd: str) -> List[str]:
    """Rutas absolutas del comando con al menos 2 segmentos (ignora /tmp, /etc sueltos)."""
    out = []
    for m in _ABS_PATH_RE.findall(cmd or ""):
        if len([seg for seg in m.strip("/").split("/") if seg]) >= 2:
            out.append(m)
    return out


def _path_known(p: str, F: dict) -> bool:
    # Normaliza ANTES de comparar: neutraliza el traversal
    # (/var/log/../../etc/shadow -> /etc/shadow). posixpath, no os.path (en
    # Windows convertiría / en \ y rompería rutas Linux).
    p = posixpath.normpath(p)
    if p in F["web_docroots"] or p in F["web_configs"] or p in F["log_paths"]:
        return True
    if any(p.startswith(dr.rstrip("/") + "/") for dr in F["web_docroots"]):
        return True
    # /etc ya NO entero (cubría /etc/shadow): solo bajo un config_path del perfil.
    if any(p.startswith(cfg.rstrip("/") + "/") for cfg in F["web_configs"]):
        return True
    return p.startswith("/var/log/")


def check_log_source(ls: dict, F: dict) -> Tuple[str, str, List[str]]:
    """(KEEP|DISCARD, motivo, downgrades) para una fuente de log sugerida."""
    downgrades: List[str] = []
    service = (ls.get("service") or "").lower()
    known = (service in F["services_procs"] or service == F["web_engine"]
             or service == F["db_engine"]
             or any(service and service in (u or "").lower() for u in F["services_units"]))
    if not known:
        return "DISCARD", f"servicio '{service}' no está en el inventario", downgrades

    src = ls.get("source")
    if src == "file":
        path = ls.get("path")
        if not path or not str(path).startswith(LOG_PATH_PREFIXES):
            return "DISCARD", f"path '{path}' fuera de la allowlist de logs", downgrades
        if path in F["log_paths"]:
            downgrades.append("ya vigilado (redundante)")
    elif src == "journald":
        unit = ls.get("unit") or ""
        ub = unit.replace(".service", "").lower()
        if not (unit in F["log_units"] or ub in F["services_procs"]
                or any(ub and ub in (u or "").lower() for u in F["services_units"])):
            return "DISCARD", f"unit '{unit}' no existe en el inventario", downgrades

    dets = set(ls.get("detectors") or [])
    if dets & _WEB_DETECTORS and service != F["web_engine"]:
        downgrades.append("detectores web sobre servicio no-web")
    if not ls.get("evidence"):
        downgrades.append("sin evidencia")
    return "KEEP", "", downgrades


def check_override(ov: dict, F: dict, profile: dict) -> Tuple[str, str, List[str]]:
    """(KEEP|DISCARD, motivo, downgrades) para un override de mitigación sugerido."""
    downgrades: List[str] = []

    for r in ov.get("requires") or []:
        if r not in F["caps_true"]:
            return "DISCARD", f"requires '{r}' no disponible en el device", downgrades

    for k, v in (ov.get("applies_if") or {}).items():
        try:
            ok = mm._condition_ok(k, v, profile)
        except Exception:
            ok = False
        if not ok:
            return "DISCARD", f"applies_if '{k}' no se cumple en el perfil", downgrades

    for field in ("command", "revert"):
        cmd = ov.get(field) or ""
        for p in extract_abs_paths(cmd):
            if not _path_known(p, F):
                return "DISCARD", f"ruta '{p}' no respaldada por el perfil (¿alucinación?)", downgrades
        for ph in mm._detect_placeholders(cmd):
            if ph in mm._LITERAL_PLACEHOLDERS:
                continue
            val = mm._resolve_placeholder(ph, profile)
            if val in (None, "", []):
                return "DISCARD", f"placeholder '{{{ph}}}' no resoluble en el perfil", downgrades

    if not ov.get("evidence"):
        downgrades.append("sin evidencia")
    return "KEEP", "", downgrades


def check_note(risk: dict, profile: dict) -> str:
    """
    Devuelve un TECHO de confianza para una nota de riesgo (nunca se descarta:
    es prosa). Sin evidencia -> 'low'; evidencia que no resuelve -> 'medium'.
    """
    evidence = risk.get("evidence") or []
    if not evidence:
        return "low"
    for ev in evidence:
        key = str(ev).split(":", 1)[0].strip()
        if key and mm._path_get(profile, key) is None:
            return "medium"
    return "high"
