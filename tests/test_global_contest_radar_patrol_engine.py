"""
Unit tests for Global Contest Radar Patrol Engine (12 Tests)
"""

import unittest
from core.global_contest_radar_patrol_engine import GlobalContestRadarPatrolEngine

class TestGlobalContestRadarPatrolEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GlobalContestRadarPatrolEngine()

    def test_01_execute_contest_radar_patrol(self):
        res = self.engine.execute_contest_radar_patrol()
        self.assertEqual(res["status"], "CONTEST_RADAR_PATROL_OPTIMAL")
        self.assertTrue(res["all_opportunities_matched"])

    def test_02_portals_monitored_count(self):
        self.assertGreaterEqual(len(self.engine.monitored_contest_portals), 6)

    def test_03_google_startups_portal_monitored(self):
        self.assertTrue(any("Google for Startups" in p["name"] for p in self.engine.monitored_contest_portals))

    def test_04_xprize_portal_monitored(self):
        self.assertTrue(any("XPRIZE" in p["name"] for p in self.engine.monitored_contest_portals))

    def test_05_opportunities_harvested_count(self):
        res = self.engine.execute_contest_radar_patrol()
        self.assertGreater(res["opportunities_harvested_count"], 0)

    def test_06_morning_routine_briefing(self):
        self.engine.execute_contest_radar_patrol()
        res = self.engine.get_morning_routine_contest_briefing()
        self.assertEqual(res["status"], "CONTEST_BRIEFING_READY")
        self.assertGreater(len(res["action_options_ready"]), 0)

    def test_07_matched_genesis_module_presence(self):
        self.engine.execute_contest_radar_patrol()
        opps = self.engine.harvested_opportunities
        self.assertTrue(any("GENESIS Core" in o["matched_genesis_module"] for o in opps))

    def test_08_xprize_matched_module_presence(self):
        self.engine.execute_contest_radar_patrol()
        opps = self.engine.harvested_opportunities
        self.assertTrue(any("SLA Second Language" in o["matched_genesis_module"] for o in opps))

    def test_09_radar_id_format(self):
        res = self.engine.execute_contest_radar_patrol()
        self.assertTrue(res["radar_id"].startswith("contest_radar_"))

    def test_10_devpost_portal_monitored(self):
        self.assertTrue(any("Devpost" in p["name"] for p in self.engine.monitored_contest_portals))

    def test_11_japanese_status_presence(self):
        res = self.engine.execute_contest_radar_patrol()
        self.assertIn("巡回完了", res["japanese_status"])

    def test_12_top_recommendation_presence(self):
        self.engine.execute_contest_radar_patrol()
        res = self.engine.get_morning_routine_contest_briefing()
        self.assertIn("Google for Startups Cloud", res["top_recommendation"])

if __name__ == "__main__":
    unittest.main()
