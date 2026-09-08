"""
================================================================================
TEST SUITE: GENESIS TRANSPORT SHIELD (Phase 3)
Tests core/genesis_transport_shield_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_transport_shield_engine import transport_shield_engine

class TestGenesisTransportShield(unittest.TestCase):

    def test_01_coercion_and_obstruction_detection(self):
        text = "土下座しろ！運賃タダにしろ！会社に電話してクビにしてやるぞ！"
        res = transport_shield_engine.analyze_speech_and_harassment("DRV-8821", text, "TAXI-304")
        self.assertEqual(res["status"], "HARASSMENT_ANALYSIS_COMPLETE")
        self.assertTrue(res["is_harassment"])
        self.assertEqual(res["severity"], "CRITICAL")
        
        statutes = [c["statute"] for c in res["detected_violations"]]
        self.assertTrue(any("強要罪" in s for s in statutes))
        self.assertTrue(any("威力業務妨害罪" in s for s in statutes))
        self.assertIn("土下座", str(res["detected_violations"]))
        print(f"🚨 Coercion/Obstruction Detection: {statutes} | Severity: {res['severity']}")

    def test_02_threat_to_life_detection(self):
        text = "殺すぞ！タダじゃおかないからな！後悔させてやる！"
        res = transport_shield_engine.analyze_speech_and_harassment("DRV-8821", text, "TAXI-304")
        self.assertEqual(res["severity"], "CRITICAL")
        statutes = [c["statute"] for c in res["detected_violations"]]
        self.assertTrue(any("脅迫罪" in s for s in statutes))
        self.assertTrue(len(res["in_vehicle_audio_warning"]) > 0)
        print(f"🚨 Threat Detection: {statutes} | Audio Warning: {res['in_vehicle_audio_warning']}")

    def test_03_refusal_to_exit_detection(self):
        text = "降りてやるもんか、警察でも呼べ！"
        res = transport_shield_engine.analyze_speech_and_harassment("DRV-8821", text, "TAXI-304")
        self.assertEqual(res["severity"], "HIGH")
        statutes = [c["statute"] for c in res["detected_violations"]]
        self.assertTrue(any("不退去罪" in s for s in statutes))
        print(f"⚠️ Unlawful Refusal Detection: {statutes}")

    def test_04_safe_normal_conversation(self):
        text = "次の交差点を右にお願いします。ありがとうございます。"
        res = transport_shield_engine.analyze_speech_and_harassment("DRV-8821", text, "TAXI-304")
        self.assertFalse(res["is_harassment"])
        self.assertEqual(res["severity"], "SAFE")
        self.assertEqual(len(res["detected_violations"]), 0)
        print("🟢 Safe Passenger Interaction: Verified")

    def test_05_damages_calculation_and_notice(self):
        # 45 minutes delay with CRITICAL severity
        res = transport_shield_engine.calculate_legal_damages(delay_minutes=45, severity_level="CRITICAL", cleaning_required=False)
        self.assertEqual(res["status"], "DAMAGES_CALCULATED")
        
        # Expected: (45/60 * 6500) = 4875 (biz loss) + 50000 (consolation) + 10000 (legal admin) = 64875
        self.assertEqual(res["damage_breakdown"]["business_opportunity_loss_yen"], 4875)
        self.assertEqual(res["damage_breakdown"]["mental_consolation_money_yen"], 50000)
        self.assertEqual(res["total_compensation_amount_yen"], 64875)
        self.assertIn("民法第709条", res["statutory_basis"])
        self.assertIn("64,875", res["billing_notice_text"])
        print(f"💰 Legal Damages Calculated: {res['total_compensation_amount_yen']:,} Yen")

if __name__ == "__main__":
    unittest.main()
