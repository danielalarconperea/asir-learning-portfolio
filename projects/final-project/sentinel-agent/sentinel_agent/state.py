"""Persistencia mínima del estado del perfil (hash + versión) entre arranques."""

from __future__ import annotations

import json
import os
from typing import Optional, Tuple


def load_state(path: str) -> Tuple[Optional[str], int]:
    """Devuelve (last_profile_hash, last_profile_version). (None, 0) si no existe."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("profile_hash"), int(data.get("profile_version", 0))
    except (FileNotFoundError, ValueError, OSError):
        return None, 0


def save_state(path: str, profile_hash: str, profile_version: int) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"profile_hash": profile_hash, "profile_version": profile_version}, f)
    os.replace(tmp, path)
