"""
Unit tests for Phase 23 Extended Brain Organs Master Orchestrator (Gemma 4 Bound - 8 Tests)
"""

import unittest
from core.gemma4_bridge import Gemma4EngineBridge
from core.organs.angular_gyrus.angular_gyrus import AngularGyrusOrgan
from core.organs.retrosplenial_cortex.retrosplenial_cortex import RetrosplenialCortexOrgan
from core.organs.rlPFC.rlpfc_metacognition import RlPFCMetacognitionOrgan
from core.organs.sma_stg.sma_stg_auditory_motor import SMASTGAuditoryMotorOrgan
from modules.phase23_extended_brain_organs_orchestrator import Phase23ExtendedBrainOrgansOrchestrator

class TestPhase23ExtendedBrainOrgansOrchestrator(unittest.TestCase):
    def setUp(self):
        self.gemma4_bridge = Gemma4EngineBridge()
        self.ag_organ = AngularGyrusOrgan()
        self.rsc_organ = RetrosplenialCortexOrgan()
        self.rlpfc_organ = RlPFCMetacognitionOrgan()
        self.sma_organ = SMASTGAuditoryMotorOrgan()
        self.orchestrator = Phase23ExtendedBrainOrgansOrchestrator()

    def test_01_gemma4_bridge_status(self):
        self.assertEqual(self.gemma4_bridge.status, "GEMMA4_ONLINE")
        self.assertIn("Gemma-4", self.gemma4_bridge.model_version)

    def test_02_angular_gyrus_gemma4_bound(self):
        res = self.ag_organ.process_semantic_abstraction("Gemma 4 高度概念言語テスト", "ja")
        self.assertTrue(res["gemma4_bound"])
        self.assertEqual(res["cortex_memory_link_status"], "SYNAPSED_TO_GRIMOIRE_G_VIA_GEMMA4")

    def test_03_retrosplenial_cortex_gemma4_vision_bound(self):
        res = self.rsc_organ.transform_spatial_frame(["car_approaching_rear"])
        self.assertTrue(res["gemma4_bound"])
        self.assertEqual(res["hazard_risk_level"], "CRITICAL_HAZARD")

    def test_04_rlpfc_metacognition_gemma4_bound(self):
        res = self.rlpfc_organ.evaluate_knowledge_comprehension("Gemma 4 Deep Learning", ["Concept1", "Concept2"])
        self.assertTrue(res["gemma4_bound"])
        self.assertGreaterEqual(res["comprehension_score"], 80.0)

    def test_05_sma_stg_auditory_gemma4_bound(self):
        res = self.sma_organ.process_auditory_eeg_loop([440.0, 493.88], 0.8, 0.2)
        self.assertTrue(res["gemma4_bound"])
        self.assertIn("Gemma4 Music Prompt", res["gemma4_music_prompt"])

    def test_06_orchestrator_initialization(self):
        self.assertEqual(self.orchestrator.status, "INITIALIZED")

    def test_07_orchestrator_gemma4_synapse_loop(self):
        res = self.orchestrator.execute_all_brain_synaptic_loop()
        self.assertEqual(res["phase"], "PHASE_23_EXTENDED_BRAIN_ORGANS_GEMMA4_BOUND")
        self.assertTrue(res["gemma4_bound_verified"])
        self.assertTrue(res["all_green"])

    def test_08_all_brain_organs_synapsed_flag(self):
        res = self.orchestrator.execute_all_brain_synaptic_loop()
        self.assertTrue(res["all_brain_organs_synapsed"])

if __name__ == "__main__":
    unittest.main()
