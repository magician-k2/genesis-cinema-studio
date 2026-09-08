"""
================================================================================
TEST SUITE: GENESIS NIGHT AUDIT & MORNING SAFETY GATE
Tests core/genesis_night_audit_engine.py
================================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_mainframe_core import mainframe
from core.genesis_night_audit_engine import night_audit_engine

class TestGenesisNightAudit(unittest.TestCase):

    def test_01_run_night_triple_audit(self):
        report = night_audit_engine.run_night_triple_audit()
        self.assertEqual(report["status"], "NIGHT_AUDIT_COMPLETED")
        self.assertGreaterEqual(len(report["incidents_detected"]), 1)
        self.assertEqual(len(report["morning_quizzes"]), 3)
        self.assertIn("saved_path", report)
        self.assertTrue(os.path.exists(report["saved_path"]))
        print(f"✅ Night Audit Output: {report['saved_path']}")

    def test_02_get_morning_quiz(self):
        quiz_data = night_audit_engine.get_morning_quiz("STAFF-004")
        self.assertEqual(quiz_data["staff_id"], "STAFF-004")
        self.assertEqual(len(quiz_data["quizzes"]), 3)
        for q in quiz_data["quizzes"]:
            self.assertIn("question", q)
            self.assertEqual(len(q["options"]), 4)
            self.assertIn("correct_index", q)
            self.assertIn("explanation", q)

    def test_03_submit_quiz_failure_locks_system(self):
        # Deliberately submit wrong answers [0, 0, 0]
        sub_res = night_audit_engine.evaluate_quiz_submission("STAFF-004", [0, 0, 0])
        self.assertFalse(sub_res["passed"])
        self.assertIn("不合格", sub_res["message"])
        
        # Verify access still locked
        auth = mainframe.verify_staff_access("STAFF-004")
        self.assertFalse(auth["authorized"])

    def test_04_submit_quiz_success_unlocks_system(self):
        # Extract correct answers from current quiz
        correct_indices = [q["correct_index"] for q in night_audit_engine.current_morning_quizzes]
        self.assertEqual(len(correct_indices), 3)

        # Submit perfect answers
        sub_res = night_audit_engine.evaluate_quiz_submission("STAFF-004", correct_indices)
        self.assertTrue(sub_res["passed"])
        self.assertEqual(sub_res["score"], "3/3")
        self.assertIn("全問正解", sub_res["message"])

        # Verify access unlocked
        auth = mainframe.verify_staff_access("STAFF-004")
        self.assertTrue(auth["authorized"])
        self.assertEqual(auth["score"], "3/3")
        print(f"✅ STAFF-004 Access Unlocked: {auth}")

if __name__ == "__main__":
    unittest.main()
