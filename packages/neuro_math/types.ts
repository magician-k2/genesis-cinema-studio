/**
 * 🧠 GENESIS Cybernetics - Strict TypeScript Interfaces (Zero-Mock)
 * Guarantees physical unit safety (mV, ms, nA, Hz) across Web Studio & Extension
 */

export interface LIFParameters {
    readonly tauM_ms: number;       // 膜時定数 τm [ms] (通常 20ms)
    readonly tauRef_ms: number;     // 絶対不応期 τref [ms] (通常 2ms)
    readonly vRest_mv: number;      // 静止電位 Vrest [mV] (-70mV)
    readonly vReset_mv: number;     // リセット電位 Vreset [mV] (-75mV)
    readonly vTh_mv: number;        // 発火閾値 Vth [mV] (-55mV)
    readonly rM_mohm: number;       // 膜抵抗 Rm [MΩ] (1.0)
}

export interface STDPParameters {
    readonly aPlus: number;         // LTP 学習率 A+ (0.01)
    readonly aMinus: number;        // LTD 学習率 A- (0.0105)
    readonly tauPlus_ms: number;    // LTP 時定数 τ+ [ms] (20ms)
    readonly tauMinus_ms: number;   // LTD 時定数 τ- [ms] (20ms)
    readonly wMin: number;          // 最小結合荷重 (0.0)
    readonly wMax: number;          // 最大結合荷重 (1.0)
}

export interface NeuromodulatorRibbonState {
    dopamine_da: number;           // 0.0 - 1.0 (報酬予測誤差)
    noradrenaline_na: number;      // 0.0 - 1.0 (危機覚醒)
    serotonin_5ht: number;         // 0.0 - 1.0 (恒常性抑制)
    homeostasis_percent: number;   // 0 - 100%
    status: 'EQUILIBRIUM' | 'SURGE' | 'FATIGUE' | 'CRITICAL';
}

export interface SevenPillarsTelemetry {
    readonly domain: string;
    readonly confidence: number;
    readonly elapsedMs: number;
    readonly nengoLifRateHz: number;
    readonly snntorchStdpDeltaW: number;
    readonly pymdpFreeEnergyF: number;
    readonly webgpuNeurons: number;
    readonly webgpuElapsedMs: number;
    readonly flywireSynapses: number;
    readonly prunedBranches: number;
    readonly rootCause: string;
    readonly actionPlan: string;
    readonly receiptId: string;
    readonly proofHash: string;
}

export interface XAIAttribution {
    readonly flywire: number;        // e.g. 45.2%
    readonly nengo: number;          // e.g. 28.6%
    readonly snntorch: number;       // e.g. 18.2%
    readonly pymdp: number;          // e.g. 8.0%
    readonly rationale: string;
}

export interface SemanticDiff {
    readonly rawLabel: string;
    readonly rawText: string;
    readonly geminiLabel: string;
    readonly geminiText: string;
    readonly cosine: number;
    readonly astVerified: boolean;
}
