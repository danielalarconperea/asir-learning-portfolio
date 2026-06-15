"""Tests de las funciones puras de cross-check del enriquecedor (Fase 4)."""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tools import enrichment_crosscheck as cc


def _profile():
    return {
        "sensor": "web-prod-01", "profile_hash": "sha256:abc", "profile_version": 3,
        "host": {"os_id": "debian", "arch": "aarch64"},
        "firewall": {"active_manager": "nftables"},
        "web_server": {"engine": "nginx", "config_paths": ["/etc/nginx/nginx.conf"],
                       "docroots": ["/var/www/html"], "listen_ports": [443]},
        "db_engine": {"engine": "mysql"},
        "services": [{"proc": "sshd", "port": 22}, {"proc": "nginx", "port": 443},
                     {"proc": "mysqld", "port": 3306}],
        "log_sources": [{"id": "web_access", "service": "nginx", "source": "file",
                         "path": "/var/log/nginx/access.log", "parser": "nginx_access",
                         "detectors": ["sqli", "xss", "web_bruteforce"]}],
        "capabilities": {"restic": False, "mysql": True, "php": False, "fail2ban": True},
        "surface": {"exposed_ports": [443, 22], "loopback_only": [3306]},
    }


# --- log_source -----------------------------------------------------------

def test_log_source_real_service_kept():
    F = cc.facts(_profile())
    ls = {"id": "mysql_err", "service": "mysqld", "source": "file",
          "path": "/var/log/mysql/error.log", "parser": "mysql_log",
          "detectors": ["db_compromise"], "evidence": ["services.proc:mysqld"]}
    verdict, reason, downs = cc.check_log_source(ls, F)
    assert verdict == "KEEP"


def test_log_source_unknown_service_discarded():
    F = cc.facts(_profile())
    ls = {"id": "pg", "service": "postgres", "source": "file",
          "path": "/var/log/postgresql/x.log", "parser": "pg", "detectors": [], "evidence": ["x"]}
    verdict, reason, _ = cc.check_log_source(ls, F)
    assert verdict == "DISCARD"
    assert "postgres" in reason


def test_log_source_path_outside_allowlist_discarded():
    F = cc.facts(_profile())
    ls = {"id": "x", "service": "nginx", "source": "file", "path": "/home/x/app.log",
          "parser": "nginx_access", "detectors": [], "evidence": ["x"]}
    assert cc.check_log_source(ls, F)[0] == "DISCARD"


def test_log_source_journald_unknown_unit_discarded():
    F = cc.facts(_profile())
    ls = {"id": "x", "service": "nginx", "source": "journald", "unit": "ghost.service",
          "parser": "nginx_access", "detectors": [], "evidence": ["x"]}
    assert cc.check_log_source(ls, F)[0] == "DISCARD"


# --- override -------------------------------------------------------------

def _ov(**kw):
    base = {"id": "x", "intent": "diagnostic", "severity": "baja", "requires": [],
            "applies_if": {}, "match": {}, "command": "sudo ss -tulpnH", "explanation": "x",
            "confidence": "medium", "evidence": ["services.proc:nginx"]}
    base.update(kw)
    return base


def test_override_requires_missing_capability_discarded():
    F = cc.facts(_profile())
    ov = _ov(requires=["restic"])
    assert cc.check_override(ov, F, _profile())[0] == "DISCARD"


def test_override_applies_if_false_discarded():
    p = _profile()
    F = cc.facts(p)
    assert cc.check_override(_ov(applies_if={"web_server.engine": "apache"}), F, p)[0] == "DISCARD"
    assert cc.check_override(_ov(applies_if={"db_engine.engine": "postgres"}), F, p)[0] == "DISCARD"


def test_override_hallucinated_path_discarded():
    p = _profile()
    F = cc.facts(p)
    ov = _ov(command="bash /opt/secret/restore.sh")
    assert cc.check_override(ov, F, p)[0] == "DISCARD"


def test_override_unresolvable_placeholder_discarded():
    # {web_log} sin fuente web -> no resoluble; aquí el perfil SÍ tiene web_log, así que usamos otro
    p = _profile()
    p["log_sources"] = []   # sin fuentes -> {web_log} no resuelve
    F = cc.facts(p)
    ov = _ov(command="sudo grep x {web_log}")
    assert cc.check_override(ov, F, p)[0] == "DISCARD"


def test_override_with_ip_literal_kept():
    p = _profile()
    F = cc.facts(p)
    ov = _ov(intent="mitigation", command="sudo nft add rule inet filter input ip saddr {ip} drop")
    verdict, reason, _ = cc.check_override(ov, F, p)
    assert verdict == "KEEP", reason


# --- notas / utilidades ---------------------------------------------------

def test_override_path_traversal_discarded():
    p = _profile()
    F = cc.facts(p)
    assert cc.check_override(_ov(command="sudo cat /var/log/../../etc/shadow"), F, p)[0] == "DISCARD"


def test_override_etc_shadow_discarded():
    p = _profile()
    F = cc.facts(p)
    assert cc.check_override(_ov(command="cat /etc/shadow"), F, p)[0] == "DISCARD"


def test_override_real_config_path_kept():
    p = _profile()
    F = cc.facts(p)
    # /etc/nginx/nginx.conf SÍ está en web_configs del perfil -> KEEP
    assert cc.check_override(_ov(command="sudo nginx -t -c /etc/nginx/nginx.conf"), F, p)[0] == "KEEP"


def test_check_note_evidence_resolves():
    p = _profile()
    assert cc.check_note({"text": "x", "evidence": ["surface.loopback_only"]}, p) == "high"
    assert cc.check_note({"text": "x", "evidence": []}, p) == "low"
    assert cc.check_note({"text": "x", "evidence": ["nope.field"]}, p) == "medium"


def test_extract_abs_paths():
    paths = cc.extract_abs_paths("sudo grep x /var/log/nginx/access.log && cat /tmp")
    assert "/var/log/nginx/access.log" in paths
    assert "/tmp" not in paths   # 1 segmento, ignorado
