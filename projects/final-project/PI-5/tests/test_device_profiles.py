"""Tests de persistencia del System Profile (device_profiles) en PI-5."""
import os
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from database import init_schema
from tools import db_tools


def _profile(device="web-prod-01", version=1, phash="sha256:aaa"):
    return {
        "tipo": "PERFIL_SISTEMA", "schema_version": 1, "sensor": device,
        "dispositivo": device, "profile_version": version, "profile_hash": phash,
        "discovered_at": "2026-06-14T10:00:00Z",
        "host": {"os_id": "debian", "os_version": "12", "arch": "aarch64"},
        "firewall": {"active_manager": "nftables"},
        "web_server": {"engine": "nginx", "version": "1.22"},
        "db_engine": {"engine": "mysql"},
        "capabilities": {"restic": False},
    }


class TestDeviceProfiles(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        tmp.close()
        self.db = tmp.name
        init_schema(self.db)

    def tearDown(self):
        try:
            os.unlink(self.db)
        except OSError:
            pass

    def test_upsert_inserts_and_get_returns_profile(self):
        res = db_tools.upsert_device_profile("web-prod-01", _profile(), db_path=self.db)
        self.assertEqual(res["status"], "success")
        self.assertTrue(res["changed"])
        got = db_tools.get_device_profile("web-prod-01", db_path=self.db)
        self.assertEqual(got["web_server"]["engine"], "nginx")
        self.assertEqual(got["firewall"]["active_manager"], "nftables")

    def test_upsert_dedupes_by_hash(self):
        db_tools.upsert_device_profile("d", _profile(version=1, phash="sha256:x"), db_path=self.db)
        # Mismo hash -> no reescribe (changed False) aunque cambie discovered_at.
        again = db_tools.upsert_device_profile("d", _profile(version=1, phash="sha256:x"), db_path=self.db)
        self.assertFalse(again["changed"])

    def test_upsert_updates_on_hash_change(self):
        db_tools.upsert_device_profile("d", _profile(version=1, phash="sha256:x"), db_path=self.db)
        changed = db_tools.upsert_device_profile("d", _profile(version=2, phash="sha256:y"), db_path=self.db)
        self.assertTrue(changed["changed"])
        got = db_tools.get_device_profile("d", db_path=self.db)
        self.assertEqual(got["profile_version"], 2)

    def test_get_missing_returns_empty(self):
        self.assertEqual(db_tools.get_device_profile("nope", db_path=self.db), {})

    def test_one_row_per_device(self):
        import sqlite3
        db_tools.upsert_device_profile("d", _profile(version=1, phash="a"), db_path=self.db)
        db_tools.upsert_device_profile("d", _profile(version=2, phash="b"), db_path=self.db)
        conn = sqlite3.connect(self.db)
        n = conn.execute("SELECT COUNT(*) FROM device_profiles WHERE device='d'").fetchone()[0]
        conn.close()
        self.assertEqual(n, 1)


if __name__ == '__main__':
    unittest.main()
