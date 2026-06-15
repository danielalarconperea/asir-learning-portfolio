"""
Detectores declarativos: convierten observaciones (de los parsers) en eventos
de seguridad, con umbrales/ventanas configurables en vez de hardcodeados.

Dos familias:
  * Fuerza bruta: contador de ventana deslizante por IP (SSH/FTP/web).
  * Patrones de payload: SQLi/XSS por coincidencia de substrings en la URL.

Los eventos resultantes se publican a seguridad/<device>/evento con el shape
flexible que el triage de PI-5 ya sabe interpretar.
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List, Optional

# Patrones por defecto (configurables vía sentinel.local.yml).
DEFAULT_SQLI = ["UNION SELECT", "' OR ", "1=1", "-- -", "DROP TABLE", "INSERT INTO", "OR 1=1"]
DEFAULT_XSS = ["<script", "javascript:", "onerror=", "onload=", "<img", "%3Cscript"]


class SlidingWindowCounter:
    """
    Cuenta hits por clave en una ventana temporal deslizante. `now` se inyecta
    para que los tests sean deterministas (no depende del reloj real).
    """

    def __init__(self, threshold: int, window_seconds: float):
        self.threshold = threshold
        self.window = window_seconds
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)

    def hit(self, key: str, now: float) -> int:
        """Registra un hit y devuelve el conteo dentro de la ventana actual."""
        dq = self._hits[key]
        dq.append(now)
        cutoff = now - self.window
        while dq and dq[0] < cutoff:
            dq.popleft()
        return len(dq)

    def exceeded(self, key: str, now: float) -> bool:
        """Registra un hit y devuelve True si alcanza/supera el umbral."""
        return self.hit(key, now) >= self.threshold

    def reset(self, key: str) -> None:
        self._hits.pop(key, None)


def match_patterns(text: str, patterns: List[str]) -> Optional[str]:
    """Devuelve el primer patrón (case-insensitive) presente en text, o None."""
    if not text:
        return None
    upper = text.upper()
    for p in patterns:
        if p.upper() in upper:
            return p
    return None


class DetectorEngine:
    """
    Aplica detectores a las observaciones de los parsers según la config del
    log_source. Mantiene el estado de los contadores de fuerza bruta.
    """

    def __init__(self, config: Optional[dict] = None):
        config = config or {}
        thr = config.get("thresholds", {})
        self.ssh = SlidingWindowCounter(thr.get("ssh_fail", 5), thr.get("ssh_window", 60))
        self.ftp = SlidingWindowCounter(thr.get("ftp_fail", 10), thr.get("ftp_window", 30))
        self.web = SlidingWindowCounter(thr.get("web_fail", 20), thr.get("web_window", 60))
        self.sqli_patterns = config.get("sqli_patterns", DEFAULT_SQLI)
        self.xss_patterns = config.get("xss_patterns", DEFAULT_XSS)

    def evaluate(self, obs: dict, now: float, sensor: str) -> List[dict]:
        """
        Dada una observación, devuelve 0..N eventos de seguridad listos para
        publicar (cada uno con evento/ip/prioridad/sensor/timestamp lo añade el
        caller). Aquí se decide QUÉ es un ataque.
        """
        events: List[dict] = []
        kind = obs.get("kind")
        ip = obs.get("ip")

        if kind == "ssh_auth_fail" and ip:
            if self.ssh.exceeded(ip, now):
                self.ssh.reset(ip)
                events.append({"evento": "SSH_FUERZA_BRUTA", "ip": ip,
                               "prioridad": "ALTA", "usuario": obs.get("user")})

        elif kind == "ftp_auth_fail" and ip:
            if self.ftp.exceeded(ip, now):
                self.ftp.reset(ip)
                events.append({"evento": "FTP_FUERZA_BRUTA", "ip": ip,
                               "prioridad": "ALTA", "usuario": obs.get("user")})

        elif kind == "web_request" and ip:
            path = obs.get("path", "")
            sqli = match_patterns(path, self.sqli_patterns)
            if sqli:
                events.append({"evento": "SQL_INJECTION", "ip": ip, "prioridad": "ALTA",
                               "patron": sqli, "ruta": path})
            xss = match_patterns(path, self.xss_patterns)
            if xss:
                events.append({"evento": "XSS_DETECTADO", "ip": ip, "prioridad": "ALTA",
                               "patron": xss, "ruta": path})
            if obs.get("status") in (401, 403) and self.web.exceeded(ip, now):
                self.web.reset(ip)
                events.append({"evento": "WEB_FUERZA_BRUTA", "ip": ip, "prioridad": "MEDIA"})

        return events
