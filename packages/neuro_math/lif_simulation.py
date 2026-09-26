"""
🧠 GENESIS LIF (Leaky Integrate-and-Fire) Simulation Engine
Euler, Runge-Kutta 4th, and Nengo Analytic Closed-Form Firing Rate Formulation
"""

import math
from typing import List, Tuple
from packages.neuro_math.types import LIFParameters


class LIFNeuronEngine:
    def __init__(self, params: LIFParameters = None):
        self.params = params or LIFParameters()

    def nengo_analytic_firing_rate(self, current_j: float) -> float:
        """
        Nengo公式世界標準 LIF定常発火率 閉形式解析解
        r(J) = 1 / (tau_ref - tau_m * ln(1 - V_th / (J * R_m)))
        """
        tau_m = self.params.tau_m_ms / 1000.0  # 秒単位
        tau_ref = self.params.tau_ref_ms / 1000.0
        v_th = abs(self.params.v_th_mv - self.params.v_rest_mv) / 1000.0  # mV -> V相対値
        r_m = self.params.r_m_mohm * 1.0  # 正規化

        if current_j * r_m <= v_th:
            return 0.0  # 閾値未満では発火なし

        arg = 1.0 - (v_th / (current_j * r_m))
        if arg <= 0:
            return 1.0 / tau_ref

        period = tau_ref - tau_m * math.log(arg)
        if period <= 0:
            return 1.0 / tau_ref
        return 1.0 / period

    def step_euler(self, v_prev: float, i_inj: float, dt_ms: float) -> Tuple[float, bool]:
        """オイラー法による1ステップ積分"""
        tau_m = self.params.tau_m_ms
        v_rest = self.params.v_rest_mv
        v_th = self.params.v_th_mv
        v_reset = self.params.v_reset_mv
        r_m = self.params.r_m_mohm

        dv = (-(v_prev - v_rest) + r_m * i_inj) * (dt_ms / tau_m)
        v_next = v_prev + dv

        if v_next >= v_th:
            return v_reset, True
        return v_next, False

    def step_runge_kutta_4th(self, v_prev: float, i_inj: float, dt_ms: float) -> Tuple[float, bool]:
        """古典的4次ルンゲ＝クッタ法 (RK4) による高精度ステップ積分"""
        tau_m = self.params.tau_m_ms
        v_rest = self.params.v_rest_mv
        v_th = self.params.v_th_mv
        v_reset = self.params.v_reset_mv
        r_m = self.params.r_m_mohm

        f = lambda v: (-(v - v_rest) + r_m * i_inj) / tau_m

        k1 = f(v_prev)
        k2 = f(v_prev + 0.5 * dt_ms * k1)
        k3 = f(v_prev + 0.5 * dt_ms * k2)
        k4 = f(v_prev + dt_ms * k3)

        v_next = v_prev + (dt_ms / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

        if v_next >= v_th:
            return v_reset, True
        return v_next, False
