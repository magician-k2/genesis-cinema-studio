"""
GENESIS Cortical Shared Bus (Phase 31)
Unified Event & State Bus for Cross-Application Brain Sync and Reflex Query.
Enables Chrome Extension, 3D Simulator, Music DNA, Paper Engine, and Dashcam
to share synaptic failure-solution memories, neuromodulator telemetry, and artifacts.
"""

import os
import json
import time
import sys
from typing import Dict, Any, List, Optional

try:
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

WORKSPACE_ROOT = r"G:\マイドライブ\GENESIS_ROOT"
SYNAPTIC_MEMORY_PATH = os.path.join(WORKSPACE_ROOT, "knowledge_bank", "hippocampus", "synaptic_failure_solution_memory.json")
ARTIFACTS_MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, "knowledge_bank", "genesis_unified_artifacts_manifest.json")

class CorticalSharedBus:
    """
    大脳皮質 統合通信バス (Event & State Bus)
    全アプリ共通のシナプス記憶クエリ、神経修飾物質シグナル、成果物カタログ共有を担う。
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CorticalSharedBus, cls).__new__(cls)
            cls._instance._init_bus()
        return cls._instance

    def _init_bus(self):
        self.synaptic_memory: Dict[str, Any] = {}
        self.neuromodulators = {
            "dopamine": 0.85,       # 報酬予測誤差・学習加速 (0.0 - 1.0)
            "noradrenaline": 0.32,  # 危機覚醒・注意集中・枝刈りブースト (0.0 - 1.0)
            "serotonin": 0.90       # 安定・衝動抑制・定常巡航 (0.0 - 1.0)
        }
        self.homeostasis = {
            "battery_level": 0.94,      # バッテリー残量 (0.0 - 1.0)
            "core_temperature_c": 42.5, # コア温度 (°C)
            "chassis_integrity": 1.0,   # 機体健全性 (0.0 - 1.0)
            "status": "HOMEOSTATIC_EQUILIBRIUM"
        }
        self.load_synaptic_memory()

    def load_synaptic_memory(self):
        if os.path.exists(SYNAPTIC_MEMORY_PATH):
            try:
                with open(SYNAPTIC_MEMORY_PATH, "r", encoding="utf-8") as f:
                    self.synaptic_memory = json.load(f)
            except Exception as e:
                self.synaptic_memory = {}

    def query_reflex_rules(self, query_context: str) -> List[Dict[str, Any]]:
        """
        与えられたコンテキスト（コード、エラー、プロンプト）から、
        過去の失敗を未然に防ぐための『シナプス反射ルール』を側抑制検索して返す。
        """
        if not self.synaptic_memory:
            self.load_synaptic_memory()

        matched_rules = []
        patterns = self.synaptic_memory.get("synaptic_patterns", [])
        q_lower = query_context.lower()

        for p in patterns:
            # ドメインまたはキーワード合致判定
            domain_match = p.get("domain", "").lower() in q_lower
            title_words = [w.lower() for w in p.get("title", "").split() if len(w) > 3]
            symptom_match = any(w in q_lower for w in title_words)
            
            # 特有キーワード検出
            if "csp" in q_lower or "inline" in q_lower:
                if p["id"] == "SYN-FAIL-001":
                    matched_rules.append(p)
                    continue
            if "duplicate" in q_lower or "重複" in q_lower or "debounce" in q_lower:
                if p["id"] == "SYN-FAIL-002":
                    matched_rules.append(p)
                    continue
            if "drone" in q_lower or "旋回" in q_lower or "deadlock" in q_lower or "直進" in q_lower:
                if p["id"] == "SYN-FAIL-003":
                    matched_rules.append(p)
                    continue
            if "snn" in q_lower or "spike" in q_lower or "clock" in q_lower or "消費電力" in q_lower:
                if p["id"] == "SYN-FAIL-004":
                    matched_rules.append(p)
                    continue
            if "hallucination" in q_lower or "幻覚" in q_lower or "監査" in q_lower or "diff" in q_lower:
                if p["id"] == "SYN-FAIL-005":
                    matched_rules.append(p)
                    continue

            if domain_match or symptom_match:
                matched_rules.append(p)

        return matched_rules

    def update_neuromodulators(self, da: Optional[float] = None, na: Optional[float] = None, st: Optional[float] = None):
        """神経修飾物質の動的更新"""
        if da is not None: self.neuromodulators["dopamine"] = max(0.0, min(1.0, da))
        if na is not None: self.neuromodulators["noradrenaline"] = max(0.0, min(1.0, na))
        if st is not None: self.neuromodulators["serotonin"] = max(0.0, min(1.0, st))

    def get_telemetry_packet(self) -> Dict[str, Any]:
        """全アプリ共通の同期テレメトリパケット"""
        return {
            "timestamp": time.time(),
            "neuromodulators": self.neuromodulators,
            "homeostasis": self.homeostasis,
            "synapse_rules_count": self.synaptic_memory.get("total_synaptic_rules", 0)
        }

    def build_unified_artifacts_manifest(self) -> Dict[str, Any]:
        """outputs/ および主要ディレクトリの全成果物をインデックス化してデータレイクを生成"""
        manifest = {
            "version": "1.0.0-UNIFIED-ARTIFACTS",
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "artifacts": []
        }

        outputs_dir = os.path.join(WORKSPACE_ROOT, "outputs")
        if os.path.exists(outputs_dir):
            for fname in os.listdir(outputs_dir):
                fpath = os.path.join(outputs_dir, fname)
                if os.path.isfile(fpath):
                    ext = os.path.splitext(fname)[1].lower()
                    cat = "package" if ext == ".zip" else ("image" if ext in [".png", ".jpg"] else ("document" if ext in [".md", ".pdf", ".txt"] else "code"))
                    manifest["artifacts"].append({
                        "filename": fname,
                        "relative_path": f"outputs/{fname}",
                        "size_bytes": os.path.getsize(fpath),
                        "category": cat,
                        "description": f"Shared GENESIS Artifact ({cat})"
                    })

        with open(ARTIFACTS_MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"✅ Unified Artifacts Manifest generated: {ARTIFACTS_MANIFEST_PATH} ({len(manifest['artifacts'])} items)")
        return manifest

if __name__ == "__main__":
    bus = CorticalSharedBus()
    manifest = bus.build_unified_artifacts_manifest()
    
    # テストクエリ
    test_q = "Chrome拡張機能で画面をクリックしたときにバグが出ないようにしたい"
    reflexes = bus.query_reflex_rules(test_q)
    print(f"\n🔍 Query Test: '{test_q}'")
    print(f"⚡ Matched Reflex Rules: {len(reflexes)}")
    for r in reflexes:
        print(f"  - [{r['id']}] {r['title']}: {r['prevention_rule']}")
