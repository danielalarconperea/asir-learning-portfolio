import json
import time
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

class AWSMqttClient:
    """
    Cliente para la gestion de conexiones MQTT con AWS IoT Core mediante mTLS.
    """
    def __init__(self, endpoint, cert_path, key_path, root_ca_path, client_id):
        self.endpoint = endpoint
        self.cert_path = cert_path
        self.key_path = key_path
        self.root_ca_path = root_ca_path
        self.client_id = client_id
        self.connection = None
        # Estado real de la conexion, mantenido por los callbacks del SDK.
        # awscrt reconecta solo, pero sin estos callbacks nadie se entera de
        # que la conexion cayo: is_alive() mentia y los publish fallaban en
        # silencio hasta el primer wait_for_ack.
        self._interrupted = False
        # topic -> callback, para re-suscribir si AWS no conserva la sesion.
        self._subscriptions = {}

    def _on_connection_interrupted(self, connection, error, **kwargs):
        self._interrupted = True
        print(f"[WARNING] Conexion MQTT [{self.client_id}] interrumpida: {error}")

    def _on_connection_resumed(self, connection, return_code, session_present, **kwargs):
        self._interrupted = False
        print(
            f"[INFO] Conexion MQTT [{self.client_id}] reanudada "
            f"(rc={return_code}, session_present={session_present})"
        )
        # Si el broker no conservo la sesion, las suscripciones se perdieron.
        if not session_present and self._subscriptions:
            print(f"[INFO] Sesion no conservada — re-suscribiendo {len(self._subscriptions)} topics...")
            for topic, callback in self._subscriptions.items():
                try:
                    connection.subscribe(
                        topic=topic,
                        qos=mqtt.QoS.AT_LEAST_ONCE,
                        callback=callback,
                    )
                except Exception as e:
                    print(f"[ERROR] Fallo re-suscribiendo a {topic}: {e}")

    def connect(self):
        """
        Establece la conexion segura con AWS IoT.
        """
        print(f"[INFO] Conectando cliente IoT: {self.client_id}")

        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            cert_filepath=self.cert_path,
            pri_key_filepath=self.key_path,
            ca_filepath=self.root_ca_path,
            client_id=self.client_id,
            clean_session=False,
            keep_alive_secs=30,
            on_connection_interrupted=self._on_connection_interrupted,
            on_connection_resumed=self._on_connection_resumed,
        )

        # Iniciar conexion asincrona
        connect_future = mqtt_connection.connect()
        connect_future.result()

        self.connection = mqtt_connection
        self._interrupted = False
        print(f"[SUCCESS] Cliente [{self.client_id}] conectado con exito.")

    def is_alive(self):
        """
        Comprueba si la conexion MQTT subyacente sigue viva.
        Devuelve False si no existe conexion, si el SDK notifico una
        interrupcion aun no reanudada, o si el handle nativo fue liberado.
        """
        if self.connection is None:
            return False
        if self._interrupted:
            return False
        try:
            # El SDK de awscrt expone _binding como handle nativo.
            # Si el handle es None la conexion ya fue liberada.
            binding = getattr(self.connection, '_binding', None)
            if binding is None:
                return False
            return True
        except Exception:
            return False

    def disconnect(self):
        """
        Desconecta limpiamente el cliente MQTT para permitir reconexion.
        """
        if self.connection is not None:
            try:
                disconnect_future = self.connection.disconnect()
                disconnect_future.result(timeout=3.0)
            except Exception:
                pass  # Best-effort: la conexion puede ya estar muerta
            finally:
                self.connection = None
                self._interrupted = False
                self._subscriptions = {}
        print(f"[INFO] Cliente [{self.client_id}] desconectado.")

    def publish(self, topic, payload_dict, wait_for_ack=False, ack_timeout=5.0):
        """
        Publica un mensaje en formato JSON al topic especificado.

        Por defecto el envio es asincrono (fire-and-forget): la llamada encola
        el publish en el event loop de awscrt y retorna inmediatamente. Esto
        es suficiente para el agente, que tolera un retraso de unos milisegundos.

        El dashboard HITL necesita la garantia opuesta: cuando el operador
        aprueba un comando, queremos confirmar antes de devolver el 200 al
        navegador que el broker ya tiene el PUBACK. Para ese caso se llama con
        wait_for_ack=True; el metodo bloquea hasta `ack_timeout` segundos
        esperando el resultado del future y propaga la excepcion si el broker
        rechaza el publish o si la conexion esta caida. Asi el endpoint puede
        devolver un error real al frontend en vez de un falso exito.
        """
        if not self.connection:
            print("[ERROR] No hay conexion activa.")
            if wait_for_ack:
                raise RuntimeError("MQTT connection not established")
            return

        if not self.is_alive():
            print("[ERROR] Conexion MQTT zombie detectada en publish.")
            self.connection = None
            if wait_for_ack:
                raise RuntimeError("MQTT connection is dead (zombie state)")
            return

        message_json = json.dumps(payload_dict)
        publish_future, _packet_id = self.connection.publish(
            topic=topic,
            payload=message_json,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )

        if wait_for_ack:
            try:
                publish_future.result(timeout=ack_timeout)
            except Exception as e:
                # Si el future falla, la conexion probablemente murio.
                # Limpiamos para que get_mqtt_client() fuerce reconexion.
                self.connection = None
                error_msg = str(e) if str(e).strip() else "PUBACK timeout or connection lost"
                raise RuntimeError(f"MQTT publish failed: {error_msg}") from e
            print(f"[INFO] Mensaje publicado y confirmado (PUBACK) en {topic}")
        else:
            print(f"[INFO] Mensaje publicado en {topic}")

    def subscribe(self, topic, callback_function):
        """
        Suscribe el cliente a un topic y asigna una funcion de callback.
        """
        if not self.connection:
            print("[ERROR] Sin conexion para suscribir.")
            return

        subscribe_future, packet_id = self.connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=callback_function
        )
        subscribe_future.result()
        # Recordar la suscripcion para reponerla si AWS pierde la sesion.
        self._subscriptions[topic] = callback_function
        print(f"[INFO] Suscrito a: {topic}")

if __name__ == '__main__':
    # Validacion rapida de conectividad
    ENDPOINT = "aj4wsdnimoej8-ats.iot.eu-north-1.amazonaws.com"
    CLIENT_ID = "Pi5-dani-test"
    
    client = AWSMqttClient(
        endpoint=ENDPOINT,
        cert_path="./Pi5-dani.cert.pem", 
        key_path="./Pi5-dani.private.key", 
        root_ca_path="./root-CA.crt", 
        client_id=CLIENT_ID
    )
    
    try:
        client.connect()
        client.publish("seguridad/test", {"status": "ready", "timestamp": time.time()})
        time.sleep(2)
    except Exception as e:
        print(f"[ERROR] Error en la prueba de conexion: {e}")

