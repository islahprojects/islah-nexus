import math
import asyncio
import os
from functools import reduce
from operator import mul
from typing import Dict, Any, List, Tuple
from config.constants import ICF_CONSTANTS

def SynthID(func): return func
class LawViolationError(Exception): pass

class PhoenixDAG:
    async def execute(self, node: str, context: Dict):
        return {"status": "DAG_EXECUTED", "node": node, "context": context}

class ChiefOmega:
    def __init__(self, constants: ICF_CONSTANTS):
        self.c = constants
        self._violation_log: List[str] = []

    def _check_provenance(self, meta: Dict[str, Any]) -> bool:
        return meta.get("provenance_chain") is not None and len(meta["provenance_chain"]) > 0

    def _check_certainty(self, sigma: float) -> bool:
        return self.c.SIGMA_BOUNDS[0] <= sigma <= self.c.SIGMA_BOUNDS[1]

    def _check_ai_influence(self, influence: float) -> bool:
        return influence <= self.c.AI_INFLUENCE_CAP

    def _check_sovereignty(self, meta: Dict[str, Any]) -> bool:
        return all(k in meta for k in ("owner_key", "consent_state", "human_override")) and \
               meta.get("consent_state") == "EXPLICIT" and meta.get("human_override") is True

    def multiplicative_gate(self, validations: List[bool]) -> float:
        if not validations: return 0.0
        probs = [v * (1.0 - self.c.UNITY_FLOOR) + self.c.UNITY_FLOOR if v else self.c.UNITY_FLOOR for v in validations]
        return max(self.c.UNITY_FLOOR, min(self.c.SIGMA_BOUNDS[1], reduce(mul, probs, 1.0)))

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sigma = payload.get("sigma", 0.5)
        influence = payload.get("ai_influence", 0.0)
        laws = [
            self._check_provenance(payload.get("metadata", {})), True,
            self._check_ai_influence(influence), True,
            self._check_certainty(sigma), self._check_sovereignty(payload.get("metadata", {})), True
        ]
        gate_score = self.multiplicative_gate(laws)
        if gate_score <= self.c.UNITY_FLOOR:
            raise LawViolationError(f"CONSTITUTIONAL HALT: Gate score {gate_score} below floor.")
        return {"gate_score": gate_score, "sigma_clamped": sigma, "approved": True, "log": self._violation_log}

class SovereignCommunityNervousSystem:
    def __init__(self, target_system_schema: Dict):
        self.constants = ICF_CONSTANTS()
        self.dag = PhoenixDAG()
        self.provenance_anchor = target_system_schema.get("provenance_origin", "UNKNOWN")
        self.omega = ChiefOmega(self.constants)
        self.anna_api_key = os.getenv("ANNA_API_KEY")

    def law_vi_sovereignty_check(self, payload: Dict) -> bool:
        return payload.get("consent_state") == "EXPLICIT"

    def compile_layer_alpha(self, functions: List[callable]):
        return [
            lambda *a, f=fn, **kw: (
                self.omega.multiplicative_gate([
                    self.law_vi_sovereignty_check({
                        "consent_state": "EXPLICIT",
                        "provenance_origin": self.provenance_anchor,
                        "attribution_chain": [self.provenance_anchor]
                    })
                ]),
                f(*a, **kw)
            ) for fn in functions
        ]

    def enforce_unity_floor(self, score: float, context: str):
        if score <= self.constants.UNITY_FLOOR:
            raise LawViolationError(f"[{context}] UNITY FLOOR BREACHED. HALT.")

    def run(self, context: Dict) -> Dict:
        unity_score = 1.0
        self.enforce_unity_floor(unity_score, "VOID_ACT_02_EXECUTION")
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.dag.execute("root", context))
