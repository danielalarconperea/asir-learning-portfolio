"""
Probe de stack: identifica servidor web, motor de BD, FTP, SSH y DNS a partir
de los procesos a la escucha (no del puerto: el 80 puede ser un proxy).
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from . import _util

# proc del listener -> familia de servicio.
_WEB_PROCS = {"nginx": "nginx", "apache2": "apache", "httpd": "apache", "caddy": "caddy"}
_DB_PROCS = {"mysqld": "mysql", "mariadbd": "mysql", "postgres": "postgres",
             "postmaster": "postgres", "mongod": "mongodb"}
_FTP_PROCS = {"vsftpd": "vsftpd", "proftpd": "proftpd", "pure-ftpd": "pureftpd"}
_DNS_PROCS = {"named": "bind", "dnsmasq": "dnsmasq", "unbound": "unbound"}


def classify_services(services: List[dict]) -> dict:
    """
    Lógica pura: a partir de la lista de listeners (con `proc` y `port`) decide
    qué motores corren y en qué puertos. Devuelve un dict por familia.
    """
    out = {"web_server": None, "db_engine": None, "ftp": None, "ssh": None, "dns": None}
    for svc in services:
        proc = (svc.get("proc") or "").lower()
        port = svc.get("port")
        if proc in _WEB_PROCS and out["web_server"] is None:
            out["web_server"] = {"engine": _WEB_PROCS[proc], "listen_ports": [port]}
        elif proc in _WEB_PROCS:
            out["web_server"]["listen_ports"].append(port)
        if proc in _DB_PROCS and out["db_engine"] is None:
            out["db_engine"] = {"engine": _DB_PROCS[proc],
                                "listen": [{"port": port, "bind": svc.get("bind")}]}
        elif proc in _DB_PROCS:
            out["db_engine"]["listen"].append({"port": port, "bind": svc.get("bind")})
        if proc in _FTP_PROCS and out["ftp"] is None:
            out["ftp"] = {"engine": _FTP_PROCS[proc]}
        if proc == "sshd" and out["ssh"] is None:
            out["ssh"] = {"engine": "openssh", "port": port}
        if proc in _DNS_PROCS and out["dns"] is None:
            out["dns"] = {"engine": _DNS_PROCS[proc]}
    return out


def parse_nginx_version(text: Optional[str]) -> str:
    if not text:
        return "unknown"
    m = re.search(r"nginx/(\S+)", text)
    return m.group(1) if m else "unknown"


def parse_nginx_conf_path(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    m = re.search(r"--conf-path=(\S+)", text)
    return m.group(1) if m else None


def parse_apache_version(text: Optional[str]) -> str:
    if not text:
        return "unknown"
    m = re.search(r"Apache/(\S+)", text)
    return m.group(1) if m else "unknown"


def parse_apache_conf_path(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    m = re.search(r'SERVER_CONFIG_FILE="([^"]+)"', text)
    return m.group(1) if m else None


def collect(services: List[dict]) -> Tuple[dict, list]:
    """Clasifica el stack y enriquece el servidor web con versión y config_path."""
    degraded = []
    stack = classify_services(services)

    web = stack.get("web_server")
    if web:
        engine = web["engine"]
        if engine == "nginx":
            v = _util.run(["nginx", "-V"], merge_stderr=True)
            web["version"] = parse_nginx_version(v)
            cp = parse_nginx_conf_path(v)
            web["config_paths"] = [cp] if cp else []
        elif engine == "apache":
            v = _util.run(["apache2ctl", "-V"], merge_stderr=True) or \
                _util.run(["httpd", "-V"], merge_stderr=True)
            web["version"] = parse_apache_version(v)
            cp = parse_apache_conf_path(v)
            web["config_paths"] = [cp] if cp else []
        else:
            web.setdefault("version", "unknown")
            web.setdefault("config_paths", [])
        web.setdefault("docroots", [])
        web.setdefault("reverse_proxy_to", [])

    db = stack.get("db_engine")
    if db and db["engine"] == "mysql":
        v = _util.run(["mysqld", "--version"]) or _util.run(["mariadbd", "--version"])
        m = re.search(r"\b(\d+\.\d+\.\d+)", v) if v else None
        db["version"] = m.group(1) if m else "unknown"
    elif db and db["engine"] == "postgres":
        v = _util.run(["postgres", "--version"])
        m = re.search(r"\b(\d+(?:\.\d+)?)", v) if v else None
        db["version"] = m.group(1) if m else "unknown"

    return {"stack": stack}, degraded
