"""
🧠 GENESIS PyMDP Variational Free Energy Engine
公式規格準拠：F = D_KL(q(s) || p(s)) - E_q[ln p(o|s)]
"""

import math
from typing import List


class ActiveInferenceEngine:
    @staticmethod
    def compute_free_energy(
        q_s: List[float], 
        p_s: List[float], 
        obs_idx: int, 
        a_matrix: List[List[float]]
    ) -> float:
        """
        変分自由エネルギー F の厳密数値計算
        q_s: 事後信念分布 (State Belief)
        p_s: 事前信念分布 (Prior)
        obs_idx: 現在の観測インデックス
        a_matrix: 尤度行列 A [num_obs][num_states]
        """
        eps = 1e-12

        # 1. KLダイバージェンス: D_KL(q(s) || p(s)) = sum_s q(s) * ln(q(s) / p(s))
        kl_div = 0.0
        for qs, ps in zip(q_s, p_s):
            if qs > eps:
                kl_div += qs * math.log((qs + eps) / (ps + eps))

        # 2. 期待対数尤度: E_q[ln p(o|s)] = sum_s q(s) * ln p(o | s)
        expected_log_lik = 0.0
        for s_idx, qs in enumerate(q_s):
            p_o_given_s = a_matrix[obs_idx][s_idx]
            expected_log_lik += qs * math.log(p_o_given_s + eps)

        # F = KL - E[ln p(o|s)]
        f = kl_div - expected_log_lik
        return f
