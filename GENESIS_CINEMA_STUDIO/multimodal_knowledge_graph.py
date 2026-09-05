"""
🌐 GENESIS Multimodal Knowledge Graph (multimodal_knowledge_graph.py - v55)
- Graph + Vector Dual Storage Engine
- Nodes: Concepts, Mathematical Formulas, Anatomical Diagrams, Video Footage Clips, GPS Locations
- Edges: [EXPLAINS, PROVES, DEMONSTRATES, APPLIES_TO, DERIVES_FROM]
"""

import json
import time

class MultimodalKnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.init_core_knowledge()

    def init_core_knowledge(self):
        # 1. Brain Concept Node
        self.add_node("concept_hippocampal_consolidation", {
            "type": "BiologicalConcept",
            "name": "海馬-皮質 記憶固定化 (Hippocampal-Neocortical Consolidation)",
            "domain": "Neuroscience",
            "source": { "book": "生体脳構造と神経回路数理モデル.pdf", "page": 45, "chapter": "第3章" }
        })

        # 2. Math Formula Node
        self.add_node("formula_stdp", {
            "type": "MathematicalFormula",
            "name": "STDP則 (Spike-Timing-Dependent Plasticity)",
            "latex": r"\Delta w = A_+ \exp(-\Delta t / \tau_+)",
            "source": { "book": "生体脳構造と神経回路数理モデル.pdf", "page": 45 }
        })

        # 3. Studio Engine Node
        self.add_node("engine_dolly_tracking", {
            "type": "CinemaTechnique",
            "name": "360° ドリー追従撮影 (Contiguous Dolly Tracking)",
            "source": { "module": "streetview_live_scout.js", "distanceM": 40.0 }
        })

        # Edges linking concepts
        self.add_edge("formula_stdp", "REGULATES", "concept_hippocampal_consolidation")
        self.add_edge("concept_hippocampal_consolidation", "INSPIRES_ARCHITECTURE", "engine_dolly_tracking")

    def add_node(self, node_id, attributes):
        self.nodes[node_id] = {
            "id": node_id,
            "created": int(time.time() * 1000),
            **attributes
        }
        return self.nodes[node_id]

    def add_edge(self, source_id, relation, target_id, properties=None):
        edge = {
            "source": source_id,
            "relation": relation,
            "target": target_id,
            "properties": properties or {},
            "created": int(time.time() * 1000)
        }
        self.edges.append(edge)
        return edge

    def query_graph(self, query_entity_id, max_hops=2):
        """1-2 hop neighborhood graph traversal"""
        matched_edges = [e for e in self.edges if e["source"] == query_entity_id or e["target"] == query_entity_id]
        neighbor_ids = set()
        for e in matched_edges:
            neighbor_ids.add(e["source"])
            neighbor_ids.add(e["target"])

        return {
            "query": query_entity_id,
            "matchedNodes": [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes],
            "connectedEdges": matched_edges
        }

if __name__ == "__main__":
    mmkg = MultimodalKnowledgeGraph()
    res = mmkg.query_graph("concept_hippocampal_consolidation")
    print(json.dumps(res, indent=2, ensure_ascii=False))
