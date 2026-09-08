"""
Unit tests for Conversation Context Lightweight Handover Engine (6 Tests)
"""

import unittest
import os
from core.conversation_context_lightweight_handover_engine import ConversationContextLightweightHandoverEngine

class TestConversationContextLightweightHandoverEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ConversationContextLightweightHandoverEngine()

    def test_01_generate_and_export_handover_package(self):
        res = self.engine.generate_and_export_handover_package()
        self.assertEqual(res["status"], "HANDOVER_PACKAGE_EXPORTED_SUCCESS")
        self.assertTrue(os.path.exists(res["handover_file"]))

    def test_02_handover_file_content_cortex_nodes(self):
        self.engine.generate_and_export_handover_package()
        with open(self.engine.handover_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("10,787", content)
        self.assertIn("490/490 ALL GREEN", content)

    def test_03_handover_file_japanese_directive(self):
        self.engine.generate_and_export_handover_package()
        with open(self.engine.handover_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("完全日本語化", content)
        self.assertIn("事前承認", content)

    def test_04_handover_prompt_presence(self):
        self.engine.generate_and_export_handover_package()
        with open(self.engine.handover_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("NEXT_CHAT_HANDOVER_SUMMARY.md", content)

    def test_05_cortex_nodes_stat(self):
        res = self.engine.generate_and_export_handover_package()
        self.assertEqual(res["cortex_nodes"], 10787)

    def test_06_test_status_stat(self):
        res = self.engine.generate_and_export_handover_package()
        self.assertEqual(res["test_status"], "490/490 ALL GREEN")

if __name__ == "__main__":
    unittest.main()
