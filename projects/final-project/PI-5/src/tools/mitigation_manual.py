"""
Motor del manual de mitigación parametrizado por el perfil del device.

Sustituye la lógica "leer recommendations.json del honeypot y, si no hay match,
devolver TODO el manual". Ahora:
  * Manual GENÉRICO (recommendations/generic.json): entradas parametrizables solo
    con lo derivable de un System Profile (bloquear IP por firewall activo,
    reiniciar el servicio web descubierto, diagnósticos de lectura).
  * OVERRIDES por device (recommendations/<device>.json): mitigaciones específicas
    del sitio (backups, scripts propios). El honeypot es recommendations/Pi4-Felix.json.

consultar() filtra por requires (capabilities) y applies_if (perfil), elige la
plantilla del firewall ACTIVO, sustituye placeholders desde el perfil, fusiona los
overrides y, ante 0 coincidencias o perfil ausente, devuelve acciones genéricas
seguras — NUNCA el manual del honeypot.

Ver docs/diseno_agente_discovery.md §11 (Fase 2).
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import List, Optional, Tuple

from tools.db_tools import get_device_profile

logger = logging.getLogger("CoordinatorSOC")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RECS_DIR = os.path.join(BASE_DIR, 'src', 'recommendations')
GENERIC_PATH = os.path.join(RECS_DIR, 'generic.json')

# device sano para evitar path traversal al abrir <device>.json
_SAFE_DEVICE = re.compile(r'^[A-Za-z0-9_-]+$')

FW_PREFERENCE = ["ufw", "firewalld", "nftables", "iptables"]

# Familia inferida de la keyword del query.
_FAMILY_KEYWORDS = [
    (("ssh", "brute", "bruteforce", "fuerza bruta"), "ssh_bruteforce"),
    (("ftp", "vsftpd", "proftpd"), "ftp_bruteforce"),
    (("sqli", "sql", "injection", "inyeccion"), "sqli"),
    (("xss", "script", "cross-site"), "xss"),
    (("web", "login", "bruteforce_web"), "web_bruteforce"),
    (("session", "hijack", "sesion"), "session_hijacking"),
    (("deface", "defacement"), "defacement"),
    (("db", "database", "bbdd", "credential"), "db_compromise"),
    (("scan", "nmap", "sondeo", "port"), "port_scan"),
    (("recon",), "recon"),
]

# placeholder -> (ruta_anidada, index|None, default). {ip}/{nombre_usuario} NO van aquí (literales).
_PLACEHOLDER_PATHS = {
    "web_docroot": ("web_server.docroots", 0),
    "web_config": ("web_server.config_paths", 0),
    "proxy_to": ("web_server.reverse_proxy_to", 0),
    "db_engine": ("db_engine.engine", None),
}

_LITERAL_PLACEHOLDERS = {"ip", "nombre_usuario"}

_IP_RE = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
_PATH_ALLOWLIST = {
    "web_docroot": ("/var/www", "/srv", "/home", "/usr/share"),
    "web_log": ("/var/log", "/var/www", "/etc"),
    "web_config": ("/var/log", "/var/www", "/etc"),
}
_WEB_UNITS = {"nginx", "apache2", "httpd"}

# --- caches ----------------------------------------------------------------
_generic_cache: Optional[list] = None
_override_cache: dict = {}


def _load_generic() -> list:
    global _generic_cache
    if _generic_cache is not None:
        return _generic_cache
    try:
        with open(GENERIC_PATH, "r", encoding="utf-8") as f:
            _generic_cache = json.load(f).get("entries", [])
    except Exception as e:  # noqa: BLE001
        logger.error(f"[MANUAL] No se pudo cargar generic.json: {e}")
        _generic_cache = []
    return _generic_cache


def _load_override(device: str) -> list:
    if device in _override_cache:
        return _override_cache[device]
    entries: list = []
    if device and _SAFE_DEVICE.match(device):
        path = os.path.join(RECS_DIR, f"{device}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    entries = json.load(f).get("entries", [])
            except Exception as e:  # noqa: BLE001
                logger.error(f"[MANUAL] No se pudo cargar override {device}: {e}")
    _override_cache[device] = entries
    return entries


def clear_cache() -> None:
    """Para tests: olvida los ficheros cacheados."""
    global _generic_cache
    _generic_cache = None
    _override_cache.clear()


# --- navegación del perfil -------------------------------------------------
def _path_get(profile: dict, dotted: str, index: Optional[int] = None):
    cur = profile
    for part in dotted.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
        if cur is None:
            return None
    if index is not None and isinstance(cur, list):
        return cur[index] if len(cur) > index else None
    return cur


def family_for(query: str) -> str:
    q = (query or "").lower()
    for keys, fam in _FAMILY_KEYWORDS:
        if any(k in q for k in keys):
            return fam
    return q


# --- filtros ---------------------------------------------------------------
def _caps(profile: dict) -> set:
    return {k for k, v in (profile.get("capabilities") or {}).items() if v}


def matches_generic(entry: dict, query: str, family: str) -> bool:
    fam = entry.get("family")
    if fam == family or fam == "_universal":
        return True
    q = (query or "").lower().strip()
    if not q:
        return False
    haystack = " ".join([
        fam or "", " ".join(entry.get("keywords", [])), entry.get("explanation", ""),
    ]).lower()
    return q in haystack


def matches_override(entry: dict, query: str, family: str) -> bool:
    m = entry.get("match", {})
    if family in (m.get("families") or []):
        return True
    q = (query or "").lower().strip()
    if not q:
        return False
    haystack = " ".join(m.get("keywords", []) + (m.get("families") or [])).lower()
    return q in haystack


def passes_requires(entry: dict, caps: set, profile: dict) -> bool:
    req = entry.get("requires") or []
    if not req:
        return True
    if not profile:
        return False  # conservador: no proponer herramientas no verificadas
    return all(r in caps for r in req)


def passes_applies_if(entry: dict, profile: dict) -> bool:
    cond = entry.get("applies_if") or {}
    if not cond:
        return True
    if not profile:
        return False
    for clave, want in cond.items():
        if not _condition_ok(clave, want, profile):
            return False
    return True


def _condition_ok(clave: str, want, profile: dict) -> bool:
    # Operadores de override.
    if clave.endswith("_contains_all"):
        got = _path_get(profile, clave[:-len("_contains_all")])
        return isinstance(got, list) and all(x in got for x in (want or []))
    if clave.endswith("_contains"):
        got = _path_get(profile, clave[:-len("_contains")])
        return isinstance(got, list) and want in got
    if clave.startswith("capabilities."):
        cap = clave.split(".", 1)[1]
        return (cap in _caps(profile)) if want else True
    got = _path_get(profile, clave)
    if want == "*":
        return got not in (None, "", [], {})
    if isinstance(got, list):
        return want in got
    return got == want


# --- selección de comando y placeholders -----------------------------------
def pick_command(entry: dict, fw: str, notes: list, key: str = "command_templates") -> Optional[str]:
    t = entry.get(key) or {}
    if not t:
        return None
    if "default" in t:
        return t["default"]
    if fw in t:
        return t[fw]
    for cand in FW_PREFERENCE:
        if cand in t:
            notes.append(f"{entry.get('id')}: firewall '{fw}' sin plantilla, usando '{cand}' (verificar antes de aprobar)")
            return t[cand]
    return None


def _resolve_placeholder(ph: str, profile: dict):
    if ph in _PLACEHOLDER_PATHS:
        dotted, idx = _PLACEHOLDER_PATHS[ph]
        return _path_get(profile, dotted, idx)
    if ph == "web_port":
        val = _path_get(profile, "web_server.listen_ports", 0)
        if val:
            return val
        for p in (profile.get("surface") or {}).get("exposed_ports", []):
            if p in (80, 443, 8080):
                return p
        return None
    if ph == "ssh_port":
        for svc in profile.get("services") or []:
            if (svc.get("proc") or "").lower() == "sshd" and svc.get("port"):
                return svc["port"]
        return 22
    if ph == "ftp_port":
        for svc in profile.get("services") or []:
            if (svc.get("proc") or "").lower() in ("vsftpd", "proftpd", "pure-ftpd") and svc.get("port"):
                return svc["port"]
        return 21
    if ph == "web_log":
        for src in profile.get("log_sources") or []:
            parser = src.get("parser", "")
            dets = set(src.get("detectors") or [])
            if src.get("id") == "web_access" or parser.endswith("_access") or dets & {"sqli", "xss", "web_bruteforce"}:
                return src.get("path")  # None si journald
        return None
    if ph == "web_unit":
        web = profile.get("web_server") or {}
        engine = web.get("engine")
        if engine == "nginx":
            return "nginx"
        if engine == "apache":
            os_id = (profile.get("host") or {}).get("os_id", "")
            return "apache2" if os_id in ("debian", "ubuntu", "raspbian") else "httpd"
        return None
    return None


def _validate_placeholder(ph: str, val) -> bool:
    if ph in ("web_port", "ssh_port", "ftp_port"):
        try:
            return 1 <= int(val) <= 65535
        except (TypeError, ValueError):
            return False
    if ph in _PATH_ALLOWLIST:
        return isinstance(val, str) and val.startswith(_PATH_ALLOWLIST[ph])
    if ph == "web_unit":
        return val in _WEB_UNITS
    return True


def resolve_and_validate(text: str, declared: List[str], profile: dict) -> Tuple[str, List[str]]:
    """Sustituye placeholders resolubles; deja {ip}/{nombre_usuario} literales.
    Devuelve (texto, lista de placeholders que faltan o no validan)."""
    missing: List[str] = []
    for ph in declared:
        if ph in _LITERAL_PLACEHOLDERS:
            continue
        val = _resolve_placeholder(ph, profile)
        if val in (None, "", []):
            missing.append(ph)
            continue
        if not _validate_placeholder(ph, val):
            missing.append(ph)
            continue
        text = text.replace("{" + ph + "}", str(val))
    # residual: cualquier {x} que no sea literal y no se haya resuelto
    residual = [m for m in re.findall(r"\{([a-zA-Z_]+)\}", text) if m not in _LITERAL_PLACEHOLDERS]
    missing.extend(m for m in residual if m not in missing)
    return text, missing


def _detect_placeholders(text: str) -> List[str]:
    return sorted(set(re.findall(r"\{([a-zA-Z_]+)\}", text)))


# --- 0 matches / perfil ausente: acciones genéricas seguras (NUNCA honeypot) ---
_BLOCK_TEMPLATES = {
    "iptables": "sudo iptables -I INPUT 1 -s {ip} -j DROP",
    "ufw": "sudo ufw insert 1 deny from {ip}",
    "nftables": "sudo nft add rule inet filter input ip saddr {ip} drop",
    "firewalld": "sudo firewall-cmd --add-rich-rule=\"rule family='ipv4' source address='{ip}' drop\"",
}


def _minimal(fw: str, query: str, notes: list) -> list:
    block = _BLOCK_TEMPLATES.get(fw)
    note = ""
    if not block:
        block = _BLOCK_TEMPLATES["iptables"]
        note = " [PERFIL/FW NO DESCUBIERTO: verifica el firewall antes de aplicar]"
    return [
        {"id": "minimal_block_ip", "intent": "mitigation",
         "command": block, "revert": "", "source": "minimal",
         "explanation": f"Bloqueo genérico de la IP atacante a nivel de firewall.{note}"},
        {"id": "minimal_inspect_logs", "intent": "diagnostic",
         "command": "sudo journalctl -n 200 --no-pager", "revert": "", "source": "minimal",
         "explanation": "Inspección de los últimos eventos del sistema."},
        {"id": "minimal_listening_ports", "intent": "diagnostic",
         "command": "sudo ss -tulpnH", "revert": "", "source": "minimal",
         "explanation": "Puertos a la escucha y su proceso."},
    ]


# --- formato para el LLM ---------------------------------------------------
def _format(results: list, notes: list, device: str, has_profile: bool) -> str:
    header = f"Recomendaciones para el dispositivo '{device}'"
    header += " (filtradas y parametrizadas a su sistema real):" if has_profile else \
        " (PERFIL NO DESCUBIERTO: acciones genéricas; verifica firewall/rutas antes de aprobar):"
    lines = [header, ""]
    for r in results:
        block = [f"- [{r.get('source', 'generic')}] {r.get('id')} ({r.get('intent', '')})",
                 f"  Comando: {r.get('command')}"]
        if r.get("revert"):
            block.append(f"  Revertir: {r['revert']}")
        if r.get("explanation"):
            block.append(f"  Explicación: {r['explanation']}")
        lines.append("\n".join(block))
    if notes:
        lines.append("")
        lines.append("Notas: " + "; ".join(notes))
    return "\n\n".join(lines)


# --- entrada principal -----------------------------------------------------
def consultar(query: str, device: str = "", fallback_device: str = "") -> str:
    try:
        eff = (device or "").strip() or (fallback_device or "").strip()
        profile = get_device_profile(eff) if eff else {}
        # El LLM pasó device pero no tiene perfil y el del módulo sí -> preferir módulo.
        if (device or "").strip() and not profile and fallback_device:
            eff = fallback_device.strip()
            profile = get_device_profile(eff)

        caps = _caps(profile)
        fw = (profile.get("firewall") or {}).get("active_manager", "none")
        family = family_for(query)
        notes: List[str] = []

        # (1) Genéricos
        generic_results = []
        for e in _load_generic():
            if not matches_generic(e, query, family):
                continue
            if not passes_requires(e, caps, profile):
                continue
            if not passes_applies_if(e, profile):
                continue
            cmd = pick_command(e, fw, notes, "command_templates")
            if cmd is None:
                continue
            cmd, missing = resolve_and_validate(cmd, e.get("placeholders", []), profile)
            if missing:
                notes.append(f"omitida {e.get('id')}: falta/invalido {', '.join(missing)}")
                continue
            rev = pick_command(e, fw, [], "revert_templates")
            if rev:
                rev, rmiss = resolve_and_validate(rev, e.get("placeholders", []), profile)
                if rmiss:
                    rev = ""
            generic_results.append({
                "id": e.get("id"), "family": e.get("family"), "intent": e.get("intent"),
                "command": cmd, "revert": rev or "", "explanation": e.get("explanation", ""),
                "source": "generic",
            })

        # (2) Overrides (solo con perfil de confianza)
        override_results = []
        if profile:
            for e in _load_override(eff):
                if not matches_override(e, query, family):
                    continue
                if not passes_requires(e, caps, profile):
                    continue
                cond = e.get("applies_if") or {}
                if cond and not all(_condition_ok(k, v, profile) for k, v in cond.items()):
                    continue
                cmd, miss = resolve_and_validate(e.get("command", ""), _detect_placeholders(e.get("command", "")), profile)
                hard_miss = [m for m in miss if m not in _LITERAL_PLACEHOLDERS]
                if hard_miss:
                    notes.append(f"override {e.get('id')} omitido: {', '.join(hard_miss)}")
                    continue
                override_results.append({
                    "id": e.get("id"), "intent": e.get("intent"),
                    "command": cmd, "revert": e.get("revert", ""),
                    "explanation": e.get("explanation", ""), "source": "override",
                })

        # (3) Merge: overrides primero, luego genéricos
        merged = override_results + generic_results

        # (4) 0 matches -> mínimo genérico, NUNCA honeypot
        if not merged:
            merged = _minimal(fw, query, notes)
            notes.append(f"no hay recomendación específica catalogada para '{query}'; estas son acciones genéricas seguras")

        return _format(merged, notes, eff or "desconocido", bool(profile))
    except Exception as ex:  # noqa: BLE001 — nunca devolver el honeypot por error
        logger.error(f"[MANUAL] Error en consultar: {ex}")
        return f"Error consultando el manual de mitigación: {ex}"
