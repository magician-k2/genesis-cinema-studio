"""
================================================================================
TEST SUITE: GENESIS NOTEBOOKLM PLATFORM ENGINE
Tests core/genesis_notebook_lm_platform_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_notebook_lm_platform_engine import notebook_lm_platform

class TestGenesisNotebookLMPlatform(unittest.TestCase):

    def test_01_create_notebook(self):
        res = notebook_lm_platform.create_notebook(
            "GENESIS Multi-Organ Architecture Study",
            [
                {"name": "Architecture Overview", "content": "GENESIS uses Gemini 3.7 Flash with 3072-dimensional embeddings."},
                {"name": "Clinical Safety", "content": "Clinical HUD performs 0.3s bedside inference and night audits."}
            ]
        )
        self.assertEqual(res["status"], "NOTEBOOK_CREATED")
        self.assertEqual(res["notebook_data"]["total_sources"], 2)
        print(f"📚 Notebook Created: {res['notebook_id']} - {res['notebook_data']['title']}")

    def test_02_query_notebook_with_citations(self):
        res = notebook_lm_platform.query_notebook("default", "GENESISの主要機能とアーキテクチャの特徴を教えて")
        self.assertEqual(res["status"], "NOTEBOOK_QUERY_SUCCESS")
        self.assertIn("answer", res)
        self.assertTrue(len(res["answer"]) > 30)
        print(f"🧠 NotebookLM Grounded Answer (Latency: {res['latency_ms']}ms):\n{res['answer'][:200]}...")

    def test_03_generate_audio_overview(self):
        res = notebook_lm_platform.generate_audio_overview("NB_test", "GENESIS AI OS")
        self.assertEqual(res["status"], "AUDIO_OVERVIEW_GENERATED")
        self.assertTrue(len(res["dialogue"]) >= 2)
        print(f"🎙️ Audio Overview Podcast Generated: {res['audio_url']} (Latency: {res['latency_sec']}s)")

if __name__ == "__main__":
    unittest.main()
