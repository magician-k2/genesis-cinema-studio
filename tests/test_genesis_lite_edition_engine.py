"""
Unit tests for GENESIS Lite Edition Ultra-Lightweight App Engine (12 Tests)
"""

import unittest
from core.genesis_lite_edition_engine import GenesisLiteEditionEngine

class TestGenesisLiteEditionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GenesisLiteEditionEngine()

    def test_01_create_instant_lite_study_app(self):
        res = self.engine.create_instant_lite_study_app("中学英語をもう一度ひとつひとつわかりやすく。")
        self.assertEqual(res["status"], "GENESIS_LITE_CREATION_SUCCESS")
        self.assertTrue(res["pro_upgrade_path_available"])

    def test_02_lite_version_identifier(self):
        self.assertEqual(self.engine.lite_version, "v1.0_LITE_INSTANT")

    def test_03_ram_footprint_within_budget(self):
        res = self.engine.create_instant_lite_study_app("サンプル書籍")
        self.assertIn("48.5 MB", res["ram_footprint"])

    def test_04_startup_speed_instant(self):
        res = self.engine.create_instant_lite_study_app("サンプル書籍")
        self.assertIn("0.15s", res["startup_speed"])

    def test_05_generated_lite_apps_history_accumulation(self):
        self.engine.create_instant_lite_study_app("Book A")
        self.engine.create_instant_lite_study_app("Book B")
        self.assertEqual(len(self.engine.generated_lite_apps), 2)

    def test_06_evaluate_pro_upgrade_eligibility(self):
        res_create = self.engine.create_instant_lite_study_app("Book A")
        res_eval = self.engine.evaluate_pro_upgrade_eligibility(res_create["lite_app_id"])
        self.assertEqual(res_eval["status"], "PRO_UPGRADE_BRIDGE_READY")
        self.assertTrue(res_eval["upgrade_recommended"])

    def test_07_unlocked_pro_features_list(self):
        res_eval = self.engine.evaluate_pro_upgrade_eligibility("test_id")
        self.assertIn("Full Dual-AI ALT Support System", res_eval["unlocked_pro_features"])
        self.assertIn("Google Pay Direct Cash Payout Mining", res_eval["unlocked_pro_features"])

    def test_08_target_device_reflection(self):
        self.engine.create_instant_lite_study_app("Book", target_device="SMARTPHONE")
        app_rec = self.engine.generated_lite_apps[0]
        self.assertEqual(app_rec["target_device"], "SMARTPHONE")

    def test_09_lite_app_id_format(self):
        res = self.engine.create_instant_lite_study_app("Book")
        self.assertTrue(res["lite_app_id"].startswith("genesis_lite_app_"))

    def test_10_features_list_presence(self):
        self.engine.create_instant_lite_study_app("Book")
        app_rec = self.engine.generated_lite_apps[0]
        self.assertIn("1-Click Ebook Processing", app_rec["features"])

    def test_11_lite_app_title_format(self):
        res = self.engine.create_instant_lite_study_app("高校英文法")
        self.assertIn("【Lite版】高校英文法", res["app_title"])

    def test_12_status_lite_app_ready_for_deployment(self):
        self.engine.create_instant_lite_study_app("Book")
        app_rec = self.engine.generated_lite_apps[0]
        self.assertEqual(app_rec["status"], "LITE_APP_READY_FOR_DEPLOYMENT")

if __name__ == "__main__":
    unittest.main()
