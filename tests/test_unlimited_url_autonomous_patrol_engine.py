"""
Unit tests for Unlimited URL Autonomous Patrol & Diff-Learning Engine (12 Tests)
"""

import unittest
from core.unlimited_url_autonomous_patrol_engine import UnlimitedUrlAutonomousPatrolEngine

class TestUnlimitedUrlAutonomousPatrolEngine(unittest.TestCase):
    def setUp(self):
        self.engine = UnlimitedUrlAutonomousPatrolEngine()

    def test_01_register_patrol_url(self):
        res = self.engine.register_patrol_url("https://ai.google.dev", "AI_DOCS", 4.0)
        self.assertEqual(res["status"], "PATROL_URL_REGISTERED_AND_INGESTED")
        self.assertEqual(res["total_registered_urls"], 1)

    def test_02_first_pass_full_ingestion(self):
        res = self.engine.register_patrol_url("https://note.com/google_gemini", "GEMINI_BLOG")
        first_pass = res["first_pass_result"]
        self.assertEqual(first_pass["status"], "FIRST_PASS_FULL_INGESTION_SUCCESS")
        self.assertEqual(first_pass["chunks_absorbed"], 120)

    def test_03_execute_scheduled_patrol_diff_check(self):
        self.engine.register_patrol_url("https://example.com/ai")
        res = self.engine.execute_scheduled_patrol_diff_check()
        self.assertEqual(res["status"], "PATROL_DIFF_CYCLE_OPTIMAL")
        self.assertTrue(res["all_deltas_auto_learned"])

    def test_04_multiple_unlimited_url_registrations(self):
        self.engine.register_patrol_url("https://url1.com")
        self.engine.register_patrol_url("https://url2.com")
        self.engine.register_patrol_url("https://url3.com")
        self.assertEqual(len(self.engine.registered_urls), 3)

    def test_05_cortex_nodes_synapsed_count(self):
        res = self.engine.register_patrol_url("https://url1.com")
        self.assertEqual(res["first_pass_result"]["cortex_nodes_synapsed"], 10787)

    def test_06_diff_detected_count_reflection(self):
        self.engine.register_patrol_url("https://url1.com")
        self.engine.register_patrol_url("https://url2.com")
        res = self.engine.execute_scheduled_patrol_diff_check()
        self.assertEqual(res["diff_detected_count"], 2)

    def test_07_patrol_logs_accumulation(self):
        self.engine.register_patrol_url("https://url1.com")
        self.engine.execute_scheduled_patrol_diff_check()
        self.engine.execute_scheduled_patrol_diff_check()
        self.assertEqual(len(self.engine.patrol_logs), 2)

    def test_08_url_id_format(self):
        res = self.engine.register_patrol_url("https://test.com")
        self.assertTrue(res["url_id"].startswith("url_"))

    def test_09_japanese_status_presence(self):
        self.engine.register_patrol_url("https://test.com")
        res = self.engine.execute_scheduled_patrol_diff_check()
        self.assertIn("巡回完了", res["japanese_status"])

    def test_10_first_pass_error_handling(self):
        res = self.engine.execute_first_pass_full_ingestion("non_existent_url_id")
        self.assertEqual(res["status"], "ERROR_URL_NOT_FOUND")

    def test_11_patrol_interval_hours_stored(self):
        res = self.engine.register_patrol_url("https://test.com", "TECH", 12.0)
        record = self.engine.registered_urls[res["url_id"]]
        self.assertEqual(record["interval_hours"], 12.0)

    def test_12_total_knowledge_chunks_growth(self):
        res = self.engine.register_patrol_url("https://test.com")
        initial_chunks = self.engine.registered_urls[res["url_id"]]["total_knowledge_chunks"]
        self.engine.execute_scheduled_patrol_diff_check()
        updated_chunks = self.engine.registered_urls[res["url_id"]]["total_knowledge_chunks"]
        self.assertGreater(updated_chunks, initial_chunks)

if __name__ == "__main__":
    unittest.main()
