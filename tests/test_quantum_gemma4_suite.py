"""
⚛️ Q-Gemma 4 Quantum Optimization Test Suite (tests/test_quantum_gemma4_suite.py)
Tests:
1. SQA QUBO Mathematical Convergence
2. NLE Video Timeline Quantum Cut Optimization API (/api/quantum/optimize_timeline)
3. 3D Pose Bone Collision Resolution API (/api/quantum/optimize_3d_pose)
4. Dual-AI Code AST Verification API (/api/quantum/code_assist)
5. MMKG Multimodal Knowledge Graph Quantum Node Traversal
"""

import unittest
import json
import urllib.request
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.quantum_gemma4_engine import QuantumGemma4Engine
from GENESIS_CINEMA_STUDIO.multimodal_knowledge_graph import MultimodalKnowledgeGraph

class TestQuantumGemma4Suite(unittest.TestCase):
    def setUp(self):
        self.engine = QuantumGemma4Engine(num_trotter_slices=8)
        self.base_url = "http://localhost:8080"

    def test_01_sqa_qubo_solver_convergence(self):
        # Minimize: E = -2*s0 - 3*s1 + 4*s0*s1
        Q = {(0, 0): -2.0, (1, 1): -3.0, (0, 1): 4.0}
        state, energy = self.engine.solve_qubo(Q, 2, steps=100)
        self.assertIn(state, [[0, 1], [1, 0]]) # Optimum is s1=1, s0=0 -> E=-3.0
        self.assertLessEqual(energy, -2.0)

    def test_02_timeline_cuts_optimization(self):
        clips = [
            {"id": "clip_1", "duration": 4.0, "shot_type": "Wide", "score": 0.95},
            {"id": "clip_2", "duration": 2.0, "shot_type": "CloseUp", "score": 0.85},
            {"id": "clip_3", "duration": 4.0, "shot_type": "CloseUp", "score": 0.60},
            {"id": "clip_4", "duration": 6.0, "shot_type": "Drone", "score": 0.90},
        ]
        res = self.engine.optimize_timeline_cuts(clips, target_duration_sec=16.0, bpm=120.0)
        self.assertTrue(res["success"])
        self.assertEqual(res["engine"], "Q-Gemma 4 SQA (Simulated Quantum Annealing)")
        self.assertGreater(len(res["selected_clips"]), 0)
        self.assertLess(res["latency_ms"], 50.0)

    def test_03_api_optimize_timeline(self):
        payload = {
            "clips": [
                {"id": "shot_a", "duration": 4.0, "shot_type": "Wide", "score": 0.9},
                {"id": "shot_b", "duration": 2.0, "shot_type": "Medium", "score": 0.88}
            ],
            "target_duration_sec": 6.0,
            "bpm": 120.0
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/quantum/optimize_timeline",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data["success"])
            self.assertIn("selected_clips", data)

    def test_04_api_optimize_3d_pose(self):
        payload = {
            "joint_angles": [0.0, 0.5, -0.2, 1.2],
            "collision_pairs": [[0, 1], [2, 3]],
            "desired_pose_weights": [1.0, 1.0, 0.8, 0.9]
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/quantum/optimize_3d_pose",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data["success"])
            self.assertIn("optimized_state", data)

    def test_05_api_code_assist_verification(self):
        payload = {
            "symbols": ["QuantumGemma4Engine", "solve_qubo", "optimize_timeline_cuts"],
            "required_calls": ["solve_qubo", "optimize_timeline_cuts"]
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/quantum/code_assist",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data["valid"])
            self.assertEqual(data["confidence_score"], 1.0)
            self.assertIn("quantum_verification_hash", data)

    def test_06_mmkg_quantum_knowledge_graph(self):
        mmkg = MultimodalKnowledgeGraph()
        res = mmkg.query_graph("concept_quantum_annealing_sqa")
        self.assertGreater(len(res["matchedNodes"]), 0)
        names = [n["name"] for n in res["matchedNodes"]]
        self.assertTrue(any("量子" in n for n in names))

if __name__ == "__main__":
    unittest.main()
