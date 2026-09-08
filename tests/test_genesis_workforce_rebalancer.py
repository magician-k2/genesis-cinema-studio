"""
================================================================================
TEST SUITE: GENESIS WORKFORCE REBALANCER (Phase 4)
Tests core/genesis_workforce_rebalancer_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_workforce_rebalancer_engine import workforce_rebalancer_engine

class TestGenesisWorkforceRebalancer(unittest.TestCase):

    def test_01_ward_initial_schedule(self):
        res = workforce_rebalancer_engine.get_current_ward_schedule()
        self.assertIn("staffs", res)
        self.assertIn("patient_beds", res)
        self.assertEqual(len(res["staffs"]), 4)
        print(f"✅ Initial Ward Schedule Active Staff: {res['active_staff_count']}")

    def test_02_sudden_absence_multi_constraint_rebalance(self):
        res = workforce_rebalancer_engine.rebalance_on_sudden_absence(
            absent_staff_id="STAFF-004",
            reason="突発発熱 38.5℃ (急性咽頭炎)"
        )
        self.assertEqual(res["status"], "REBALANCE_COMPLETED")
        self.assertIn("STAFF-004", res["absent_staff"])
        
        # Verify Reassigned Ward Map
        ward_map = res["reassigned_ward_map"]
        self.assertIn("STAFF-001 (佐藤 結衣)", ward_map)
        self.assertIn("STAFF-003 (渡辺 健一 / 招集)", ward_map)
        
        # Verify Standby Summon Action
        actions = res["actions_taken"]
        call_in_action = next((a for a in actions if a["action"] == "EMERGENCY_CALL_IN"), None)
        self.assertIsNotNone(call_in_action)
        self.assertIn("渡辺 健一", call_in_action["target_staff"])
        
        # Verify GAS & AppSheet Payload
        gas_sync = res["gas_appsheet_sync"]
        self.assertEqual(gas_sync["event"], "SUDDEN_ABSENCE_REBALANCE")
        self.assertEqual(gas_sync["google_sheet_target"], "GENESIS_3F_Ward_Roster_Master")
        self.assertIn("渡辺 健一", gas_sync["calendar_event"])
        self.assertIn("AppSheet", str(gas_sync["appsheet_notification"]))
        
        print(f"🔄 0.3s Rebalance Complete: Latency {res['inference_time_ms']}ms | Standby Summoned: {call_in_action['target_staff']}")

if __name__ == "__main__":
    unittest.main()
