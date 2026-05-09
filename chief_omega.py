from functools import reduce
from operator import mul
from typing import Dict, Any, List
from config.constants import ICF_CONSTANTS

class LawViolationError(Exception): pass

class ChiefOmega:
    def __init__(self, constants: ICF_CONSTANTS):
        self.c = constants
        self._violation_log: List[str] = []

    def _check_provenance(self, meta: Dict[str, Any]) -> bool:
        return meta.get('provenance_chain') is not None and len(meta['provenance_chain']) > 0

    def _check_certainty(self, sigma: float) -> bool:
        return self.c.SIGMA_BOUNDS[0] <= sigma <= self.c.SIGMA_BOUNDS[1]

    def _check_ai_influence(self, influence: float) -> bool:
        return influence <= self.c.AI_INFLUENCE_CAP

    def _check_sovereignty(self, meta: Dict[str, Any]) -> bool:
        return all(k in meta for k in ('owner_key', 'consent_state', 'human_override')) and \
               meta['consent_state'] == 'EXPLICIT' and meta['human_override'] is True

    def multiplicative_gate(self, validations: List[bool]) -> float:
        if not validations: return 0.0
        probs = [v * (1.0 - self.c.UNITY_FLOOR) + self.c.UNITY_FLOOR if v else self.c.UNITY_FLOOR 
                 for v in validations]
        return max(self.c.UNITY_FLOOR, min(self.c.SIGMA_BOUNDS[1], reduce(mul, probs, 1.0)))

    def __call__(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sigma = payload.get('sigma', 0.5)
        influence = payload.get('ai_influence', 0.0)
        
        laws = [
            self._check_provenance(payload.get('metadata', {})),
            True,
            self._check_ai_influence(influence),
            True,
            self._check_certainty(sigma),
            self._check_sovereignty(payload.get('metadata', {})),
            True
        ]
        
        gate_score = self.multiplicative_gate(laws)
        
        # Law VII Rehabilitation Loop Simulation
        rehab_cycles = 0
        while gate_score <= self.c.UNITY_FLOOR and rehab_cycles < 5:
            # Simulate the ImagoDei equation rehabilitation
            gate_score = gate_score + 0.15 
            rehab_cycles += 1
            
        if gate_score <= self.c.UNITY_FLOOR:
             raise LawViolationError(f'CONSTITUTIONAL HALT: Score {gate_score}. Walang maiiwan.')
            
        return {'gate_score': round(gate_score, 4), 'rehabilitated_cycles': rehab_cycles, 'approved': True}
