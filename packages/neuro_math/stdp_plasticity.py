"""
🧠 GENESIS snnTorch Bi-Exponential STDP (Spike-Timing-Dependent Plasticity) Engine
公式規格準拠：Δw = A+ * exp(-Δt/τ+) (LTP) / -A- * exp(Δt/τ-) (LTD)
"""

import math
from packages.neuro_math.types import STDPParameters


class STDPEngine:
    def __init__(self, params: STDPParameters = None):
        self.params = params or STDPParameters()

    def compute_weight_change(self, delta_t_ms: float) -> float:
        """
        スパイク時間差 Δt = t_post - t_pre [ms] に基づくシナプス荷重変化 Δw
        """
        if delta_t_ms > 0:
            # LTP (Long-Term Potentiation): 前シナプス発火直後に後シナプス発火
            return self.params.a_plus * math.exp(-delta_t_ms / self.params.tau_plus_ms)
        elif delta_t_ms < 0:
            # LTD (Long-Term Depression): 逆順発火
            return -self.params.a_minus * math.exp(delta_t_ms / self.params.tau_minus_ms)
        else:
            return 0.0

    def update_weight(self, current_w: float, delta_t_ms: float) -> float:
        """荷重更新と境界クランプ [w_min, w_max]"""
        dw = self.compute_weight_change(delta_t_ms)
        new_w = current_w + dw
        return max(self.params.w_min, min(self.params.w_max, new_w))
