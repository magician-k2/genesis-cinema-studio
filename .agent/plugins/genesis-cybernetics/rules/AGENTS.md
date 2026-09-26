# 🧠 GENESIS Rigorous Cybernetics & Engineering Guidelines

## 🌟 Zero-Mock & Mathematical Rigor Law (数学的厳密性の完全保証)
Whenever implementing or upgrading cybernetics, SNN, or neural simulation modules:

1. **No Mock Data / No Stub Equations (見せかけ・スタブの完全禁止)**:
   - Always implement verified numerical formulas:
     - **LIF Integration**: $\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I(t)$ with Euler/Runge-Kutta stepping.
     - **STDP Learning**: $\Delta w = A_+ e^{-\Delta t/\tau_+}$ (LTP) and $-A_- e^{\Delta t/\tau_-}$ (LTD).
     - **Variational Free Energy**: $F = D_{KL}(q(s) \parallel p(s)) - \mathbb{E}_q[\ln p(o \mid s)]$.
2. **Framework Compliance (国際標準フレームワーク準拠)**:
   - Ensure interoperability with **Nengo**, **snnTorch**, and **PyMDP** standard formulations.
3. **Hardware-Parallel Execution (WebGPU / SIMD)**:
   - For scale > 1,000 neurons, compute via **WebGPU WGSL compute shaders** or vectorized Float32Array SIMD.
4. **Biological Grounding (生体実データ実体化)**:
   - Ground connectivity matrices in Princeton **FlyWire Connectome (139k neurons)** or real-world open neuroscience datasets.
