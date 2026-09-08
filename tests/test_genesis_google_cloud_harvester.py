"""
================================================================================
TEST SUITE: GENESIS GOOGLE CLOUD OMNI HARVESTER & DELTA ENGINE
Tests core/genesis_google_cloud_omni_harvester.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_google_cloud_omni_harvester import google_cloud_harvester

class TestGenesisGoogleCloudHarvester(unittest.TestCase):

    def test_01_gcloud_insights_status(self):
        insights = google_cloud_harvester.get_latest_gcloud_insights()
        self.assertEqual(insights["root_url"], "https://cloud.google.com/")
        self.assertIn("master_directory", insights)
        self.assertIn("delta_directory", insights)
        print(f"✅ GCloud Insights Status: Ingested={insights['total_articles']} | Deltas={insights['total_deltas']}")

    def test_02_recommend_architecture_task(self):
        task = "スマートグラス向け Gemini 3.7 Flash 超低遅延ストリーミング推論とCloud Run構成"
        rec = google_cloud_harvester.recommend_architecture_for_task(task)
        self.assertEqual(rec["status"], "ARCHITECTURE_RECOMMENDED")
        self.assertIn("recommendation", rec)
        self.assertTrue(len(rec["recommendation"]) > 50)
        print(f"💡 Recommended Architecture (Latency: {rec['inference_time_ms']}ms):\n{rec['recommendation'][:200]}...")

    def test_03_state_index_verification(self):
        state = google_cloud_harvester.state
        self.assertIn("fingerprints", state)
        self.assertIn("version", state)
        print(f"🔒 State Index Fingerprint Count: {len(state['fingerprints'])}")

if __name__ == "__main__":
    unittest.main()
