# -*- coding: utf-8 -*-
"""
================================================================================
TEST SUITE: GENESIS 90s-00s JAPANESE TECHNO 2-HOUR DJ REMIX ENGINE
(tests/test_genesis_techno_dj_remix_engine.py)
================================================================================
"""

import unittest
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_techno_dj_remix_engine import techno_dj_engine

class TestGenesisTechnoDjRemixEngine(unittest.TestCase):

    def test_01_tracklist_structure(self):
        """全20曲のトラックリスト、BPM、キー、尺の検証"""
        summary = techno_dj_engine.get_tracklist_summary()
        self.assertEqual(summary.get("total_tracks"), 20)
        tracks = summary.get("tracks", [])
        self.assertEqual(len(tracks), 20)
        
        # BPMの範囲が130〜140であることを確認
        for t in tracks:
            self.assertGreaterEqual(t["bpm"], 130)
            self.assertLessEqual(t["bpm"], 140)
            self.assertIn("key", t)
            self.assertIn("title", t)

    def test_02_synthesize_2hour_master_mix(self):
        """2時間20曲 連続DJリミックスの自動合成とCamelot Wheel遷移の検証"""
        mix_res = techno_dj_engine.synthesize_2hour_master_mix()
        self.assertEqual(mix_res.get("status"), "MASTER_DJ_MIX_SYNTHESIZED")
        self.assertEqual(mix_res.get("total_tracks"), 20)
        self.assertGreaterEqual(mix_res.get("total_duration_minutes"), 110.0)
        
        # 19個のトランジションタイムラインが生成されていることを確認
        transitions = mix_res.get("transitions_timeline", [])
        self.assertEqual(len(transitions), 19)
        for trans in transitions:
            self.assertIn("from_track", trans)
            self.assertIn("to_track", trans)
            self.assertIn("eq_curve", trans)
            self.assertEqual(trans.get("harmonic_compatibility"), "PERFECT_MATCH (Camelot Wheel Adjacent)")

        # Google Drive正本保存の確認
        self.assertIn("saved_path", mix_res)
        self.assertTrue(os.path.exists(mix_res["saved_path"]))

if __name__ == "__main__":
    unittest.main()
