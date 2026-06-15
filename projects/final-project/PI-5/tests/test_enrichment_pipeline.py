"""Tests del pipeline de enriquecimiento (Fase 4): BD, end-to-end, promoción, aislamiento, auth."""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database import init_schema
from tools import db_tools, mitigation_manual
from tools import profile_enricher as pe


def _profile():
    return {
        "tipo": "PERFIL_SISTEMA", "schema_version": 1, "sensor": "enrichhost", "dispositivo": "enrichhost",
        "profile_hash": "sha256:abc", "profile_version": 3,
        "host": {"os_id": "debian", "pretty_name": "Debian 12", "arch": "aarch64"},
        "package_manager": "apt", "firewall": {"active_manager": "nftables"},
        "web_server": {"engine": "nginx", "config_paths": ["/etc/nginx/nginx.conf"],
                       "docroots": ["/var/www/html"], "listen_ports": [443]},
        "db_engine": {"engine": "mysql"},
        "services": [{"proc": "nginx", "port": 443}, {"proc": "mysqld", "port": 3306}],
        "log_sources": [{"id": "web_access", "service": "nginx", "source": "file",
                         "path": "/var/log/nginx/access.log", "parser": "nginx_access",
                         "detectors": ["sqli", "xss"]}],
        "capabilities": {"restic": False, "mysql": True, "fail2ban": True},
        "surface": {"exposed_ports": [443], "loopback_only": [3306]},
    }


def _enrichment_payload():
    return {
        "schema_version": 1, "device": "enrichhost", "based_on_profile_hash": "sha256:abc",
        "global_confidence": "medium",
        "host_notes": {"summary": "ok", "risks": []},
        "suggested_log_sources": [],
        "suggested_recommendation_overrides": [{
            "id": "taillog", "intent": "diagnostic", "severity": "baja", "requires": [],
            "applies_if": {"web_server.engine": "nginx"},
            "match": {"families": ["web_bruteforce"], "keywords": ["web", "acceso"]},
            "command": "sudo tail -n 100 /var/log/nginx/access.log", "revert": "",
            "placeholders": [], "explanation": "Ver accesos.", "confidence": "medium",
            "evidence": ["log_sources.id:web_access"]}],
    }


class TestEnrichmentDB(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.db'); tmp.close()
        self.db = tmp.name
        init_schema(self.db)
        db_tools.upsert_device_profile("enrichhost", _profile(), db_path=self.db)

    def tearDown(self):
        try:
            os.unlink(self.db)
        except OSError:
            pass

    def test_save_get_list_status(self):
        eid = db_tools.save_enrichment("enrichhost", "sha256:abc", 3, _enrichment_payload(), [],
                                       model_used="ollama/x", ai_mode="local", confidence="medium", db_path=self.db)
        got = db_tools.get_enrichment(eid, db_path=self.db)
        self.assertEqual(got["status"], "PENDING_REVIEW")
        self.assertEqual(got["ai_mode"], "local")
        self.assertEqual(len(db_tools.list_enrichments("enrichhost", "PENDING_REVIEW", db_path=self.db)), 1)
        db_tools.set_enrichment_status(eid, "DISCARDED", db_path=self.db)
        self.assertEqual(db_tools.get_enrichment(eid, db_path=self.db)["status"], "DISCARDED")

    def test_new_profile_supersedes_pending(self):
        db_tools.save_enrichment("enrichhost", "sha256:abc", 3, _enrichment_payload(), [], db_path=self.db)
        # nuevo perfil (hash distinto) -> el pendiente pasa a SUPERSEDED
        p2 = _profile(); p2["profile_hash"] = "sha256:NEW"; p2["profile_version"] = 4
        db_tools.upsert_device_profile("enrichhost", p2, db_path=self.db)
        rows = db_tools.list_enrichments("enrichhost", db_path=self.db)
        self.assertEqual(rows[0]["status"], "SUPERSEDED")

    def test_enrich_end_to_end_isolated(self):
        # LLM mockeado; modo local explícito.
        with patch.object(pe, "_raw_completion", lambda m, msg, **k: json.dumps(_enrichment_payload())), \
             patch.dict(os.environ, {"ENRICH_MODE": "local", "ENRICH_MODEL": "ollama/test"}):
            res = pe.enrich("enrichhost", db_path=self.db)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["counts"]["overrides"], 1)
        # el perfil determinista NO se tocó
        prof = db_tools.get_device_profile("enrichhost", db_path=self.db)
        self.assertEqual(prof["profile_hash"], "sha256:abc")
        # se guardó en device_enrichments
        self.assertEqual(len(db_tools.list_enrichments("enrichhost", "PENDING_REVIEW", db_path=self.db)), 1)

    def test_enrich_aborts_without_profile(self):
        res = pe.enrich("nohost", db_path=self.db)
        self.assertEqual(res["status"], "error")
        self.assertIn("perfil", res["reason"])


class TestPromotion(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.db'); tmp.close()
        self.db = tmp.name
        init_schema(self.db)
        db_tools.upsert_device_profile("enrichhost", _profile(), db_path=self.db)
        self.recs_dir = tempfile.mkdtemp()
        # cargar el módulo CLI por ruta
        spec = importlib.util.spec_from_file_location(
            "enrich_cli", os.path.join(os.path.dirname(__file__), "..", "scripts", "enrich_profile.py"))
        self.cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.cli)

    def tearDown(self):
        try:
            os.unlink(self.db)
        except OSError:
            pass

    def test_promote_writes_override_and_marks_promoted(self):
        eid = db_tools.save_enrichment("enrichhost", "sha256:abc", 3, _enrichment_payload(), [], db_path=self.db)
        with patch.object(mitigation_manual, "RECS_DIR", self.recs_dir):
            res = self.cli.promote_override("enrichhost", eid, db_path=self.db)
            self.assertEqual(res["status"], "success")
            path = os.path.join(self.recs_dir, "enrichhost.json")
            self.assertTrue(os.path.exists(path))
            doc = json.load(open(path, encoding="utf-8"))
            entry = doc["entries"][0]
            self.assertTrue(entry["id"].startswith("enrichhost-enrich-"))
            self.assertEqual(entry["source_enrichment"], eid)
            self.assertNotIn("confidence", entry)   # se limpian campos de enrichment
            # re-entra por el camino de Fase 2: _load_override lo devuelve
            mitigation_manual.clear_cache()
            loaded = mitigation_manual._load_override("enrichhost")
            self.assertTrue(any(e["id"] == entry["id"] for e in loaded))
        self.assertEqual(db_tools.get_enrichment(eid, db_path=self.db)["status"], "PROMOTED")

    def test_promote_rejects_interpreter_draft(self):
        # Defensa en profundidad: re-clasificación al promover rechaza un draft
        # con ejecución por intérprete aunque pasara el cross-check.
        payload = _enrichment_payload()
        payload["suggested_recommendation_overrides"][0]["command"] = 'sh -c "systemctl restart nginx"'
        eid = db_tools.save_enrichment("enrichhost", "sha256:abc", 3, payload, [], db_path=self.db)
        with patch.object(mitigation_manual, "RECS_DIR", self.recs_dir):
            res = self.cli.promote_override("enrichhost", eid, db_path=self.db)
        self.assertEqual(res["status"], "error")
        self.assertIn("re-clasificar", res["reason"])
        self.assertFalse(os.path.exists(os.path.join(self.recs_dir, "enrichhost.json")))

    def test_promote_blocked_when_profile_changed(self):
        eid = db_tools.save_enrichment("enrichhost", "sha256:OLD", 2, _enrichment_payload(), [], db_path=self.db)
        with patch.object(mitigation_manual, "RECS_DIR", self.recs_dir):
            res = self.cli.promote_override("enrichhost", eid, db_path=self.db)
        self.assertEqual(res["status"], "error")
        self.assertIn("stale", res["reason"].lower() + " " + res.get("reason", ""))
        self.assertFalse(os.path.exists(os.path.join(self.recs_dir, "enrichhost.json")))

    def test_promote_blocked_when_enrichment_hash_missing(self):
        # Regresión anti-stale (fail-closed): un enrichment guardado con
        # profile_hash=None NO debe poder promoverse cuando el inventario actual
        # SÍ tiene hash. Antes el guard se saltaba (gateado en truthiness del
        # hash del enrichment) y promovía a ciegas sobre el perfil vigente.
        eid = db_tools.save_enrichment("enrichhost", None, 3, _enrichment_payload(), [], db_path=self.db)
        with patch.object(mitigation_manual, "RECS_DIR", self.recs_dir):
            res = self.cli.promote_override("enrichhost", eid, db_path=self.db)
        self.assertEqual(res["status"], "error")
        self.assertIn("anti-stale", res["reason"].lower())
        self.assertFalse(os.path.exists(os.path.join(self.recs_dir, "enrichhost.json")))
        # el enrichment no se marcó PROMOTED: sigue pendiente de revisión.
        self.assertEqual(db_tools.get_enrichment(eid, db_path=self.db)["status"], "PENDING_REVIEW")


class TestEnrichEndpointsAuth(unittest.TestCase):
    def test_endpoints_require_auth(self):
        os.environ.setdefault("DASHBOARD_USER", "admin")
        os.environ.setdefault("DASHBOARD_PASSWORD", "testpass")
        import types
        from unittest.mock import MagicMock
        sys.modules.setdefault('awscrt', types.SimpleNamespace(io=MagicMock(), mqtt=MagicMock()))
        sys.modules.setdefault('awsiot', types.SimpleNamespace(mqtt_connection_builder=MagicMock()))
        import aws_connector
        aws_connector.AWSMqttClient = MagicMock()
        import dashboard_soc
        client = dashboard_soc.app.test_client()
        self.assertEqual(client.get('/api/enrich/web-prod-01').status_code, 401)
        self.assertEqual(client.post('/api/enrich/web-prod-01').status_code, 401)
        self.assertEqual(client.post('/api/enrich/promote', json={}).status_code, 401)


if __name__ == '__main__':
    unittest.main()
