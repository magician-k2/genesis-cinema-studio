"""
Unit tests for Silent Telepathy Mouse Listener Module (8 Tests)
"""

import unittest
import os
from modules.integrated_pc_control_engine import IntegratedPcControlEngine
from modules.silent_telepathy_mouse_listener import SilentTelepathyMouseListener

class TestSilentTelepathyMouseListener(unittest.TestCase):
    def setUp(self):
        self.pc_engine = IntegratedPcControlEngine()
        self.listener = SilentTelepathyMouseListener(self.pc_engine)

    def test_01_init_and_properties(self):
        self.assertFalse(self.listener.is_running)
        self.assertFalse(self.listener.is_processing)
        self.assertEqual(self.listener.total_triggers_count, 0)

    def test_02_start_and_stop(self):
        self.listener.start()
        self.assertTrue(self.listener.is_running)
        self.listener.stop()
        self.assertFalse(self.listener.is_running)

    def test_03_capture_and_solve_science(self):
        self.pc_engine.save_telepathy_config(
            subject="逆さ科学史",
            storage_source="local",
            folder_path=r"C:\GENESIS_DEV_NEW\GHOST_DATA\courses\逆さ科学史"
        )
        res = self.listener.capture_and_solve(100, 100)
        self.assertEqual(res["status"], "answered")
        self.assertIn("ウェーゲナー", res["answer_text"])
        self.assertIn("逆さ科学史", res["explanation"])

    def test_04_capture_and_solve_translation(self):
        self.pc_engine.save_telepathy_config(
            subject="機械翻訳実践（情報）",
            storage_source="local",
            folder_path=r"C:\GENESIS_DEV_NEW\GHOST_DATA\courses\機械翻訳実践（情報）"
        )
        res = self.listener.capture_and_solve(100, 100)
        self.assertEqual(res["status"], "answered")
        self.assertIn("主語＋動詞", res["answer_text"])

    def test_05_capture_and_solve_ai(self):
        self.pc_engine.save_telepathy_config(
            subject="AI社会の歩き方",
            storage_source="local",
            folder_path=r"C:\GENESIS_DEV_NEW\GHOST_DATA\courses\AI社会の歩き方"
        )
        res = self.listener.capture_and_solve(100, 100)
        self.assertEqual(res["status"], "answered")
        self.assertIn("AI倫理", res["answer_text"])

    def test_06_capture_and_solve_management(self):
        self.pc_engine.save_telepathy_config(
            subject="企業経営",
            storage_source="local",
            folder_path=r"C:\GENESIS_DEV_NEW\GHOST_DATA\courses\企業経営"
        )
        res = self.listener.capture_and_solve(100, 100)
        self.assertEqual(res["status"], "answered")
        self.assertIn("コア・コンピタンス", res["answer_text"])

    def test_07_clipboard_copy(self):
        # Should not raise exception
        self.listener.copy_to_clipboard("テスト解答テキスト")

    def test_08_trigger_callback(self):
        called = []
        def callback(data):
            called.append(data)
        cb_listener = SilentTelepathyMouseListener(self.pc_engine, on_answer_callback=callback)
        cb_listener.capture_and_solve()
        self.assertEqual(len(called), 1)

if __name__ == "__main__":
    unittest.main()
