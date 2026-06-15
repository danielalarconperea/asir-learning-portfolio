"""Tests de los parsers de log (línea -> observación normalizada)."""

from sentinel_agent import parsers


def test_sshd_failed_password():
    obs = parsers.sshd_auth("Mar 10 10:00:01 host sshd[812]: Failed password for root from 1.2.3.4 port 55012 ssh2")
    assert obs == {"kind": "ssh_auth_fail", "ip": "1.2.3.4", "user": "root"}


def test_sshd_invalid_user():
    obs = parsers.sshd_auth("Failed password for invalid user admin from 9.9.9.9 port 22 ssh2")
    assert obs["ip"] == "9.9.9.9"
    assert obs["user"] == "admin"


def test_sshd_accepted():
    obs = parsers.sshd_auth("Accepted publickey for daniel from 10.0.0.1 port 5000 ssh2")
    assert obs["kind"] == "ssh_login_ok"
    assert obs["ip"] == "10.0.0.1"


def test_sshd_no_match():
    assert parsers.sshd_auth("some unrelated log line") is None


def test_vsftpd_fail_login():
    obs = parsers.vsftpd('Mon Mar 10 [pi] FAIL LOGIN: Client "::ffff:192.168.1.50"')
    assert obs == {"kind": "ftp_auth_fail", "ip": "192.168.1.50", "user": "pi"}


def test_nginx_access_get():
    line = '203.0.113.5 - - [10/Mar/2026:10:00:00 +0000] "GET /admin?id=1 HTTP/1.1" 200 1024 "-" "curl/8"'
    obs = parsers.nginx_access(line)
    assert obs["kind"] == "web_request"
    assert obs["ip"] == "203.0.113.5"
    assert obs["method"] == "GET"
    assert obs["path"] == "/admin?id=1"
    assert obs["status"] == 200


def test_nginx_access_no_match():
    assert parsers.nginx_access("garbage") is None


def test_get_parser_registry():
    assert parsers.get_parser("sshd_auth") is parsers.sshd_auth
    assert parsers.get_parser("apache_access") is parsers.nginx_access
    assert parsers.get_parser("nope") is None
