/**
 * ================================================================================
 * 🌟 GENESIS REVERSE MINDMAP ENGINE (The Convergent Mesh v2.0)
 * ================================================================================
 * High-performance 2D/3D canvas rendering for Causal DAG convergence.
 * Visualizes the deep learning dilemma cure:
 *  - Outer periphery symptoms emit energetic particles.
 *  - Particles follow directed causal edges through intermediate AST/Protocol nodes.
 *  - 100% converge into the pulsating central core (μTRON CORE / Root Cause).
 * ================================================================================
 */

class ConvergentMeshStudio {
    constructor() {
        this.canvas = document.getElementById('mindmap-canvas');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');

        this.nodes = [];
        this.links = [];
        this.particles = [];
        this.selectedNode = null;
        this.hoveredNode = null;

        this.currentScenario = 'swe_bench_bug';
        this.dagData = null;

        this.centerNode = {
            id: 'core_root_cause',
            x: 0,
            y: 0,
            radius: 54,
            label: "μTRON CORE",
            subLabel: "Root Cause",
            pulse: 1.0,
            confidence: 0.998,
            color: '#00f0ff',
            glow: '#00f0ff'
        };

        this.initEventListeners();
        this.resize();
        this.loadScenario('swe_bench_bug');
        this.animate();

        console.log("[GENESIS] The Convergent Mesh Studio v2.0 Online.");
    }

    initEventListeners() {
        window.addEventListener('resize', () => this.resize());

        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;

            let hit = null;
            for (const n of this.nodes) {
                const dist = Math.hypot(n.x - mx, n.y - my);
                if (dist <= (n.radius || 18)) {
                    hit = n;
                    break;
                }
            }
            this.hoveredNode = hit;
            this.canvas.style.cursor = hit ? 'pointer' : 'crosshair';
        });

        this.canvas.addEventListener('click', (e) => {
            if (this.hoveredNode) {
                this.selectNode(this.hoveredNode);
            } else {
                this.selectNode(null);
            }
        });
    }

    resize() {
        this.canvas.width = this.canvas.parentElement.clientWidth;
        this.canvas.height = this.canvas.parentElement.clientHeight;
        this.centerNode.x = this.canvas.width / 2;
        this.centerNode.y = this.canvas.height / 2;
        if (this.dagData) {
            this.layoutDAG(this.dagData);
        }
    }

    loadScenario(scenarioKey) {
        this.currentScenario = scenarioKey;
        // 組み込みプリセットデータ (サーバー未接続時でも即座に完全稼働)
        const PRESETS = {
            swe_bench_bug: {
                domain: "SWE-bench Verified / Autonomous Software Patching",
                confidence: 0.998,
                elapsed_ms: 1.2,
                root_cause: "activeBypassUntilZ Comparison Inequality Locking Heading to 0",
                action_plan: "Apply Atomic Diff: Guard activeBypassUntilZ > -90000 and enable yaw priority deceleration",
                receipt_id: "RCPT-XAI-7F4B2E9901C2",
                proof_hash: "SHA256:9B83802F9A34CC01",
                pruned_branches: 60,
                nodes: [
                    { id: "symptom_1", label: "TypeError: 'NoneType' has no attribute 'z'", layer: "periphery", type: "exception", severity: "CRITICAL", source: "Pytest L6708", color: "#ef4444", details: "activeBypassUntilZ inequality evaluated true for initial negative sentinels." },
                    { id: "symptom_2", label: "HeadingLock: headingDiff clamped at 0.0 rad", layer: "periphery", type: "assertion", severity: "HIGH", source: "Unit Test Suite", color: "#f59e0b", details: "Desired heading locked to North (0 deg) despite victim located East (+25m)." },
                    { id: "symptom_3", label: "Telemetry: Infinite straight cruise without yaw turn", layer: "periphery", type: "telemetry", severity: "MEDIUM", source: "Sensor Stream", color: "#f59e0b", details: "Yaw heading rate remained 0 for 3.5s in AIR mode." },
                    { id: "intermediate_1", label: "AST CallGraph Trace: activeBypassUntilZ Sentinel Flow", layer: "intermediate", type: "ast_rule", authority: "Tree-Sitter AST", pruned_branches: 42, color: "#8b5cf6", details: "Traced variable initialization -99999 triggering permanent detour bypass branch." },
                    { id: "intermediate_2", label: "Fly-Brain 5s Deadlock Detector: Yaw Priority Reflex", layer: "intermediate", type: "reflex_rule", authority: "MaleCNS SNN Layer", pruned_branches: 18, color: "#8b5cf6", details: "Detected straight drift deadlock; issued speed modulation (8km/h) for quick on-the-spot yaw." }
                ],
                links: [
                    { source: "symptom_1", target: "intermediate_1" },
                    { source: "symptom_2", target: "intermediate_1" },
                    { source: "symptom_3", target: "intermediate_2" },
                    { source: "intermediate_1", target: "core_root_cause" },
                    { source: "intermediate_2", target: "core_root_cause" }
                ]
            },
            rescue_drone_3d: {
                domain: "3D Bio-Cybernetics Autonomous Search & Rescue",
                confidence: 0.994,
                elapsed_ms: 0.9,
                root_cause: "Casualty Trapped behind Northeast Alleyway with Obstructed Line-of-Sight",
                action_plan: "Execute Slalom Detour, decel to 8km/h, hover at 2.2m and deploy emerald vital shield",
                receipt_id: "RCPT-XAI-3D09AF4162B8",
                proof_hash: "SHA256:7C22E109DF9981A4",
                pruned_branches: 20,
                nodes: [
                    { id: "symptom_1", label: "Thermal Sensor: 38.8℃ Biological Heat Signature", layer: "periphery", type: "thermal", severity: "CRITICAL", source: "IR Camera Array", color: "#ef4444", details: "Target detected at (X: 25.0m, Z: -15.0m) emitting metabolic IR spectrum." },
                    { id: "symptom_2", label: "LiDAR: Boulevard Wall Encroachment (Dist: 2.1m)", layer: "periphery", type: "lidar", severity: "HIGH", source: "Solid-State LiDAR", color: "#f59e0b", details: "Left building facade proximity triggering LPTC optical flow torque." },
                    { id: "symptom_3", label: "Acoustic Sensor: Distress Signal Detection 1.2kHz", layer: "periphery", type: "audio", severity: "MEDIUM", source: "Beamforming Mic", color: "#f59e0b", details: "Periodic acoustic pulse verified at azimuth -58.2 deg." },
                    { id: "intermediate_1", label: "LPTC Centering Bypass Rule (Rescue Target Priority)", layer: "intermediate", type: "cybernetics_rule", authority: "MaleCNS LPTC Circuit", pruned_branches: 12, color: "#8b5cf6", details: "Overrode street centering torque when valid casualty beacon is targeted." },
                    { id: "intermediate_2", label: "150m Rescue Zone Safety Geofence Boundary", layer: "intermediate", type: "geofence_rule", authority: "M3 Mission System", pruned_branches: 8, color: "#8b5cf6", details: "Target strictly bounded inside [-75m, +75m] operating area." }
                ],
                links: [
                    { source: "symptom_1", target: "intermediate_1" },
                    { source: "symptom_2", target: "intermediate_1" },
                    { source: "symptom_3", target: "intermediate_2" },
                    { source: "intermediate_1", target: "core_root_cause" },
                    { source: "intermediate_2", target: "core_root_cause" }
                ]
            },
            clinical_safety: {
                domain: "Clinical AI & Smart-Glass Medication Safety",
                confidence: 0.999,
                elapsed_ms: 1.5,
                root_cause: "Medication Order 100% Validated for Patient P-102 (Warfarin 2mg Oral)",
                action_plan: "Authorize bedside dispensing and generate HL7/SS-MIX2 administration record",
                receipt_id: "RCPT-XAI-88A92DF00341",
                proof_hash: "SHA256:4FA299B017CC6809",
                pruned_branches: 88,
                nodes: [
                    { id: "symptom_1", label: "Camera OCR: Warfarin 2.0mg Tablet PTP Sheet", layer: "periphery", type: "vision", severity: "HIGH", source: "Smart-Glass Camera", color: "#f59e0b", details: "High-resolution OCR matched GS1 barcode 498712345678." },
                    { id: "symptom_2", label: "Voice EHR: Nurse query 'Warfarin administration for P-102'", layer: "periphery", type: "audio", severity: "MEDIUM", source: "Bone-Conduction Mic", color: "#10b981", details: "Speech-to-text converted with 99.1% acoustic confidence." },
                    { id: "symptom_3", label: "Telemetry: Patient INR Value = 2.45 (Target: 2.0-3.0)", layer: "periphery", type: "vital", severity: "MEDIUM", source: "EHR Bridge", color: "#10b981", details: "Lab result dated 2026-09-25 08:30 in therapeutic range." },
                    { id: "intermediate_1", label: "JCQHC 5R Protocol (Patient, Drug, Dose, Route, Time)", layer: "intermediate", type: "medical_rule", authority: "MHLW Guidelines", pruned_branches: 64, color: "#8b5cf6", details: "All 5 verification criteria cross-checked against doctor's prescription." },
                    { id: "intermediate_2", label: "Contraindication Matrix (Drug Interaction Check)", layer: "intermediate", type: "pharma_rule", authority: "PMDA Drug Database", pruned_branches: 24, color: "#8b5cf6", details: "Zero dangerous drug-drug interactions detected for P-102." }
                ],
                links: [
                    { source: "symptom_1", target: "intermediate_1" },
                    { source: "symptom_2", target: "intermediate_1" },
                    { source: "symptom_3", target: "intermediate_2" },
                    { source: "intermediate_1", target: "core_root_cause" },
                    { source: "intermediate_2", target: "core_root_cause" }
                ]
            }
        };

        const data = PRESETS[scenarioKey] || PRESETS.swe_bench_bug;
        this.dagData = data;
        this.layoutDAG(data);
        this.updateHUD(data);
        this.selectNode(null);
    }

    layoutDAG(data) {
        this.nodes = [];
        this.links = [];
        this.particles = [];

        const cx = this.centerNode.x;
        const cy = this.centerNode.y;

        // 1. 中心ノード
        this.centerNode.label = "μTRON CORE";
        this.centerNode.subLabel = data.root_cause;
        this.centerNode.confidence = data.confidence;
        this.centerNode.pulse = 1.0;
        this.nodes.push(this.centerNode);

        // 2. 外周ノード (Periphery: 半径 R = min(W, H) * 0.40)
        const peripheryNodes = data.nodes.filter(n => n.layer === 'periphery');
        const pRadius = Math.min(this.canvas.width, this.canvas.height) * 0.40;
        const pCount = peripheryNodes.length;

        peripheryNodes.forEach((n, i) => {
            const angle = (i / pCount) * Math.PI * 2 - Math.PI / 2;
            n.x = cx + Math.cos(angle) * pRadius;
            n.y = cy + Math.sin(angle) * pRadius;
            n.radius = 16;
            this.nodes.push(n);
        });

        // 3. 中間層ノード (Intermediate: 半径 R = min(W, H) * 0.22)
        const interNodes = data.nodes.filter(n => n.layer === 'intermediate');
        const iRadius = Math.min(this.canvas.width, this.canvas.height) * 0.22;
        const iCount = interNodes.length;

        interNodes.forEach((n, i) => {
            const angle = (i / iCount) * Math.PI * 2 - Math.PI / 2 + (Math.PI / iCount * 0.5);
            n.x = cx + Math.cos(angle) * iRadius;
            n.y = cy + Math.sin(angle) * iRadius;
            n.radius = 20;
            this.nodes.push(n);
        });

        // 4. リンク構築
        data.links.forEach(l => {
            const sourceNode = this.nodes.find(n => n.id === l.source);
            const targetNode = this.nodes.find(n => n.id === l.target);
            if (sourceNode && targetNode) {
                this.links.push({
                    source: sourceNode,
                    target: targetNode
                });
            }
        });
    }

    spawnParticle(link) {
        this.particles.push({
            startX: link.source.x,
            startY: link.source.y,
            targetX: link.target.x,
            targetY: link.target.y,
            progress: 0,
            speed: 0.012 + Math.random() * 0.016,
            color: link.source.color || '#00f0ff',
            size: 2.5 + Math.random() * 2.0,
            targetIsCore: (link.target.id === 'core_root_cause')
        });
    }

    selectNode(node) {
        this.selectedNode = node;
        const panel = document.getElementById('inspector-panel');
        if (!panel) return;

        if (!node) {
            panel.classList.remove('active');
            return;
        }

        panel.classList.add('active');
        document.getElementById('insp-title').innerText = node.label || "Node Inspector";
        document.getElementById('insp-type').innerText = (node.type || node.layer || "NODE").toUpperCase();
        document.getElementById('insp-layer').innerText = (node.layer || "CORE").toUpperCase();
        document.getElementById('insp-details').innerText = node.details || node.subLabel || node.description || "No further details.";

        const extraBox = document.getElementById('insp-extra');
        if (node.id === 'core_root_cause') {
            extraBox.innerHTML = `
                <div class="stat-pill"><span class="label">Confidence</span><span class="val" style="color:#00f0ff">${(node.confidence * 100).toFixed(1)}%</span></div>
                <div class="stat-pill"><span class="label">State</span><span class="val" style="color:#10b981">CONVERGED 100%</span></div>
            `;
        } else if (node.layer === 'intermediate') {
            extraBox.innerHTML = `
                <div class="stat-pill"><span class="label">Authority</span><span class="val">${node.authority || 'Protocol'}</span></div>
                <div class="stat-pill"><span class="label">Pruned Branches</span><span class="val" style="color:#a855f7">${node.pruned_branches || 0} branches</span></div>
            `;
        } else {
            extraBox.innerHTML = `
                <div class="stat-pill"><span class="label">Source</span><span class="val">${node.source || 'Sensor'}</span></div>
                <div class="stat-pill"><span class="label">Severity</span><span class="val" style="color:${node.color}">${node.severity || 'INFO'}</span></div>
            `;
        }
    }

    updateHUD(data) {
        const lblTitle = document.getElementById('hud-scenario-title');
        const lblLatency = document.getElementById('hud-latency');
        const lblConfidence = document.getElementById('hud-confidence');
        const lblPruned = document.getElementById('hud-pruned');
        const lblRootCause = document.getElementById('hud-root-cause');

        if (lblTitle) lblTitle.innerText = data.domain;
        if (lblLatency) lblLatency.innerText = `${data.elapsed_ms}ms`;
        if (lblConfidence) lblConfidence.innerText = `${(data.confidence * 100).toFixed(1)}%`;
        if (lblPruned) lblPruned.innerText = `${data.pruned_branches} branches`;
        if (lblRootCause) lblRootCause.innerText = data.root_cause;
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        // 1. 半透明ブラッククリア（残像粒子トレイル）
        this.ctx.fillStyle = 'rgba(7, 9, 14, 0.25)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 2. 確率的パーティクル生成（因果エッジを伝って外周から中心へ光が流れる）
        if (this.links.length > 0 && Math.random() < 0.65) {
            const randomLink = this.links[Math.floor(Math.random() * this.links.length)];
            this.spawnParticle(randomLink);
        }

        // 3. リンク（因果有向エッジ）の描画
        for (const link of this.links) {
            this.ctx.beginPath();
            this.ctx.moveTo(link.source.x, link.source.y);
            this.ctx.lineTo(link.target.x, link.target.y);
            this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
            this.ctx.lineWidth = 1.2;
            this.ctx.stroke();
        }

        // 4. 粒子（収束光流）の更新・描画
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.progress += p.speed;

            if (p.progress >= 1.0) {
                if (p.targetIsCore) {
                    this.centerNode.pulse = 1.0; // 中心核が光を受け取ってパルス！
                }
                this.particles.splice(i, 1);
                continue;
            }

            // 加速カーブ（中心に近づくほど引力で加速）
            const ease = p.progress * p.progress;
            const cx = p.startX + (p.targetX - p.startX) * ease;
            const cy = p.startY + (p.targetY - p.startY) * ease;

            this.ctx.beginPath();
            this.ctx.arc(cx, cy, p.size, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.shadowBlur = 12;
            this.ctx.shadowColor = p.color;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        }

        // 5. ノード描画
        for (const n of this.nodes) {
            if (n.id === 'core_root_cause') continue; // 中心核は後で巨大描画

            const isHover = (this.hoveredNode === n);
            const isSel = (this.selectedNode === n);

            this.ctx.beginPath();
            this.ctx.arc(n.x, n.y, (n.radius || 16) + (isHover ? 4 : 0), 0, Math.PI * 2);
            this.ctx.fillStyle = isSel ? '#ffffff' : '#111827';
            this.ctx.fill();
            this.ctx.lineWidth = isSel ? 3 : 2;
            this.ctx.strokeStyle = n.color || '#00f0ff';
            this.ctx.shadowBlur = isHover ? 18 : 8;
            this.ctx.shadowColor = n.color || '#00f0ff';
            this.ctx.stroke();
            this.ctx.shadowBlur = 0;

            // ラベル
            this.ctx.fillStyle = '#e2e8f0';
            this.ctx.font = '500 11px system-ui, -apple-system, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(n.label, n.x, n.y + (n.radius || 16) + 16);
        }

        // 6. 中心核（μTRON CORE: 重力レンズ & パルスリング）の描画
        if (this.centerNode.pulse > 0) this.centerNode.pulse -= 0.015;
        const pulseR = this.centerNode.radius + (this.centerNode.pulse * 28);

        // 外周エネルギーフィールド
        this.ctx.beginPath();
        this.ctx.arc(this.centerNode.x, this.centerNode.y, pulseR, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(0, 240, 255, ${0.12 + this.centerNode.pulse * 0.35})`;
        this.ctx.fill();

        // コア本体
        const isCoreHover = (this.hoveredNode === this.centerNode);
        const isCoreSel = (this.selectedNode === this.centerNode);
        this.ctx.beginPath();
        this.ctx.arc(this.centerNode.x, this.centerNode.y, this.centerNode.radius + (isCoreHover ? 4 : 0), 0, Math.PI * 2);
        this.ctx.fillStyle = isCoreSel ? '#041d28' : '#060c14';
        this.ctx.fill();
        this.ctx.lineWidth = 2.5;
        this.ctx.strokeStyle = '#00f0ff';
        this.ctx.shadowBlur = 24;
        this.ctx.shadowColor = '#00f0ff';
        this.ctx.stroke();
        this.ctx.shadowBlur = 0;

        // コアラベル
        this.ctx.fillStyle = '#00f0ff';
        this.ctx.font = 'bold 13px "JetBrains Mono", monospace';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText("μTRON CORE", this.centerNode.x, this.centerNode.y - 10);

        this.ctx.fillStyle = '#10b981';
        this.ctx.font = '600 10px system-ui, sans-serif';
        this.ctx.fillText("ROOT CAUSE LOCKED", this.centerNode.x, this.centerNode.y + 10);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.meshStudio = new ConvergentMeshStudio();
});