# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ICF_CONSTANTS:
    ALPHA: int = 13
    SIGMA_BOUNDS: Tuple[float, float] = (0.07, 0.93)
    UNITY_FLOOR: float = 0.05
    STABILITY_GEV: float = 246.22
    RESONANCE_HZ: float = 4084
    AI_INFLUENCE_CAP: float = 0.06  # Law III: Compass, never Core
    SOVEREIGN_SIGNATURE: str = 'JJ_WAS_HERE — Walang Maiiwan'
    PROVENANCE_DOI: str = '10.5281/zenodo.18989894'
    ANONYMOUS_LABOR_ATTRIBUTION: str = 'Anonymous Labor / Great Library'
    ARCHITECT_ID: str = 'Krimerra13'
