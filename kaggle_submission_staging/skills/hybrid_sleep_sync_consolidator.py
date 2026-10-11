# -*- coding: utf-8 -*-
"""
GENESIS Nighttime Hybrid Sleep-Sync Consolidator
================================================================================
Mathematical Rigor & Cybernetics Law:
- Spike-Timing-Dependent Plasticity (STDP):
    delta_w = A_+ * exp(-dt / tau_+)  (LTP, dt > 0)
    delta_w = -A_- * exp(dt / tau_-)  (LTD, dt < 0)
- Variational Free Energy Minimization:
    F = D_KL(q(s) || p(s)) - E_q[ln p(o | s)]
- Multi-tier knowledge consolidation:
    Local ambient harvest -> Colab GPU batch -> Mobile STDP sleep sync -> Edge rehydration
================================================================================
"""

import math
import time
from typing import Dict, List, Any

class HybridSleepSyncConsolidator:
    """
    Offline consolidator implementing synaptic plasticity and variational free energy.
    Transfers episodic task resolutions into persistent structural weights.
    """
    def __init__(self, a_plus: float = 0.015, a_minus: float = 0.012, tau_plus: float = 20.0, tau_minus: float = 20.0):
        self.a_plus = a_plus
        self.a_minus = a_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus
        self.synaptic_weights: Dict[str, float] = {}

    def compute_stdp_update(self, pre_time: float, post_time: float, current_weight: float) -> float:
        """Evaluates exact bi-exponential STDP rule."""
        dt = post_time - pre_time
        if dt > 0:
            dw = self.a_plus * math.exp(-dt / self.tau_plus)
        elif dt < 0:
            dw = -self.a_minus * math.exp(dt / self.tau_minus)
        else:
            dw = 0.0
        # Bound weights in [0.01, 3.0]
        return max(0.01, min(3.0, current_weight + dw))

    def compute_variational_free_energy(self, observations: List[float], priors: List[float]) -> float:
        """
        F = D_KL(q(s) || p(s)) - E_q[ln p(o|s)]
        Measures surprise / prediction error across the causal diagnostic path.
        """
        eps = 1e-9
        kl_div = 0.0
        expected_log_lik = 0.0
        for o, p in zip(observations, priors):
            q_val = max(eps, min(1.0 - eps, o))
            p_val = max(eps, min(1.0 - eps, p))
            kl_div += q_val * math.log(q_val / p_val)
            expected_log_lik += q_val * math.log(p_val)
        return max(0.0, kl_div - expected_log_lik)

    def consolidate_task_resolution(self, task_id: str, exception_types: List[str], diff_lines: int) -> Dict[str, Any]:
        """
        Simulates overnight STDP consolidation cycle for a resolved task instance.
        """
        t_pre = 10.0
        t_post = 25.0  # Positive pairing (LTP reinforcement)
        
        weight_key = "_".join(exception_types) if exception_types else "GenericFix"
        current_w = self.synaptic_weights.get(weight_key, 0.5)
        new_w = self.compute_stdp_update(t_pre, t_post, current_w)
        self.synaptic_weights[weight_key] = new_w

        obs = [min(1.0, diff_lines / 10.0)]
        priors = [0.2]
        fe = self.compute_variational_free_energy(obs, priors)

        return {
            "task_id": task_id,
            "consolidated_pattern": weight_key,
            "synaptic_weight_before": round(current_w, 4),
            "synaptic_weight_after": round(new_w, 4),
            "stdp_delta_w": round(new_w - current_w, 4),
            "variational_free_energy": round(fe, 4),
            "sync_status": "CONSOLIDATED_OFFLINE",
            "lifecycle_phase": "Phase3_Mobile_STDP_Sleep_Sync"
        }

def consolidate_sleep_weights(task_id: str, exception_types: List[str], diff_lines: int) -> Dict[str, Any]:
    consolidator = HybridSleepSyncConsolidator()
    return consolidator.consolidate_task_resolution(task_id, exception_types, diff_lines)
