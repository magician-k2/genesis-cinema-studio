"""
Unit tests for App Generation Mode Selector Engine (12 Tests)
"""

import unittest
from core.app_generation_mode_selector import AppGenerationModeSelector

class TestAppGenerationModeSelector(unittest.TestCase):
    def setUp(self):
        self.selector = AppGenerationModeSelector()

    def test_01_execute_mode_app_generation_dual_hybrid(self):
        res = self.selector.execute_mode_app_generation("DUAL_HYBRID_MODE")
        self.assertEqual(res["status"], "MODE_SELECTION_OPTIMAL")
        self.assertEqual(res["packages_generated_count"], 2)
        self.assertTrue(res["dual_hybrid_ready"])

    def test_02_execute_integrated_mode_only(self):
        res = self.selector.execute_mode_app_generation("INTEGRATED_MODE")
        self.assertEqual(res["packages_generated_count"], 1)
        self.assertTrue(res["integrated_mode_ready"])
        self.assertFalse(res["standalone_mode_ready"])

    def test_03_execute_standalone_single_book_mode_only(self):
        res = self.selector.execute_mode_app_generation("STANDALONE_SINGLE_BOOK_MODE", target_single_book="英語の発音ひとつひとつ")
        self.assertEqual(res["packages_generated_count"], 1)
        self.assertTrue(res["standalone_mode_ready"])
        self.assertFalse(res["integrated_mode_ready"])

    def test_04_supported_modes_list(self):
        self.assertIn("INTEGRATED_MODE", self.selector.supported_modes)
        self.assertIn("STANDALONE_SINGLE_BOOK_MODE", self.selector.supported_modes)
        self.assertIn("DUAL_HYBRID_MODE", self.selector.supported_modes)

    def test_05_invalid_mode_fallback_to_dual_hybrid(self):
        res = self.selector.execute_mode_app_generation("INVALID_MODE")
        self.assertEqual(res["generation_mode"], "DUAL_HYBRID_MODE")

    def test_06_target_single_book_reflected(self):
        res = self.selector.execute_mode_app_generation("STANDALONE_SINGLE_BOOK_MODE", target_single_book="会話英単語ひとつひとつ")
        self.assertEqual(res["target_single_book"], "会話英単語ひとつひとつ")

    def test_07_history_logging(self):
        self.selector.execute_mode_app_generation("INTEGRATED_MODE")
        self.assertEqual(len(self.selector.generation_mode_history), 1)

    def test_08_mode_id_format(self):
        self.selector.execute_mode_app_generation()
        history_entry = self.selector.generation_mode_history[0]
        self.assertTrue(history_entry["mode_id"].startswith("mode_gen_"))

    def test_09_standalone_weakness_drill_flag(self):
        self.selector.execute_mode_app_generation("STANDALONE_SINGLE_BOOK_MODE", "英語の発音ひとつひとつ")
        pkg = self.selector.generation_mode_history[0]["generated_packages"][0]
        self.assertTrue(pkg["laser_focused_weakness_drill"])

    def test_10_integrated_fused_books_count(self):
        self.selector.execute_mode_app_generation("INTEGRATED_MODE", all_books_list=["B1", "B2", "B3", "B4"])
        pkg = self.selector.generation_mode_history[0]["generated_packages"][0]
        self.assertEqual(pkg["fused_books_count"], 4)

    def test_11_multiple_generation_runs_accumulate_history(self):
        self.selector.execute_mode_app_generation("INTEGRATED_MODE")
        self.selector.execute_mode_app_generation("STANDALONE_SINGLE_BOOK_MODE")
        self.assertEqual(len(self.selector.generation_mode_history), 2)

    def test_12_status_mode_selection_optimal(self):
        res = self.selector.execute_mode_app_generation("DUAL_HYBRID_MODE")
        self.assertEqual(res["status"], "MODE_SELECTION_OPTIMAL")

if __name__ == "__main__":
    unittest.main()
