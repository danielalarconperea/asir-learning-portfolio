"""
Contexto del sistema objetivo para el LLM de triage.

Lee el System Profile persistido por el agente Discovery (tabla device_profiles)
y lo renderiza como un bloque compacto que se antepone al log de cada evento,
para que el triage razone sobre el OS/firewall/web reales en vez de asumir el
honeypot. Cachea por device, invalidando cuando cambia profile_version.

Ver docs/diseno_agente_discovery.md §9.
"""

from __future__ import annotations

import logging
import threading
from typing import Optional

from tools.db_tools import get_device_profile

logger = logging.getLogger("CoordinatorSOC")

_lock = threading.Lock()
# device -> (profile_version, rendered_block)
_cache: dict = {}


def get_profile(device: str) -> dict:
    """Perfil completo del device (dict) o {} si no hay."""
    return get_device_profile(device)


def get_context_block(device: str) -> str:
    """
    Devuelve el bloque de contexto renderizado para el device, usando caché
    invalidada por profile_version. "" si el device no tiene perfil.
    """
    profile = get_device_profile(device)
    if not profile:
        return ""
    version = profile.get("profile_version", 0)
    with _lock:
        cached = _cache.get(device)
        if cached and cached[0] == version:
            return cached[1]
        block = render_profile_block(profile)
        _cache[device] = (version, block)
        return block


def invalidate(device: str) -> None:
    with _lock:
        _cache.pop(device, None)


def render_profile_block(profile: dict) -> str:
    """
    Pure: convierte un System Profile en un bloque de texto compacto para el
    prompt. Resiliente a campos ausentes (perfil degradado).
    """
    if not profile:
        return ""
    host = profile.get("host") or {}
    fw = profile.get("firewall") or {}
    web = profile.get("web_server") or {}
    dbe = profile.get("db_engine") or {}
    caps = profile.get("capabilities") or {}
    surface = profile.get("surface") or {}

    lines = [f"### CONTEXTO DEL SISTEMA OBJETIVO (device={profile.get('sensor', '?')})"]

    os_line = f"OS: {host.get('pretty_name') or host.get('os_id', 'desconocido')}"
    if host.get("arch"):
        os_line += f" ({host['arch']})"
    lines.append(os_line)

    if profile.get("package_manager") and profile["package_manager"] != "unknown":
        lines.append(f"Gestor de paquetes: {profile['package_manager']}")

    if fw.get("active_manager") and fw["active_manager"] != "none":
        backend = f", backend {fw['backend']}" if fw.get("backend") and fw["backend"] != fw["active_manager"] else ""
        lines.append(
            f"Firewall ACTIVO: {fw['active_manager']}{backend} — usa la herramienta de ESE gestor "
            f"(p. ej. ufw/firewall-cmd/nft), no reglas iptables-legacy crudas si el backend es nft"
        )

    if web.get("engine"):
        cfg = ", ".join(web.get("config_paths") or []) or "?"
        proxy = f", proxy a {web['reverse_proxy_to']}" if web.get("reverse_proxy_to") else ""
        lines.append(f"Web: {web['engine']} {web.get('version', '')} (config: {cfg}{proxy})".strip())

    if dbe.get("engine"):
        lines.append(f"BD: {dbe['engine']} {dbe.get('version', '')}".strip())

    present = sorted(k for k, v in caps.items() if v)
    absent = sorted(k for k, v in caps.items() if not v)
    if present or absent:
        lines.append(
            f"Herramientas disponibles: {', '.join(present) or 'ninguna'}"
            + (f" | NO disponibles: {', '.join(absent)}" if absent else "")
        )

    if surface.get("exposed_ports"):
        lines.append(f"Puertos expuestos: {', '.join(str(p) for p in surface['exposed_ports'])}")

    if profile.get("degraded"):
        lines.append(f"(Descubrimiento parcial: {', '.join(profile['degraded'])})")

    return "\n".join(lines)
