# -*- coding: utf-8 -*-
"""
Tests for Autonomous Knowledge Harvester & Night Synaptic Consolidator
"""

import unittest
import os
import sys
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.autonomous_knowledge_harvester import AutonomousKnowledgeHarvester
from core.night_synaptic_consolidator import NightSynapticConsolidator

class TestKnowledgeAndConsolidation(unittest.TestCase):
    def setUp(self):
        self.test_vault = os.path.join(ROOT_DIR, "knowledge_bank", "test_vault")
        os.makedirs(self.test_vault, exist_ok=True)
        self.harvester = AutonomousKnowledgeHarvester(vault_dir=self.test_vault)
        self.test_weights = os.path.join(self.test_vault, "test_weights.json")
        self.consolidator = NightSynapticConsolidator(weights_file=self.test_weights, harvester=self.harvester)

    def tearDown(self):
        if os.path.exists(self.test_vault):
            try:
                shutil.rmtree(self.test_vault)
            except Exception:
                pass

    def test_harvest_and_consolidation_flow(self):
        title = "Google Cloud Run WebGPU Architecture Guide"
        content = """
Google Cloud Run now supports high-performance GPU execution including WebGPU runtimes.
Developers can deploy Gemma 4 containerized instances with ultra-low cold start times.
Combined with WebGPU client browsers, this allows global distributed quantum tensor streaming.
"""
        # 1. 収穫
        entry = self.harvester.harvest_document(title, content, source_type="CLOUD_DOC", tags=["GCP", "WEBGPU", "GEMMA4"])
        self.assertIn("id", entry)
        self.assertEqual(entry["title"], title)
        self.assertEqual(entry["status"], "AWAITING_CONSOLIDATION")

        # 2. 保留中リストの取得
        pending = self.harvester.get_pending_consolidation_entries()
        self.assertTrue(any(p["id"] == entry["id"] for p in pending))

        # 3. 深夜海馬リプレイによる固定化
        report = self.consolidator.run_night_replay_consolidation(iterations=4)
        self.assertEqual(report["status"], "CONSOLIDATION_SUCCESS")
        self.assertGreaterEqual(report["consolidated_docs_count"], 1)
        self.assertGreater(report["total_synaptic_delta"], 0.0)

        # 4. 固定化完了確認
        pending_after = self.harvester.get_pending_consolidation_entries()
        self.assertFalse(any(p["id"] == entry["id"] for p in pending_after))

if __name__ == "__main__":
    unittest.main()
