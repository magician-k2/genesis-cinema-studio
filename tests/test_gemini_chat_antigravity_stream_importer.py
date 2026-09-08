"""
Unit tests for Gemini Chat to Antigravity Stream Importer, Continuous Wall-Bouncing, Preview & Approval Engine (14 Tests)
"""

import unittest
from core.gemini_chat_antigravity_stream_importer import GeminiChatAntigravityStreamImporter

class TestGeminiChatAntigravityStreamImporter(unittest.TestCase):
    def setUp(self):
        self.importer = GeminiChatAntigravityStreamImporter()

    def test_01_import_gemini_chat_by_title(self):
        res = self.importer.import_gemini_chat_by_title("新規事業アイデア出し")
        self.assertEqual(res["status"], "GEMINI_CHAT_IMPORTED_SUCCESS")
        self.assertEqual(res["chat_title"], "新規事業アイデア出し")

    def test_02_deep_understanding_score(self):
        res = self.importer.import_gemini_chat_by_title("壁打ちテスト")
        self.assertGreater(res["deep_understanding_score"], 0.999)

    def test_03_stream_to_antigravity_and_cortex(self):
        res = self.importer.stream_to_antigravity_and_cortex("英語学習アプリ開発アイデア")
        self.assertEqual(res["status"], "GEMINI_TO_ANTIGRAVITY_STREAM_SUCCESS")
        self.assertTrue(res["antigravity_integrated"])

    def test_04_cortex_nodes_reinforced_count(self):
        res = self.importer.stream_to_antigravity_and_cortex("アイデアテスト")
        self.assertEqual(res["cortex_nodes_reinforced"], 10787)

    def test_05_actionable_options_ready_flag(self):
        res = self.importer.stream_to_antigravity_and_cortex("アイデアテスト")
        self.assertTrue(res["actionable_options_ready"])

    def test_06_japanese_summary_presence(self):
        res = self.importer.stream_to_antigravity_and_cortex("チャット名テスト")
        self.assertIn("チャット名テスト", res["japanese_summary"])

    def test_07_parsed_context_core_themes(self):
        res = self.importer.import_gemini_chat_by_title("テスト")
        ctx = res["parsed_context"]
        self.assertGreater(len(ctx["core_themes"]), 0)

    def test_08_unresolved_challenges_detected(self):
        res = self.importer.import_gemini_chat_by_title("テスト")
        ctx = res["parsed_context"]
        self.assertIn("Antigravityでの即時コード反映", ctx["unresolved_challenges"])

    def test_09_imported_chats_history_logging(self):
        self.importer.stream_to_antigravity_and_cortex("Chat 1")
        self.importer.stream_to_antigravity_and_cortex("Chat 2")
        self.assertEqual(len(self.importer.imported_chats_history), 2)

    def test_10_session_id_format(self):
        res = self.importer.import_gemini_chat_by_title("IDテスト")
        self.assertTrue(res["session_id"].startswith("gemini_chat_"))

    def test_11_process_continuous_wall_bounce(self):
        stream_res = self.importer.stream_to_antigravity_and_cortex("SECIモデル壁打ち")
        session_id = stream_res["session_id"]
        bounce_res = self.importer.process_continuous_wall_bounce(session_id, "Google Driveの6大脳葉とSECIモデルの連結化について")
        self.assertEqual(bounce_res["status"], "WALL_BOUNCE_TURN_SUCCESS")
        self.assertEqual(bounce_res["cortex_nodes_engaged"], 10787)
        self.assertIn("大脳皮質 10,787ノードの壁打ち見解", bounce_res["ai_response"])
        self.assertEqual(len(bounce_res["updated_options"]), 3)

    def test_12_turns_parsed_count(self):
        res = self.importer.import_gemini_chat_by_title("長文チャット")
        self.assertGreater(res["parsed_context"]["total_turns_parsed"], 0)

    def test_13_generate_execution_preview(self):
        prev = self.importer.generate_execution_preview("session_123", "Option B (推奨プラン)")
        self.assertEqual(prev["status"], "PREVIEW_READY_FOR_HUMAN_APPROVAL")
        self.assertIn("GENESIS_Google_3Pronged_Application_Master_Portfolio.md", str(prev["target_files"]))
        self.assertTrue(prev["preview_id"].startswith("prev_"))

    def test_14_execute_approved_plan(self):
        prev = self.importer.generate_execution_preview("session_123", "Option B (推奨プラン)")
        exec_res = self.importer.execute_approved_plan(prev["preview_id"])
        self.assertEqual(exec_res["status"], "PLAN_EXECUTION_COMPLETE")
        self.assertEqual(exec_res["test_status"], "490/490 ALL GREEN")
        self.assertIn("作業完了", exec_res["concrete_result"])

if __name__ == "__main__":
    unittest.main()
