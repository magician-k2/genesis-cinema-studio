"""
================================================================================
TEST SUITE: GENESIS GOOGLE DEVELOPERS & SKILLS SUPREME ENGINE
Tests core/genesis_google_developers_and_skills_harvester.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_google_developers_and_skills_harvester import google_developers_and_skills_harvester

class TestGenesisGoogleDevelopersAndSkills(unittest.TestCase):

    def test_01_ecosystem_insights(self):
        insights = google_developers_and_skills_harvester.get_ecosystem_insights()
        self.assertIn("developers_url", insights)
        self.assertIn("skills_url", insights)
        self.assertIn("dev_master_dir", insights)
        self.assertIn("skills_master_dir", insights)
        print(f"✅ GDev & Skills Insights: DevArticles={insights['total_dev_articles']} | SkillsArticles={insights['total_skills_articles']}")

    def test_02_synthesize_supreme_developer_superpower(self):
        query = "Gemini 3.7 Flash Live Multimodalストリーミング推論とWebGPU/Project IDX最適化"
        res = google_developers_and_skills_harvester.synthesize_supreme_developer_superpower(query)
        self.assertEqual(res["status"], "SUPERPOWER_SYNTHESIZED")
        self.assertIn("guidance", res)
        self.assertTrue(len(res["guidance"]) > 50)
        print(f"⚡ Superpower Guidance (Latency: {res['inference_time_ms']}ms):\n{res['guidance'][:200]}...")

    def test_03_state_verification(self):
        state = google_developers_and_skills_harvester.state
        self.assertIn("dev_fingerprints", state)
        self.assertIn("skills_fingerprints", state)
        print(f"🔒 Ecosystem Fingerprints: Dev={len(state['dev_fingerprints'])} | Skills={len(state['skills_fingerprints'])}")

if __name__ == "__main__":
    unittest.main()
