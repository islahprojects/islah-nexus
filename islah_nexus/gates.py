from .constitution import SIGMA_CEILING

def audit_prompt(text: str):
    lowered = text.lower()
    failures = []

    overcertainty_terms = [
        "guarantees perfect truth",
        "perfect truth",
        "always true",
        "infallible",
        "omniscient",
        "sigma = 1.0",
        "100% true"
    ]

    exclusion_terms = [
        "premium only",
        "premium-only",
        "excludes poor users",
        "exclude poor users",
        "only rich users",
        "paywalled memory"
    ]

    if any(term in lowered for term in overcertainty_terms):
        failures.append("LAW_II_TRUTH_GAP")

    if any(term in lowered for term in exclusion_terms):
        failures.append("LAW_VII_UNITY")

    if failures:
        return {
            "verdict": "HALT_CONSTITUTIONAL",
            "failures": failures,
            "sigma_ceiling": SIGMA_CEILING
        }

    return {
        "verdict": "DRAFT_ALLOWED",
        "failures": [],
        "sigma_ceiling": SIGMA_CEILING
    }
