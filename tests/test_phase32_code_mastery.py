"""
Unit tests for Phase 32: Autonomous Programming Code Mastery Engine (12 Tests)
"""

import unittest
from core.autonomous_code_mastery_engine import (
    AutonomousCodeMasteryEngine,
    QrCodeResourceExtractor,
    SampleCodeProjectIngestor,
    PublisherErrataOverrider
)

class TestPhase32CodeMastery(unittest.TestCase):
    def setUp(self):
        self.code_engine = AutonomousCodeMasteryEngine()
        self.qr_extractor = QrCodeResourceExtractor()
        self.sample_ingestor = SampleCodeProjectIngestor()
        self.errata_overrider = PublisherErrataOverrider()

    def test_01_generate_code_mastery_app(self):
        res = self.code_engine.generate_code_mastery_app("PRO専門書: Pythonグラフィックス最適化", "PRO_SPECIALIST")
        self.assertEqual(res["status"], "CODE_MASTERY_GENERATION_OPTIMAL")
        self.assertEqual(res["mastery_tier"], "PRO_SPECIALIST")

    def test_02_qr_code_resource_extraction(self):
        res = self.qr_extractor.extract_qr_resources("test_book")
        self.assertEqual(res["status"], "QR_RESOURCE_EXTRACTION_SUCCESS")
        self.assertGreater(res["qr_codes_detected"], 0)

    def test_03_sample_code_project_ingestion(self):
        res = self.sample_ingestor.ingest_sample_code_projects("test_project")
        self.assertEqual(res["status"], "SAMPLE_CODE_INGESTION_SUCCESS")
        self.assertIn("Python", res["languages_detected"])

    def test_04_publisher_errata_overrides(self):
        res = self.errata_overrider.apply_errata_overrides("test_book")
        self.assertEqual(res["status"], "ERRATA_OVERRIDE_SUCCESS")
        self.assertTrue(res["broken_code_fixed"])

    def test_05_official_doc_sources_integration(self):
        res = self.code_engine.generate_code_mastery_app("Python Book", "INTERMEDIATE", ["Python 3.12 Docs", "PyTorch Docs"])
        self.assertEqual(res["status"], "CODE_MASTERY_GENERATION_OPTIMAL")

    def test_06_mastery_apps_registry_logging(self):
        self.code_engine.generate_code_mastery_app("Rust Mastery")
        self.assertEqual(len(self.code_engine.mastery_apps_registry), 1)

    def test_07_qr_extraction_verified_flag(self):
        res = self.code_engine.generate_code_mastery_app("Test Book")
        self.assertTrue(res["qr_extraction_verified"])

    def test_08_sample_code_ingested_flag(self):
        res = self.code_engine.generate_code_mastery_app("Test Book")
        self.assertTrue(res["sample_code_ingested"])

    def test_09_errata_overridden_flag(self):
        res = self.code_engine.generate_code_mastery_app("Test Book")
        self.assertTrue(res["errata_overridden"])

    def test_10_dual_ai_mentor_active_flag(self):
        res = self.code_engine.generate_code_mastery_app("Test Book")
        self.assertTrue(res["dual_ai_mentor_active"])

    def test_11_4_tier_mastery_support(self):
        tiers = ["BEGINNER", "INTERMEDIATE", "APPLIED", "PRO_SPECIALIST"]
        for t in tiers:
            res = self.code_engine.generate_code_mastery_app("Multi Tier Book", t)
            self.assertEqual(res["mastery_tier"], t)

    def test_12_code_app_id_format(self):
        res = self.code_engine.generate_code_mastery_app("Python Advanced")
        self.assertTrue(res["app_id"].startswith("code_app_"))

if __name__ == "__main__":
    unittest.main()
