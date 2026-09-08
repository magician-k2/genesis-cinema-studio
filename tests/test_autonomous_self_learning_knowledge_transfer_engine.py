"""
Unit tests for Autonomous Self-Learning & Actionable Decision Transfer Engine (12 Tests)
"""

import unittest
from core.autonomous_self_learning_knowledge_transfer_engine import AutonomousSelfLearningKnowledgeTransferEngine

class TestAutonomousSelfLearningKnowledgeTransferEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AutonomousSelfLearningKnowledgeTransferEngine()

    def test_01_execute_autonomous_self_learning_cycle(self):
        res = self.engine.execute_autonomous_self_learning_cycle("量子AI専門書")
        self.assertEqual(res["status"], "AUTONOMOUS_SELF_LEARNING_OPTIMAL")
        self.assertEqual(res["cortex_nodes_reinforced"], 10787)

    def test_02_self_learning_internalization_score(self):
        res = self.engine.execute_autonomous_self_learning_cycle()
        self.assertGreater(res["internalization_depth_score"], 0.999)

    def test_03_generate_human_knowledge_transfer_options(self):
        res = self.engine.generate_human_knowledge_transfer_options("新規事業戦略")
        self.assertEqual(res["status"], "ACTIONABLE_KNOWLEDGE_TRANSFER_OPTIMAL")
        self.assertTrue(res["human_decision_empowered"])

    def test_04_options_count_exact(self):
        res = self.engine.generate_human_knowledge_transfer_options("新機能開発")
        self.assertEqual(res["options_count"], 3)

    def test_05_recommended_option_identifier(self):
        res = self.engine.generate_human_knowledge_transfer_options("インフラ設計")
        self.assertEqual(res["recommended_option"], "OPTION_B")

    def test_06_option_a_pragmatic_presence(self):
        self.engine.generate_human_knowledge_transfer_options("テストプラン")
        session = self.engine.transfer_sessions_history[0]
        options = session["actionable_decision_options"]
        self.assertTrue(any(o["option_id"] == "OPTION_A" for o in options))

    def test_07_option_b_architectural_recommended(self):
        self.engine.generate_human_knowledge_transfer_options("テストプラン")
        session = self.engine.transfer_sessions_history[0]
        options = session["actionable_decision_options"]
        opt_b = next(o for o in options if o["option_id"] == "OPTION_B")
        self.assertTrue(opt_b["recommended"])

    def test_08_option_c_disruptive_roi_presence(self):
        self.engine.generate_human_knowledge_transfer_options("テストプラン")
        session = self.engine.transfer_sessions_history[0]
        options = session["actionable_decision_options"]
        self.assertTrue(any(o["option_id"] == "OPTION_C" for o in options))

    def test_09_cognitive_load_reduction_metric(self):
        self.engine.generate_human_knowledge_transfer_options("認知負荷テスト")
        session = self.engine.transfer_sessions_history[0]
        self.assertIn("95%", session["cognitive_load_reduction"])

    def test_10_learned_domains_initial_count(self):
        self.assertGreaterEqual(self.engine.learned_domains_count, 14)

    def test_11_transfer_sessions_history_logging(self):
        self.engine.generate_human_knowledge_transfer_options("Topic 1")
        self.engine.generate_human_knowledge_transfer_options("Topic 2")
        self.assertEqual(len(self.engine.transfer_sessions_history), 2)

    def test_12_session_id_format(self):
        res = self.engine.generate_human_knowledge_transfer_options("IDテスト")
        self.assertTrue(res["session_id"].startswith("knowledge_transfer_"))

if __name__ == "__main__":
    unittest.main()
