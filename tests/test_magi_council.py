import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.agent_magi import deliberate_sync

class TestMagiCouncil(unittest.TestCase):
    def test_official_google_announcement(self):
        content = """
Google DeepMind and Isomorphic Labs introduce AlphaFold 3, a revolutionary AI model that predicts the structure and interactions of all life's molecules.
Published in Nature with complete validation and documentation available on deepmind.google/technologies/alphafold.
"""
        res = deliberate_sync(content, {"source": "https://deepmind.google/technologies/alphafold"})
        print("\n=== TEST 1: 公式Google情報 (AlphaFold 3) ===")
        print(res["aufheben_summary"])
        self.assertTrue(res["is_approved"])
        self.assertGreaterEqual(res["agree_count"], 2)

    def test_fake_clickbait_news(self):
        content = """
Breaking: Google announces it is completely shutting down all Android and Pixel phones next week to focus only on smart toasters.
Click here for free crypto giveaway!
"""
        res = deliberate_sync(content, {"source": "http://random-scam-blog.xyz"})
        print("\n=== TEST 2: フェイク・クリックベイト情報 ===")
        print(res["aufheben_summary"])
        self.assertFalse(res["is_approved"])
        self.assertLess(res["agree_count"], 2)

if __name__ == "__main__":
    unittest.main()
