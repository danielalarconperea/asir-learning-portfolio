"""Utilidades compartidas por los probes de discovery (I/O fina y aislada)."""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import List, Optional


def run(cmd: List[str], timeout: float = 5.0, merge_stderr: bool = False) -> Optional[str]:
    """
    Ejecuta un comando (lista de args, sin shell) y devuelve su stdout como
    str, o None si el binario no existe, falla o agota el timeout.

    `merge_stderr=True` concatena stderr a stdout (lo necesitan herramientas
    como `nginx -V` que escriben su versión en stderr).

    Nunca lanza: los probes deben degradar, no romper.
    """
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None
    if merge_stderr:
        return (proc.stdout or "") + (proc.stderr or "")
    return proc.stdout


def which(name: str) -> Optional[str]:
    """Ruta del binario `name` si está en PATH, o None. Equivale a `command -v`."""
    return shutil.which(name)


def read_text(path: str, limit: int = 65536) -> Optional[str]:
    """Lee un fichero de texto (hasta `limit` bytes) o None si no se puede."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(limit)
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        return None


def is_root() -> bool:
    """True si el proceso corre como root (geteuid 0). False en plataformas sin geteuid."""
    geteuid = getattr(os, "geteuid", None)
    return geteuid() == 0 if geteuid else False
