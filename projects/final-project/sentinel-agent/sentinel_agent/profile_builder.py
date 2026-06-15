"""
Ensamblado del System Profile y cálculo de profile_hash / profile_version.

El profile_hash se calcula SOLO sobre las secciones materiales (estructura del
sistema), excluyendo campos volátiles (discovered_at, profile_version, trigger,
PIDs). Así el sensor republica el perfil únicamente cuando algo cambia de
verdad y PI-5 puede deduplicar el upsert.

Ver docs/diseno_agente_discovery.md §7.
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
from typing import Optional, Tuple

from . import AGENT_NAME
from .discovery import (
    caps_probe,
    firewall_probe,
    log_probe,
    os_probe,
    services_probe,
    surface_probe,
    users_probe,
)

logger = logging.getLogger("sentinel-agent")

SCHEMA_VERSION = 1

# Secciones que cuentan para el profile_hash (estructura material del sistema).
_MATERIAL_KEYS = (
    "host", "package_manager", "firewall", "web_server", "db_engine",
    "services", "log_sources", "capabilities",
)


def _canonical_material(profile: dict) -> bytes:
    """
    Serialización determinista de las secciones materiales, con los PIDs (y el
    is_root, que puede variar) eliminados para que reinicios o cambios de
    privilegio no alteren el hash.
    """
    material = {k: copy.deepcopy(profile.get(k)) for k in _MATERIAL_KEYS}
    svcs = material.get("services")
    if isinstance(svcs, list):
        for svc in svcs:
            if isinstance(svc, dict):
                svc.pop("pid", None)  # PID es volatil (cambia en cada reinicio del servicio)
                svc.pop("exe", None)  # exe es volatil: "(deleted)" tras apt upgrade, rutas versionadas
        # `ss` no garantiza orden estable: ordenar para que reordenar la lista
        # no cambie el hash (evita republicaciones y reinicios espurios).
        svcs.sort(key=lambda s: (
            str((s or {}).get("proto", "")), str((s or {}).get("port", "")),
            str((s or {}).get("bind", "")), str((s or {}).get("proc", "")),
        ))
        material["services"] = svcs
    host = material.get("host")
    if isinstance(host, dict):
        host.pop("is_root", None)
    return json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_profile_hash(profile: dict) -> str:
    """Devuelve 'sha256:<hex>' sobre las secciones materiales del perfil."""
    digest = hashlib.sha256(_canonical_material(profile)).hexdigest()
    return f"sha256:{digest}"


def next_profile_version(prev_hash: Optional[str], prev_version: int, new_hash: str) -> Tuple[int, bool]:
    """
    (version, changed): si el hash no cambió, conserva la versión; si cambió
    (o es el primer perfil), incrementa.
    """
    if prev_hash == new_hash and prev_version > 0:
        return prev_version, False
    return prev_version + 1, True


def assemble_core(device_id: str, sections: dict, discovered_at: str, trigger: str) -> dict:
    """
    Pure: monta el perfil (sin profile_hash/profile_version definitivos) a
    partir de las secciones ya recolectadas. `sections` es el dict agregado de
    los probes (host, package_manager, services, firewall, stack, log_sources,
    capabilities, users, surface, degraded).
    """
    stack = sections.get("stack") or {}
    return {
        "tipo": "PERFIL_SISTEMA",
        "schema_version": SCHEMA_VERSION,
        "sensor": device_id,
        "dispositivo": device_id,
        "profile_version": 0,
        "profile_hash": "",
        "agent_version": AGENT_NAME,
        "discovered_at": discovered_at,
        "trigger": trigger,
        "host": sections.get("host", {}),
        "package_manager": sections.get("package_manager", "unknown"),
        "firewall": sections.get("firewall", {}),
        "web_server": stack.get("web_server"),
        "db_engine": stack.get("db_engine"),
        "services": sections.get("services", []),
        "log_sources": sections.get("log_sources", []),
        "capabilities": sections.get("capabilities", {}),
        "users": sections.get("users", {}),
        "surface": sections.get("surface", {}),
        "degraded": sections.get("degraded", []),
    }


def finalize(profile: dict, prev_hash: Optional[str], prev_version: int) -> Tuple[dict, bool]:
    """Calcula y fija profile_hash + profile_version. Devuelve (profile, changed)."""
    new_hash = compute_profile_hash(profile)
    version, changed = next_profile_version(prev_hash, prev_version, new_hash)
    profile["profile_hash"] = new_hash
    profile["profile_version"] = version
    return profile, changed


def discover_sections() -> dict:
    """
    Ejecuta todos los probes y agrega sus secciones. Cada probe va en su propio
    try/except: un fallo degrada SU sección sin tumbar el snapshot.
    """
    sections = {"degraded": []}

    def _run(name, fn, *args):
        try:
            section, degraded = fn(*args)
            sections.update(section)
            sections["degraded"].extend(degraded)
        except Exception as e:  # noqa: BLE001 — degradar, nunca romper el snapshot
            logger.warning(f"[DISCOVERY] probe {name} falló: {e}")
            sections["degraded"].append(f"{name}_error")

    _run("os", os_probe.collect)
    _run("services", services_probe.collect)
    # stack/log/surface dependen de los servicios descubiertos.
    services = sections.get("services", [])
    _run("stack", stack_collect_wrapper, services)
    stack = sections.get("stack", {})
    _run("log", log_probe.collect, stack)
    _run("firewall", firewall_probe.collect)
    _run("caps", caps_probe.collect)
    _run("users", users_probe.collect)
    _run("surface", surface_probe.collect, services)
    return sections


def stack_collect_wrapper(services):
    from .discovery import stack_probe
    return stack_probe.collect(services)
