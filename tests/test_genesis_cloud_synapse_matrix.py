"""
================================================================================
TEST SUITE: GENESIS CLOUD SYNAPSE MATRIX & KNOWLEDGE COMPRESSOR
Tests core/genesis_cloud_synapse_matrix_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_cloud_synapse_matrix_engine import cloud_synapse_engine

class TestGenesisCloudSynapseMatrix(unittest.TestCase):

    def test_01_synapse_insights(self):
        insights = cloud_synapse_engine.get_synapse_insights()
        self.assertGreaterEqual(insights["total_nodes"], 10)
        self.assertGreaterEqual(insights["total_synapse_bridges"], 20)
        self.assertGreater(insights["vault_archive_bytes"], 1000)
        print(f"✅ Synapse Insights: Nodes={insights['total_nodes']} | Bridges={insights['total_synapse_bridges']} | Vault={insights['vault_archive_bytes']} bytes")

    def test_02_vector_search_and_synthesis(self):
        query = "Cloud Run 2026年最新仕様とGemini 3.7 Live Multimodalストリーミング推論"
        res = cloud_synapse_engine.search_and_synthesize(query)
        self.assertEqual(res["status"], "SYNAPSE_SYNTHESIZED")
        self.assertTrue(len(res["top_synapse_matches"]) > 0)
        self.assertIn("synthesized_guidance", res)
        print(f"⚡ Synapse Search Match: {res['top_synapse_matches'][0]['title']} ({res['top_synapse_matches'][0]['similarity']}%) | Latency: {res['inference_time_ms']}ms")

    def test_03_vault_integrity(self):
        insights = cloud_synapse_engine.get_synapse_insights()
        vault_file = insights["vault_file"]
        self.assertTrue(os.path.exists(vault_file))
        print(f"🔒 Vault File Verified: {vault_file} ({os.path.getsize(vault_file)} bytes)")

if __name__ == "__main__":
    unittest.main()
