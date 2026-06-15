"""Tests de los detectores (ventana deslizante + patrones)."""

from sentinel_agent.detectors import DetectorEngine, SlidingWindowCounter, match_patterns


def test_sliding_window_counts_within_window():
    c = SlidingWindowCounter(threshold=3, window_seconds=10)
    assert c.hit("ip", now=100) == 1
    assert c.hit("ip", now=101) == 2
    assert c.hit("ip", now=102) == 3


def test_sliding_window_evicts_old_hits():
    c = SlidingWindowCounter(threshold=3, window_seconds=10)
    c.hit("ip", now=100)
    c.hit("ip", now=101)
    # A los 115s, los hits de 100/101 ya salieron de la ventana de 10s.
    assert c.hit("ip", now=115) == 1


def test_exceeded_triggers_at_threshold():
    c = SlidingWindowCounter(threshold=2, window_seconds=60)
    assert c.exceeded("ip", now=1) is False
    assert c.exceeded("ip", now=2) is True


def test_match_patterns():
    assert match_patterns("/login?id=1 OR 1=1", ["OR 1=1"]) == "OR 1=1"
    assert match_patterns("/x?q=<script>", ["<script"]) == "<script"
    assert match_patterns("/normal", ["<script"]) is None


def test_engine_ssh_bruteforce():
    eng = DetectorEngine({"thresholds": {"ssh_fail": 3, "ssh_window": 60}})
    obs = {"kind": "ssh_auth_fail", "ip": "1.2.3.4", "user": "root"}
    assert eng.evaluate(obs, now=1, sensor="d") == []
    assert eng.evaluate(obs, now=2, sensor="d") == []
    events = eng.evaluate(obs, now=3, sensor="d")
    assert len(events) == 1
    assert events[0]["evento"] == "SSH_FUERZA_BRUTA"
    assert events[0]["ip"] == "1.2.3.4"


def test_engine_sqli_in_web_request():
    eng = DetectorEngine()
    obs = {"kind": "web_request", "ip": "9.9.9.9", "path": "/login?email=a' UNION SELECT 1", "status": 200}
    events = eng.evaluate(obs, now=1, sensor="d")
    kinds = {e["evento"] for e in events}
    assert "SQL_INJECTION" in kinds


def test_engine_xss_in_web_request():
    eng = DetectorEngine()
    obs = {"kind": "web_request", "ip": "9.9.9.9", "path": "/c?msg=<script>alert(1)</script>", "status": 200}
    events = eng.evaluate(obs, now=1, sensor="d")
    assert any(e["evento"] == "XSS_DETECTADO" for e in events)


def test_engine_benign_web_request_no_events():
    eng = DetectorEngine()
    obs = {"kind": "web_request", "ip": "9.9.9.9", "path": "/index.html", "status": 200}
    assert eng.evaluate(obs, now=1, sensor="d") == []
