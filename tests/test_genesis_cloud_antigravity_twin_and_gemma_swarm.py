# -*- coding: utf-8 -*-
"""
================================================================================
TEST SUITE: GENESIS CLOUD ANTIGRAVITY TWIN & GEMMA 4 NEURAL ORGANS
(tests/test_genesis_cloud_antigravity_twin_and_gemma_swarm.py)
================================================================================
"""

import unittest
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_cloud_antigravity_twin_syncer import cloud_antigravity_syncer
from core.genesis_gemma_neural_organ_orchestrator import gemma_organ_orchestrator

class TestGenesisCloudAntigravityTwinAndGemmaSwarm(unittest.TestCase):

    def test_01_cloud_antigravity_twin_sync(self):
        """ローカル✕クラウド Antigravity デジタルツイン同期の検証"""
        sync_res = cloud_antigravity_syncer.sync_chat_chronicles_and_memory()
        self.assertEqual(sync_res.get("status"), "TWIN_SYNC_COMPLETE")
        self.assertTrue(sync_res.get("digital_twin_ready"))
        self.assertGreaterEqual(sync_res.get("synced_conversations", 0), 0)

        # SDK整合性チェック
        sdk_res = cloud_antigravity_syncer.verify_sdk_version_alignment()
        self.assertEqual(sdk_res.get("status"), "SDK_ALIGNED")
        self.assertFalse(sdk_res.get("version_mismatch"))

    def test_02_gemma_neural_organ_pipeline(self):
        """Gemma 4 脳器官クラスター（視床・扁桃体・海馬・MAGI・新皮質）の超低遅延協調動作"""
        task_prompt = "新機能：救急搬送トリアージAIのコードを生成して"
        pipeline_res = gemma_organ_orchestrator.dispatch_neural_pipeline(task_prompt)
        
        self.assertEqual(pipeline_res.get("status"), "NEURAL_PIPELINE_RESOLVED")
        self.assertEqual(pipeline_res.get("organs_activated_count"), 6)
        self.assertTrue(pipeline_res.get("sub_300ms_guarantee"))
        self.assertLess(pipeline_res.get("total_latency_ms"), 300.0)

        # クラスターステータス
        cluster_status = gemma_organ_orchestrator.get_organ_cluster_status()
        self.assertEqual(cluster_status.get("cluster_state"), "ALL_ORGANS_ACTIVE_100_PERCENT_GREEN")
        self.assertEqual(cluster_status.get("total_organs"), 6)

        # Google Drive正本保存の確認
        self.assertIn("saved_path", pipeline_res)
        self.assertTrue(os.path.exists(pipeline_res["saved_path"]))

if __name__ == "__main__":
    unittest.main()
