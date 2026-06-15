"""Probe de sistema operativo, arquitectura, virtualización y gestor de paquetes."""

from __future__ import annotations

import os
import platform
from typing import Optional, Tuple

from . import _util


def parse_os_release(text: Optional[str]) -> dict:
    """
    Parsea el contenido de /etc/os-release (clave=valor, valores con comillas)
    y devuelve {os_id, os_version, pretty_name}. Campos ausentes -> "unknown".
    """
    out = {"os_id": "unknown", "os_version": "unknown", "pretty_name": "unknown"}
    if not text:
        return out
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        val = val.strip().strip('"').strip("'")
        data[key.strip()] = val
    out["os_id"] = data.get("ID", "unknown") or "unknown"
    out["os_version"] = data.get("VERSION_ID", "unknown") or "unknown"
    out["pretty_name"] = data.get("PRETTY_NAME", "unknown") or "unknown"
    return out


def detect_package_manager(which=_util.which) -> str:
    """Devuelve el gestor de paquetes presente (apt|dnf|yum|apk|pacman|zypper|unknown)."""
    for mgr in ("apt-get", "dnf", "yum", "apk", "pacman", "zypper"):
        if which(mgr):
            return {"apt-get": "apt", "yum": "yum"}.get(mgr, mgr)
    return "unknown"


def collect() -> Tuple[dict, list]:
    """Ensambla el bloque `host` + `package_manager`. Degrada por campo."""
    degraded = []

    os_rel = parse_os_release(_util.read_text("/etc/os-release"))

    try:
        uname = os.uname()
        kernel = uname.release
        arch = uname.machine
        hostname = uname.nodename
    except AttributeError:
        # Windows (desarrollo): os.uname no existe.
        kernel = platform.release()
        arch = platform.machine()
        hostname = platform.node()
        degraded.append("os_uname_unavailable")

    virt = _detect_virt()
    if virt == "unknown":
        degraded.append("virt_unknown")

    host = {
        "hostname": hostname or "unknown",
        "os_id": os_rel["os_id"],
        "os_version": os_rel["os_version"],
        "pretty_name": os_rel["pretty_name"],
        "kernel": kernel or "unknown",
        "arch": arch or "unknown",
        "virt": virt,
        "init": _detect_init(),
        "is_root": _util.is_root(),
    }
    return {"host": host, "package_manager": detect_package_manager()}, degraded


def _detect_virt() -> str:
    out = _util.run(["systemd-detect-virt"])
    if out is not None:
        v = out.strip()
        return v or "none"
    # Fallbacks: contenedor Docker / cgroup de PID 1.
    if os.path.exists("/.dockerenv"):
        return "docker"
    cgroup = _util.read_text("/proc/1/cgroup")
    if cgroup and ("docker" in cgroup or "lxc" in cgroup):
        return "container"
    return "unknown"


def _detect_init() -> str:
    if os.path.isdir("/run/systemd/system"):
        return "systemd"
    comm = _util.read_text("/proc/1/comm")
    if comm:
        return comm.strip() or "unknown"
    return "unknown"
