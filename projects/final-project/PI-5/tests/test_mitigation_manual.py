"""Tests del motor del manual de mitigación parametrizado por perfil (Fase 2)."""
import os
import sys
from unittest.mock import patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tools import mitigation_manual as mm


# --- perfiles de prueba ----------------------------------------------------

def _generic_host():
    """nginx + mysql + nftables, SIN restic, fail2ban presente."""
    return {
        "sensor": "web-prod-01",
        "host": {"os_id": "debian", "arch": "aarch64"},
        "firewall": {"active_manager": "nftables", "backend": "iptables-nft"},
        "web_server": {"engine": "nginx", "docroots": ["/var/www/html"],
                       "config_paths": ["/etc/nginx/nginx.conf"], "listen_ports": [443],
                       "reverse_proxy_to": []},
        "db_engine": {"engine": "mysql"},
        "services": [{"proc": "sshd", "port": 2222}],
        "log_sources": [{"id": "web_access", "parser": "nginx_access",
                         "path": "/var/log/nginx/access.log", "detectors": ["sqli", "xss", "web_bruteforce"]}],
        "capabilities": {"restic": False, "mysql": True, "php": False, "systemctl": True,
                         "ss": True, "fail2ban": True, "nftables": True},
        "surface": {"exposed_ports": [443, 2222]},
    }


def _honeypot():
    """apache + mysql + iptables + restic: el perfil real del honeypot Pi4-Felix."""
    return {
        "sensor": "Pi4-Felix",
        "host": {"os_id": "debian", "arch": "aarch64"},
        "firewall": {"active_manager": "iptables", "backend": "iptables-nft"},
        "web_server": {"engine": "apache", "docroots": ["/var/www/html/sentinelti.com"],
                       "reverse_proxy_to": [8080], "listen_ports": [8080]},
        "db_engine": {"engine": "mysql"},
        "services": [{"proc": "sshd", "port": 22}],
        "log_sources": [{"id": "web_access", "parser": "apache_access",
                         "path": "/var/log/apache2/access.log", "detectors": ["sqli", "xss"]}],
        "capabilities": {"restic": True, "mysql": True, "php": True, "systemctl": True,
                         "iptables": True, "fail2ban": False},
        "surface": {"exposed_ports": [80, 8080, 22]},
    }


@pytest.fixture(autouse=True)
def _clear():
    mm.clear_cache()
    yield
    mm.clear_cache()


def _consultar(query, device, profile):
    profiles = {device: profile} if profile else {}
    with patch.object(mm, "get_device_profile", lambda d: profiles.get(d, {})):
        return mm.consultar(query, device)


# --- unidades puras --------------------------------------------------------

def test_family_for():
    assert mm.family_for("SSH brute force") == "ssh_bruteforce"
    assert mm.family_for("xss") == "xss"
    assert mm.family_for("port_scan") == "port_scan"


def test_path_get_nested_and_index():
    p = _generic_host()
    assert mm._path_get(p, "firewall.active_manager") == "nftables"
    assert mm._path_get(p, "web_server.docroots", 0) == "/var/www/html"
    assert mm._path_get(p, "no.existe") is None


def test_passes_requires():
    caps = {"fail2ban", "mysql"}
    assert mm.passes_requires({"requires": []}, caps, {"x": 1}) is True
    assert mm.passes_requires({"requires": ["fail2ban"]}, caps, {"x": 1}) is True
    assert mm.passes_requires({"requires": ["restic"]}, caps, {"x": 1}) is False
    # sin perfil, requires no vacío -> False (conservador)
    assert mm.passes_requires({"requires": ["mysql"]}, caps, {}) is False


def test_applies_if_nested_and_wildcard():
    p = _generic_host()
    assert mm.passes_applies_if({"applies_if": {"web_server.engine": "nginx"}}, p) is True
    assert mm.passes_applies_if({"applies_if": {"web_server.engine": "apache"}}, p) is False
    assert mm.passes_applies_if({"applies_if": {"web_server.docroots": "*"}}, p) is True
    assert mm.passes_applies_if({"applies_if": {}}, p) is True


def test_applies_if_override_operators():
    p = _honeypot()
    assert mm._condition_ok("web_server.docroots_contains", "/var/www/html/sentinelti.com", p) is True
    assert mm._condition_ok("surface.exposed_ports_contains_all", [80, 8080], p) is True
    assert mm._condition_ok("surface.exposed_ports_contains_all", [80, 9999], p) is False
    assert mm._condition_ok("capabilities.restic", True, p) is True


def test_pick_command_fw_and_fallback():
    entry = {"id": "x", "command_templates": {"iptables": "A", "ufw": "B", "nftables": "C"}}
    assert mm.pick_command(entry, "nftables", []) == "C"
    notes = []
    # fw 'none' no está -> fallback por preferencia (ufw primero)
    assert mm.pick_command(entry, "none", notes) == "B"
    assert notes  # deja nota de fallback
    assert mm.pick_command({"command_templates": {"default": "D"}}, "iptables", []) == "D"


def test_resolve_keeps_ip_literal_and_substitutes_ports():
    p = _generic_host()
    text, missing = mm.resolve_and_validate("nft ... ip saddr {ip} tcp dport {ssh_port} drop", ["ip", "ssh_port"], p)
    assert "{ip}" in text          # se deja literal para el LLM
    assert "2222" in text          # ssh_port del perfil
    assert missing == []


def test_resolve_omits_when_path_placeholder_unresolvable():
    # web_docroot resuelve a None -> missing -> la entrada se omitiría
    text, missing = mm.resolve_and_validate("grep x {web_docroot}", ["web_docroot"], {"web_server": {}})
    assert "web_docroot" in missing


def test_resolve_validates_path_allowlist():
    bad = {"web_server": {"docroots": ["/etc/passwd_dir_raro"]}}
    # /etc no está en la allowlist de web_docroot -> inválido -> missing
    _, missing = mm.resolve_and_validate("grep x {web_docroot}", ["web_docroot"], bad)
    assert "web_docroot" in missing


# --- consultar end-to-end --------------------------------------------------

def test_ssh_query_uses_nftables_template_and_real_port():
    out = _consultar("ssh", "web-prod-01", _generic_host())
    assert "ip saddr {ip}" in out          # plantilla nftables, {ip} literal
    assert "2222" in out                    # puerto SSH real del perfil
    # nunca cuela el honeypot
    assert "sentinelti.com" not in out
    assert "restic" not in out
    assert "/home/lopex" not in out


def test_restic_recovery_filtered_out_when_no_capability():
    out = _consultar("defacement", "web-prod-01", _generic_host())
    # el host genérico no tiene restic -> ningún COMANDO restic propuesto
    assert "restic restore" not in out
    assert "/home/lopex" not in out
    # sí aparece el marcador de gobernanza (recuperación requiere override)
    assert "RECUPERACION NO DISPONIBLE" in out.upper() or "OVERRIDE" in out.upper()


def test_honeypot_device_gets_its_overrides():
    out = _consultar("xss", "Pi4-Felix", _honeypot())
    # el device Pi4-Felix SÍ recibe sus mitigaciones específicas
    assert "sentinelti.com" in out
    assert "[override]" in out.lower()


def test_honeypot_overrides_never_leak_to_other_device():
    # mismo ataque, otro device: jamás debe aparecer nada del honeypot
    out = _consultar("xss", "web-prod-01", _generic_host())
    assert "sentinelti.com" not in out
    assert "restic" not in out
    assert "cerrar_sesion_admin" not in out


def test_unknown_query_returns_universal_block_not_honeypot():
    # Las entradas _universal (bloqueo de IP) matchean cualquier query;
    # nunca se devuelve el honeypot.
    out = _consultar("algo_raro_sin_familia", "web-prod-01", _generic_host())
    assert "sentinelti.com" not in out
    assert "ip saddr {ip}" in out          # bloqueo universal por nftables


def test_minimal_fallback_when_manual_empty_never_honeypot():
    # Si generic.json no carga (vacío), se cae al mínimo seguro, NUNCA al honeypot.
    with patch.object(mm, "_load_generic", lambda: []), \
         patch.object(mm, "get_device_profile", lambda d: _generic_host()):
        out = mm.consultar("ssh", "web-prod-01")
    assert "sentinelti.com" not in out
    assert "ss -tulpnH" in out or "journalctl" in out


def test_no_profile_returns_generic_with_warning():
    out = _consultar("ssh", "fantasma", None)
    assert "PERFIL NO DESCUBIERTO" in out.upper()
    assert "sentinelti.com" not in out
    # fail2ban requiere capability -> sin perfil no se propone
    assert "fail2ban-client set sshd banip" not in out


def test_consultar_never_raises_on_bad_profile():
    with patch.object(mm, "get_device_profile", lambda d: None):
        out = mm.consultar("ssh", "x")
    assert isinstance(out, str)
