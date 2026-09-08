"""
================================================================================
TEST SUITE: GENESIS GOOGLE SUPREME OMNI CORTEX ENGINE
Tests core/genesis_google_supreme_omni_cortex.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_google_supreme_omni_cortex import google_supreme_cortex, GOOGLE_SUPREME_TARGETS

class TestGenesisGoogleSupremeOmniCortex(unittest.TestCase):

    def test_01_target_domain_matrix(self):
        self.assertEqual(len(GOOGLE_SUPREME_TARGETS), 20)
        insights = google_supreme_cortex.get_supreme_insights()
        self.assertEqual(insights["total_tracked_targets"], 20)
        print(f"✅ Supreme Targets: {insights['total_tracked_targets']} domains registered.")

    def test_02_query_supreme_google_knowledge(self):
        query = "Google Pixel 10 On-device Gemini NanoとCloud Run Vertex AIのハイブリッド超低遅延連携"
        res = google_supreme_cortex.query_supreme_google_knowledge(query)
        self.assertEqual(res["status"], "SUPREME_KNOWLEDGE_SYNTHESIZED")
        self.assertIn("supreme_guidance", res)
        self.assertTrue(len(res["supreme_guidance"]) > 50)
        print(f"👑 Supreme Guidance (Latency: {res['inference_time_ms']}ms):\n{res['supreme_guidance'][:200]}...")

    def test_03_vault_and_synapse_integrity(self):
        insights = google_supreme_cortex.get_supreme_insights()
        vault_file = insights["vault_file"]
        self.assertTrue(os.path.exists(vault_file))
        print(f"🔒 Supreme Vault File: {vault_file} ({os.path.getsize(vault_file)} bytes)")

if __name__ == "__main__":
    unittest.main()
