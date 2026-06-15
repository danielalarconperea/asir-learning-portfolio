"""Tests del executor: denylist local + verificación + eco de log_id."""

from sentinel_agent import executor


# --- denylist pura --------------------------------------------------------

def test_denylist_blocks_rm():
    denied, verbs = executor.is_denied("sudo rm -rf /var/www")
    assert denied is True
    assert "rm" in verbs


def test_denylist_blocks_chained_destructive():
    denied, verbs = executor.is_denied("sudo iptables -L; shutdown -h now")
    assert denied is True
    assert "shutdown" in verbs


def test_denylist_blocks_absolute_path_binary():
    denied, verbs = executor.is_denied("/sbin/mkfs.ext4 /dev/sda1")
    assert denied is True
    assert "mkfs" in verbs


def test_denylist_allows_legit_mitigation():
    assert executor.is_denied("sudo iptables -A INPUT -s 1.2.3.4 -j DROP")[0] is False
    assert executor.is_denied("sudo systemctl restart nginx")[0] is False
    assert executor.is_denied("sudo nft add rule inet filter input ip saddr 1.2.3.4 drop")[0] is False


def test_denylist_ignores_quoted_text():
    # 'rm' dentro de comillas (p. ej. un grep) no debe bloquear.
    assert executor.is_denied("grep 'please rm this' /var/log/app.log")[0] is False


# --- process_command (con verify/runner inyectados) -----------------------

def _ok_verify(payload):
    return True, ""


def _fake_runner(command, run_as=None):
    return {"exitcode": 0, "stdout": f"ran: {command}", "stderr": "", "timed_out": False}


def test_process_valid_command_executes_and_echoes_log_id():
    payload = {"accion": "ejecutar_comando",
               "comando": "sudo iptables -A INPUT -s 1.2.3.4 -j DROP", "log_id": 42}
    resp = executor.process_command(payload, "web-prod-01", verify=_ok_verify,
                                    runner=_fake_runner, now_iso="2026-06-14T10:00:00Z")
    assert resp["sensor"] == "web-prod-01"
    assert resp["tipo"] == "RESULTADO_COMANDO"
    assert resp["log_id"] == 42                      # eco obligatorio
    assert resp["resultado"]["exitcode"] == 0
    assert "ran:" in resp["resultado"]["stdout"]
    assert "status" not in resp or resp.get("status") != "rejected_local_policy"


def test_process_rejects_bad_signature():
    payload = {"accion": "ejecutar_comando", "comando": "ls", "log_id": 7}
    resp = executor.process_command(payload, "d", verify=lambda p: (False, "firma Ed25519 inválida"),
                                    runner=_fake_runner)
    assert resp["status"] == "rejected_signature"
    assert resp["log_id"] == 7
    assert resp["resultado"]["exitcode"] == -1


def test_process_blocks_destructive_even_with_valid_signature():
    payload = {"accion": "ejecutar_comando", "comando": "rm -rf /var/www", "log_id": 9}
    resp = executor.process_command(payload, "d", verify=_ok_verify, runner=_fake_runner)
    assert resp["status"] == "rejected_local_policy"
    assert resp["log_id"] == 9
    assert "rm" in resp["resultado"]["error"]


def test_process_non_executable_action_ignored():
    payload = {"accion": "redescubrir", "log_id": None}
    resp = executor.process_command(payload, "d", verify=_ok_verify, runner=_fake_runner)
    assert resp["status"] == "ignored"
