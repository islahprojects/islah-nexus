"""
NexusGPT Equation scoring engine.

C_NexusGPT =
(K_Nexus + U_Nexus + G_Nexus) * E_Nexus * T_Nexus

This is an audit score, not a claim of intelligence or authority.
"""

from dataclasses import dataclass, field
from math import log
from typing import Sequence


@dataclass
class RetrievalFactor:
    authority: float
    relevance: float
    recency: float
    coverage: float
    extractability: float

    def score(self) -> float:
        return self.authority * self.relevance * self.recency * self.coverage * self.extractability


@dataclass
class ToolFactor:
    availability: float
    correctness: float
    determinism: float
    latency_factor: float

    def score(self) -> float:
        return self.availability * self.correctness * self.determinism * self.latency_factor


@dataclass
class NexusGPTInputs:
    # Known terms
    D_model: float = 0.5
    D_user: float = 0.5
    M_memory: float = 0.0
    P_projects: float = 0.0
    A_apps: float = 0.0
    I_instructions: float = 0.5

    retrievals: Sequence[RetrievalFactor] = field(default_factory=list)
    tools: Sequence[ToolFactor] = field(default_factory=list)

    # Unknown terms
    ambiguity: float = 0.3
    unverifiability: float = 0.3
    model_disagreement: float = 0.3

    # Granular terms
    prompt_sensitivity: float = 0.2
    context_order_effects: float = 0.2
    retrieval_jitter: float = 0.2

    # Environment
    q_prompt_quality: float = 1.0
    r_routing_fit: float = 1.0
    s_safety_fit: float = 1.0
    x_access: float = 1.0
    c_context_fit: float = 1.0
    o_platform_health: float = 1.0

    # Time
    usable_tokens: float = 1000.0
    iteration_count: float = 1.0


@dataclass
class NexusGPTWeights:
    w_model: float = 1.0
    w_user: float = 1.2
    w_retrieval: float = 1.4
    w_tools: float = 1.1
    w_memory: float = 0.8
    w_projects: float = 0.8
    w_apps: float = 0.8
    w_instructions: float = 1.0

    alpha_ambiguity: float = 0.4
    beta_unverifiability: float = 0.4
    gamma_disagreement: float = 0.2

    delta_prompt_sensitivity: float = 0.2
    epsilon_order_effects: float = 0.2
    zeta_retrieval_jitter: float = 0.2


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def score_nexusgpt(inputs: NexusGPTInputs, weights: NexusGPTWeights | None = None) -> dict:
    w = weights or NexusGPTWeights()

    d_retrieved = sum(r.score() for r in inputs.retrievals)
    f_tools = sum(t.score() for t in inputs.tools)

    k_nexus = (
        w.w_model * clamp01(inputs.D_model)
        + w.w_user * clamp01(inputs.D_user)
        + w.w_retrieval * d_retrieved
        + w.w_tools * f_tools
        + w.w_memory * clamp01(inputs.M_memory)
        + w.w_projects * clamp01(inputs.P_projects)
        + w.w_apps * clamp01(inputs.A_apps)
        + w.w_instructions * clamp01(inputs.I_instructions)
    )

    u_nexus = (
        w.alpha_ambiguity * clamp01(inputs.ambiguity)
        + w.beta_unverifiability * clamp01(inputs.unverifiability)
        + w.gamma_disagreement * clamp01(inputs.model_disagreement)
    )

    g_nexus = (
        w.delta_prompt_sensitivity * clamp01(inputs.prompt_sensitivity)
        + w.epsilon_order_effects * clamp01(inputs.context_order_effects)
        + w.zeta_retrieval_jitter * clamp01(inputs.retrieval_jitter)
    )

    e_nexus = (
        clamp01(inputs.q_prompt_quality)
        * clamp01(inputs.r_routing_fit)
        * clamp01(inputs.s_safety_fit)
        * clamp01(inputs.x_access)
        * clamp01(inputs.c_context_fit)
        * clamp01(inputs.o_platform_health)
    )

    t_nexus = log(1.0 + max(0.0, inputs.usable_tokens)) * max(1.0, inputs.iteration_count)

    c_nexusgpt = (k_nexus + u_nexus + g_nexus) * e_nexus * t_nexus

    return {
        "C_NexusGPT": round(c_nexusgpt, 6),
        "K_Nexus": round(k_nexus, 6),
        "U_Nexus": round(u_nexus, 6),
        "G_Nexus": round(g_nexus, 6),
        "E_Nexus": round(e_nexus, 6),
        "T_Nexus": round(t_nexus, 6),
        "note": "Audit score only; not a claim of omniscience, autonomy, or access to all data.",
    }
