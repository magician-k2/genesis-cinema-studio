"""
================================================================================
TEST SUITE: GENESIS REHAB MOTION & CARE WATCHDOG ENGINES (Phase 2)
Tests core/genesis_rehab_motion_engine.py and core/genesis_care_watchdog_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_rehab_motion_engine import rehab_motion_engine
from core.genesis_care_watchdog_engine import care_watchdog_engine

class TestGenesisRehabAndCare(unittest.TestCase):

    def test_01_rehab_3d_angle_calculation(self):
        # 90-degree right angle (hip, knee, ankle)
        hip = (0.0, 1.0)
        knee = (0.0, 0.0)
        ankle = (1.0, 0.0)
        angle = rehab_motion_engine.calculate_angle_3d(hip, knee, ankle)
        self.assertEqual(angle, 90.0)

    def test_02_rehab_normal_exercise_analysis(self):
        landmarks = {
            "hip": (0.5, 0.6),
            "knee": (0.65, 0.6),
            "ankle": (0.75, 0.6),  # Well extended
            "shoulder": (0.5, 0.4),
            "ear": (0.5, 0.25)     # Straight posture
        }
        res = rehab_motion_engine.analyze_exercise_frame("knee_extension", landmarks, "P-102")
        self.assertEqual(res["status"], "ANALYSIS_SUCCESS")
        self.assertGreaterEqual(res["score"], 70)
        self.assertIn("guidance_audio_text", res)
        print(f"✅ Rehab Normal Score: {res['score']} | Guidance: {res['guidance_audio_text']}")

    def test_03_rehab_compensation_detection(self):
        landmarks = {
            "hip": (0.5, 0.6),
            "knee": (0.65, 0.6),
            "ankle": (0.75, 0.6),
            "shoulder": (0.4, 0.4),
            "ear": (0.35, 0.25)    # Leaning back heavily (Trunk Tilt > 15 deg)
        }
        res = rehab_motion_engine.analyze_exercise_frame("knee_extension", landmarks, "P-102")
        self.assertEqual(res["status"], "ANALYSIS_SUCCESS")
        self.assertTrue(len(res["compensatory_movements"]) > 0)
        print(f"⚠️ Rehab Compensation Alert: {res['compensatory_movements']}")

    def test_04_care_voice_quality_empathy(self):
        text = "佐藤様、大丈夫ですか？ゆっくりでいいですよ、お手伝いしますね。"
        res = care_watchdog_engine.analyze_staff_interaction("STAFF-001", text, "P-102")
        self.assertEqual(res["status"], "CARE_INTERACTION_EVALUATED")
        self.assertGreaterEqual(res["score"], 88)
        self.assertEqual(res["rating"], "EXCELLENT")
        self.assertEqual(res["alert_level"], "NORMAL")
        print(f"🌸 Care Empathy Score: {res['score']} | Rating: {res['rating']}")

    def test_05_care_voice_inappropriate_cues(self):
        text = "ちょっと待ってて！動かないでって言ったでしょ！"
        res = care_watchdog_engine.analyze_staff_interaction("STAFF-004", text, "P-102")
        self.assertEqual(res["alert_level"], "WARNING")
        self.assertIn("動かないで", res["detected_risk_cues"])
        print(f"🚨 Inappropriate Care Alert: {res['detected_risk_cues']} | Feedback: {res['feedback']}")

    def test_06_care_fall_risk_and_emergency_dispatch(self):
        # 1. Stable
        res_safe = care_watchdog_engine.analyze_bed_posture_and_fall_risk("P-102", "lying_stable", {})
        self.assertEqual(res_safe["severity"], "SAFE")
        self.assertFalse(res_safe["emergency_dispatch_triggered"])

        # 2. Unstable standing attempt (Fall imminent)
        res_critical = care_watchdog_engine.analyze_bed_posture_and_fall_risk("P-102", "unstable_standing", {})
        self.assertEqual(res_critical["severity"], "CRITICAL")
        self.assertTrue(res_critical["emergency_dispatch_triggered"])
        self.assertIsNotNone(res_critical["assigned_first_responder"])
        print(f"🚨 Fall Emergency Dispatch Triggered: {res_critical['assigned_first_responder']}")

if __name__ == "__main__":
    unittest.main()
