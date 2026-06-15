"""Tests del ensamblado del perfil, el profile_hash (material) y la versión."""

from sentinel_agent import profile_builder as pb


def _sections():
    return {
        "host": {"hostname": "web-prod-01", "os_id": "debian", "os_version": "12",
                 "arch": "aarch64", "virt": "kvm", "init": "systemd", "is_root": True},
        "package_manager": "apt",
        "firewall": {"active_manager": "nftables", "active": True, "backend": "iptables-nft"},
        "services": [{"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd",
                      "pid": 812, "exe": "/usr/sbin/sshd"}],
        "stack": {"web_server": {"engine": "nginx", "version": "1.22.1"},
                  "db_engine": {"engine": "mysql"}},
        "log_sources": [{"id": "ssh", "parser": "sshd_auth"}],
        "capabilities": {"restic": False, "fail2ban": True},
        "users": {"sudoers": ["admin"]},
        "surface": {"exposed_ports": [22], "loopback_only": [3306]},
        "degraded": [],
    }


def test_assemble_core_maps_sections():
    p = pb.assemble_core("web-prod-01", _sections(), "2026-06-14T10:00:00Z", "boot")
    assert p["tipo"] == "PERFIL_SISTEMA"
    assert p["sensor"] == "web-prod-01"
    assert p["dispositivo"] == "web-prod-01"
    assert p["web_server"]["engine"] == "nginx"
    assert p["db_engine"]["engine"] == "mysql"
    assert p["package_manager"] == "apt"


def test_hash_is_deterministic():
    p1 = pb.assemble_core("d", _sections(), "2026-06-14T10:00:00Z", "boot")
    p2 = pb.assemble_core("d", _sections(), "2026-06-14T23:59:59Z", "periodic")
    # discovered_at y trigger NO deben afectar al hash.
    assert pb.compute_profile_hash(p1) == pb.compute_profile_hash(p2)


def test_hash_ignores_volatile_pid_and_is_root():
    s1 = _sections()
    s2 = _sections()
    s2["services"][0]["pid"] = 99999        # reinicio: PID distinto
    s2["host"]["is_root"] = False           # arrancado sin root
    p1 = pb.assemble_core("d", s1, "t", "boot")
    p2 = pb.assemble_core("d", s2, "t", "boot")
    assert pb.compute_profile_hash(p1) == pb.compute_profile_hash(p2)


def test_hash_changes_on_material_change():
    s1 = _sections()
    s2 = _sections()
    s2["firewall"]["active_manager"] = "ufw"   # cambio real de firewall
    p1 = pb.assemble_core("d", s1, "t", "boot")
    p2 = pb.assemble_core("d", s2, "t", "boot")
    assert pb.compute_profile_hash(p1) != pb.compute_profile_hash(p2)


def test_next_profile_version():
    assert pb.next_profile_version(None, 0, "sha256:a") == (1, True)        # primer perfil
    assert pb.next_profile_version("sha256:a", 1, "sha256:a") == (1, False)  # sin cambios
    assert pb.next_profile_version("sha256:a", 1, "sha256:b") == (2, True)   # cambió


def test_finalize_sets_hash_and_version():
    p = pb.assemble_core("d", _sections(), "t", "boot")
    p, changed = pb.finalize(p, prev_hash=None, prev_version=0)
    assert p["profile_hash"].startswith("sha256:")
    assert p["profile_version"] == 1
    assert changed is True


def test_hash_stable_under_services_reorder():
    # `ss` no garantiza orden; reordenar services NO debe cambiar el hash.
    s1 = _sections()
    s1["services"] = [
        {"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd", "pid": 1},
        {"proto": "tcp", "port": 443, "bind": "0.0.0.0", "proc": "nginx", "pid": 2},
    ]
    s2 = _sections()
    s2["services"] = [
        {"proto": "tcp", "port": 443, "bind": "0.0.0.0", "proc": "nginx", "pid": 999},  # reordenado + pid distinto
        {"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd", "pid": 888},
    ]
    p1 = pb.assemble_core("d", s1, "t", "boot")
    p2 = pb.assemble_core("d", s2, "t", "boot")
    assert pb.compute_profile_hash(p1) == pb.compute_profile_hash(p2)


def test_hash_ignores_volatile_exe():
    # exe cambia tras `apt upgrade` ("(deleted)") sin cambiar la topología.
    s1 = _sections()
    s1["services"] = [{"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd",
                       "pid": 1, "exe": "/usr/sbin/sshd"}]
    s2 = _sections()
    s2["services"] = [{"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd",
                       "pid": 999, "exe": "/usr/sbin/sshd (deleted)"}]
    p1 = pb.assemble_core("d", s1, "t", "boot")
    p2 = pb.assemble_core("d", s2, "t", "boot")
    assert pb.compute_profile_hash(p1) == pb.compute_profile_hash(p2)


def test_hash_changes_on_new_service():
    s1 = _sections()
    s1["services"] = [{"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd", "pid": 1}]
    s2 = _sections()
    s2["services"] = [
        {"proto": "tcp", "port": 22, "bind": "0.0.0.0", "proc": "sshd", "pid": 1},
        {"proto": "tcp", "port": 3306, "bind": "0.0.0.0", "proc": "mysqld", "pid": 2},
    ]
    p1 = pb.assemble_core("d", s1, "t", "boot")
    p2 = pb.assemble_core("d", s2, "t", "boot")
    assert pb.compute_profile_hash(p1) != pb.compute_profile_hash(p2)


def test_discover_sections_degrades_without_crashing():
    # En Windows/sin herramientas Linux los probes degradan, no rompen.
    sections = pb.discover_sections()
    assert "degraded" in sections
    assert isinstance(sections["degraded"], list)
    assert "host" in sections
