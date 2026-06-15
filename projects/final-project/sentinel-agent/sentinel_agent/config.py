"""Carga de sentinel.local.yml con defaults sensatos."""

from __future__ import annotations

import os
from typing import Optional

import yaml

_DEFAULTS = {
    "device_id": None,                      # OBLIGATORIO: == sufijo del topic /comando
    "aws": {
        "endpoint": None,
        "cert_path": None,
        "key_path": None,
        "root_ca": None,
    },
    "signing": {
        "public_key_path": None,            # OBLIGATORIO: clave pública Ed25519 de PI-5 (actual)
        "next_public_key_path": None,       # OPCIONAL: clave 'next' durante una rotación sin downtime
    },
    "executor": {"run_as": None, "timeout": 30},   # run_as None = root (default del proyecto)
    "discovery": {"rediscovery_interval": 0},      # 0 = solo snapshot al arranque (Fase 1)
    "detectors": {"thresholds": {}, "sqli_patterns": None, "xss_patterns": None},
    "state_path": "~/.sentinel-agent/state.json",
    "telemetry_interval": 30,
    "logging": {"file_path": None, "level": "INFO"},
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load(path: str) -> dict:
    """Carga el YAML y lo mezcla sobre los defaults. Valida lo imprescindible."""
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    cfg = _deep_merge(_DEFAULTS, raw)
    cfg["state_path"] = os.path.expanduser(cfg["state_path"])
    _validate(cfg)
    return cfg


def _validate(cfg: dict) -> None:
    if not cfg.get("device_id"):
        raise ValueError("sentinel.local.yml: falta 'device_id' (debe coincidir con el sufijo del topic /comando)")
    if not (cfg.get("signing") or {}).get("public_key_path"):
        raise ValueError("sentinel.local.yml: falta signing.public_key_path (clave pública Ed25519 de PI-5)")
    aws = cfg.get("aws") or {}
    for key in ("endpoint", "cert_path", "key_path", "root_ca"):
        if not aws.get(key):
            raise ValueError(f"sentinel.local.yml: falta aws.{key}")


def topics_for(device_id: str) -> dict:
    """Deriva los 4 topics del esquema seguridad/<device>/<categoria>."""
    return {
        "evento": f"seguridad/{device_id}/evento",
        "telemetria": f"seguridad/{device_id}/telemetria",
        "respuesta": f"seguridad/{device_id}/respuesta",
        "perfil": f"seguridad/{device_id}/perfil",
        "comando": f"seguridad/{device_id}/comando",
    }
