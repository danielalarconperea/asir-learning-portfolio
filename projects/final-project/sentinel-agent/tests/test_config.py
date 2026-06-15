"""Tests de la carga/validación de config y la derivación de topics."""

import pytest

from sentinel_agent import config as cfg_mod


def _write(tmp_path, text):
    p = tmp_path / "sentinel.local.yml"
    p.write_text(text, encoding="utf-8")
    return str(p)


_VALID = """
device_id: web-prod-01
aws:
  endpoint: ep
  cert_path: c
  key_path: k
  root_ca: ca
signing:
  public_key_path: pub.pem
"""


def test_load_valid_merges_defaults(tmp_path):
    cfg = cfg_mod.load(_write(tmp_path, _VALID))
    assert cfg["device_id"] == "web-prod-01"
    assert cfg["executor"]["run_as"] is None          # default: root
    assert cfg["discovery"]["rediscovery_interval"] == 0
    assert cfg["aws"]["endpoint"] == "ep"


def test_load_missing_device_id_raises(tmp_path):
    bad = _VALID.replace("device_id: web-prod-01", "")
    with pytest.raises(ValueError, match="device_id"):
        cfg_mod.load(_write(tmp_path, bad))


def test_load_missing_signing_raises(tmp_path):
    bad = _VALID.replace("  public_key_path: pub.pem", "")
    with pytest.raises(ValueError, match="public_key_path"):
        cfg_mod.load(_write(tmp_path, bad))


def test_next_public_key_path_optional_defaults_none(tmp_path):
    """Sin rotación en curso, next_public_key_path es None (campo opcional)."""
    cfg = cfg_mod.load(_write(tmp_path, _VALID))
    assert cfg["signing"]["public_key_path"] == "pub.pem"
    assert cfg["signing"]["next_public_key_path"] is None


def test_next_public_key_path_is_merged(tmp_path):
    """Durante una rotación, next_public_key_path se carga junto a la actual."""
    rotating = _VALID + "  next_public_key_path: next.pem\n"
    cfg = cfg_mod.load(_write(tmp_path, rotating))
    assert cfg["signing"]["public_key_path"] == "pub.pem"
    assert cfg["signing"]["next_public_key_path"] == "next.pem"


def test_load_missing_aws_field_raises(tmp_path):
    bad = _VALID.replace("  endpoint: ep", "")
    with pytest.raises(ValueError, match="aws.endpoint"):
        cfg_mod.load(_write(tmp_path, bad))


def test_topics_for_derives_four_plus_command():
    t = cfg_mod.topics_for("web-prod-01")
    assert t["evento"] == "seguridad/web-prod-01/evento"
    assert t["perfil"] == "seguridad/web-prod-01/perfil"
    assert t["comando"] == "seguridad/web-prod-01/comando"
    assert t["respuesta"] == "seguridad/web-prod-01/respuesta"
