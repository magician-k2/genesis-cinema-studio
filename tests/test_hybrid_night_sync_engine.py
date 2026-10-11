#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for GenesisHybridNightSyncEngine
"""

import unittest
import json
from pathlib import Path
from core.genesis_hybrid_night_sync_engine import GenesisHybridNightSyncEngine

class TestGenesisHybridNightSyncEngine(unittest.TestCase):

    def setUp(self):
        self.engine = GenesisHybridNightSyncEngine()

    def test_stage_1_pc_ambient_harvest(self):
        res = self.engine.stage_1_pc_ambient_harvest()
        self.assertEqual(res["phase"], "PC_AMBIENT_HARVEST")
        self.assertFalse(res["gpu_required"])
        self.assertEqual(res["token_cost"], 0.00)
        self.assertTrue(res["batch_id"].startswith("night_batch_"))

    def test_stage_2_colab_pro_batch_dispatch(self):
        harvest_data = {
            "batch_id": "test_batch_12345",
            "items": [{"filename": "sample.pdf", "sha256": "dummy"}]
        }
        res = self.engine.stage_2_colab_pro_batch_dispatch(harvest_data)
        self.assertEqual(res["status"], "DISPATCHED")
        self.assertEqual(res["job_id"], "test_batch_12345")
        self.assertEqual(res["token_cost"], 0.00)
        self.assertTrue(Path(res["job_path"]).exists())
        # Clean up test job file
        Path(res["job_path"]).unlink(missing_ok=True)

    def test_stage_3_mobile_edge_sleep_sync(self):
        res = self.engine.stage_3_mobile_edge_sleep_sync(active_neurons=10000)
        self.assertEqual(res["phase"], "MOBILE_EDGE_SLEEP_SYNC")
        self.assertIn("Delta w = A_+ * exp(-Delta t / tau_+)", res["stdp_plasticity_update"]["formula"])
        self.assertGreater(res["stdp_plasticity_update"]["delta_w"], 0.0)
        self.assertIn("F = D_KL", res["variational_free_energy"]["formula"])
        self.assertEqual(res["token_cost"], 0.00)

    def test_stage_4_morning_rehydration(self):
        res = self.engine.stage_4_morning_rehydration("test_batch_rehydrate")
        self.assertEqual(res["status"], "ALL_GREEN_READY_FOR_USER")
        self.assertEqual(res["google_drive_parity"], "100%")
        self.assertEqual(res["total_token_cost"], 0.00)

    def test_full_night_cycle(self):
        cycle_res = self.engine.run_full_night_cycle()
        self.assertTrue(cycle_res["success"])
        self.assertEqual(cycle_res["total_token_cost"], 0.00)
        self.assertIn("Colab Pro", cycle_res["colab_tier_target"])


if __name__ == "__main__":
    unittest.main()
