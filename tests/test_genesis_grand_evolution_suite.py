"""
================================================================================
TEST SUITE: GENESIS GRAND EVOLUTION SUITE
Tests stealth_whisper_engine, pr_studio_saas, sheets_canvas_engine, contest_packager
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_stealth_whisper_engine import stealth_whisper_engine
from core.genesis_pr_studio_saas_engine import pr_studio_saas
from core.genesis_sheets_canvas_spark_engine import sheets_canvas_engine
from core.genesis_official_package_packager import contest_packager

class TestGenesisGrandEvolutionSuite(unittest.TestCase):

    def test_01_stealth_whisper_dispatch(self):
        res = stealth_whisper_engine.trigger_stealth_whisper("問3の正解は 4番：ガリレオ・ガリレイの地動説 です", "+20%")
        self.assertEqual(res["status"], "WHISPER_DISPATCHED")
        self.assertIn("ガリレオ", res["whisper_text"])
        status = stealth_whisper_engine.get_whisper_status()
        self.assertEqual(status["status"], "ONLINE")
        print(f"🕶️ Stealth Whisper Verified: Latency {res['latency_ms']}ms | Text: {res['whisper_text']}")

    def test_02_pr_studio_project_creation(self):
        res = pr_studio_saas.create_pr_project(
            "GENESIS AI Clinic OS",
            "病院長・クリニック経営者",
            ["看護師残業ゼロ", "0.3s即時推論", "3点照合自動化"]
        )
        self.assertEqual(res["status"], "PROJECT_CREATED")
        self.assertEqual(len(res["project_data"]["cuts"]), 6)
        print(f"🎬 PR Studio Project Created: {res['project_id']} (Total Duration: {res['project_data']['total_duration_sec']}s)")

    def test_03_sheets_canvas_telemetry(self):
        res = sheets_canvas_engine.get_canvas_telemetry()
        self.assertEqual(res["status"], "SHEETS_CANVAS_SYNCED")
        self.assertIn("kpi_metrics", res)
        csv_res = sheets_canvas_engine.export_sheets_csv()
        self.assertEqual(csv_res["status"], "CSV_EXPORTED")
        self.assertTrue(os.path.exists(csv_res["csv_file"]))
        print(f"📊 Sheets Canvas CSV Verified: {csv_res['csv_file']}")

    def test_04_official_package_generation(self):
        res = contest_packager.build_official_submission_packages()
        self.assertEqual(res["status"], "PACKAGES_GENERATED_SUCCESS")
        self.assertTrue(os.path.exists(res["master_zip_package"]))
        print(f"🏆 Official Contest Package Verified: {res['master_zip_package']} ({res['zip_size_bytes']} bytes)")

if __name__ == "__main__":
    unittest.main()
