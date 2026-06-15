"""
Probe de fuentes de log: dónde está cada log y con qué formato/parser.

Para servicios systemd se prefiere journald (estructurado). Para servidores
web/FTP se derivan rutas de fichero (de la config del servicio cuando se puede,
con defaults por familia si no). Cada fuente lleva el `parser` a usar y los
`detectors` aplicables; las rutas no van cableadas en el código.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from . import _util

# Defaults por familia de servidor web (si no se puede leer la config).
_WEB_DEFAULTS = {
    "nginx": {"path": "/var/log/nginx/access.log", "parser": "nginx_access"},
    "apache": {"path": "/var/log/apache2/access.log", "parser": "apache_access"},
}


def build_log_sources(stack: dict) -> List[dict]:
    """
    Lógica pura: a partir del stack descubierto construye la lista de fuentes
    de log con parser y detectores asociados.
    """
    sources: List[dict] = []

    if stack.get("ssh"):
        sources.append({
            "id": "ssh", "service": "ssh", "source": "journald",
            "unit": "ssh.service", "path": None, "format": "journald-json",
            "parser": "sshd_auth", "detectors": ["ssh_bruteforce"],
        })

    web = stack.get("web_server")
    if web:
        engine = web.get("engine")
        default = _WEB_DEFAULTS.get(engine, {"path": None, "parser": "web_access"})
        sources.append({
            "id": "web_access", "service": engine, "source": "file", "unit": None,
            "path": web.get("access_log") or default["path"],
            "format": "combined", "parser": default["parser"],
            "detectors": ["web_bruteforce", "sqli", "xss"],
        })

    ftp = stack.get("ftp")
    if ftp:
        sources.append({
            "id": "ftp", "service": ftp.get("engine"), "source": "file", "unit": None,
            "path": "/var/log/vsftpd.log", "format": "vsftpd",
            "parser": "vsftpd", "detectors": ["ftp_bruteforce"],
        })

    return sources


def parse_nginx_access_log(conf_text: Optional[str]) -> Optional[str]:
    """Extrae la primera directiva `access_log <ruta>` de una config nginx."""
    if not conf_text:
        return None
    m = re.search(r"^\s*access_log\s+(\S+)", conf_text, re.MULTILINE)
    if not m:
        return None
    path = m.group(1).rstrip(";")
    return path if path and path != "off" else None


def collect(stack: dict) -> Tuple[dict, list]:
    degraded = []
    # Enriquecer la ruta del access_log de nginx desde su config si es posible.
    web = stack.get("web_server")
    if web and web.get("engine") == "nginx":
        for cfg in web.get("config_paths", []):
            path = parse_nginx_access_log(_util.read_text(cfg))
            if path:
                web["access_log"] = path
                break
    sources = build_log_sources(stack)
    if not sources:
        degraded.append("no_log_sources")
    return {"log_sources": sources}, degraded
