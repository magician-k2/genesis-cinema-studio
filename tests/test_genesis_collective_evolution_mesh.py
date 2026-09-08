# -*- coding: utf-8 -*-
"""
================================================================================
TEST SUITE: GENESIS COLLECTIVE EVOLUTION & COMPUTE SHARING MESH
(tests/test_genesis_collective_evolution_mesh.py)
================================================================================
"""

import unittest
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.genesis_collective_evolution_mesh import collective_evolution_mesh

class TestGenesisCollectiveEvolutionMesh(unittest.TestCase):

    def test_01_privacy_preserving_telemetry_and_iq_growth(self):
        """個人情報ゼロでメタ操作データのみを記録し、機械脳の集合知IQが上昇することを検証"""
        initial_status = collective_evolution_mesh.get_mesh_status()
        initial_events = initial_status["evolution_level"]["total_events"]
        initial_iq = initial_status["evolution_level"]["collective_iq"]

        # ワークフロー操作メタデータを記録
        res = collective_evolution_mesh.record_usage_telemetry(
            organ_name="EBOOK_APP",
            action_type="GENERATE_COMBINED_APP",
            latency_ms=45.2,
            success=True,
            next_organ="DUAL_AI_ALT"
        )
        self.assertEqual(res.get("status"), "TELEMETRY_INGESTED")
        self.assertEqual(res.get("privacy_status"), "100% ANONYMIZED_ZERO_PERSONAL_DATA")

        # 進化レベルの更新確認
        updated_status = collective_evolution_mesh.get_mesh_status()
        self.assertGreater(updated_status["evolution_level"]["total_events"], initial_events)
        self.assertGreaterEqual(updated_status["evolution_level"]["collective_iq"], initial_iq)

    def test_02_node_registration_and_heartbeat(self):
        """空き計算ノードの登録と生存確認"""
        res = collective_evolution_mesh.register_or_heartbeat_node(
            node_id="node_rtx4090_test_user",
            device_type="Desktop PC (RTX 4090)",
            idle_capacity_pct=85.0
        )
        self.assertEqual(res.get("status"), "NODE_UPDATED")
        node = res.get("node", {})
        self.assertEqual(node.get("node_id"), "node_rtx4090_test_user")
        self.assertEqual(node.get("status"), "AVAILABLE")

    def test_03_request_compute_rental_and_credits_reward(self):
        """重いタスク（2時間テクノDJミックス）のオンデマンド分散配分とクレジット付与"""
        rental_res = collective_evolution_mesh.request_compute_rental(
            task_name="2_HOUR_90S_JAPANESE_TECHNO_MIX_RENDER",
            required_flops_level="HIGH",
            estimated_duration_sec=12
        )
        self.assertEqual(rental_res.get("status"), "COMPUTE_RENTED_SUCCESS")
        self.assertIn("transaction_id", rental_res)
        self.assertGreater(rental_res.get("credits_rewarded_to_host", 0), 0)
        self.assertIsNotNone(rental_res.get("assigned_node"))

    def test_04_mesh_aggregate_metrics(self):
        """メッシュ全体の集合知指標と分散リソース総量の集計"""
        status = collective_evolution_mesh.get_mesh_status()
        self.assertIn("evolution_level", status)
        self.assertGreater(status.get("total_nodes_registered", 0), 0)
        self.assertGreater(status.get("total_credits_circulated", 0), 0)

if __name__ == "__main__":
    unittest.main()
