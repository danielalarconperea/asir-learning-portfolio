"""Tests de la firma de log_sources (qué se vigila) — pura, sin Monitor."""

from sentinel_agent.monitor import log_sources_signature


def _src(id, source="file", path="/var/log/x", unit=None, parser="nginx_access"):
    return {"id": id, "source": source, "path": path, "unit": unit, "parser": parser}


def test_signature_stable_under_reorder():
    a = {"log_sources": [_src("ssh"), _src("web")]}
    b = {"log_sources": [_src("web"), _src("ssh")]}
    assert log_sources_signature(a) == log_sources_signature(b)


def test_signature_changes_on_field_change():
    base = {"log_sources": [_src("web", path="/var/log/nginx/access.log")]}
    changed = {"log_sources": [_src("web", path="/var/log/apache2/access.log")]}
    assert log_sources_signature(base) != log_sources_signature(changed)
    # cambio de parser también cuenta
    p2 = {"log_sources": [_src("web", parser="apache_access")]}
    assert log_sources_signature(base) != log_sources_signature(p2)


def test_signature_ignores_other_sections():
    a = {"log_sources": [_src("ssh")], "firewall": {"active_manager": "nftables"}}
    b = {"log_sources": [_src("ssh")], "firewall": {"active_manager": "ufw"}}
    assert log_sources_signature(a) == log_sources_signature(b)


def test_signature_none_vs_empty_path_equivalent():
    a = {"log_sources": [{"id": "ssh", "source": "journald", "path": None, "unit": "ssh", "parser": "sshd_auth"}]}
    b = {"log_sources": [{"id": "ssh", "source": "journald", "path": "", "unit": "ssh", "parser": "sshd_auth"}]}
    assert log_sources_signature(a) == log_sources_signature(b)


def test_signature_empty_list():
    assert log_sources_signature({"log_sources": []}) == log_sources_signature({})
