"""
Orquestador del sensor genérico: discovery al arranque, publicación del perfil,
monitorización de logs (tailers + parsers + detectores) y ejecución de comandos
firmados. Reemplaza al monolito agente_monitor3.py.

Fase 3 (perfil vivo): el re-descubrimiento periódico/on-demand republica el
perfil solo si cambia, y si cambia QUÉ se vigila (log_sources) reinicia de forma
controlada el conjunto de tailers — sin tocar la conexión MQTT ni el handler de
comandos. Ver docs/diseno_agente_discovery.md §12 (Fase 3).
"""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import threading
import time
from collections import deque
from typing import Iterator, Optional

from . import config as cfg_mod
from . import profile_builder, signing, state
from . import executor as exec_mod
from .detectors import DetectorEngine
from .parsers import get_parser
from .transport import MqttTransport

logger = logging.getLogger("sentinel-agent")


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log_sources_signature(profile: dict) -> str:
    """
    Huella de QUÉ se vigila. Proyecta solo (id, source, path, unit, parser) de
    cada log_source y los ordena: reordenar la lista NO cambia la firma, y un
    cambio que NO toque log_sources (p. ej. solo firewall) la deja idéntica.
    """
    srcs = profile.get("log_sources") or []
    norm = sorted(
        (str(s.get("id", "")), str(s.get("source", "")), str(s.get("path") or ""),
         str(s.get("unit") or ""), str(s.get("parser", "")))
        for s in srcs
    )
    blob = json.dumps(norm, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def tail_file(path: str, stop: threading.Event, from_end: bool = True) -> Iterator[str]:
    """Generador de líneas nuevas de un fichero (estilo `tail -f`)."""
    try:
        f = open(path, "r", encoding="utf-8", errors="replace")
    except OSError as e:
        logger.error(f"[TAIL] No se pudo abrir {path}: {e}")
        return
    with f:
        if from_end:
            f.seek(0, 2)
        while not stop.is_set():
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line.rstrip("\n")


def tail_journal(unit: str, stop: threading.Event, on_proc=None) -> Iterator[str]:
    """
    Generador de mensajes de journald para una unit (journalctl -f -o json).

    `on_proc(proc)` registra el Popen para que el orquestador pueda matarlo en
    un restart: readline() es bloqueante y no ve el stop hasta que el pipe se
    cierra, así que sin terminate() el subprocess quedaría huérfano.
    """
    proc = subprocess.Popen(
        ["journalctl", "-u", unit, "-f", "-n", "0", "-o", "json"],
        stdout=subprocess.PIPE, text=True,
    )
    if on_proc:
        on_proc(proc)
    try:
        while not stop.is_set():
            line = proc.stdout.readline()
            if not line:
                break
            try:
                msg = json.loads(line).get("MESSAGE", "")
            except ValueError:
                msg = line
            if msg:
                yield msg
    finally:
        proc.terminate()


class Monitor:
    def __init__(self, config: dict):
        self.cfg = config
        self.device_id = config["device_id"]
        self.topics = cfg_mod.topics_for(self.device_id)
        self.detectors = DetectorEngine(config.get("detectors") or {})
        self.transport: Optional[MqttTransport] = None
        self._stop = threading.Event()                      # stop del MONITOR ENTERO
        self._run_as = (config.get("executor") or {}).get("run_as")

        # --- Fase 3: generación de tailers + restart controlado ---
        self._tailers_stop = threading.Event()              # stop de la GENERACIÓN actual
        self._tailer_threads: list = []                     # hilos de la generación actual
        self._tailer_procs: list = []                       # Popen (journalctl) de la generación actual
        self._active_log_sources_sig: Optional[str] = None  # firma de lo que se vigila
        self._discovery_lock = threading.Lock()             # serializa boot/periodic/on_demand
        _disc = self.cfg.get("discovery") or {}
        self._tailer_join_timeout = _disc.get("tailer_join_timeout", 3.0)
        self._restart_min_interval = _disc.get("restart_min_interval", 120.0)
        self._restart_cap_per_hour = _disc.get("restart_cap_per_hour", 6)
        self._restart_history: deque = deque(maxlen=64)     # time.monotonic() de cada restart

    # --- arranque ---------------------------------------------------------
    def run(self) -> None:
        _sig = self.cfg["signing"]
        signing.load_public_keys([_sig["public_key_path"], _sig.get("next_public_key_path")])
        aws = self.cfg["aws"]
        self.transport = MqttTransport(
            self.device_id, aws["endpoint"], aws["cert_path"], aws["key_path"], aws["root_ca"])
        self.transport.connect()
        self.transport.subscribe(self.topics["comando"], self._on_command)

        # boot arranca los tailers DENTRO de _discover_and_publish (bajo el lock),
        # para que un 'redescubrir' temprano no cree una generación duplicada.
        self._discover_and_publish(trigger="boot")

        interval = (self.cfg.get("discovery") or {}).get("rediscovery_interval", 0)
        if interval and 0 < interval < 60:
            logger.warning(f"[MONITOR] rediscovery_interval={interval}s es bajo; "
                           f"recomendado 300-900s (coste de subprocess por ciclo).")
        if interval and interval > 0:
            threading.Thread(target=self._rediscovery_loop, args=(interval,),
                             daemon=True, name="rediscovery").start()

        logger.info(f"[MONITOR] Sensor '{self.device_id}' activo.")
        try:
            while not self._stop.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("[MONITOR] Detenido por el usuario.")
        finally:
            self._stop.set()            # detiene el rediscovery y marca shutdown global
            self._tailers_stop.set()    # corta la generación viva antes de soltar MQTT
            if self.transport:
                self.transport.disconnect()

    # --- discovery --------------------------------------------------------
    def _discover_and_publish(self, trigger: str) -> Optional[dict]:
        # Shutdown en curso: no descubrir ni reiniciar tailers (evita revivir una
        # generación tras run() haber cortado la conexión MQTT).
        if self._stop.is_set():
            return None
        # boot adquiere BLOQUEANTE (no puede perderse el arranque); periodic y
        # on_demand adquieren NO bloqueante: si coinciden, el segundo se descarta
        # idempotentemente (nunca dos generaciones de tailers a la vez).
        blocking = (trigger == "boot")
        if not self._discovery_lock.acquire(blocking=blocking):
            logger.info(f"[MONITOR] Re-descubrimiento '{trigger}' descartado: otro ciclo en curso.")
            return None
        try:
            sections = profile_builder.discover_sections()
            profile = profile_builder.assemble_core(self.device_id, sections, _now_iso(), trigger)
            prev_hash, prev_version = state.load_state(self.cfg["state_path"])
            profile, changed = profile_builder.finalize(profile, prev_hash, prev_version)
            if changed or trigger == "boot":
                self.transport.publish(self.topics["perfil"], profile)
                state.save_state(self.cfg["state_path"], profile["profile_hash"], profile["profile_version"])
                logger.info(f"[MONITOR] Perfil publicado (v{profile['profile_version']}, "
                            f"{'cambió' if changed else 'sin cambios'}).")
            else:
                logger.info("[MONITOR] Perfil sin cambios; no se republica.")

            # Tailers (todo bajo el lock): en boot arranca la generación inicial;
            # en periodic/on_demand reinicia solo si cambió log_sources.
            if trigger == "boot":
                self._start_tailers(profile)
            else:
                new_sig = log_sources_signature(profile)
                if new_sig != self._active_log_sources_sig:
                    if self._restart_allowed():
                        self._restart_tailers(profile)
                else:
                    logger.debug("[MONITOR] log_sources sin cambios; tailers intactos.")
            return profile
        finally:
            self._discovery_lock.release()

    def _rediscovery_loop(self, interval: int) -> None:
        while not self._stop.wait(interval):
            try:
                self._discover_and_publish(trigger="periodic")
            except Exception as e:  # noqa: BLE001
                logger.error(f"[MONITOR] Error en re-descubrimiento: {e}")

    # --- restart controlado de tailers ------------------------------------
    def _restart_allowed(self) -> bool:
        """Debounce + cap por hora para no parpadear ante flapping de servicios."""
        now = time.monotonic()
        hist = self._restart_history
        while hist and now - hist[0] > 3600.0:
            hist.popleft()
        if hist and now - hist[-1] < self._restart_min_interval:
            logger.info(f"[MONITOR] Restart de tailers suprimido por debounce "
                        f"(<{self._restart_min_interval}s); se conserva el set vigente.")
            return False
        if len(hist) >= self._restart_cap_per_hour:
            logger.warning(f"[MONITOR] Cap de restarts/hora alcanzado "
                           f"({self._restart_cap_per_hour}); se conserva el set vigente. "
                           f"PI-5 puede quedar desincronizado hasta el próximo ciclo.")
            return False
        return True

    def _stop_tailers(self) -> None:
        old_stop = self._tailers_stop
        old_threads = self._tailer_threads
        old_procs = self._tailer_procs
        old_stop.set()
        # Matar los journalctl de esta generación: su readline() está bloqueado y
        # no ve el stop hasta que el pipe se cierra. terminate() cierra el pipe ->
        # readline() retorna '' -> el generador hace break y su finally limpia.
        for p in old_procs:
            try:
                p.terminate()
            except Exception:  # noqa: BLE001
                pass
        for t in old_threads:
            t.join(timeout=self._tailer_join_timeout)
            if t.is_alive():
                logger.warning(f"[MONITOR] tailer {t.name} no terminó en "
                               f"{self._tailer_join_timeout}s; queda como daemon huérfano.")
        self._tailer_threads = []
        self._tailer_procs = []
        self._tailers_stop = threading.Event()   # Event LIMPIO para la próxima generación

    def _restart_tailers(self, profile: dict) -> None:
        n_old = len(self._tailer_threads)
        n_new = len(profile.get("log_sources", []))
        logger.info(f"[MONITOR] log_sources cambió; reiniciando tailers ({n_old} -> {n_new}).")
        self._stop_tailers()
        self._start_tailers(profile)
        self._restart_history.append(time.monotonic())
        logger.info("[MONITOR] Tailers reiniciados.")

    # --- monitorización ---------------------------------------------------
    def _start_tailers(self, profile: dict) -> None:
        self._tailer_threads = []
        self._tailer_procs = []
        for src in profile.get("log_sources", []):
            t = threading.Thread(target=self._tail_source, args=(src,),
                                 daemon=True, name=f"tail:{src.get('id')}")
            t.start()
            self._tailer_threads.append(t)
        self._active_log_sources_sig = log_sources_signature(profile)

    def _tail_source(self, src: dict) -> None:
        # Snapshot del Event de ESTA generación: cuando _restart_tailers reasigna
        # self._tailers_stop a un Event nuevo, los hilos viejos siguen mirando el
        # suyo (ya seteado) y terminan; el nuevo no los "revive".
        stop = self._tailers_stop
        parser = get_parser(src.get("parser", ""))
        if parser is None:
            logger.warning(f"[MONITOR] Sin parser para {src.get('id')} ({src.get('parser')})")
            return
        if src.get("source") == "journald" and src.get("unit"):
            lines = tail_journal(src["unit"], stop, on_proc=self._tailer_procs.append)
        elif src.get("path"):
            lines = tail_file(src["path"], stop)
        else:
            logger.warning(f"[MONITOR] Fuente de log sin path/unit: {src.get('id')}")
            return
        for line in lines:
            if stop.is_set():    # corte adicional por si el parser bloquea entre líneas
                break
            try:
                obs = parser(line)
                if not obs:
                    continue
                for event in self.detectors.evaluate(obs, time.time(), self.device_id):
                    self._publish_event(event)
            except Exception as e:  # noqa: BLE001
                logger.error(f"[MONITOR] Error procesando línea de {src.get('id')}: {e}")

    def _publish_event(self, event: dict) -> None:
        if self._stop.is_set():    # no publicar durante/después del shutdown
            return
        payload = {"timestamp": _now_iso(), "sensor": self.device_id, **event}
        self.transport.publish(self.topics["evento"], payload)

    # --- comandos firmados ------------------------------------------------
    def _on_command(self, client, userdata, message) -> None:
        try:
            payload = json.loads(message.payload if isinstance(message.payload, str)
                                 else message.payload.decode("utf-8"))
        except Exception:  # noqa: BLE001
            logger.error("[MONITOR] Payload de comando ilegible.")
            return
        if not isinstance(payload, dict):
            return

        accion = payload.get("accion") or payload.get("action", "")
        # Acción especial: re-descubrir bajo demanda (firmada).
        if accion == "redescubrir":
            ok, motivo = signing.verify_payload(payload)
            if ok:
                logger.info("[MONITOR] Re-descubrimiento on-demand solicitado.")
                try:
                    self._discover_and_publish(trigger="on_demand")
                except Exception as e:  # noqa: BLE001 — no tumbar el hilo de red de paho
                    logger.error(f"[MONITOR] Error en re-descubrimiento on-demand: {e}")
            else:
                logger.error(f"[MONITOR] redescubrir rechazado por firma: {motivo}")
            return

        resp = exec_mod.process_command(payload, self.device_id, run_as=self._run_as)
        self.transport.publish(self.topics["respuesta"], resp)
