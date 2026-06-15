"""Tests del orquestador del enriquecedor (Fase 4): modelo api/local, LLM, validación, sanitización."""
import json
import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tools import profile_enricher as pe


def _profile():
    return {
        "sensor": "web-prod-01", "profile_hash": "sha256:abc", "profile_version": 3,
        "host": {"os_id": "debian", "pretty_name": "Debian 12", "arch": "aarch64"},
        "package_manager": "apt",
        "firewall": {"active_manager": "nftables"},
        "web_server": {"engine": "nginx", "version": "1.22", "config_paths": ["/etc/nginx/nginx.conf"],
                       "docroots": ["/var/www/html"], "listen_ports": [443]},
        "db_engine": {"engine": "mysql"},
        "services": [{"proc": "sshd", "port": 22, "bind": "0.0.0.0"},
                     {"proc": "nginx", "port": 443, "bind": "0.0.0.0"},
                     {"proc": "mysqld", "port": 3306, "bind": "127.0.0.1"}],
        "log_sources": [{"id": "web_access", "service": "nginx", "source": "file",
                         "path": "/var/log/nginx/access.log", "parser": "nginx_access",
                         "detectors": ["sqli", "xss", "web_bruteforce"]}],
        "capabilities": {"restic": False, "mysql": True, "php": False, "fail2ban": True, "systemctl": True},
        "surface": {"exposed_ports": [443, 22], "loopback_only": [3306]},
        "degraded": [],
    }


def _valid_enrichment():
    return {
        "schema_version": 1, "device": "ignored", "based_on_profile_hash": "ignored",
        "global_confidence": "medium",
        "host_notes": {"summary": "Host nginx+mysql.", "risks": [
            {"text": "MySQL en loopback", "confidence": "high", "evidence": ["surface.loopback_only"]}]},
        "suggested_log_sources": [{
            "id": "mysql_error", "service": "mysqld", "source": "file",
            "path": "/var/log/mysql/error.log", "unit": None, "format": None,
            "parser": "mysql_log", "detectors": ["db_compromise"], "confidence": "medium",
            "evidence": ["services.proc:mysqld"]}],
        "suggested_recommendation_overrides": [{
            "id": "tail-web", "intent": "diagnostic", "severity": "baja", "requires": [],
            "applies_if": {"web_server.engine": "nginx"},
            "match": {"families": ["web_bruteforce"], "keywords": ["web"]},
            "command": "sudo tail -n 100 /var/log/nginx/access.log", "revert": "",
            "placeholders": [], "explanation": "Ver accesos.", "confidence": "medium",
            "evidence": ["log_sources.id:web_access"]}],
    }


# --- selección de modelo (dualidad) ---------------------------------------

def test_model_config_default_local(monkeypatch):
    monkeypatch.delenv("ENRICH_MODE", raising=False)
    monkeypatch.delenv("ENRICH_MODEL", raising=False)
    monkeypatch.setenv("AI_MODE", "local")
    monkeypatch.setenv("AI_MODEL", "ollama/gemma4:e2b")
    mode, model, extra = pe._resolve_model_config()
    assert mode == "local"
    assert model == "ollama/gemma4:e2b"
    assert "api_base" in extra


def test_model_config_api_needs_key(monkeypatch):
    monkeypatch.setenv("ENRICH_MODE", "api")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(pe.ProviderError) as ei:
        pe._resolve_model_config()
    assert ei.value.kind == "connection"


def test_model_override_does_not_touch_environ(monkeypatch):
    monkeypatch.setenv("AI_MODE", "local")
    monkeypatch.setenv("ENRICH_MODE", "api")
    monkeypatch.setenv("ENRICH_MODEL", "gemini-3-pro")
    monkeypatch.setenv("GEMINI_API_KEY", "k")
    mode, model, extra = pe._resolve_model_config()
    assert mode == "api" and model == "gemini-3-pro"
    assert os.environ["AI_MODE"] == "local"          # no se tocó el toggle del triage
    assert "OLLAMA_API_BASE" not in os.environ or os.environ.get("OLLAMA_API_BASE") != extra.get("api_base")


# --- llm_call --------------------------------------------------------------

def test_llm_call_response_format_per_mode(monkeypatch):
    seen = {}
    def fake(model, messages, **kw):
        seen.update(kw)
        return json.dumps(_valid_enrichment())
    monkeypatch.setattr(pe, "_raw_completion", fake)
    pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "api", "gemini", {"api_key": "k"})
    assert seen["response_format"]["type"] == "json_schema"
    assert seen["response_format"]["json_schema"]["strict"] is True
    pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "local", "ollama/x", {"api_base": "b"})
    assert seen["response_format"]["type"] == "json_object"


def test_llm_call_parses_json_wrapped_in_prose(monkeypatch):
    payload = _valid_enrichment()
    monkeypatch.setattr(pe, "_raw_completion",
                        lambda m, msg, **k: "Aquí tienes:\n```json\n" + json.dumps(payload) + "\n```\nfin")
    out = pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "local", "x", {})
    assert out["schema_version"] == 1


def test_llm_call_non_json_raises_hallucination(monkeypatch):
    monkeypatch.setattr(pe, "_raw_completion", lambda m, msg, **k: "no es json")
    with pytest.raises(pe.HallucinationError):
        pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "local", "x", {})


def test_llm_call_rate_limit_retries_then_provider_error(monkeypatch):
    class RateLimitError(Exception):
        pass
    calls = {"n": 0}
    def boom(m, msg, **k):
        calls["n"] += 1
        raise RateLimitError("429")
    monkeypatch.setattr(pe, "_raw_completion", boom)
    monkeypatch.setattr(pe.time, "sleep", lambda s: None)
    with pytest.raises(pe.ProviderError) as ei:
        pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "local", "x", {}, max_retries=2)
    assert ei.value.kind == "rate_limit"
    assert calls["n"] == 3   # 1 + 2 reintentos


def test_llm_call_connection_error_no_retry(monkeypatch):
    class APIConnectionError(Exception):
        pass
    calls = {"n": 0}
    def boom(m, msg, **k):
        calls["n"] += 1
        raise APIConnectionError("down")
    monkeypatch.setattr(pe, "_raw_completion", boom)
    with pytest.raises(pe.ProviderError) as ei:
        pe.llm_call("p", pe.ENRICHMENT_SCHEMA, "local", "x", {}, max_retries=2)
    assert ei.value.kind == "connection"
    assert calls["n"] == 1   # sin reintento


# --- validación + cross-check + sanitización ------------------------------

def test_schema_rejects_invented_field(monkeypatch):
    bad = _valid_enrichment()
    bad["campo_inventado"] = "x"
    with pytest.raises(pe.HallucinationError):
        pe.validate_and_crosscheck(bad, _profile(), "web-prod-01")


def test_validate_keeps_valid_and_seals_device():
    res = pe.validate_and_crosscheck(_valid_enrichment(), _profile(), "web-prod-01")
    kept = res["kept"]
    assert kept["device"] == "web-prod-01"
    assert kept["based_on_profile_hash"] == "sha256:abc"   # sellado con el real
    assert len(kept["suggested_log_sources"]) == 1
    assert len(kept["suggested_recommendation_overrides"]) == 1


def test_validate_discards_hallucinated_override():
    data = _valid_enrichment()
    data["suggested_recommendation_overrides"][0]["command"] = "cat /opt/secret/x.conf"
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    assert res["kept"]["suggested_recommendation_overrides"] == []
    assert any(d["type"] == "override" for d in res["discarded"])


def test_validate_rejects_destructive_override():
    data = _valid_enrichment()
    ov = data["suggested_recommendation_overrides"][0]
    ov["intent"] = "mitigation"
    ov["command"] = "sudo rm -rf {web_docroot}"
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    assert res["kept"]["suggested_recommendation_overrides"] == []
    assert any("destructivo" in d["reason"] for d in res["discarded"])


def test_validate_annotates_risk_level():
    # El comando base ("sudo tail -n 100 ...") es lectura -> SAFE_READ.
    res = pe.validate_and_crosscheck(_valid_enrichment(), _profile(), "web-prod-01")
    ov = res["kept"]["suggested_recommendation_overrides"][0]
    assert ov["risk_level"] == "SAFE_READ"
    assert "policy_reasons" in ov


def test_validate_rejects_interpreter_override():
    data = _valid_enrichment()
    data["suggested_recommendation_overrides"][0].update({
        "intent": "mitigation", "command": 'sh -c "systemctl restart nginx"'})
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    assert res["kept"]["suggested_recommendation_overrides"] == []
    assert any("interprete" in d["reason"] for d in res["discarded"])


def test_validate_rejects_newline_in_command():
    data = _valid_enrichment()
    data["suggested_recommendation_overrides"][0].update({
        "intent": "mitigation",
        "command": "cat /var/log/nginx/access.log\nsystemctl restart nginx"})
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    assert res["kept"]["suggested_recommendation_overrides"] == []


def test_validate_caps_recovery_confidence():
    data = _valid_enrichment()
    data["suggested_recommendation_overrides"][0].update({
        "intent": "recovery", "confidence": "high"})
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    ov = res["kept"]["suggested_recommendation_overrides"][0]
    assert ov["confidence"] in ("medium", "low")   # recovery nunca high


def test_validate_sanitizes_prose():
    data = _valid_enrichment()
    data["host_notes"]["summary"] = "ejecuta $(whoami) y `id`"
    res = pe.validate_and_crosscheck(data, _profile(), "web-prod-01")
    s = res["kept"]["host_notes"]["summary"]
    assert "$(" not in s and "`" not in s


# --- arquitectura: el enricher NO toca la ruta caliente -------------------

def _read(rel):
    p = os.path.join(os.path.dirname(__file__), '..', 'src', rel)
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def test_enricher_source_no_imports_hot_path():
    # Solo las LÍNEAS de import cuentan (el docstring puede nombrar los módulos).
    forbidden = ("aws_connector", "iot_tools", "google.adk", "main_coordinator", "signing")
    for rel in ("tools/profile_enricher.py", "tools/enrichment_crosscheck.py"):
        for line in _read(rel).splitlines():
            s = line.strip()
            if s.startswith("import ") or s.startswith("from "):
                for f in forbidden:
                    assert f not in s, f"{rel}: {line}"


def test_hot_path_does_not_reference_enrichments():
    for rel in ("main_coordinator.py", "tools/profile_context.py", "tools/mitigation_manual.py"):
        src = _read(rel)
        assert "device_enrichments" not in src
        assert "profile_enricher" not in src
