"""
================================================================================
TEST SUITE: GENESIS MAINFRAME & CLINICAL DEMO ENGINE
Tests core/genesis_mainframe_core.py & core/genesis_clinical_demo_engine.py
================================================================================
"""

import os
import sys
import unittest
import time

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_mainframe_core import mainframe
from core.genesis_clinical_demo_engine import clinical_engine

class TestGenesisMainframeAndClinical(unittest.TestCase):
    
    def test_01_mainframe_initialization_and_mode(self):
        status = mainframe.get_cycle_status()
        self.assertIn("mode", status)
        self.assertEqual(status["mode"], "DAY_REALTIME")
        
        # Test mode switch
        res = mainframe.set_cycle_mode("NIGHT_AUDIT")
        self.assertEqual(res["mode"], "NIGHT_AUDIT")
        mainframe.set_cycle_mode("DAY_REALTIME")

    def test_02_reverse_mindmap_generation(self):
        graph = mainframe.generate_reverse_mindmap_xai(
            primary_conclusion="【照合一致】ワーファリン2mg",
            facts=[{"text": "カメラ読取: ワーファリン2mg", "source": "Camera"}],
            rules=[{"text": "5R原則", "authority": "JCQHC"}],
            confidence=0.995,
            action_item="投与実施"
        )
        self.assertIn("nodes", graph)
        self.assertIn("links", graph)
        self.assertGreaterEqual(len(graph["nodes"]), 3)
        self.assertGreaterEqual(len(graph["links"]), 2)
        self.assertEqual(graph["confidence"], 0.995)

    def test_03_staff_access_verification(self):
        # STAFF-001 is certified
        auth_001 = mainframe.verify_staff_access("STAFF-001")
        self.assertTrue(auth_001["authorized"])
        
        # STAFF-004 is initially locked
        auth_004 = mainframe.verify_staff_access("STAFF-004")
        self.assertFalse(auth_004["authorized"])

    def test_04_clinical_bedside_hud(self):
        t0 = time.time()
        res = clinical_engine.infer_bedside_patient("P-102")
        elapsed = time.time() - t0
        
        self.assertEqual(res["status"], "BEDSIDE_HUD_ACTIVE")
        self.assertEqual(res["patient"]["id"], "P-102")
        self.assertIn("vitals", res["patient"])
        self.assertIn("xai_tree", res)
        self.assertIn("guidance_audio", res)
        print(f"✅ Bedside HUD Latency: {round(elapsed*1000, 1)}ms (Internal: {res['latency_ms']}ms)")

    def test_05_medication_verification_safe_match(self):
        res = clinical_engine.verify_medication("P-102", "ワーファリン錠", "2mg")
        self.assertEqual(res["status"], "MEDICATION_VERIFIED")
        self.assertTrue(res["is_safe"])
        self.assertEqual(res["alert_level"], "GREEN")
        self.assertIn("xai_tree", res)

    def test_06_medication_verification_dangerous_mismatch(self):
        res = clinical_engine.verify_medication("P-102", "アスピリン 100mg", "100mg")
        self.assertEqual(res["status"], "MEDICATION_VERIFIED")
        self.assertFalse(res["is_safe"])
        self.assertEqual(res["alert_level"], "RED_CRITICAL")
        self.assertIn("🛑", res["message"])

    def test_07_emergency_dispatch(self):
        res = clinical_engine.dispatch_emergency("P-102", "血圧急低下・意識混濁", "STAFF-001")
        self.assertEqual(res["status"], "EMERGENCY_DISPATCH_TRIGGERED")
        self.assertEqual(res["alert_level"], "RED_FLASH")
        self.assertIn("assigned_responder", res)
        self.assertIn("protocol_guidance", res)

    def test_08_voice_ehr_parsing(self):
        sample_speech = "血圧138の84、脈拍76、体温36.8度、ワーファリン2mg確実に内服完了しました。"
        res = clinical_engine.parse_voice_ehr(sample_speech, "P-102")
        self.assertEqual(res["status"], "VOICE_EHR_RECORDED")
        self.assertIn("structured_vitals", res)
        self.assertIn("saved_path", res)
        self.assertTrue(os.path.exists(res["saved_path"]))

if __name__ == "__main__":
    unittest.main()
