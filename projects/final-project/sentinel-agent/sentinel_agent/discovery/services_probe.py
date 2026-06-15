"""
Probe de servicios y puertos a la escucha (mapeo puerto→proceso).

Fuente principal: `ss -H -tlnp` / `ss -H -ulnp` (reemplaza netstat). El flag
-p (proceso) requiere privilegios; sin root se degrada a puerto sin proceso.
Fallback: /proc/net/tcp si no hay `ss`.
"""

from __future__ import annotations

import os
import re
from typing import List, Optional, Tuple

from . import _util

_PROC_RE = re.compile(r'\(\("(?P<name>[^"]+)",pid=(?P<pid>\d+)')

# Binds que implican exposición fuera de la máquina.
_WILDCARD_BINDS = ("0.0.0.0", "::", "*")
_LOOPBACK_BINDS = ("127.0.0.1", "::1")


def _split_addr_port(addr: str) -> Tuple[str, Optional[int]]:
    """'0.0.0.0:22' -> ('0.0.0.0', 22); '[::]:22' -> ('::', 22); '*:53' -> ('*', 53)."""
    if ":" not in addr:
        return addr, None
    host, _, port = addr.rpartition(":")
    host = host.strip("[]")
    if host == "":
        host = "*"
    try:
        return host, int(port)
    except ValueError:
        return host, None


def parse_ss(text: Optional[str], proto: str) -> List[dict]:
    """
    Parsea la salida de `ss -H -[tu]lnp` en una lista de listeners:
    {proto, port, bind, exposed, proc, pid}. `proc`/`pid` None si no hubo
    privilegios para mapear el proceso.
    """
    listeners: List[dict] = []
    if not text:
        return listeners
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        # Formato: State Recv-Q Send-Q Local:Port Peer:Port [users:(...)]
        local = parts[3]
        bind, port = _split_addr_port(local)
        if port is None:
            continue
        proc = pid = None
        m = _PROC_RE.search(line)
        if m:
            proc = m.group("name")
            pid = int(m.group("pid"))
        listeners.append({
            "proto": proto,
            "port": port,
            "bind": bind,
            "exposed": bind in _WILDCARD_BINDS,
            "loopback": bind in _LOOPBACK_BINDS,
            "proc": proc,
            "pid": pid,
        })
    return listeners


def _exe_for_pid(pid: Optional[int]) -> Optional[str]:
    if not pid:
        return None
    try:
        return os.readlink(f"/proc/{pid}/exe")
    except OSError:
        return None


def collect() -> Tuple[dict, list]:
    """
    Devuelve {services: [...]} con los listeners descubiertos, enriquecidos con
    la ruta del binario. Degrada si falta `ss` o no hay privilegios.
    """
    degraded = []
    listeners: List[dict] = []

    tcp = _util.run(["ss", "-H", "-tlnp"])
    udp = _util.run(["ss", "-H", "-ulnp"])
    if tcp is None and udp is None:
        degraded.append("ss_unavailable")
        return {"services": []}, degraded

    listeners += parse_ss(tcp, "tcp")
    listeners += parse_ss(udp, "udp")

    if not _util.is_root():
        degraded.append("ss_no_root")  # -p sin root no muestra proceso

    for li in listeners:
        li["exe"] = _exe_for_pid(li.get("pid"))

    return {"services": listeners}, degraded
