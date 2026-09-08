"""
Unit tests for Integrated PC Control & Telepathy HUD Engine (10 Tests)
"""

import unittest
import os
from modules.integrated_pc_control_engine import IntegratedPcControlEngine

class TestIntegratedPcControlEngine(unittest.TestCase):
    def setUp(self):
        self.engine = IntegratedPcControlEngine()

    def test_01_set_and_get_subject(self):
        res = self.engine.set_subject("機械翻訳実践（情報/法学）")
        self.assertEqual(res["status"], "SUBJECT_RESTRICTION_SET")
        self.assertEqual(self.engine.get_current_subject(), "機械翻訳実践（情報/法学）")

    def test_02_clear_subject(self):
        self.engine.clear_subject()
        self.assertEqual(self.engine.get_current_subject(), "")

    def test_03_telepathy_config_save_and_get(self):
        res = self.engine.save_telepathy_config(
            subject="AI社会の歩き方",
            storage_source="local",
            folder_path=r"C:\GENESIS_DEV_NEW\GHOST_DATA\courses\AI社会の歩き方",
            auto_tts=True
        )
        self.assertEqual(res["status"], "TELEPATHY_CONFIG_SAVED")
        cfg = self.engine.get_telepathy_config()
        self.assertEqual(cfg["subject"], "AI社会の歩き方")
        self.assertIn("available_folders", cfg)

    def test_04_discover_folders(self):
        folders = self.engine.discover_available_knowledge_folders()
        self.assertIsInstance(folders, list)

    def test_05_live_telepathy_state_and_trigger(self):
        state1 = self.engine.get_live_telepathy_state()
        self.assertIn("status", state1)
        res = self.engine.trigger_analysis_cycle("テスト問題：次のうち正しいものはどれか？")
        self.assertEqual(res["status"], "answered")
        self.assertGreater(res["counter"], 0)
        self.assertGreater(len(res["history"]), 0)

    def test_06_get_captures_list(self):
        captures = self.engine.get_captures_list(limit=50)
        self.assertIsInstance(captures, list)

    def test_07_generate_academic_thesis(self):
        res = self.engine.generate_academic_thesis("GENESIS Neuro-Mesh v5 テスト論文")
        self.assertEqual(res["status"], "THESIS_GENERATED_SUCCESS")
        self.assertTrue(os.path.exists(res["doc_path"]))

    def test_08_generate_research_proposal(self):
        res = self.engine.generate_research_proposal("Google Startups 研究提案書テスト")
        self.assertEqual(res["status"], "PROPOSAL_GENERATED_SUCCESS")
        self.assertTrue(os.path.exists(res["doc_path"]))

    def test_09_capture_image_bytes(self):
        captures = self.engine.get_captures_list(limit=1)
        if captures:
            fname = captures[0]["filename"]
            img_data = self.engine.get_capture_image_bytes(fname)
            self.assertIsNotNone(img_data)

    def test_10_captures_limit_50(self):
        captures = self.engine.get_captures_list(limit=50)
        self.assertLessEqual(len(captures), 50)

if __name__ == "__main__":
    unittest.main()
