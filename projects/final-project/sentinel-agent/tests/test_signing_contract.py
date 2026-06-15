"""
Contrato criptográfico PI-5 (firma) ↔ sentinel-agent (verificación).

Valida que la canonicalización Ed25519 es byte-idéntica entre el firmante de
PI-5 y el verificador del sensor: un comando firmado por PI-5 debe verificar,
y manipulación/expiración/replay deben rechazarse.
"""

import importlib
import os
import sys

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sentinel_agent import signing as sensor_signing

# Importar el firmante de PI-5.
PI5_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "PI-5", "src"))
sys.path.insert(0, PI5_SRC)
pi5_signing = importlib.import_module("tools.signing")


def _pub_pem(priv):
    return priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def _priv_pem(priv):
    return priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _reset_signing_state():
    """Aísla los tests: limpia el estado global de ambos módulos de firma."""
    pi5_signing._private_key = None
    pi5_signing._private_key_path = None
    sensor_signing._public_keys = []
    sensor_signing._public_keys_paths = ()
    sensor_signing._seen_nonces.clear()


def _sign_with(tmp_path, priv, name, **kwargs):
    """Carga `priv` como clave de firma de PI-5 y firma un comando de prueba."""
    p = tmp_path / f"{name}.key"
    p.write_bytes(_priv_pem(priv))
    pi5_signing._private_key = None
    pi5_signing._private_key_path = None
    pi5_signing.load_private_key(str(p))
    return pi5_signing.sign_payload(_command(), **kwargs)


def _setup_rotation_sensor(tmp_path):
    """Sensor con el set {current, next}; devuelve (priv_current, priv_next)."""
    priv_cur = Ed25519PrivateKey.generate()
    priv_next = Ed25519PrivateKey.generate()
    (tmp_path / "current.pub").write_bytes(_pub_pem(priv_cur))
    (tmp_path / "next.pub").write_bytes(_pub_pem(priv_next))
    _reset_signing_state()
    sensor_signing.load_public_keys(
        [str(tmp_path / "current.pub"), str(tmp_path / "next.pub")]
    )
    return priv_cur, priv_next


@pytest.fixture
def keypair(tmp_path):
    """Genera un par Ed25519 efímero y carga priv en PI-5 y pub en el sensor."""
    priv = Ed25519PrivateKey.generate()
    priv_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    priv_path = tmp_path / "signing.key"
    pub_path = tmp_path / "signing.pub"
    priv_path.write_bytes(priv_pem)
    pub_path.write_bytes(pub_pem)

    _reset_signing_state()
    pi5_signing.load_private_key(str(priv_path))
    sensor_signing.load_public_key(str(pub_path))
    return True


def _command(log_id=42):
    return {"accion": "ejecutar_comando",
            "comando": "sudo iptables -A INPUT -s 1.2.3.4 -j DROP",
            "motivo": "test", "log_id": log_id}


def test_valid_signed_command_verifies(keypair):
    signed = pi5_signing.sign_payload(_command())
    ok, motivo = sensor_signing.verify_payload(signed)
    assert ok, motivo


def test_tampered_command_is_rejected(keypair):
    signed = pi5_signing.sign_payload(_command())
    signed["comando"] = "sudo rm -rf /"   # manipulado tras firmar
    ok, motivo = sensor_signing.verify_payload(signed)
    assert not ok
    assert "inválida" in motivo


def test_expired_command_is_rejected(keypair):
    signed = pi5_signing.sign_payload(_command(), ttl_seconds=-100)
    ok, motivo = sensor_signing.verify_payload(signed)
    assert not ok
    assert "expirado" in motivo


def test_replayed_nonce_is_rejected(keypair):
    signed = pi5_signing.sign_payload(_command())
    ok1, _ = sensor_signing.verify_payload(signed)
    ok2, motivo = sensor_signing.verify_payload(signed)   # mismo nonce otra vez
    assert ok1 is True
    assert ok2 is False
    assert "replay" in motivo


def test_missing_signature_rejected(keypair):
    payload = _command()
    ok, motivo = sensor_signing.verify_payload(payload)
    assert not ok
    assert "sig" in motivo


# --- Rotación de clave sin downtime (Fase 5): set {current, next} ---

def test_command_signed_with_current_key_verifies_during_rotation(tmp_path):
    """Con el set {current, next}, un comando firmado con la actual verifica."""
    priv_cur, _priv_next = _setup_rotation_sensor(tmp_path)
    signed = _sign_with(tmp_path, priv_cur, "current")
    ok, motivo = sensor_signing.verify_payload(signed)
    assert ok, motivo


def test_command_signed_with_next_key_verifies_during_rotation(tmp_path):
    """PI-5 ya firma con la clave 'next'; el sensor (set current+next) la acepta."""
    _priv_cur, priv_next = _setup_rotation_sensor(tmp_path)
    signed = _sign_with(tmp_path, priv_next, "next")
    ok, motivo = sensor_signing.verify_payload(signed)
    assert ok, motivo


def test_command_signed_with_foreign_key_is_rejected(tmp_path):
    """Una firma de una clave fuera del set {current, next} se rechaza."""
    _setup_rotation_sensor(tmp_path)
    priv_foreign = Ed25519PrivateKey.generate()   # no está en el set del sensor
    signed = _sign_with(tmp_path, priv_foreign, "foreign")
    ok, motivo = sensor_signing.verify_payload(signed)
    assert not ok
    assert "inválida" in motivo


def test_load_public_keys_ignores_empty_next(tmp_path):
    """Sin 'next' (None/''), el set queda con una sola clave y verifica igual."""
    priv = Ed25519PrivateKey.generate()
    (tmp_path / "current.pub").write_bytes(_pub_pem(priv))
    _reset_signing_state()
    sensor_signing.load_public_keys([str(tmp_path / "current.pub"), None, ""])
    assert len(sensor_signing._public_keys) == 1
    signed = _sign_with(tmp_path, priv, "current")
    ok, motivo = sensor_signing.verify_payload(signed)
    assert ok, motivo


def test_load_public_keys_requires_at_least_one(tmp_path):
    """Sin ninguna ruta válida, load_public_keys falla claro (no arranca a ciegas)."""
    _reset_signing_state()
    with pytest.raises(ValueError, match="ninguna ruta"):
        sensor_signing.load_public_keys([None, ""])


def test_signature_checked_before_window_in_multikey(tmp_path):
    """Firma de clave ajena Y expirada: el motivo es de FIRMA, no de ventana.

    Fija el orden: en el camino multi-clave la firma se valida ANTES que iat/exp.
    """
    _setup_rotation_sensor(tmp_path)
    priv_foreign = Ed25519PrivateKey.generate()
    signed = _sign_with(tmp_path, priv_foreign, "foreign", ttl_seconds=-100)
    ok, motivo = sensor_signing.verify_payload(signed)
    assert not ok
    assert "inválida" in motivo        # no 'expirado': la firma se comprueba primero


def test_set_transition_current_to_currentnext_to_promoted(tmp_path):
    """Simula la rotación en el sensor: {A} -> {A,B} -> {B} (post --promote + limpieza)."""
    privA = Ed25519PrivateKey.generate()
    privB = Ed25519PrivateKey.generate()
    (tmp_path / "A.pub").write_bytes(_pub_pem(privA))
    (tmp_path / "B.pub").write_bytes(_pub_pem(privB))

    # Fase inicial: solo A en el set.
    _reset_signing_state()
    sensor_signing.load_public_keys([str(tmp_path / "A.pub")])
    assert sensor_signing.verify_payload(_sign_with(tmp_path, privA, "a1"))[0]
    assert not sensor_signing.verify_payload(_sign_with(tmp_path, privB, "b1"))[0]

    # Ventana de rotación: A + B (cambia la tupla de rutas -> recarga el set).
    sensor_signing.load_public_keys([str(tmp_path / "A.pub"), str(tmp_path / "B.pub")])
    assert sensor_signing.verify_payload(_sign_with(tmp_path, privA, "a2"))[0]
    assert sensor_signing.verify_payload(_sign_with(tmp_path, privB, "b2"))[0]

    # Post-promote + limpieza: solo B; la antigua A deja de validar.
    sensor_signing.load_public_keys([str(tmp_path / "B.pub")])
    assert sensor_signing.verify_payload(_sign_with(tmp_path, privB, "b3"))[0]
    okA, motivo = sensor_signing.verify_payload(_sign_with(tmp_path, privA, "a3"))
    assert not okA
    assert "inválida" in motivo


def test_next_key_non_ed25519_fails_and_keeps_set_intact(tmp_path):
    """Un 'next' que no es Ed25519 (RSA) hace fallar la carga ENTERA y conserva el set previo."""
    from cryptography.hazmat.primitives.asymmetric import rsa

    privA = Ed25519PrivateKey.generate()
    (tmp_path / "A.pub").write_bytes(_pub_pem(privA))
    _reset_signing_state()
    sensor_signing.load_public_keys([str(tmp_path / "A.pub")])     # set válido = {A}

    rsa_pub = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    (tmp_path / "bad.pub").write_bytes(rsa_pub)

    with pytest.raises(TypeError):
        sensor_signing.load_public_keys([str(tmp_path / "A.pub"), str(tmp_path / "bad.pub")])

    # Atomicidad: el set previo {A} sigue intacto y A todavía valida.
    assert sensor_signing._public_keys
    assert sensor_signing.verify_payload(_sign_with(tmp_path, privA, "a_after"))[0]
