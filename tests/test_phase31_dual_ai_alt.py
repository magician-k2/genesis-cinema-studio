"""
Unit tests for Phase 31: Ebook App Generator & Dual-AI ALT Support System (12 Tests)
"""

import unittest
from core.ebook_app_generator import EbookAppGenerator
from core.dual_ai_alt_tutor_system import DualAiAltTutorSystem

class TestPhase31DualAiAlt(unittest.TestCase):
    def setUp(self):
        self.app_generator = EbookAppGenerator()
        self.dual_alt = DualAiAltTutorSystem()

    def test_01_generate_app_from_ebook(self):
        res = self.app_generator.generate_app_from_ebook("中学英語をもう一度ひとつひとつわかりやすく。", "ENGLISH_SLA")
        self.assertEqual(res["status"], "EBOOK_APP_GENERATION_OPTIMAL")
        self.assertEqual(res["units_count"], 5)

    def test_02_supported_series_list(self):
        self.assertIn("HITOTSU_HITOTSU_WAKARUYASUKU_SERIES", self.app_generator.supported_series)
        self.assertIn("SECOND_LANGUAGE_ACQUISITION_SLA_THEORY", self.app_generator.supported_series)

    def test_03_start_dual_ai_learning_session(self):
        res = self.dual_alt.start_dual_ai_learning_session("app_test_123")
        self.assertEqual(res["status"], "DUAL_AI_SESSION_STARTED")
        self.assertTrue(res["session_id"].startswith("session_dual_ai_"))

    def test_04_process_learner_turn_no_hesitation(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        res = self.dual_alt.process_learner_turn("I like studying AI", hesitation_detected=False)
        self.assertEqual(res["status"], "DUAL_AI_TURN_PROCESSED_OPTIMAL")
        self.assertIsNone(res["alt_support_intervention"])

    def test_05_process_learner_turn_with_hesitation(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        res = self.dual_alt.process_learner_turn("", hesitation_detected=True)
        self.assertIsNotNone(res["alt_support_intervention"])
        self.assertTrue(res["alt_support_intervention"]["triggered"])

    def test_06_stumble_keyword_intervention_hint(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        res = self.dual_alt.process_learner_turn("...", hesitation_detected=True, stumble_keyword="会話表現")
        intervention = res["alt_support_intervention"]
        self.assertIn("会話表現", intervention["alt_teacher_message"])

    def test_07_support_interventions_logging(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        self.dual_alt.process_learner_turn("", hesitation_detected=True)
        self.assertEqual(len(self.dual_alt.support_interventions_log), 1)

    def test_08_conversation_flow_preserved_flag(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        res = self.dual_alt.process_learner_turn("", hesitation_detected=True)
        self.assertTrue(res["conversation_flow_preserved"])

    def test_09_sla_confidence_score(self):
        self.dual_alt.start_dual_ai_learning_session("app_test_123")
        res = self.dual_alt.process_learner_turn("", hesitation_detected=True)
        self.assertEqual(res["alt_support_intervention"]["sla_confidence_score"], 0.999)

    def test_10_app_generator_registry_logging(self):
        self.app_generator.generate_app_from_ebook("高校英文法をもう一度ひとつひとつわかりやすく。")
        self.assertEqual(len(self.app_generator.generated_apps_registry), 1)

    def test_11_multi_subject_math_eiken_support(self):
        res = self.app_generator.generate_app_from_ebook("中学3年間の数学が1ヶ月でやり直せる本", "MATH")
        self.assertEqual(res["status"], "EBOOK_APP_GENERATION_OPTIMAL")

    def test_12_dual_ai_roles_assignment(self):
        res = self.dual_alt.start_dual_ai_learning_session("app_test_123")
        self.assertIn("Native Conversation", res["partner_ai_role"])
        self.assertIn("Gentle Hint Coach", res["alt_teacher_ai_role"])

if __name__ == "__main__":
    unittest.main()
