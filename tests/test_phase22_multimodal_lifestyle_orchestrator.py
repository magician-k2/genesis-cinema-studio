"""
Unit tests for Phase 22 Multimodal Lifestyle Orchestrator (7 Tests)
"""

import unittest
from modules.ebook_knowledge_extractor import EbookKnowledgeExtractor
from modules.language_learning_translator import LanguageLearningTranslator
from modules.eeg_humming_music_generator import EEGHummingMusicGenerator
from modules.smart_glasses_bike_dashcam import SmartGlassesBikeDashcam
from modules.phase22_multimodal_lifestyle_orchestrator import Phase22MultimodalLifestyleOrchestrator

class TestPhase22MultimodalLifestyleOrchestrator(unittest.TestCase):
    def setUp(self):
        self.ebook = EbookKnowledgeExtractor()
        self.translator = LanguageLearningTranslator()
        self.music = EEGHummingMusicGenerator()
        self.dashcam = SmartGlassesBikeDashcam()
        self.orchestrator = Phase22MultimodalLifestyleOrchestrator()

    def test_01_ebook_ingestion_and_knowhow(self):
        res = self.ebook.ingest_book_file("test_book.txt")
        self.assertEqual(res["status"], "SUCCESSFULLY_INGESTED")
        self.assertGreater(res["extracted_knowhow_count"], 0)

    def test_02_translation_service(self):
        res = self.translator.translate_text("こんにちは", "ja", "en")
        self.assertIn("Translated", res["translated_text"])

    def test_03_english_expression_evaluation(self):
        res = self.translator.evaluate_english_expression("This is a test of GENESIS English tutor.")
        self.assertGreater(res["grammar_score"], 70)

    def test_04_eeg_music_generation(self):
        res = self.music.generate_music_from_eeg(0.8, 0.2)
        self.assertEqual(res["status"], "MUSIC_GENERATED")
        self.assertIn("Chill", res["generated_genre"])

    def test_05_humming_pitch_tracker(self):
        res = self.music.process_humming_pitch([440.0, 493.88, 523.25])
        self.assertEqual(len(res["extracted_melody"]), 5)

    def test_06_smart_glasses_dashcam_hazard_alert(self):
        self.dashcam.start_dashcam()
        res = self.dashcam.process_camera_frame("f100", ["car_approaching_rear"])
        self.assertTrue(res["alert_triggered"])
        self.assertIn("car_approaching_rear", res["hazards_detected"])

    def test_07_phase22_master_lifestyle_cycle(self):
        res = self.orchestrator.run_lifestyle_cycle("demo_book.txt")
        self.assertEqual(res["phase"], "PHASE_22_MULTIMODAL_LIFESTYLE")
        self.assertEqual(res["overall_status"], "PHASE22_OPTIMAL")
        self.assertTrue(res["all_green"])

if __name__ == "__main__":
    unittest.main()
