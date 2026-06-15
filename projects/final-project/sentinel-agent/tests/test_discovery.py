"""Tests de las funciones de parseo PURAS de los probes de discovery."""

from sentinel_agent.discovery import (
    caps_probe,
    firewall_probe,
    log_probe,
    os_probe,
    services_probe,
    stack_probe,
    surface_probe,
    users_probe,
)

# --- os_probe -------------------------------------------------------------

OS_RELEASE = '''PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
ID=debian
HOME_URL="https://www.debian.org/"
'''


def test_parse_os_release():
    out = os_probe.parse_os_release(OS_RELEASE)
    assert out["os_id"] == "debian"
    assert out["os_version"] == "12"
    assert out["pretty_name"] == "Debian GNU/Linux 12 (bookworm)"


def test_parse_os_release_empty():
    out = os_probe.parse_os_release(None)
    assert out["os_id"] == "unknown"


def test_detect_package_manager():
    assert os_probe.detect_package_manager(which=lambda n: "/usr/bin/apt-get" if n == "apt-get" else None) == "apt"
    assert os_probe.detect_package_manager(which=lambda n: "/usr/bin/dnf" if n == "dnf" else None) == "dnf"
    assert os_probe.detect_package_manager(which=lambda n: None) == "unknown"


# --- services_probe -------------------------------------------------------

SS_OUTPUT = '''LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=812,fd=3))
LISTEN 0      511          0.0.0.0:80         0.0.0.0:*    users:(("nginx",pid=900,fd=6))
LISTEN 0      128        127.0.0.1:3306       0.0.0.0:*    users:(("mysqld",pid=1001,fd=20))
LISTEN 0      128             [::]:22            [::]:*     users:(("sshd",pid=812,fd=4))
'''


def test_parse_ss_maps_port_to_process():
    listeners = services_probe.parse_ss(SS_OUTPUT, "tcp")
    by_port = {l["port"]: l for l in listeners}
    assert by_port[22]["proc"] == "sshd"
    assert by_port[22]["pid"] == 812
    assert by_port[80]["proc"] == "nginx"
    assert by_port[80]["exposed"] is True
    assert by_port[3306]["bind"] == "127.0.0.1"
    assert by_port[3306]["loopback"] is True
    assert by_port[3306]["exposed"] is False


def test_parse_ss_ipv6_bind_normalized():
    listeners = services_probe.parse_ss(SS_OUTPUT, "tcp")
    ipv6 = [l for l in listeners if l["bind"] == "::"]
    assert ipv6 and ipv6[0]["port"] == 22


def test_parse_ss_without_process_info():
    # Sin -p/sin root: no hay users:((...)).
    line = "LISTEN 0 128 0.0.0.0:443 0.0.0.0:*"
    listeners = services_probe.parse_ss(line, "tcp")
    assert listeners[0]["port"] == 443
    assert listeners[0]["proc"] is None


# --- stack_probe ----------------------------------------------------------

def test_classify_services_detects_web_db_ssh():
    services = services_probe.parse_ss(SS_OUTPUT, "tcp")
    stack = stack_probe.classify_services(services)
    assert stack["web_server"]["engine"] == "nginx"
    assert stack["db_engine"]["engine"] == "mysql"
    assert stack["ssh"]["engine"] == "openssh"
    assert stack["ftp"] is None


def test_parse_nginx_version_and_conf():
    v = "nginx version: nginx/1.22.1\nconfigure arguments: --prefix=/etc/nginx --conf-path=/etc/nginx/nginx.conf"
    assert stack_probe.parse_nginx_version(v) == "1.22.1"
    assert stack_probe.parse_nginx_conf_path(v) == "/etc/nginx/nginx.conf"


def test_parse_apache_version_and_conf():
    v = 'Server version: Apache/2.4.57 (Debian)\n -D SERVER_CONFIG_FILE="/etc/apache2/apache2.conf"'
    assert stack_probe.parse_apache_version(v) == "2.4.57"
    assert stack_probe.parse_apache_conf_path(v) == "/etc/apache2/apache2.conf"


# --- firewall_probe -------------------------------------------------------

def test_firewall_active_ufw():
    fw = firewall_probe.decide_active_manager(
        ufw_status="Status: active", firewalld_active=None, nft_ruleset=None,
        iptables_save=None, present={"ufw": True, "iptables": True})
    assert fw["active_manager"] == "ufw"
    assert fw["active"] is True


def test_firewall_active_nftables():
    fw = firewall_probe.decide_active_manager(
        ufw_status="Status: inactive", firewalld_active=None,
        nft_ruleset="table inet filter {\n chain input { type filter hook input }\n}",
        iptables_save=None, present={"nft": True})
    assert fw["active_manager"] == "nftables"


def test_firewall_active_iptables_nft_backend():
    fw = firewall_probe.decide_active_manager(
        ufw_status=None, firewalld_active=None, nft_ruleset=None,
        iptables_save="*filter\n-A INPUT -s 1.2.3.4 -j DROP\nCOMMIT",
        present={"iptables": True, "nft": True})
    assert fw["active_manager"] == "iptables"
    assert fw["backend"] == "iptables-nft"


def test_firewall_none():
    fw = firewall_probe.decide_active_manager(None, None, None, None, present={})
    assert fw["active_manager"] == "none"
    assert fw["active"] is False


# --- caps_probe -----------------------------------------------------------

def test_detect_tools_presence():
    present = {"restic", "mysql", "nft"}
    caps = caps_probe.detect_tools(which=lambda b: "/usr/bin/x" if b in present else None)
    assert caps["restic"] is True
    assert caps["mysql"] is True
    assert caps["nftables"] is True  # alias de 'nft'
    assert caps["docker"] is False


# --- users_probe ----------------------------------------------------------

def test_parse_getent_group():
    text = "sudo:x:27:admin,daniel"
    assert users_probe.parse_getent_group(text, "sudo") == ["admin", "daniel"]


def test_parse_getent_group_missing():
    assert users_probe.parse_getent_group(None, "sudo") == []
    assert users_probe.parse_getent_group("wheel:x:10:", "sudo") == []


# --- log_probe ------------------------------------------------------------

def test_build_log_sources_for_nginx_ssh():
    stack = {"ssh": {"engine": "openssh", "port": 22},
             "web_server": {"engine": "nginx"}, "ftp": None, "db_engine": None}
    sources = log_probe.build_log_sources(stack)
    by_id = {s["id"]: s for s in sources}
    assert by_id["ssh"]["source"] == "journald"
    assert by_id["ssh"]["parser"] == "sshd_auth"
    assert by_id["web_access"]["parser"] == "nginx_access"
    assert by_id["web_access"]["path"] == "/var/log/nginx/access.log"
    assert "sqli" in by_id["web_access"]["detectors"]


def test_parse_nginx_access_log_directive():
    conf = "http {\n  access_log /var/log/nginx/custom.log combined;\n}"
    assert log_probe.parse_nginx_access_log(conf) == "/var/log/nginx/custom.log"
    assert log_probe.parse_nginx_access_log("access_log off;") is None


# --- surface_probe --------------------------------------------------------

def test_build_surface_classifies_exposure():
    services = services_probe.parse_ss(SS_OUTPUT, "tcp")
    surface = surface_probe.build_surface(services)
    assert 22 in surface["exposed_ports"]
    assert 80 in surface["exposed_ports"]
    assert 3306 in surface["loopback_only"]
    assert surface["internet_facing"] is True
