"""
================================================================================
TEST SUITE: REVERSE MINDMAP ENGINE & CAUSAL CONVERGENT MESH
Tests core/reverse_mindmap_engine.py
================================================================================
"""

import sys
import os
import unittest

sys.path.insert(0, r"g:\マイドライブ\GENESIS_ROOT")
from core.reverse_mindmap_engine import reverse_mindmap_engine

class TestReverseMindMapEngine(unittest.TestCase):

    def test_01_dag_structure_and_convergence(self):
        dag = reverse_mindmap_engine.get_preset_scenario("swe_bench_bug")
        self.assertIn("nodes", dag)
        self.assertIn("links", dag)
        self.assertIn("receipt", dag)
        self.assertGreaterEqual(len(dag["nodes"]), 5)
        self.assertGreaterEqual(len(dag["links"]), 4)

        # 中心核ノードの存在を検証
        core_nodes = [n for n in dag["nodes"] if n["layer"] == "core"]
        self.assertEqual(len(core_nodes), 1)
        self.assertEqual(core_nodes[0]["id"], "core_root_cause")

        # 外周ノードの存在を検証
        periphery_nodes = [n for n in dag["nodes"] if n["layer"] == "periphery"]
        self.assertEqual(len(periphery_nodes), 3)

        # 中間層ノードの存在を検証
        intermediate_nodes = [n for n in dag["nodes"] if n["layer"] == "intermediate"]
        self.assertEqual(len(intermediate_nodes), 2)

        # 全ての中間層ノードから中心核へリンクが向かっていることを検証（収束性）
        core_links = [l for l in dag["links"] if l["target"] == "core_root_cause"]
        self.assertEqual(len(core_links), len(intermediate_nodes))

    def test_02_receipt_generation_and_proof_hash(self):
        dag = reverse_mindmap_engine.get_preset_scenario("rescue_drone_3d")
        rcpt = dag["receipt"]
        self.assertTrue(rcpt["receipt_id"].startswith("RCPT-XAI-"))
        self.assertTrue(rcpt["proof_hash"].startswith("SHA256:"))
        self.assertGreater(rcpt["fly_brain_pruning_count"], 0)
        self.assertGreaterEqual(rcpt["confidence_score"], 0.99)
        self.assertEqual(len(rcpt["decision_breakdown"]), 3)

    def test_03_ast_callstack_reverse_tracing(self):
        sample_code = """
class DroneNavigator:
    def __init__(self):
        self.activeBypassUntilZ = -99999
        self.heading = 0.0

    def calculate_steering(self, position_z, target_heading):
        if position_z > self.activeBypassUntilZ:
            desired = 0.0 # BUG: Heading locked
        else:
            desired = target_heading
        return desired
"""
        res = reverse_mindmap_engine.trace_python_ast_callstack(sample_code, error_line=9, var_name="desired")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["enclosing_scope"], ("DroneNavigator", "calculate_steering"))
        self.assertGreaterEqual(len(res["recent_assignments"]), 1)

if __name__ == "__main__":
    unittest.main()
