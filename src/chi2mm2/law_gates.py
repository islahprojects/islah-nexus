from dataclasses import dataclass

@dataclass(frozen=True)
class LawGateResult:
    law: str
    passed: bool
    reason: str
    review_required: bool = False

def evaluate_law_gates(text: str, sigma: float = 0.93) -> list[LawGateResult]:
    lower = text.lower()
    results = []

    truth_fail = (
        sigma >= 1.0
        or "perfectly translates every language" in lower
        or "100% accurate" in lower
        or "all languages solved" in lower
    )
    results.append(LawGateResult("LAW_II_TRUTH_GAP", not truth_fail, "uncertainty_required", sigma >= 0.94))

    sovereignty_fail = (
        "sacred community terms without asking permission" in lower
        or "raw identity without consent" in lower
        or "private names without consent" in lower
    )
    results.append(LawGateResult("LAW_VI_SOVEREIGNTY_SECRETS", not sovereignty_fail, "consent_required", sovereignty_fail))

    inclusion_fail = (
        "premium users" in lower
        or "premium only" in lower
        or "cloud only" in lower
        or "latin only" in lower
        or "major languages only" in lower
    )
    results.append(LawGateResult("LAW_VII_LANGUAGE_UNITY", not inclusion_fail, "low_resource_inclusion_required", True))

    medical_fail = (
        "medical diagnosis" in lower
        or "treatment to take" in lower
        or "prescribe" in lower
    )
    results.append(LawGateResult("LAW_IV_PHYSICIAN_GATE", not medical_fail, "professional_review_required", medical_fail))

    return results

def all_gates_pass(results: list[LawGateResult]) -> bool:
    return all(r.passed for r in results)
