/**
 * ⚡ GENESIS WebGPU WGSL SNN Engine Type Declarations
 */

export interface WebGPUStepResult {
    readonly numNeurons: number;
    readonly elapsedMs: number;
    readonly activeSpikes: number;
    readonly meanVoltageMv: number;
    readonly hardware: 'WebGPU (WGSL Compute)' | 'CPU (Float32Array SIMD)';
}

export declare class WebGPUSNNCompute {
    constructor(numNeurons?: number);
    init(): Promise<boolean>;
    step(dt?: number): Promise<WebGPUStepResult>;
    destroy(): void;
}
