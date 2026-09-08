"""
Unit tests for Hybrid Local & Cloud Dual Wall-Bounce Execution Engine (12 Tests)
"""

import unittest
from core.hybrid_local_cloud_wall_bounce_executor import HybridLocalCloudWallBounceExecutor

class TestHybridLocalCloudWallBounceExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = HybridLocalCloudWallBounceExecutor()

    def test_01_execute_dual_local_cloud_wall_bounce(self):
        res = self.executor.execute_dual_local_cloud_wall_bounce()
        self.assertEqual(res["status"], "HYBRID_LOCAL_CLOUD_WALL_BOUNCE_OPTIMAL")
        self.assertTrue(res["local_executed"])
        self.assertTrue(res["cloud_executed"])

    def test_02_dual_location_synced_flag(self):
        res = self.executor.execute_dual_local_cloud_wall_bounce()
        self.assertTrue(res["dual_location_synced"])

    def test_03_dual_execution_history_logging(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        self.assertEqual(len(self.executor.dual_execution_history), 1)

    def test_04_exec_id_format(self):
        res = self.executor.execute_dual_local_cloud_wall_bounce()
        self.assertTrue(res["exec_id"].startswith("hybrid_wb_"))

    def test_05_local_execution_node_name(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]["local_execution"]
        self.assertEqual(rec["node"], "LOCAL_PC_STORAGE")

    def test_06_cloud_execution_node_name(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]["cloud_execution"]
        self.assertEqual(rec["node"], "GOOGLE_DRIVE_CLOUD_WORKSPACE")

    def test_07_cortex_nodes_tested_count_in_local(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]["local_execution"]
        self.assertEqual(rec["cortex_nodes_tested"], 10787)

    def test_08_cortex_nodes_tested_count_in_cloud(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]["cloud_execution"]
        self.assertEqual(rec["cortex_nodes_tested"], 10787)

    def test_09_cloud_sync_verified_flag(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]["cloud_execution"]
        self.assertTrue(rec["cloud_sync_verified"])

    def test_10_dual_location_parity_match(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]
        self.assertEqual(rec["dual_location_parity"], "100_PERCENT_MATCH")

    def test_11_multiple_executions_accumulate(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        self.executor.execute_dual_local_cloud_wall_bounce()
        self.assertEqual(len(self.executor.dual_execution_history), 2)

    def test_12_status_hybrid_dual_wall_bounce_success(self):
        self.executor.execute_dual_local_cloud_wall_bounce()
        rec = self.executor.dual_execution_history[0]
        self.assertEqual(rec["status"], "HYBRID_DUAL_WALL_BOUNCE_SUCCESS")

if __name__ == "__main__":
    unittest.main()
