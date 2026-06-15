"""
Verificacion de comandos firmados por PI-5 (Ed25519).

PI-4 conoce unicamente la CLAVE PUBLICA del coordinador, lo que significa
que comprometer este sensor no permite a un atacante forjar comandos
nuevos: solo el coordinador (con su privada) puede emitir ordenes que
pasen verify_payload().

Reglas de aceptacion:
  1. Firma Ed25519 valida sobre el JSON canonico sin el campo `sig`.
  2. `exp` (unix seconds) aun no ha pasado (con un margen de gracia que
     absorbe pequenos desfases de reloj). NTP en ambos lados es
     obligatorio.
  3. `nonce` no se ha visto antes en la ventana de tiempo. Esto evita
     que un atacante reenvie un comando legitimo capturado dentro de su
     TTL.
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

logger = logging.getLogger("SensorSOC")

# Margen de gracia (segundos) para absorber desfases de reloj entre PI-5 y
# PI-4. Vale tanto para `iat` como para `exp`.
CLOCK_SKEW_SECONDS = 5

# Periodo (segundos) tras el cual una entrada del nonce cache puede ser
# descartada. Con un TTL nominal de 60s y skew de 5s, 120s da margen mas
# que suficiente sin crecer indefinidamente.
NONCE_CACHE_TTL = 120

_public_key: Optional[Ed25519PublicKey] = None
_public_key_path: Optional[str] = None

_nonce_lock = threading.Lock()
_seen_nonces: dict = {}  # nonce -> first_seen_ts


class VerificationError(Exception):
    """Razon legible de por que un payload no paso la verificacion."""


def load_public_key(path: str) -> None:
    """Carga la clave publica Ed25519 desde un PEM en disco."""
    global _public_key, _public_key_path
    abs_path = os.path.abspath(path)
    if _public_key is not None and _public_key_path == abs_path:
        return

    with open(abs_path, "rb") as f:
        key = serialization.load_pem_public_key(f.read())
    if not isinstance(key, Ed25519PublicKey):
        raise TypeError(
            f"La clave en {abs_path} no es Ed25519 (es {type(key).__name__})."
        )
    _public_key = key
    _public_key_path = abs_path
    logger.info(f"[SIGN] Clave publica Ed25519 cargada desde {abs_path}")


def verify_payload(payload: dict) -> Tuple[bool, str]:
    """
    Devuelve (True, "") si el payload supera todas las comprobaciones, o
    (False, motivo) si no. No lanza excepciones: que el caller decida
    como reaccionar (logear, publicar rejected_signature, abortar...).
    """
    if _public_key is None:
        return False, "clave publica no cargada en PI-4"

    sig_b64 = payload.get("sig")
    if not sig_b64:
        return False, "payload sin campo 'sig'"

    for field in ("iat", "exp", "nonce"):
        if field not in payload:
            return False, f"payload sin campo obligatorio '{field}'"

    try:
        signature = base64.b64decode(sig_b64)
    except Exception as exc:
        return False, f"firma no es base64 valido: {exc}"

    message = _canonical_bytes(payload)
    try:
        _public_key.verify(signature, message)
    except InvalidSignature:
        return False, "firma Ed25519 invalida"

    now = int(time.time())
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


def _nonce_already_seen(nonce: str, now: int) -> bool:
    """
    Registra el nonce. Si ya estaba en cache devuelve True. Limpia
    entradas antiguas oportunisticamente para no crecer sin limite.
    """
    with _nonce_lock:
        # Limpieza perezosa: solo cuando hay riesgo de crecer.
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
    Reproduce exactamente la serializacion que hizo PI-5 (sort_keys,
    separators compactos, campo `sig` excluido). Cualquier cambio aqui
    debe replicarse en PI-5/src/tools/signing.py:_canonical_bytes.
    """
    to_sign = {k: v for k, v in payload.items() if k != "sig"}
    return json.dumps(to_sign, sort_keys=True, separators=(",", ":")).encode("utf-8")
