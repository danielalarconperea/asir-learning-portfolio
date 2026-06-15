"""
Parsers por tipo de servicio: convierten una línea de log en una "observación"
normalizada (dict con al menos {kind, ip}) que consumen los detectores.

Cada parser es una función pura `parse(line) -> dict | None`. Se seleccionan
por el campo `parser` de cada log_source del System Profile, en vez de las
regexes fijas a vsftpd/apache/sshd del monolito.
"""

from __future__ import annotations

import re
from typing import Optional

# sshd: "Failed password for [invalid user ]<user> from <ip> port ..."
_SSH_FAIL = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})")
_SSH_OK = re.compile(r"Accepted \w+ for (?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})")

# vsftpd: '... [user] FAIL LOGIN: Client "::ffff:1.2.3.4"' o sin ::ffff:
_FTP_FAIL = re.compile(r"\[(?P<user>[^\]]+)\] FAIL LOGIN: Client \"(?:::ffff:)?(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\"")

# Combined/Common Log Format: '<ip> - - [date] "METHOD /path HTTP/x" status size ...'
_WEB = re.compile(r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+\S+\s+\S+\s+\[[^\]]+\]\s+"(?P<method>\S+)\s+(?P<path>\S+)[^"]*"\s+(?P<status>\d{3})')


def sshd_auth(line: str) -> Optional[dict]:
    m = _SSH_FAIL.search(line)
    if m:
        return {"kind": "ssh_auth_fail", "ip": m.group("ip"), "user": m.group("user")}
    m = _SSH_OK.search(line)
    if m:
        return {"kind": "ssh_login_ok", "ip": m.group("ip"), "user": m.group("user")}
    return None


def vsftpd(line: str) -> Optional[dict]:
    m = _FTP_FAIL.search(line)
    if m:
        return {"kind": "ftp_auth_fail", "ip": m.group("ip"), "user": m.group("user")}
    return None


def nginx_access(line: str) -> Optional[dict]:
    m = _WEB.search(line)
    if not m:
        return None
    return {
        "kind": "web_request",
        "ip": m.group("ip"),
        "method": m.group("method"),
        "path": m.group("path"),
        "status": int(m.group("status")),
    }


# apache usa el mismo combined log format.
apache_access = nginx_access


# Registro nombre->función para selección por log_source.parser.
PARSERS = {
    "sshd_auth": sshd_auth,
    "vsftpd": vsftpd,
    "nginx_access": nginx_access,
    "apache_access": apache_access,
    "web_access": nginx_access,
}


def get_parser(name: str):
    """Devuelve la función de parseo por nombre, o None si no existe."""
    return PARSERS.get(name)
