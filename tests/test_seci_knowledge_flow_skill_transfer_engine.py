"""
Unit tests for SECI Knowledge Flow & Skill Transfer Engine (12 Tests)
"""

import unittest
from core.seci_knowledge_flow_skill_transfer_engine import SeciKnowledgeFlowSkillTransferEngine

class TestSeciKnowledgeFlowSkillTransferEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SeciKnowledgeFlowSkillTransferEngine()

    def test_01_execute_seci_spiral_cycle(self):
        res = self.engine.execute_seci_spiral_cycle("開発メモ")
        self.assertEqual(res["status"], "SECI_SKILL_TRANSFER_SUCCESS")
        self.assertTrue(res["tacit_to_explicit_converted"])

    def test_02_seci_stages_count(self):
        self.assertEqual(len(self.engine.seci_stages), 4)
        self.assertIn("1. Socialization (共同化)", self.engine.seci_stages)

    def test_03_socialization_stage_presence(self):
        res = self.engine.execute_seci_spiral_cycle("現場ログ")
        record = self.engine.transferred_skills_history[0]
        stages = record["seci_stages"]
        soc = next(s for s in stages if "Socialization" in s["stage"])
        self.assertTrue(soc["tacit_knowledge_detected"])

    def test_04_externalization_rules_generation(self):
        res = self.engine.execute_seci_spiral_cycle("現場ログ")
        record = self.engine.transferred_skills_history[0]
        stages = record["seci_stages"]
        ext = next(s for s in stages if "Externalization" in s["stage"])
        self.assertGreater(len(ext["explicit_rules_generated"]), 0)

    def test_05_combination_cortex_organs(self):
        res = self.engine.execute_seci_spiral_cycle("現場ログ")
        record = self.engine.transferred_skills_history[0]
        stages = record["seci_stages"]
        comb = next(s for s in stages if "Combination" in s["stage"])
        self.assertEqual(comb["cortex_organs_integrated"], 29)

    def test_06_internalization_mastery_rate(self):
        res = self.engine.execute_seci_spiral_cycle("現場ログ")
        record = self.engine.transferred_skills_history[0]
        stages = record["seci_stages"]
        intern = next(s for s in stages if "Internalization" in s["stage"])
        self.assertEqual(intern["cortex_mastery_rate"], "99.99%")

    def test_07_cortex_nodes_reinforced_count(self):
        res = self.engine.execute_seci_spiral_cycle("現場ログ")
        self.assertEqual(res["cortex_nodes_reinforced"], 10787)

    def test_08_human_augmentation_factor_metric(self):
        self.engine.execute_seci_spiral_cycle("スキルテスト")
        record = self.engine.transferred_skills_history[0]
        self.assertIn("10x", record["human_augmentation_factor"])

    def test_09_knowledge_base_status_active(self):
        res = self.engine.execute_seci_spiral_cycle("スキルテスト")
        self.assertEqual(res["knowledge_base_status"], "LIVING_VERIFIED_KNOWLEDGE_BASE_ACTIVE")

    def test_10_transferred_skills_history_logging(self):
        self.engine.execute_seci_spiral_cycle("Skill 1")
        self.engine.execute_seci_spiral_cycle("Skill 2")
        self.assertEqual(len(self.engine.transferred_skills_history), 2)

    def test_11_spiral_id_format(self):
        res = self.engine.execute_seci_spiral_cycle("IDテスト")
        self.assertTrue(res["spiral_id"].startswith("seci_spiral_"))

    def test_12_internalization_stage_name_check(self):
        self.assertTrue(any("Internalization" in s for s in self.engine.seci_stages))

if __name__ == "__main__":
    unittest.main()
