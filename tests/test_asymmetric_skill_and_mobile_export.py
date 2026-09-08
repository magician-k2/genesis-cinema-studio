"""
Unit tests for Asymmetric Skill Matrix, Stylus Handwriting Engine & Mobile Exporter (12 Tests)
"""

import unittest
from core.asymmetric_skill_matrix_evaluator import AsymmetricSkillMatrixEvaluator
from core.tablet_stylus_handwriting_engine import TabletStylusHandwritingEngine
from core.mobile_exportable_translator_packager import MobileExportableTranslatorPackager

class TestAsymmetricSkillAndMobileExport(unittest.TestCase):
    def setUp(self):
        self.evaluator = AsymmetricSkillMatrixEvaluator()
        self.handwriting = TabletStylusHandwritingEngine()
        self.packager = MobileExportableTranslatorPackager()

    def test_01_evaluate_learner_performance(self):
        res = self.evaluator.evaluate_learner_performance("I am learning English")
        self.assertEqual(res["status"], "ASYMMETRIC_MATRIX_EVALUATION_OPTIMAL")
        self.assertIn("grammar_comprehension", res["skill_matrix"])

    def test_02_pronunciation_score_update(self):
        res = self.evaluator.evaluate_learner_performance("Hello", pronunciation_score=95.0)
        self.assertGreater(res["skill_matrix"]["phonetics_pronunciation"], 50.0)

    def test_03_hesitation_impact_on_fluency(self):
        res = self.evaluator.evaluate_learner_performance("...", hesitation_seconds=3.5)
        self.assertLess(res["skill_matrix"]["conversational_fluency"], 45.0)

    def test_04_alt_pacing_strategy_generation(self):
        res = self.evaluator.evaluate_learner_performance("Test")
        self.assertEqual(res["alt_pacing"]["grammar_level"], "ADVANCED_HIGH_SCHOOL")

    def test_05_process_handwriting_and_voice(self):
        res = self.handwriting.process_handwriting_and_voice("Practice makes perfect", "Practice makes perfect", "Practice makes perfect")
        self.assertEqual(res["status"], "HANDWRITING_DICTATION_OPTIMAL")
        self.assertEqual(res["overall_mastery"], 96.8)

    def test_06_handwriting_dictation_session_logging(self):
        self.handwriting.process_handwriting_and_voice("Sentence 1", "Sentence 1", "Sentence 1")
        self.assertEqual(len(self.handwriting.dictation_sessions), 1)

    def test_07_export_mobile_translator_app(self):
        res = self.packager.export_mobile_translator_app("GENESIS_Mobile_App")
        self.assertEqual(res["status"], "MOBILE_EXPORT_COMPLETED_OPTIMAL")
        self.assertTrue(res["remote_prompt_fix_ready"])

    def test_08_exported_apps_registry(self):
        self.packager.export_mobile_translator_app("App 1")
        self.assertEqual(len(self.packager.exported_apps_registry), 1)

    def test_09_process_mobile_remote_prompt_code_fix(self):
        res = self.packager.process_mobile_remote_prompt_code_fix("Fix null pointer in line 42", "main.py")
        self.assertEqual(res["status"], "MOBILE_REMOTE_PROMPT_FIX_APPLIED")
        self.assertTrue(res["code_refactored"])

    def test_10_target_platforms_in_mobile_export(self):
        self.packager.export_mobile_translator_app()
        reg = self.packager.exported_apps_registry[0]
        self.assertIn("Android_Smartphone", reg["target_platforms"])
        self.assertIn("WearOS_Smartwatch", reg["target_platforms"])

    def test_11_written_vs_spoken_accuracy_split(self):
        res = self.handwriting.process_handwriting_and_voice("Sample", "Sample", "Wrong")
        self.assertEqual(res["written_accuracy"], 98.5)
        self.assertEqual(res["spoken_accuracy"], 88.0)

    def test_12_evaluation_history_logging(self):
        self.evaluator.evaluate_learner_performance("Test 1")
        self.assertEqual(len(self.evaluator.evaluation_history), 1)

if __name__ == "__main__":
    unittest.main()
