"""
Unit tests for ALL-GOOGLE Executive Agent Swarm Engine (12 Tests)
"""

import unittest
from core.all_google_executive_agent_swarm import AllGoogleExecutiveAgentSwarm

class TestAllGoogleExecutiveAgentSwarm(unittest.TestCase):
    def setUp(self):
        self.swarm = AllGoogleExecutiveAgentSwarm()

    def test_01_execute_all_google_executive_cycle(self):
        res = self.swarm.execute_all_google_executive_cycle()
        self.assertEqual(res["status"], "ALL_GOOGLE_SWARM_OPTIMAL")
        self.assertTrue(res["all_google_ecosystem_active"])

    def test_02_routine_agents_count(self):
        self.assertEqual(len(self.swarm.routine_agents), 3)
        self.assertIn("きょうの準備サマリー", self.swarm.routine_agents)

    def test_03_specialist_agents_count(self):
        self.assertEqual(len(self.swarm.specialist_agents), 13)

    def test_04_strategic_wall_bounce_agent_presence(self):
        self.assertTrue(any("戦略の壁打ち" in a for a in self.swarm.specialist_agents))

    def test_05_risk_assessment_agent_presence(self):
        self.assertTrue(any("反論・リスク検証" in a for a in self.swarm.specialist_agents))

    def test_06_revenue_pricing_agent_presence(self):
        self.assertTrue(any("収益モデル・価格設計" in a for a in self.swarm.specialist_agents))

    def test_07_google_calendar_synced_flag(self):
        res = self.swarm.execute_all_google_executive_cycle()
        log = self.swarm.execution_logs[0]
        self.assertTrue(log["routine_output"]["google_calendar_synced"])

    def test_08_total_google_services_linked_count(self):
        res = self.swarm.execute_all_google_executive_cycle()
        self.assertEqual(res["total_google_services_linked"], 11)

    def test_09_all_google_services_engaged_list(self):
        self.swarm.execute_all_google_executive_cycle()
        log = self.swarm.execution_logs[0]
        self.assertIn("Gemini 3.7 Flash", log["all_google_services_engaged"])
        self.assertIn("Google Pay", log["all_google_services_engaged"])
        self.assertIn("Google NotebookLM", log["all_google_services_engaged"])

    def test_10_execution_logs_accumulation(self):
        self.swarm.execute_all_google_executive_cycle("きょうの準備サマリー")
        self.swarm.execute_all_google_executive_cycle("きょうの振り返り")
        self.assertEqual(len(self.swarm.execution_logs), 2)

    def test_11_google_application_portfolio(self):
        res = self.swarm.get_google_application_portfolio()
        self.assertEqual(res["status"], "GOOGLE_APPLICATION_PORTFOLIO_OPTIMAL")
        apps = res["applications"]
        self.assertIn("program_1_startups_cloud", apps)
        self.assertIn("program_2_xprize_gemini", apps)
        self.assertIn("program_3_play_accelerator", apps)

    def test_12_all_google_ecosystem_verified_flag(self):
        self.assertTrue(self.swarm.all_google_ecosystem_verified)

if __name__ == "__main__":
    unittest.main()
