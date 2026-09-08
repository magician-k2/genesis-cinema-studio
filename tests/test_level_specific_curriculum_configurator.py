"""
Unit tests for Level-Specific Curriculum Configurator Engine (12 Tests)
"""

import unittest
from core.level_specific_curriculum_configurator import LevelSpecificCurriculumConfigurator

class TestLevelSpecificCurriculumConfigurator(unittest.TestCase):
    def setUp(self):
        self.configurator = LevelSpecificCurriculumConfigurator()

    def test_01_default_level_config(self):
        cfg = self.configurator.level_config
        self.assertIn("grammar_reading_level", cfg)
        self.assertEqual(cfg["programming_mastery_level"], "PRO_SPECIALIST")

    def test_02_set_dimension_level(self):
        res = self.configurator.set_dimension_level("grammar_reading_level", "CEFR_C1")
        self.assertEqual(res["status"], "LEVEL_CONFIG_UPDATED_SUCCESS")
        self.assertEqual(res["new_level_target"], "CEFR_C1")

    def test_03_calibrate_synthesized_problems(self):
        sample_pkg = {"problem_set_id": "p_01", "problems": []}
        res = self.configurator.calibrate_synthesized_problems(sample_pkg)
        self.assertEqual(res["status"], "LEVEL_CALIBRATION_OPTIMAL")
        self.assertTrue(res["calibrated_problem_package"]["level_calibration_applied"])

    def test_04_eiken_grade_setting(self):
        self.configurator.set_dimension_level("vocabulary_memory_level", "EIKEN_GRADE_1")
        self.assertEqual(self.configurator.level_config["vocabulary_memory_level"], "EIKEN_GRADE_1")

    def test_05_school_grade_setting(self):
        self.configurator.set_dimension_level("conversational_fluency_level", "JUNIOR_HIGH_L1")
        self.assertEqual(self.configurator.level_config["conversational_fluency_level"], "JUNIOR_HIGH_L1")

    def test_06_cefr_scale_setting(self):
        self.configurator.set_dimension_level("phonetics_pronunciation_level", "CEFR_B2")
        self.assertEqual(self.configurator.level_config["phonetics_pronunciation_level"], "CEFR_B2")

    def test_07_handwriting_dictation_level_setting(self):
        self.configurator.set_dimension_level("handwriting_dictation_level", "HIGH_SCHOOL_L3")
        self.assertEqual(self.configurator.level_config["handwriting_dictation_level"], "HIGH_SCHOOL_L3")

    def test_08_invalid_dimension_ignored(self):
        res = self.configurator.set_dimension_level("non_existent_key", "LEVEL_X")
        self.assertNotIn("non_existent_key", res["current_full_config"])

    def test_09_full_config_snapshot(self):
        res = self.configurator.set_dimension_level("grammar_reading_level", "CEFR_A2")
        self.assertEqual(res["current_full_config"]["grammar_reading_level"], "CEFR_A2")

    def test_10_applied_levels_in_calibration(self):
        sample_pkg = {"test": 123}
        res = self.configurator.calibrate_synthesized_problems(sample_pkg)
        self.assertIn("applied_levels", res)

    def test_11_calibrated_status_in_pkg(self):
        sample_pkg = {"test": 123}
        res = self.configurator.calibrate_synthesized_problems(sample_pkg)
        self.assertEqual(res["calibrated_problem_package"]["status"], "PROBLEMS_CALIBRATED_TO_LEVELS_SUCCESS")

    def test_12_programming_tier_setting(self):
        self.configurator.set_dimension_level("programming_mastery_level", "BEGINNER")
        self.assertEqual(self.configurator.level_config["programming_mastery_level"], "BEGINNER")

if __name__ == "__main__":
    unittest.main()
