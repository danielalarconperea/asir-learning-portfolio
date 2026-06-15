"""
Tests del endpoint HITL critico /api/mitigate/approve y de los gates de
seguridad del dashboard (/revert CRITICAL, autenticacion fail-closed).

Era la logica mas sensible del sistema sin ningun test: re-clasificacion del
comando editado por el humano, bloqueo de CRITICAL sin confirm_critical,
publish firmado con wait_for_ack y correlacion log_id comando<->respuesta.
"""
import os
import sys
import sqlite3
import tempfile
import unittest
import base64
import types
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock AWSMqttClient before importing dashboard_soc to avoid AWS connection attempts
sys.modules.setdefault('awscrt', types.SimpleNamespace(io=MagicMock(), mqtt=MagicMock()))
sys.modules.setdefault('awsiot', types.SimpleNamespace(mqtt_connection_builder=MagicMock()))
import aws_connector
aws_connector.AWSMqttClient = MagicMock()

os.environ['DASHBOARD_USER'] = 'admin'
os.environ['DASHBOARD_PASSWORD'] = 'testpass'

import dashboard_soc
from dashboard_soc import app
from database import init_schema


class FakeMqttClient:
    def __init__(self):
        self.published = []

    def is_alive(self):
        return True

    def publish(self, topic, payload, wait_for_ack=False):
        self.published.append((topic, payload, wait_for_ack))


def create_temp_db_with_pending_row(command, status='PENDING'):
    """BD temporal con el esquema REAL (database.init_schema) y una fila."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    tmp.close()
    init_schema(tmp.name)
    conn = sqlite3.connect(tmp.name)
    conn.execute(
        '''
        INSERT INTO logs (
            dispositivo, servicio, log_original, ip_origen, nivel_gravedad,
            veredicto_ia, accion_tomada, status, pending_command, rationale
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            'Pi4-Felix', 'SSH', '{}', '1.2.3.4', 'Alta',
            'Ataque', 'Requiere Revision', status, command, 'test',
        ),
    )
    conn.commit()
    conn.close()
    return tmp.name


class TestApproveEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        auth_string = "admin:testpass"
        self.auth_headers = {
            'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        }
        self.mqtt = FakeMqttClient()
        dashboard_soc.mqtt_client = self.mqtt

    def tearDown(self):
        dashboard_soc.mqtt_client = None

    def _post_approve(self, db_path, body):
        with patch('dashboard_soc.DB_PATH', db_path), \
             patch('dashboard_soc.get_mqtt_client', return_value=self.mqtt), \
             patch('dashboard_soc.signing.sign_payload', side_effect=lambda payload: payload), \
             patch('dashboard_soc.policy_engine.audit'):
            return self.client.post(
                '/api/mitigate/approve', json=body, headers=self.auth_headers
            )

    def test_approve_low_dispatches_signed_command_with_log_id(self):
        command = 'sudo iptables -A INPUT -s 1.2.3.4 -j DROP'
        db_path = create_temp_db_with_pending_row(command)
        try:
            response = self._post_approve(db_path, {
                'log_id': 1, 'action': 'approve', 'final_command': command,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['status'], 'dispatching')

            # Publish firmado con wait_for_ack y correlacion log_id
            self.assertEqual(len(self.mqtt.published), 1)
            topic, payload, wait_for_ack = self.mqtt.published[0]
            self.assertTrue(wait_for_ack)
            self.assertEqual(payload['comando'], command)
            self.assertEqual(payload['log_id'], 1)

            conn = sqlite3.connect(db_path)
            row = conn.execute(
                'SELECT status, estado_mitigacion FROM logs WHERE id = 1'
            ).fetchone()
            conn.close()
            self.assertEqual(row[0], 'APPROVED')
            self.assertIsNone(row[1])  # reseteado: esperando round-trip
        finally:
            os.unlink(db_path)

    def test_approve_critical_without_confirmation_is_blocked(self):
        command = 'sudo rm -rf /var/www/html'
        db_path = create_temp_db_with_pending_row(command)
        try:
            response = self._post_approve(db_path, {
                'log_id': 1, 'action': 'approve', 'final_command': command,
            })
            self.assertEqual(response.status_code, 400)
            body = response.get_json()
            self.assertEqual(body['status'], 'needs_confirmation')
            self.assertEqual(body['risk_level'], 'CRITICAL')
            self.assertEqual(self.mqtt.published, [])  # nada salio al sensor

            conn = sqlite3.connect(db_path)
            status = conn.execute('SELECT status FROM logs WHERE id = 1').fetchone()[0]
            conn.close()
            self.assertEqual(status, 'PENDING')  # la fila no cambia
        finally:
            os.unlink(db_path)

    def test_approve_critical_with_confirmation_dispatches(self):
        command = 'sudo rm -rf /var/www/html'
        db_path = create_temp_db_with_pending_row(command)
        try:
            response = self._post_approve(db_path, {
                'log_id': 1, 'action': 'approve', 'final_command': command,
                'confirm_critical': True,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['status'], 'dispatching')
            self.assertEqual(len(self.mqtt.published), 1)
        finally:
            os.unlink(db_path)

    def test_reject_marks_row_without_publishing(self):
        command = 'sudo iptables -A INPUT -s 1.2.3.4 -j DROP'
        db_path = create_temp_db_with_pending_row(command)
        try:
            response = self._post_approve(db_path, {
                'log_id': 1, 'action': 'reject', 'final_command': command,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['status'], 'success')
            self.assertEqual(self.mqtt.published, [])

            conn = sqlite3.connect(db_path)
            status = conn.execute('SELECT status FROM logs WHERE id = 1').fetchone()[0]
            conn.close()
            self.assertEqual(status, 'REJECTED')
        finally:
            os.unlink(db_path)

    def test_approve_missing_parameters_is_400(self):
        db_path = create_temp_db_with_pending_row('ls')
        try:
            response = self._post_approve(db_path, {'action': 'approve'})
            self.assertEqual(response.status_code, 400)
        finally:
            os.unlink(db_path)


class TestRevertCriticalGate(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        auth_string = "admin:testpass"
        self.auth_headers = {
            'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        }
        self.mqtt = FakeMqttClient()
        dashboard_soc.mqtt_client = self.mqtt

    def tearDown(self):
        dashboard_soc.mqtt_client = None

    def _post_revert(self, db_path, body=None):
        with patch('dashboard_soc.DB_PATH', db_path), \
             patch('dashboard_soc.get_mqtt_client', return_value=self.mqtt), \
             patch('dashboard_soc.signing.sign_payload', side_effect=lambda payload: payload), \
             patch('dashboard_soc.policy_engine.audit'):
            if body is None:
                return self.client.post('/revert/1', headers=self.auth_headers)
            return self.client.post('/revert/1', json=body, headers=self.auth_headers)

    def test_critical_revert_without_confirmation_is_blocked(self):
        db_path = create_temp_db_with_pending_row(
            'sudo iptables -A INPUT -s 1.2.3.4 -j DROP', status='APPROVED'
        )
        try:
            response = self._post_revert(db_path, {'command': 'sudo rm -rf /tmp/backup'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()['status'], 'needs_confirmation')
            self.assertEqual(self.mqtt.published, [])
        finally:
            os.unlink(db_path)

    def test_critical_revert_with_confirmation_dispatches(self):
        db_path = create_temp_db_with_pending_row(
            'sudo iptables -A INPUT -s 1.2.3.4 -j DROP', status='APPROVED'
        )
        try:
            response = self._post_revert(db_path, {
                'command': 'sudo rm -rf /tmp/backup', 'confirm_critical': True,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(self.mqtt.published), 1)
        finally:
            os.unlink(db_path)

    def test_revert_payload_includes_log_id(self):
        db_path = create_temp_db_with_pending_row(
            'sudo iptables -A INPUT -s 1.2.3.4 -j DROP', status='APPROVED'
        )
        try:
            response = self._post_revert(db_path)
            self.assertEqual(response.status_code, 200)
            _, payload, _ = self.mqtt.published[0]
            self.assertEqual(payload['log_id'], 1)
        finally:
            os.unlink(db_path)


class TestFailClosedAuth(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_no_credentials_configured_denies_everything(self):
        auth_string = "admin:whatever"
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        }
        with patch.object(dashboard_soc, '_AUTH_PASS_HASH', ''):
            response = self.client.get('/api/data', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_wrong_password_is_rejected(self):
        auth_string = "admin:wrongpass"
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        }
        response = self.client.get('/api/data', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_no_auth_header_is_rejected(self):
        response = self.client.get('/api/data')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
