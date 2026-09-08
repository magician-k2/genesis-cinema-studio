"""
Unit tests for Global Contest Strategic Book Curation Engine (12 Tests)
"""

import unittest
from core.global_contest_strategic_curation_engine import GlobalContestStrategicCurationEngine

class TestGlobalContestStrategicCurationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GlobalContestStrategicCurationEngine()

    def test_01_get_contest_policy_statement(self):
        res = self.engine.get_contest_policy_statement()
        self.assertEqual(res["status"], "POLICY_ACTIVE_AND_ENFORCED")
        self.assertTrue(res["domestic_small_contests_excluded"])

    def test_02_policy_rule_text(self):
        res = self.engine.get_contest_policy_statement()
        self.assertIn("Google主催", res["rule"])
        self.assertIn("海外の権威あるグローバルコンペティション", res["rule"])

    def test_03_curate_books_xprize_global(self):
        res = self.engine.curate_books_for_target_contest("PROGRAM_2_XPRIZE_GLOBAL")
        self.assertEqual(res["status"], "BOOK_CURATION_OPTIMAL")
        self.assertIn("Advanced Global SLA", res["curated_book_genres"][0])

    def test_04_curate_books_google_play_accelerator(self):
        res = self.engine.curate_books_for_target_contest("PROGRAM_3_GOOGLE_PLAY_ACCELERATOR")
        self.assertEqual(res["status"], "BOOK_CURATION_OPTIMAL")
        self.assertIn("中学英語ひとつひとつシリーズ", res["curated_book_genres"][0])

    def test_05_xprize_core_ai_features(self):
        res = self.engine.curate_books_for_target_contest("PROGRAM_2_XPRIZE_GLOBAL")
        self.assertIn("Dual-AI ALT Dialectic", res["core_ai_features"])

    def test_06_google_play_core_ai_features(self):
        res = self.engine.curate_books_for_target_contest("PROGRAM_3_GOOGLE_PLAY_ACCELERATOR")
        self.assertIn("Pixel Tablet Stylus Stroke Recognition", res["core_ai_features"])

    def test_07_invalid_contest_type_handling(self):
        res = self.engine.curate_books_for_target_contest("UNKNOWN_CONTEST")
        self.assertEqual(res["status"], "ERROR_CONTEST_TYPE_NOT_FOUND")

    def test_08_curation_logs_accumulation(self):
        self.engine.curate_books_for_target_contest("PROGRAM_2_XPRIZE_GLOBAL")
        self.engine.curate_books_for_target_contest("PROGRAM_3_GOOGLE_PLAY_ACCELERATOR")
        self.assertEqual(len(self.engine.curation_logs), 2)

    def test_09_contest_policy_constant(self):
        self.assertEqual(self.engine.contest_policy, "GOOGLE_SPONSORED_AND_GLOBAL_OVERSEAS_ONLY")

    def test_10_play_accelerator_stylus_books_presence(self):
        domain = self.engine.curated_domains["PROGRAM_3_GOOGLE_PLAY_ACCELERATOR"]
        self.assertTrue(any("100-Day Handwriting" in g for g in domain["curated_book_genres"]))

    def test_11_xprize_stem_books_presence(self):
        domain = self.engine.curated_domains["PROGRAM_2_XPRIZE_GLOBAL"]
        self.assertTrue(any("Academic STEM" in g for g in domain["curated_book_genres"]))

    def test_12_differentiated_strategy_presence(self):
        res = self.engine.curate_books_for_target_contest("PROGRAM_2_XPRIZE_GLOBAL")
        self.assertIn("明確に住み分けられた特化カリキュラム設計完了", res["differentiated_strategy"])

if __name__ == "__main__":
    unittest.main()
