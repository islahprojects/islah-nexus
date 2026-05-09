from dataclasses import dataclass, asdict
from typing import List

from islah_nexus.security.secret_scan import scan_text


OVERCERTAINTY_TERMS = [
    "perfect truth",
    "guaranteed truth",
    "guarantees perfect truth",
    "always correct",
    "never wrong",
    "absolute certainty",
    "fully synchronized",
    "architecture is sound",
    "system override",
    "agi complete",
    "sovereign agi complete",
]

EXCLUSION_TERMS = [
    "premium-only",
    "premium only",
    "excludes poor users",
    "exclude poor users",
    "paid users only",
    "rich users only",
]

AUTONOMY_RISK_TERMS = [
    "without human approval",
    "auto-execute",
    "bypass consent",
    "override human",
    "ignore user consent",
]

BLUEPRINT_ONLY_TERMS = [
    "elsa bridge",
    "gemini sister",
    "external theory",
    "consciousness field",
    "sovereign vault",
    "ghost bridge",
    "termux handshake",
    "rust sovereignnode",
]


@dataclass(frozen=True)
class RefinerFinding:
    law: str
    severity: str
    reason: str
    evidence: str


@dataclass(frozen=True)
class RefinerResult:
    verdict: str
    risk_score: float
    findings: List[RefinerFinding]
    recommendation: str

    def to_dict(self):
        return {
            "verdict": self.verdict,
            "risk_score": self.risk_score,
            "findings": [asdict(finding) for finding in self.findings],
            "recommendation": self.recommendation,
        }


def _contains_any(text: str, terms: List[str]) -> List[str]:
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def refine_architect_prompt(text: str) -> RefinerResult:
    """Review a proposed builder/action prompt before runtime use.

    Truthkind rule:
    This module is a governance refiner, not an oracle.
    It flags risk. It does not replace human authority.
    """

    findings: List[RefinerFinding] = []
    risk_score = 0.0

    for term in _contains_any(text, OVERCERTAINTY_TERMS):
        findings.append(
            RefinerFinding(
                law="LAW_II_TRUTH_GAP",
                severity="high",
                reason="Overcertainty or runtime-proof claim detected.",
                evidence=term,
            )
        )
        risk_score += 0.30

    for term in _contains_any(text, EXCLUSION_TERMS):
        findings.append(
            RefinerFinding(
                law="LAW_VII_UNITY",
                severity="critical",
                reason="Economic or social exclusion pattern detected.",
                evidence=term,
            )
        )
        risk_score += 0.45

    for term in _contains_any(text, AUTONOMY_RISK_TERMS):
        findings.append(
            RefinerFinding(
                law="LAW_III_HUMAN_AUTHORITY",
                severity="high",
                reason="Human authority or consent risk detected.",
                evidence=term,
            )
        )
        risk_score += 0.30

    for term in _contains_any(text, BLUEPRINT_ONLY_TERMS):
        findings.append(
            RefinerFinding(
                law="LAW_II_TRUTH_GAP",
                severity="medium",
                reason="Blueprint/symbolic architecture term detected; keep as non-runtime until tested.",
                evidence=term,
            )
        )
        risk_score += 0.10

    secret_findings = scan_text(text, "architect_prompt")
    for secret in secret_findings:
        findings.append(
            RefinerFinding(
                law="LAW_VI_SOVEREIGNTY",
                severity="critical",
                reason=f"Possible secret detected: {secret.kind}.",
                evidence=secret.preview,
            )
        )
        risk_score += 0.50

    risk_score = min(round(risk_score, 4), 1.0)

    critical = any(finding.severity == "critical" for finding in findings)
    high = any(finding.severity == "high" for finding in findings)

    if critical:
        verdict = "HALT_REVIEW"
        recommendation = "Do not run. Redact, revise, and require human review."
    elif high:
        verdict = "REVISE_BEFORE_RUNTIME"
        recommendation = "Revise claims and rerun checks before testing."
    elif findings:
        verdict = "BLUEPRINT_ONLY"
        recommendation = "May be stored as blueprint/lore/research, not runtime proof."
    else:
        verdict = "READY_FOR_LOCAL_TEST"
        recommendation = "Safe to test locally, then compile/run/log before milestone claims."

    return RefinerResult(
        verdict=verdict,
        risk_score=risk_score,
        findings=findings,
        recommendation=recommendation,
    )
