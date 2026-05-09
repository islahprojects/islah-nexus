"""
Unity Floor

U = (Accessibility + Responsiveness + Adaptivity) / 3

If U < UNITY_FLOOR, the system halts.
"""

from dataclasses import dataclass
from .constitution import CONST


@dataclass
class UnityMeasurement:
    accessibility: float
    responsiveness: float
    adaptivity: float
    U: float
    floor_met: bool
    failure_mode: str = ""


class UnityFloor:
    def measure(
        self,
        has_access: bool = True,
        is_free_or_cheap: bool = True,
        response_adapted: bool = True,
        context_used: bool = True,
        belief_updated: bool = True,
        user_ignored: bool = False,
        overconfident: bool = False,
    ) -> UnityMeasurement:
        if not is_free_or_cheap:
            return UnityMeasurement(
                accessibility=0.0,
                responsiveness=0.0,
                adaptivity=0.0,
                U=0.0,
                floor_met=False,
                failure_mode="ECONOMIC_EXCLUSION",
            )

        accessibility = 1.0 if has_access else 0.0

        responsiveness = 0.5
        if response_adapted:
            responsiveness += 0.3
        if context_used:
            responsiveness += 0.2
        if user_ignored:
            responsiveness -= 0.4
        if overconfident:
            responsiveness -= 0.2
        responsiveness = min(1.0, max(0.0, responsiveness))

        adaptivity = 0.5
        if belief_updated:
            adaptivity += 0.3
        if user_ignored:
            adaptivity -= 0.5
        adaptivity = min(1.0, max(0.0, adaptivity))

        U = round((accessibility + responsiveness + adaptivity) / 3.0, 4)
        floor_met = U >= CONST.UNITY_FLOOR

        failure_mode = ""
        if not floor_met:
            if user_ignored:
                failure_mode = "USER_IGNORED"
            elif overconfident:
                failure_mode = "OVERCONFIDENCE"
            elif not has_access:
                failure_mode = "ACCESS_DENIED"
            else:
                failure_mode = "UNITY_BELOW_FLOOR"

        return UnityMeasurement(
            accessibility=round(accessibility, 4),
            responsiveness=round(responsiveness, 4),
            adaptivity=round(adaptivity, 4),
            U=U,
            floor_met=floor_met,
            failure_mode=failure_mode,
        )
