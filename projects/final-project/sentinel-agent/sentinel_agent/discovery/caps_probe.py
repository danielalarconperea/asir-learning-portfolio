"""
Probe de capacidades: qué herramientas de mitigación/recuperación existen en
el host (`command -v`). Evita que el LLM proponga p. ej. restic donde no hay
restic. La lista es la base para filtrar las recomendaciones por device.
"""

from __future__ import annotations

from typing import Tuple

from . import _util

# Herramientas relevantes para mitigación, diagnóstico y recuperación.
_TOOLS = (
    "restic", "fail2ban-client", "docker", "podman", "mysql", "psql",
    "php", "systemctl", "journalctl", "ss", "iptables", "nft", "ufw",
    "firewall-cmd", "tcpdump", "rsync", "borg", "crontab",
)

# Alias legible -> binario.
_ALIASES = {"fail2ban-client": "fail2ban", "firewall-cmd": "firewalld", "nft": "nftables"}


def detect_tools(which=_util.which) -> dict:
    """Lógica testable: {nombre_legible: bool} según presencia en PATH."""
    caps = {}
    for binary in _TOOLS:
        name = _ALIASES.get(binary, binary)
        caps[name] = bool(which(binary))
    return caps


def collect() -> Tuple[dict, list]:
    return {"capabilities": detect_tools()}, []
