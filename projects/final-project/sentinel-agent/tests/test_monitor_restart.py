"""
Tests del restart controlado de tailers (Fase 3): decisión de reinicio,
debounce/cap, reentrancia, conservación del estado de detectores y mecánica de
hilos (parar/relanzar generaciones sin perder el control).
"""
import threading
import time

import pytest

from sentinel_agent import monitor as mon


def _config():
    return {
        "device_id": "test-host",
        "detectors": {"thresholds": {"ssh_fail": 3, "ssh_window": 60}},
        "executor": {"run_as": None},
        "discovery": {"tailer_join_timeout": 2.0, "restart_min_interval": 100.0,
                      "restart_cap_per_hour": 6},
        "state_path": "ignored",
    }


class _FakeTransport:
    def __init__(self):
        self.published = []

    def publish(self, topic, payload):
        self.published.append((topic, payload))


def _monitor():
    m = mon.Monitor(_config())
    m.transport = _FakeTransport()
    return m


def _src(id, path):
    return {"id": id, "source": "file", "path": path, "unit": None, "parser": "sshd_auth"}


def _patch_discovery(monkeypatch, profile, changed=True):
    monkeypatch.setattr(mon.profile_builder, "discover_sections", lambda: {})
    monkeypatch.setattr(mon.profile_builder, "assemble_core", lambda *a: dict(profile))
    monkeypatch.setattr(mon.profile_builder, "finalize", lambda p, ph, pv: (dict(p), changed))
    monkeypatch.setattr(mon.state, "load_state", lambda path: (None, 0))
    monkeypatch.setattr(mon.state, "save_state", lambda *a, **k: None)


# --- decisión de restart ---------------------------------------------------

def test_restart_triggers_when_source_appears(monkeypatch, tmp_path):
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    m._active_log_sources_sig = mon.log_sources_signature({"log_sources": [_src("ssh", str(f))]})
    new_profile = {"log_sources": [_src("ssh", str(f)), _src("web", str(f))],
                   "profile_hash": "h2", "profile_version": 2}
    _patch_discovery(monkeypatch, new_profile)
    calls = []
    monkeypatch.setattr(m, "_restart_tailers", lambda p: calls.append(p))
    m._discover_and_publish("periodic")
    assert len(calls) == 1


def test_restart_not_triggered_when_only_firewall_changes(monkeypatch, tmp_path):
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    sources = [_src("ssh", str(f))]
    m._active_log_sources_sig = mon.log_sources_signature({"log_sources": sources})
    new_profile = {"log_sources": sources, "firewall": {"active_manager": "ufw"},
                   "profile_hash": "h2", "profile_version": 2}
    _patch_discovery(monkeypatch, new_profile)
    calls = []
    monkeypatch.setattr(m, "_restart_tailers", lambda p: calls.append(p))
    m._discover_and_publish("periodic")
    assert calls == []


def test_boot_starts_tailers_under_lock_not_restart(monkeypatch, tmp_path):
    # En boot, _discover_and_publish arranca la generación inicial (no restart)
    # y fija la firma — todo bajo el lock (corrección de la revisión).
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    new_profile = {"log_sources": [_src("ssh", str(f))], "profile_hash": "h", "profile_version": 1}
    _patch_discovery(monkeypatch, new_profile)
    restart_calls = []
    start_calls = []
    monkeypatch.setattr(m, "_restart_tailers", lambda p: restart_calls.append(p))
    real_start = m._start_tailers
    monkeypatch.setattr(m, "_start_tailers", lambda p: start_calls.append(p) or real_start(p))
    m._discover_and_publish("boot")
    assert restart_calls == []
    assert len(start_calls) == 1                  # boot arrancó tailers
    assert m._active_log_sources_sig is not None   # firma fijada antes de soltar el lock
    m._stop_tailers()


def test_shutdown_guard_blocks_rediscovery(monkeypatch):
    # Con _stop seteado (shutdown), _discover_and_publish no descubre ni reinicia.
    m = _monitor()
    seen = []
    monkeypatch.setattr(mon.profile_builder, "discover_sections", lambda: seen.append(1) or {})
    m._stop.set()
    assert m._discover_and_publish("on_demand") is None
    assert seen == []


def test_publish_event_noop_after_shutdown():
    m = _monitor()
    m._stop.set()
    m._publish_event({"evento": "X", "ip": "1.2.3.4"})
    assert m.transport.published == []     # nada se publica tras el shutdown


# --- debounce y cap --------------------------------------------------------

def test_debounce_suppresses_restart(monkeypatch):
    m = _monitor()
    t = [1000.0]
    monkeypatch.setattr(mon.time, "monotonic", lambda: t[0])
    m._restart_history.append(t[0])           # un restart reciente
    t[0] = 1050.0                              # 50s < restart_min_interval (100)
    assert m._restart_allowed() is False


def test_cap_per_hour(monkeypatch):
    m = _monitor()
    t = [1000.0]
    monkeypatch.setattr(mon.time, "monotonic", lambda: t[0])
    for i in range(6):
        m._restart_history.append(1000.0 + i)  # 6 restarts dentro de la hora
    t[0] = 1000.0 + 200                         # pasa el debounce pero no la hora
    assert m._restart_allowed() is False
    t[0] = 1000.0 + 4000                        # pasa 1h -> history se purga
    assert m._restart_allowed() is True


# --- reentrancia -----------------------------------------------------------

def test_lock_serializes_reentrancy(monkeypatch):
    m = _monitor()
    seen = []
    monkeypatch.setattr(mon.profile_builder, "discover_sections",
                        lambda: seen.append(1) or {})
    m._discovery_lock.acquire()   # simula un ciclo en curso
    try:
        result = m._discover_and_publish("periodic")   # acquire no bloqueante -> descarta
    finally:
        m._discovery_lock.release()
    assert result is None
    assert seen == []             # ni siquiera entró a descubrir


# --- detector state --------------------------------------------------------

def test_detector_state_conserved_on_restart(monkeypatch):
    m = _monitor()
    # umbral ssh_fail=3: dos fallos no disparan
    obs = {"kind": "ssh_auth_fail", "ip": "1.2.3.4", "user": "root"}
    assert m.detectors.evaluate(obs, now=1, sensor="d") == []
    assert m.detectors.evaluate(obs, now=2, sensor="d") == []
    m._restart_tailers({"log_sources": []})   # restart no debe resetear contadores
    events = m.detectors.evaluate(obs, now=3, sensor="d")
    assert any(e["evento"] == "SSH_FUERZA_BRUTA" for e in events)


# --- mecánica de hilos -----------------------------------------------------

def test_start_and_stop_tailers(tmp_path):
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    m._start_tailers({"log_sources": [_src("ssh", str(f))]})
    time.sleep(0.1)
    assert len(m._tailer_threads) == 1
    assert m._tailer_threads[0].is_alive()
    m._stop_tailers()
    assert m._tailer_threads == []


def test_snapshot_event_avoids_revive(tmp_path):
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    m._start_tailers({"log_sources": [_src("ssh", str(f))]})
    th = m._tailer_threads[0]
    old_stop = m._tailers_stop
    # Reasignar el Event sin setear el viejo NO debe matar al hilo de la gen vieja.
    m._tailers_stop = threading.Event()
    time.sleep(0.3)
    assert th.is_alive()
    old_stop.set()                # ahora sí debe terminar
    th.join(timeout=2.0)
    assert not th.is_alive()


class _FakeJournalProc:
    """Popen falso cuyo readline() bloquea hasta terminate() (simula journalctl -f sin tráfico)."""
    def __init__(self):
        self._ev = threading.Event()
        self.terminated = False
        self.stdout = self

    def readline(self):
        self._ev.wait()      # bloquea como journalctl sin líneas
        return ""            # EOF tras terminate

    def terminate(self):
        self.terminated = True
        self._ev.set()


def test_stop_tailers_terminates_blocked_journal_proc(monkeypatch):
    m = _monitor()
    fake = _FakeJournalProc()
    monkeypatch.setattr(mon.subprocess, "Popen", lambda *a, **k: fake)
    src = {"id": "ssh", "source": "journald", "unit": "ssh", "path": None, "parser": "sshd_auth"}
    m._start_tailers({"log_sources": [src]})
    time.sleep(0.15)
    th = m._tailer_threads[0]
    assert th.is_alive()              # bloqueado en readline
    assert fake in m._tailer_procs
    m._stop_tailers()
    assert fake.terminated            # se le hizo terminate() -> readline retorna
    th.join(timeout=2.0)
    assert not th.is_alive()          # el hilo terminó (no queda huérfano)
    assert m._tailer_procs == []


def test_restart_to_empty_log_sources(tmp_path):
    m = _monitor()
    f = tmp_path / "a.log"; f.write_text("")
    m._start_tailers({"log_sources": [_src("ssh", str(f))]})
    time.sleep(0.1)
    m._restart_tailers({"log_sources": []})
    assert m._tailer_threads == []
    assert m._active_log_sources_sig == mon.log_sources_signature({"log_sources": []})


# --- on_command ------------------------------------------------------------

class _Msg:
    def __init__(self, payload):
        self.payload = payload


def test_on_command_redescubrir_does_not_kill_thread_on_error(monkeypatch):
    m = _monitor()
    monkeypatch.setattr(mon.signing, "verify_payload", lambda p: (True, ""))
    monkeypatch.setattr(m, "_discover_and_publish",
                        lambda trigger: (_ for _ in ()).throw(RuntimeError("boom")))
    import json
    # No debe propagar la excepción (el hilo de paho sobrevive).
    m._on_command(None, None, _Msg(json.dumps({"accion": "redescubrir"}).encode()))


def test_on_command_redescubrir_bad_signature_does_nothing(monkeypatch):
    m = _monitor()
    monkeypatch.setattr(mon.signing, "verify_payload", lambda p: (False, "firma invalida"))
    calls = []
    monkeypatch.setattr(m, "_discover_and_publish", lambda trigger: calls.append(trigger))
    import json
    m._on_command(None, None, _Msg(json.dumps({"accion": "redescubrir"}).encode()))
    assert calls == []
