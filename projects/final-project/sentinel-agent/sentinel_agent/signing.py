"""
Verificación de comandos firmados por PI-5 (Ed25519) — lado sensor.

El sensor conoce ÚNICAMENTE la clave pública del coordinador: comprometerlo
no permite forjar comandos.

`_canonical_bytes` DEBE ser idéntico al de PI-5/src/tools/signing.py:
    json.dumps(sort_keys=True, separators=(",", ":"))  excluyendo "sig".
Cualquier cambio aquí debe replicarse en ambos extremos o todo comando se
rechaza por firma inválida.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import threading
import time
from typing import Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

logger = logging.getLogger("sentinel-agent")

# Margen de gracia (segundos) para absorber desfases de reloj entre PI-5 y el
# sensor. NTP en ambos lados es obligatorio.
CLOCK_SKEW_SECONDS = 5

# TTL del cache de nonces (anti-replay). Con TTL nominal de 60s + skew 5s,
# 120s da margen de sobra sin crecer indefinidamente.
NONCE_CACHE_TTL = 120

# Conjunto de claves públicas válidas. En operación normal es una sola (la del
# coordinador PI-5). Durante una ROTACIÓN sin downtime contiene la actual
# ('current') y la siguiente ('next'): el sensor acepta comandos firmados con
# CUALQUIERA de ellas mientras PI-5 cambia de clave de firma. El payload firmado
# no lleva identificador de clave (kid), así que se prueban todas hasta que una
# valide; con Ed25519 verify es barato y el set es de 1-2 claves.
# Ver scripts/generate_signing_keys.py (--next/--promote) y la guía de onboarding.
_public_keys: list = []                 # [Ed25519PublicKey, ...]
_public_keys_paths: tuple = ()          # rutas absolutas cargadas (para idempotencia)

_nonce_lock = threading.Lock()
_seen_nonces: dict = {}  # nonce -> first_seen_ts


def load_public_key(path: str) -> None:
    """Carga una única clave pública Ed25519 (compat). Equivale al set {current}."""
    load_public_keys([path])


def load_public_keys(paths) -> None:
    """
    Carga el conjunto de claves públicas Ed25519 válidas (current + opcional next).

    `paths` es un iterable de rutas a PEM; las entradas None o vacías se ignoran
    (p.ej. cuando no hay 'next' en curso). Idempotente por el conjunto de rutas.
    Habilita la rotación sin downtime: durante la ventana de rotación el sensor
    verifica contra todas las claves del set.
    """
    global _public_keys, _public_keys_paths
    abs_paths = tuple(os.path.abspath(p) for p in paths if p)
    if not abs_paths:
        raise ValueError("load_public_keys: no se proporcionó ninguna ruta de clave pública")
    if _public_keys and _public_keys_paths == abs_paths:
        return

    keys = []
    for abs_path in abs_paths:
        with open(abs_path, "rb") as f:
            key = serialization.load_pem_public_key(f.read())
        if not isinstance(key, Ed25519PublicKey):
            raise TypeError(
                f"La clave en {abs_path} no es Ed25519 (es {type(key).__name__})."
            )
        keys.append(key)

    _public_keys = keys
    _public_keys_paths = abs_paths
    if len(keys) == 1:
        logger.info(f"[SIGN] Clave pública Ed25519 cargada desde {abs_paths[0]}")
    else:
        logger.info(
            f"[SIGN] {len(keys)} claves públicas Ed25519 cargadas (rotación en curso): "
            + ", ".join(abs_paths)
        )


def verify_payload(payload: dict, now: Optional[int] = None) -> Tuple[bool, str]:
    """
    Devuelve (True, "") si el payload supera firma + ventana de validez +
    anti-replay, o (False, motivo) si no. No lanza excepciones.

    `now` inyectable para tests; por defecto time.time().
    """
    if not _public_keys:
        return False, "clave pública no cargada en el sensor"

    sig_b64 = payload.get("sig")
    if not sig_b64:
        return False, "payload sin campo 'sig'"

    for field in ("iat", "exp", "nonce"):
        if field not in payload:
            return False, f"payload sin campo obligatorio '{field}'"

    try:
        signature = base64.b64decode(sig_b64)
    except Exception as exc:
        return False, f"firma no es base64 válido: {exc}"

    message = _canonical_bytes(payload)
    if not _any_key_verifies(signature, message):
        return False, "firma Ed25519 inválida"

    now = int(time.time()) if now is None else int(now)
    iat = int(payload["iat"])
    exp = int(payload["exp"])

    if iat > now + CLOCK_SKEW_SECONDS:
        return False, f"iat en el futuro (iat={iat}, ahora={now})"
    if exp + CLOCK_SKEW_SECONDS < now:
        return False, f"comando expirado (exp={exp}, ahora={now})"

    nonce = str(payload["nonce"])
    if _nonce_already_seen(nonce, now):
        return False, f"nonce {nonce} ya visto (replay)"

    return True, ""


def _any_key_verifies(signature: bytes, message: bytes) -> bool:
    """True si ALGUNA clave del set valida la firma (rotación current+next)."""
    for key in _public_keys:
        try:
            key.verify(signature, message)
            return True
        except InvalidSignature:
            continue
    return False


def _nonce_already_seen(nonce: str, now: int) -> bool:
    with _nonce_lock:
        if len(_seen_nonces) > 1024:
            cutoff = now - NONCE_CACHE_TTL
            for k in [k for k, ts in _seen_nonces.items() if ts < cutoff]:
                _seen_nonces.pop(k, None)
        if nonce in _seen_nonces:
            return True
        _seen_nonces[nonce] = now
        return False


def _canonical_bytes(payload: dict) -> bytes:
    """
    Reproduce exactamente la serialización de PI-5 (sort_keys, separators
    compactos, campo 'sig' excluido).
    """
    to_sign = {k: v for k, v in payload.items() if k != "sig"}
    return json.dumps(to_sign, sort_keys=True, separators=(",", ":")).encode("utf-8")
