"""
Tests del routing y la resiliencia del coordinador (main_coordinator.py):

  * Via rapida del round-trip HITL: un feedback con log_id actualiza la fila
    exacta via mark_mitigation_result y marca registro_directo para que el
    feedback_agent no duplique el registro.
  * Backpressure real: con la cola llena el evento NO se pierde, se persiste
    en pending_ai_events y el retry worker lo reprocesa.

Se usa la misma tecnica de stubs que test_feedback_normalizer.py: cargar
main_coordinator.py con las dependencias pesadas (AWS, ADK) sustituidas.
"""

import asyncio
import importlib.util
import json
import os
import sys
import types

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COORDINATOR_PATH = os.path.join(REPO_ROOT, "PI-5", "src", "main_coordinator.py")


@pytest.fixture(scope="module")
def coordinator():
    stubs = {
        "aws_connector": types.SimpleNamespace(AWSMqttClient=object),
        "agents.triage_agent.triage_agent": types.SimpleNamespace(triage_agent=object()),
        "agents.feedback_agent.feedback_agent": types.SimpleNamespace(feedback_agent=object()),
        "tools.iot_tools": types.SimpleNamespace(init_iot_tools=lambda *a, **kw: None),
    }

    class _DummySession:
        id = "test-session"

    class _DummySessionService:
        def create_session(self, app_name, user_id):
            async def coro():
                return _DummySession()
            return coro()

    class _DummyRunner:
        def __init__(self, *a, **kw):
            pass

    stubs["google.adk.runners"] = types.SimpleNamespace(Runner=_DummyRunner)
    stubs["google.adk.sessions"] = types.SimpleNamespace(InMemorySessionService=_DummySessionService)
    stubs["google.genai"] = types.SimpleNamespace(types=types.SimpleNamespace(
        Content=lambda **kw: None, Part=lambda **kw: None,
    ))

    saved = {k: sys.modules.get(k) for k in stubs}
    sys.modules.update(stubs)

    src_dir = os.path.join(REPO_ROOT, "PI-5", "src")
    sys.path.insert(0, src_dir)

    cwd_saved = os.getcwd()
    os.chdir(os.path.join(REPO_ROOT, "PI-5"))
    try:
        spec = importlib.util.spec_from_file_location("main_coordinator_routing", COORDINATOR_PATH)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["main_coordinator_routing"] = mod
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd_saved)
        sys.path.remove(src_dir)
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v

    return mod


class _ImmediateLoop:
    """Falso event loop: ejecuta los callbacks de forma sincrona e inmediata."""

    def is_closed(self):
        return False

    def call_soon_threadsafe(self, fn, *args):
        fn(*args)

    def run_in_executor(self, _executor, fn):
        fn()


def _feedback_payload(log_id=None, exitcode=0):
    data = {
        "sensor": "Pi4-Felix",
        "tipo": "RESULTADO_COMANDO",
        "comando": "sudo iptables -A INPUT -s 1.2.3.4 -j DROP",
        "resultado": {"exitcode": exitcode, "stdout": "ok", "stderr": "fallo", "timed_out": False},
    }
    if log_id is not None:
        data["log_id"] = log_id
    return json.dumps(data).encode("utf-8")


# ---------------------------------------------------------------------------
# Via rapida del round-trip por log_id
# ---------------------------------------------------------------------------

def test_feedback_with_log_id_marks_exact_row(coordinator, monkeypatch):
    calls = []
    monkeypatch.setattr(
        coordinator, "mark_mitigation_result",
        lambda log_id, status, output: calls.append((log_id, status, output)) or {"status": "success"},
    )
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_feedback_queue", asyncio.Queue(maxsize=10))

    coordinator.process_event("seguridad/Pi4-Felix/respuesta", _feedback_payload(log_id=42))

    assert calls == [(42, "EXITO", "ok")]
    # El evento sigue llegando al feedback_agent, pero marcado para no duplicar
    device, raw_log = coordinator._feedback_queue.get_nowait()
    assert device == "Pi4-Felix"
    assert "registro_directo: true" in raw_log


def test_feedback_error_maps_to_fallo(coordinator, monkeypatch):
    calls = []
    monkeypatch.setattr(
        coordinator, "mark_mitigation_result",
        lambda log_id, status, output: calls.append((log_id, status, output)) or {"status": "success"},
    )
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_feedback_queue", asyncio.Queue(maxsize=10))

    coordinator.process_event("seguridad/Pi4-Felix/respuesta", _feedback_payload(log_id=7, exitcode=1))

    assert calls == [(7, "FALLO", "fallo")]


def test_feedback_without_log_id_uses_no_fast_path(coordinator, monkeypatch):
    calls = []
    monkeypatch.setattr(
        coordinator, "mark_mitigation_result",
        lambda *a: calls.append(a) or {"status": "success"},
    )
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_feedback_queue", asyncio.Queue(maxsize=10))

    coordinator.process_event("seguridad/Pi4-Felix/respuesta", _feedback_payload(log_id=None))

    assert calls == []
    device, raw_log = coordinator._feedback_queue.get_nowait()
    assert "registro_directo" not in raw_log


def test_telemetry_routes_to_triage_queue(coordinator, monkeypatch):
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_triage_queue", asyncio.Queue(maxsize=10))
    monkeypatch.setattr(coordinator, "_feedback_queue", asyncio.Queue(maxsize=10))

    payload = json.dumps({"sensor": "Pi4-Felix", "raw_log": "FAIL LOGIN from 1.2.3.4"}).encode()
    coordinator.process_event("seguridad/Pi4-Felix/evento", payload)

    assert coordinator._triage_queue.qsize() == 1
    assert coordinator._feedback_queue.qsize() == 0


def test_malformed_payload_does_not_crash(coordinator, monkeypatch):
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_triage_queue", asyncio.Queue(maxsize=10))
    # No debe lanzar excepcion aunque el JSON sea basura
    coordinator.process_event("seguridad/Pi4-Felix/evento", b"esto no es json {{{")


# ---------------------------------------------------------------------------
# Backpressure: cola llena -> spill a pending_ai_events (no se pierde nada)
# ---------------------------------------------------------------------------

def test_full_queue_spills_event_to_pending_ai_events(coordinator, monkeypatch):
    saved = []
    monkeypatch.setattr(
        coordinator, "save_pending_ai_event",
        lambda db_path, device, queue_type, raw_log, error_reason: saved.append(
            {"device": device, "queue_type": queue_type, "raw_log": raw_log, "error_reason": error_reason}
        ) or 1,
    )
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())

    full_queue = asyncio.Queue(maxsize=1)
    full_queue.put_nowait(("otro", "evento previo"))

    coordinator._put_or_spill(full_queue, "triage", "Pi4-Felix", "log de ataque")

    assert len(saved) == 1
    assert saved[0]["device"] == "Pi4-Felix"
    assert saved[0]["queue_type"] == "triage"
    assert saved[0]["raw_log"] == "log de ataque"
    assert "queue_full" in saved[0]["error_reason"]


def test_queue_with_room_enqueues_normally(coordinator, monkeypatch):
    saved = []
    monkeypatch.setattr(
        coordinator, "save_pending_ai_event",
        lambda *a, **kw: saved.append(1) or 1,
    )
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())

    queue = asyncio.Queue(maxsize=5)
    coordinator._put_or_spill(queue, "triage", "Pi4-Felix", "log normal")

    assert queue.qsize() == 1
    assert saved == []


# ---------------------------------------------------------------------------
# Ingesta del System Profile (agente Discovery)
# ---------------------------------------------------------------------------

def _profile_payload(device="web-prod-01", topic_suffix="perfil"):
    data = {"tipo": "PERFIL_SISTEMA", "sensor": device, "profile_version": 3,
            "profile_hash": "sha256:abc", "host": {"os_id": "debian"}}
    return json.dumps(data).encode("utf-8")


def test_profile_on_perfil_topic_is_persisted_not_enqueued(coordinator, monkeypatch):
    upserts = []
    monkeypatch.setattr(coordinator, "upsert_device_profile",
                        lambda device, profile, db_path: upserts.append((device, profile)) or {"changed": True})
    monkeypatch.setattr(coordinator.profile_context, "invalidate", lambda d: None)
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_triage_queue", asyncio.Queue(maxsize=10))
    monkeypatch.setattr(coordinator, "_feedback_queue", asyncio.Queue(maxsize=10))

    coordinator.process_event("seguridad/web-prod-01/perfil", _profile_payload())

    assert len(upserts) == 1
    assert upserts[0][0] == "web-prod-01"
    # NO se encola para el LLM
    assert coordinator._triage_queue.qsize() == 0
    assert coordinator._feedback_queue.qsize() == 0


def test_profile_as_telemetry_type_also_persisted(coordinator, monkeypatch):
    upserts = []
    monkeypatch.setattr(coordinator, "upsert_device_profile",
                        lambda device, profile, db_path: upserts.append(device) or {"changed": False})
    monkeypatch.setattr(coordinator.profile_context, "invalidate", lambda d: None)
    monkeypatch.setattr(coordinator, "_loop", _ImmediateLoop())
    monkeypatch.setattr(coordinator, "_triage_queue", asyncio.Queue(maxsize=10))

    # Llega por el topic de telemetria pero con tipo PERFIL_SISTEMA (fallback).
    coordinator.process_event("seguridad/web-prod-01/telemetria", _profile_payload())

    assert upserts == ["web-prod-01"]
    assert coordinator._triage_queue.qsize() == 0
