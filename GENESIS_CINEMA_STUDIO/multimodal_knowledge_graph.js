/**
 * 🌐 GENESIS Multimodal Knowledge Graph Client (multimodal_knowledge_graph.js - v55)
 * - Browser-side Graph Navigator & Cross-Media Entity Resolver
 */

class MultimodalKnowledgeGraphClient {
    constructor() {
        this.nodes = {};
        this.edges = [];
        this.initDemoGraph();
    }

    initDemoGraph() {
        this.nodes["concept_hippocampus"] = {
            id: "concept_hippocampus",
            type: "NeuroscienceConcept",
            name: "海馬-皮質 記憶固定化",
            book: "生体脳構造と神経回路数理モデル.pdf",
            page: 45,
            chapter: "第3章"
        };
        this.nodes["formula_stdp"] = {
            id: "formula_stdp",
            type: "MathFormula",
            name: "STDP則 (シナプス可塑性)",
            latex: "\Delta w = A_+ \exp(-\Delta t / \tau_+)",
            page: 45
        };
        this.nodes["video_shot_01"] = {
            id: "video_shot_01",
            type: "VideoFootage",
            name: "🎬 Shot 1: 表参道・正面ドリー (40m)",
            durationSec: 5.0,
            gps: "35.6715, 139.7032"
        };

        this.edges.push({ source: "formula_stdp", relation: "PROVES", target: "concept_hippocampus" });
        this.edges.push({ source: "concept_hippocampus", relation: "SYNCHRONIZED_WITH", target: "video_shot_01" });
    }

    findNeighbors(nodeId) {
        const connectedEdges = this.edges.filter(e => e.source === nodeId || e.target === nodeId);
        const nodeIds = new Set();
        connectedEdges.forEach(e => { nodeIds.add(e.source); nodeIds.add(e.target); });

        return {
            centerNode: this.nodes[nodeId],
            neighborNodes: Array.from(nodeIds).map(id => this.nodes[id]).filter(Boolean),
            edges: connectedEdges
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MultimodalKnowledgeGraphClient };
}
if (typeof window !== 'undefined') {
    window.MultimodalKnowledgeGraphClient = new MultimodalKnowledgeGraphClient();
}
console.log("🌐 GENESIS Multimodal Knowledge Graph v55 Loaded.");
