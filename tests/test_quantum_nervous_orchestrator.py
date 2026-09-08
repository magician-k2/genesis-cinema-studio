# -*- coding: utf-8 -*-
"""
Full Test Suite for Quantum Nervous Orchestrator (Q-NO) & Server API Endpoints
"""

import unittest
import time
import os
import sys
import json
import io
from unittest.mock import MagicMock

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.quantum_nervous_orchestrator import QuantumNervousOrchestrator, QuantumOrganPulse
from GENESIS_CINEMA_STUDIO.server import GenesisCinemaHandler

class TestQuantumNervousOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = QuantumNervousOrchestrator()

    def test_default_organs_initialization(self):
        status = self.orchestrator.get_topology_status()
        self.assertGreaterEqual(status["organs_count"], 5)
        self.assertIn("CINEMA_STUDIO", status["organs"])
        self.assertIn("DEV_SYNTHESIZER", status["organs"])
        self.assertIn("CLOUD_RUNNER", status["organs"])
        self.assertIn("KNOWLEDGE_HIPPOCAMPUS", status["organs"])
        self.assertIn("THALAMUS_ROUTER", status["organs"])

    def test_register_new_organ(self):
        organ = self.orchestrator.register_organ(
            organ_id="MAGI_COUNCIL",
            name="3賢者合議審議院",
            location="HYBRID",
            capacity=3.0,
            latency_ms=15.0
        )
        self.assertEqual(organ["id"], "MAGI_COUNCIL")
        status = self.orchestrator.get_topology_status()
        self.assertIn("MAGI_COUNCIL", status["organs"])

    def test_edge_seed_registration(self):
        seed = self.orchestrator.register_edge_seed(
            node_id="ipad_pro_m2_01",
            device_type="TABLET_WEBGPU",
            gpu_vendor="APPLE_M2",
            latency_ms=4.2,
            battery_level=0.88
        )
        self.assertEqual(seed["node_id"], "ipad_pro_m2_01")
        status = self.orchestrator.get_topology_status()
        self.assertEqual(status["active_edge_seeds_count"], 1)

    def test_emit_pulse_and_routing(self):
        pulse = QuantumOrganPulse(
            source_organ="CINEMA_STUDIO",
            target_organ="KNOWLEDGE_HIPPOCAMPUS",
            action="CONSOLIDATE_FRAME_METADATA",
            payload={"frame_id": "shot_001_take_02", "confidence": 0.99},
            priority=2.0
        )
        res = self.orchestrator.emit_pulse(pulse)
        self.assertEqual(res["status"], "PULSE_FIRED")
        self.assertEqual(res["delivery"], "DELIVERED")
        
        status = self.orchestrator.get_topology_status()
        self.assertEqual(status["total_pulses"], 1)
        self.assertEqual(len(status["recent_pulses_sample"]), 1)
        self.assertEqual(status["organs"]["CINEMA_STUDIO"]["pulse_count"], 1)

    def test_qubo_workload_arbitration(self):
        tasks = [
            {"id": "task_4k_render", "title": "Heavy 4K Offline Render", "compute_weight": 5.0, "latency_critical": 0.1, "cloud_cost": 0.2},
            {"id": "task_ui_interaction", "title": "Live 60fps UI Layout", "compute_weight": 0.2, "latency_critical": 0.95, "cloud_cost": 0.8},
            {"id": "task_ast_verify", "title": "Real-time Code Syntax Check", "compute_weight": 0.5, "latency_critical": 0.8, "cloud_cost": 0.5, "dependencies": ["task_ui_interaction"]}
        ]
        res = self.orchestrator.arbitrate_workload(tasks)
        self.assertEqual(res["status"], "ARBITRATION_COMPLETE")
        self.assertEqual(res["num_tasks"], 3)
        self.assertEqual(len(res["assignments"]), 3)
        self.assertIn("energy", res)
        
        valid_destinations = {"WEBGPU_LOCAL_EDGE", "CLOUD_RUN"}
        for assign in res["assignments"]:
            self.assertIn(assign["allocated_to"], valid_destinations)

    def test_empty_tasks_arbitration(self):
        res = self.orchestrator.arbitrate_workload([])
        self.assertEqual(res["status"], "EMPTY_TASKS")
        self.assertEqual(len(res["assignments"]), 0)

    def test_server_qno_status_get(self):
        handler = GenesisCinemaHandler.__new__(GenesisCinemaHandler)
        handler.path = '/api/qno/status'
        handler.wfile = io.BytesIO()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()

        handler.do_GET()
        output_bytes = handler.wfile.getvalue()
        self.assertTrue(len(output_bytes) > 0)
        resp_json = json.loads(output_bytes.decode('utf-8'))
        self.assertIn("orchestrator_version", resp_json)
        self.assertIn("organs", resp_json)

if __name__ == "__main__":
    unittest.main()
