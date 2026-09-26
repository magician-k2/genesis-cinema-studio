---
name: rigorous-cybernetics
description: >-
  Executes mathematically rigorous neuromorphic SNN simulations, Active Inference / Free Energy computations,
  and biological FlyWire connectome parsing grounded in Nengo, snnTorch, and PyMDP standard formulations.
  Use whenever user demands mathematical verification, proof of non-mock implementations, or high-performance WebGPU execution.
---

# Rigorous Cybernetics & Neuromorphic SNN Skill

This skill provides verified, zero-mock execution pipelines for:
1. **LIF Differential Equation Solvers**: Nengo-compatible analytical & Euler numerical integration.
2. **STDP Synaptic Plasticity**: Bipolar exponential Hebbian learning with $\Delta t$ millisecond resolution.
3. **Active Inference / Variational Free Energy**: PyMDP-compliant KL-divergence and surprise minimization.
4. **FlyWire Real Biological Connectome**: Dynamic parsing of 139k Princeton EM neural wiring data.
5. **WebGPU WGSL Parallelism**: 10,000+ neuron parallel execution on hardware GPUs.

## Standard Execution Interfaces:
- `core/standard_neuro_framework_bridge.py`: Direct analytical and numerical verification.
- `core/flywire_connectome_loader.py`: Princeton connectome data parser.
- `browser_extension/webgpu_snn_compute.js`: WebGPU compute shader engine.
