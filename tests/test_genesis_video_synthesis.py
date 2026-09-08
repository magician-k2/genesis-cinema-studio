"""
================================================================================
TEST SUITE: GENESIS AI VIDEO SYNTHESIS & PRESENTATION ENGINE
Tests core/genesis_video_synthesis_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_video_synthesis_engine import video_synthesis_engine

class TestGenesisVideoSynthesis(unittest.TestCase):

    def test_01_cast_and_set_bible(self):
        bible = video_synthesis_engine.get_cast_and_set_bible()
        self.assertIn("cast", bible)
        self.assertIn("set", bible)
        self.assertEqual(len(bible["cast"]), 2)
        self.assertEqual(bible["cast"][0]["name"], "佐藤 結衣 (Yui Sato)")
        self.assertEqual(bible["cast"][1]["name"], "佐藤 ハル 様 (Haru Sato)")
        self.assertEqual(bible["set"]["room_name"], "302号室 (東棟 病室)")

    def test_02_storyboard_cuts_duration_and_consistency(self):
        cuts = video_synthesis_engine.get_storyboard()
        self.assertEqual(len(cuts), 6)
        
        total_duration = sum(c["duration_sec"] for c in cuts)
        self.assertEqual(total_duration, 120)  # Exactly 2 minutes
        
        for c in cuts:
            self.assertIn("cut_id", c)
            self.assertIn("title", c)
            self.assertIn("narration_en", c)
            self.assertIn("narration_ja", c)
            self.assertIn("hud_overlay", c)
            self.assertIn("image_file", c)

    def test_03_render_presentation_package(self):
        pkg = video_synthesis_engine.render_presentation_package()
        self.assertEqual(pkg["status"], "VIDEO_PACKAGE_SYNTHESIZED")
        self.assertEqual(pkg["total_duration_sec"], 120)
        self.assertIn("saved_path", pkg)
        self.assertTrue(os.path.exists(pkg["saved_path"]))
        print(f"✅ Presentation Package Saved: {pkg['saved_path']}")

if __name__ == "__main__":
    unittest.main()
