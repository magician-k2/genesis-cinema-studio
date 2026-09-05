# -*- coding: utf-8 -*-
"""
Tests for Mocap & Pose-Acting Transfer Engine
(tests/test_mocap_pose_transfer_engine.py)
"""

import os
import sys
import unittest
import json
import urllib.request
import urllib.parse
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.mocap_pose_transfer_engine import MocapPoseTransferEngine

class TestMocapPoseTransferEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = MocapPoseTransferEngine(root_dir=ROOT_DIR)
        cls.sample_video = os.path.join(ROOT_DIR, "GENESIS_CINEMA_STUDIO", "assets", "harajuku_straight_street_perfect.mp4")

    def test_01_engine_initialization(self):
        """Verify engine loads correctly with MediaPipe support."""
        self.assertIsNotNone(self.engine)
        self.assertTrue(hasattr(self.engine, 'has_mediapipe'))
        self.assertTrue(os.path.exists(self.engine.output_dir))

    def test_02_calculate_angle_geometry(self):
        """Verify 2D/3D angle calculation between landmark joints."""
        # 90-degree right angle (e.g., shoulder, elbow, wrist)
        a = (0.0, 1.0)
        b = (0.0, 0.0)
        c = (1.0, 0.0)
        angle_90 = self.engine.calculate_angle(a, b, c)
        self.assertAlmostEqual(angle_90, 90.0, places=1)

        # 180-degree straight arm
        c_straight = (0.0, -1.0)
        angle_180 = self.engine.calculate_angle(a, b, c_straight)
        self.assertAlmostEqual(angle_180, 180.0, delta=0.5)

    def test_03_motion_extraction_from_video(self):
        """Verify extracting 33-point body landmarks from video clip."""
        if not os.path.exists(self.sample_video):
            self.skipTest("Sample video not found, skipping video read test.")

        res = self.engine.extract_motion_from_video(
            self.sample_video, start_sec=0.0, end_sec=1.0, sample_fps=5
        )
        self.assertTrue(res.get("success"))
        self.assertGreater(res.get("total_extracted_frames"), 0)
        self.assertIn("motion_summary", res)
        self.assertIn("acting_direction", res)

        frames = res.get("frames", [])
        self.assertGreater(len(frames), 0)
        self.assertEqual(frames[0]["landmarks_count"], 33)

    def test_04_gemma4_acting_intent_analysis(self):
        """Verify Gemma 4 generates stage direction & Veo prompt from motion."""
        mock_summary = {
            "motion_type": "Sweeping Arm Action & Expressive Gestures",
            "intensity": "High (Dynamic Expression / Dance)",
            "max_joint_angle_delta": 75.4,
            "analyzed_duration_seconds": 3.0,
            "keyframe_count": 15
        }
        res = self.engine.analyze_acting_intent_with_gemma4(mock_summary)
        self.assertIsNotNone(res)
        self.assertIn("stage_direction", res)
        self.assertIn("veo_prompt", res)
        self.assertIn("camera_movement", res)
        self.assertTrue(len(res["stage_direction"]) > 10)
        self.assertTrue(len(res["veo_prompt"]) > 10)

    def test_05_server_mocap_api_endpoints(self):
        """Verify server POST /api/mocap/extract_motion & /api/mocap/apply_to_actor."""
        url_extract = "http://localhost:8080/api/mocap/extract_motion"
        payload_extract = json.dumps({"start_sec": 0.0, "end_sec": 1.0, "sample_fps": 5}).encode('utf-8')
        req = urllib.request.Request(url_extract, data=payload_extract, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get("success"))
            self.assertIn("acting_direction", data)

        # Test apply to actor
        url_apply = "http://localhost:8080/api/mocap/apply_to_actor"
        payload_apply = json.dumps({
            "character_id": "test_idol_e2e",
            "motion_data": data
        }).encode('utf-8')
        req_apply = urllib.request.Request(url_apply, data=payload_apply, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req_apply, timeout=15) as resp:
            self.assertEqual(resp.status, 200)
            applied = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(applied.get("success"))
            self.assertEqual(applied.get("character_id"), "test_idol_e2e")
            self.assertEqual(applied.get("status"), "MOTION_TRANSFERRED_TO_ACTOR")

if __name__ == '__main__':
    unittest.main()
