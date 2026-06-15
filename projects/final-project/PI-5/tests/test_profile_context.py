"""Tests del render del bloque de contexto del sistema para el triage."""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from tools import profile_context


def _profile():
    return {
        "sensor": "web-prod-01",
        "host": {"pretty_name": "Debian GNU/Linux 12", "os_id": "debian", "arch": "aarch64"},
        "package_manager": "apt",
        "firewall": {"active_manager": "nftables", "backend": "iptables-nft"},
        "web_server": {"engine": "nginx", "version": "1.22", "config_paths": ["/etc/nginx/nginx.conf"]},
        "db_engine": {"engine": "mysql", "version": "8.0"},
        "capabilities": {"restic": False, "fail2ban": True},
        "surface": {"exposed_ports": [443, 22]},
        "degraded": [],
    }


def test_render_includes_os_firewall_web_db():
    block = profile_context.render_profile_block(_profile())
    assert "CONTEXTO DEL SISTEMA OBJETIVO" in block
    assert "device=web-prod-01" in block
    assert "Debian GNU/Linux 12" in block
    assert "nftables" in block
    assert "nginx" in block
    assert "mysql" in block


def test_render_flags_available_and_missing_tools():
    block = profile_context.render_profile_block(_profile())
    assert "fail2ban" in block          # disponible
    assert "restic" in block            # listada como NO disponible


def test_render_exposed_ports():
    block = profile_context.render_profile_block(_profile())
    assert "443" in block and "22" in block


def test_render_empty_profile_is_empty_string():
    assert profile_context.render_profile_block({}) == ""


def test_render_resilient_to_degraded_profile():
    # Perfil parcial: solo host, sin firewall/web/db.
    block = profile_context.render_profile_block({"sensor": "x", "host": {"os_id": "alpine"},
                                                  "degraded": ["ss_no_root"]})
    assert "alpine" in block
    assert "Descubrimiento parcial" in block
