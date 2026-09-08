"""
Unit tests for Sleep Sync & Verified Storage Consolidator & Feature Router (12 Tests)
"""

import unittest
from core.sleep_sync_storage_consolidator import SleepSyncStorageConsolidator
from core.feature_workspace_router import FeatureWorkspaceRouter

class TestSleepSyncStorageConsolidator(unittest.TestCase):
    def setUp(self):
        self.sleep_consolidator = SleepSyncStorageConsolidator()
        self.router = FeatureWorkspaceRouter()

    def test_01_on_system_sleep_triggered(self):
        res = self.sleep_consolidator.on_system_sleep_triggered()
        self.assertEqual(res["status"], "SLEEP_SYNC_COMPLETED_OPTIMAL")
        self.assertGreater(res["synced_files_count"], 0)

    def test_02_consolidate_verified_local_data(self):
        res = self.sleep_consolidator.consolidate_verified_local_data(3)
        self.assertEqual(res["status"], "LOCAL_STORAGE_CONSOLIDATION_OPTIMAL")
        self.assertEqual(res["verification_copies"], 3)
        self.assertTrue(res["sha256_verified"])

    def test_03_reclaimed_local_mb(self):
        res = self.sleep_consolidator.consolidate_verified_local_data()
        self.assertGreater(res["reclaimed_local_mb"], 0.0)

    def test_04_sleep_sync_history_logging(self):
        self.sleep_consolidator.on_system_sleep_triggered()
        self.assertEqual(len(self.sleep_consolidator.sleep_sync_history), 1)

    def test_05_consolidation_history_logging(self):
        self.sleep_consolidator.consolidate_verified_local_data()
        self.assertEqual(len(self.sleep_consolidator.consolidation_history), 1)

    def test_06_route_feature_artifacts_to_cloud(self):
        res = self.router.route_feature_artifacts_to_cloud()
        self.assertEqual(res["status"], "FEATURE_WORKSPACE_ROUTING_OPTIMAL")
        self.assertEqual(res["feature_map_count"], 8)

    def test_07_feature_workspace_chat_archives_included(self):
        self.assertIn("chat_notebook_archives", self.router.feature_map)

    def test_08_feature_workspace_suno_music_included(self):
        self.assertIn("suno_music", self.router.feature_map)

    def test_09_feature_workspace_esl_learning_included(self):
        self.assertIn("esl_learning", self.router.feature_map)

    def test_10_feature_workspace_bci_telepathy_included(self):
        self.assertIn("bci_telepathy", self.router.feature_map)

    def test_11_feature_workspace_routing_logs(self):
        self.router.route_feature_artifacts_to_cloud()
        self.assertEqual(len(self.router.routing_logs), 1)

    def test_12_cloud_base_directory_verification(self):
        res = self.router.route_feature_artifacts_to_cloud()
        self.assertIn("cloud_workspaces", res["cloud_base_directory"])

if __name__ == "__main__":
    unittest.main()
