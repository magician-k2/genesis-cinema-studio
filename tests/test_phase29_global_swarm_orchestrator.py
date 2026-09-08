"""
Unit tests for Phase 29: Global Distributed Swarm Resonance Network & Offline-Resilient Local Intelligence (12 Tests)
"""

import unittest
from core.global_distributed_swarm_mesh import GlobalDistributedSwarmMesh
from core.offline_resilient_local_intelligence import OfflineResilientLocalIntelligence
from modules.phase29_global_swarm_orchestrator import Phase29GlobalSwarmOrchestrator

class TestPhase29GlobalSwarmOrchestrator(unittest.TestCase):
    def setUp(self):
        self.swarm_mesh = GlobalDistributedSwarmMesh()
        self.offline_intel = OfflineResilientLocalIntelligence()
        self.orchestrator = Phase29GlobalSwarmOrchestrator()

    def test_01_register_swarm_node(self):
        res = self.swarm_mesh.register_swarm_node("node_test_01", "TABLET_NPU", 8.0)
        self.assertEqual(res["status"], "SWARM_NODE_ACTIVE")
        self.assertEqual(res["compute_capacity_tflops"], 8.0)

    def test_02_synchronize_swarm_consensus(self):
        res = self.swarm_mesh.synchronize_swarm_consensus()
        self.assertEqual(res["status"], "GLOBAL_SWARM_CONSENSUS_OPTIMAL")
        self.assertEqual(res["consensus_score"], 0.999)

    def test_03_execute_offline_local_inference(self):
        res = self.offline_intel.execute_offline_local_inference("Edge OCR task")
        self.assertEqual(res["status"], "OFFLINE_LOCAL_INFERENCE_OPTIMAL")
        self.assertEqual(res["executor"], "Gemma4LowerSwarmWorker_4B")

    def test_04_offline_diff_staged_status(self):
        res = self.offline_intel.execute_offline_local_inference()
        self.assertTrue(res["diff_staged"])
        self.assertEqual(res["auto_sync"], "READY")

    def test_05_phase29_orchestrator_initialization(self):
        self.assertEqual(self.orchestrator.status, "INITIALIZED")

    def test_06_phase29_full_master_cycle(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertEqual(res["phase"], "PHASE_29_GLOBAL_DISTRIBUTED_SWARM_RESONANCE_OFFLINE_RESILIENT_INTELLIGENCE")
        self.assertTrue(res["all_green"])

    def test_07_global_swarm_mesh_verified_flag(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertTrue(res["global_swarm_mesh_verified"])

    def test_08_offline_resilient_intelligence_verified_flag(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertTrue(res["offline_resilient_intelligence_verified"])

    def test_09_p2p_consensus_verified_flag(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertTrue(res["p2p_consensus_verified_999"])

    def test_10_phase29_all_green_flag(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertTrue(res["all_green"])

    def test_11_initial_swarm_nodes_count(self):
        self.assertGreaterEqual(len(self.swarm_mesh.swarm_nodes), 3)

    def test_12_overall_status_phase29(self):
        res = self.orchestrator.execute_phase29_global_swarm_cycle()
        self.assertEqual(res["overall_status"], "PHASE29_GLOBAL_SWARM_OPTIMAL")

if __name__ == "__main__":
    unittest.main()
