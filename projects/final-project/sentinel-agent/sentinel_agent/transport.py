"""
Transporte MQTT hacia AWS IoT Core (mTLS) para el sensor genérico.

Cola de publicación + hilo publicador dedicado (publicar desde el callback
del SDK provoca publishTimeoutException). Los 4 topics se derivan de un
único device_id.

El import del SDK de AWS está protegido para poder importar este módulo en
entornos sin la librería (p. ej. la máquina de desarrollo en Windows); el SDK
solo se exige al instanciar el cliente.
"""

from __future__ import annotations

import json
import logging
import queue
import threading
from typing import Callable, Optional

logger = logging.getLogger("sentinel-agent")

try:
    from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient  # type: ignore
    _SDK_AVAILABLE = True
except Exception:  # noqa: BLE001
    AWSIoTMQTTClient = None  # type: ignore
    _SDK_AVAILABLE = False


class MqttTransport:
    """Cliente MQTT con cola de publicación thread-safe."""

    def __init__(self, device_id: str, endpoint: str, cert_path: str,
                 key_path: str, root_ca: str):
        if not _SDK_AVAILABLE:
            raise RuntimeError("AWSIoTPythonSDK no está instalado en este entorno")
        self.device_id = device_id
        self._client = AWSIoTMQTTClient(device_id, cleanSession=True)
        self._client.configureEndpoint(endpoint, 8883)
        self._client.configureCredentials(root_ca, key_path, cert_path)
        self._client.configureAutoReconnectBackoffTime(1, 32, 20)
        self._client.configureConnectDisconnectTimeout(30)
        self._client.configureMQTTOperationTimeout(10)
        self._pub_queue: "queue.Queue" = queue.Queue()
        self._stop = threading.Event()

    def connect(self) -> None:
        logger.info(f"[MQTT] Conectando como '{self.device_id}'...")
        self._client.connect()
        threading.Thread(target=self._publisher_loop, daemon=True, name="publicador").start()
        logger.info("[MQTT] Conectado.")

    def subscribe(self, topic: str, callback: Callable) -> None:
        self._client.subscribe(topic, 1, callback)
        logger.info(f"[MQTT] Suscrito a {topic}")

    def publish(self, topic: str, payload: dict) -> None:
        """Encola un mensaje (seguro desde cualquier hilo, incluido el del SDK)."""
        # Tras disconnect() (_stop seteado) no se encola nada: evita que un put()
        # tardío cuelgue _pub_queue.join() o intente publicar sobre un cliente ya
        # desconectado.
        if self._stop.is_set():
            return
        self._pub_queue.put((topic, json.dumps(payload, ensure_ascii=False)))

    def _publisher_loop(self) -> None:
        while not self._stop.is_set():
            try:
                topic, message = self._pub_queue.get(timeout=1.0)
            except queue.Empty:
                continue
            try:
                self._client.publish(topic, message, 1)
                logger.info(f"[MQTT] PUB {topic} -> {message[:160]}")
            except Exception as e:  # noqa: BLE001
                logger.error(f"[MQTT] Error publicando en {topic}: {e}")
            finally:
                self._pub_queue.task_done()

    def disconnect(self) -> None:
        self._stop.set()
        try:
            self._pub_queue.join()
            self._client.disconnect()
        except Exception:  # noqa: BLE001
            pass
