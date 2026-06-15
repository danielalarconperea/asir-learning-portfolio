"""
Probe de usuarios: administradores (grupo sudo/wheel) vía getent (soporta
NSS/LDAP). Solo informativo para el contexto del LLM.
"""

from __future__ import annotations

from typing import Optional, Tuple

from . import _util


def parse_getent_group(text: Optional[str], group: str) -> list:
    """
    Parsea una línea de `getent group <grupo>` (nombre:x:gid:miembros) y
    devuelve la lista de miembros. '' si el grupo no existe.
    """
    if not text:
        return []
    for line in text.splitlines():
        fields = line.split(":")
        if len(fields) >= 4 and fields[0] == group:
            members = fields[3].strip()
            return [m for m in members.split(",") if m]
    return []


def collect() -> Tuple[dict, list]:
    degraded = []
    sudoers = parse_getent_group(_util.run(["getent", "group", "sudo"]), "sudo")
    sudo_group = "sudo"
    if not sudoers:
        wheel = parse_getent_group(_util.run(["getent", "group", "wheel"]), "wheel")
        if wheel:
            sudoers, sudo_group = wheel, "wheel"
    if not sudoers:
        degraded.append("no_admin_group")
    return {"users": {"sudoers": sudoers, "sudo_group": sudo_group, "recent_logins": []}}, degraded
