from __future__ import annotations

import re


class TruthGapViolation(ValueError):
    pass


class DeploymentGateViolation(ValueError):
    pass


class LeakageViolation(ValueError):
    pass


BLOCKED_STATUSES = {
    "PASS",
    "VERIFIED",
    "SEALED",
    "RUNTIME_SEALED",
    "DEPLOYED",
    "PRODUCTION",
    "PRODUCTION_ACTIVATION",
}

ALLOWED_STATUSES = {
    "CODE_NEEDS_TEST",
    "BLUEPRINT_LOCKED",
    "LOCAL_DRY_RUN_ONLY",
    "DRAFT",
    "PATCH",
    "HUMAN_REVIEW_REQUIRED",
    "SYMBOLIC_FRAME_NOT_RUNTIME_PROOF",
}


def validate_confidence(value: float, field_name: str = "confidence_sigma") -> float:
    if not isinstance(value, (int, float)):
        raise TruthGapViolation(f"{field_name} must be numeric")
    value = float(value)
    if value < 0.0 or value >= 1.0:
        raise TruthGapViolation(
            f"ERROR_TRUTH_GAP_VIOLATION | BLOCK_COMMIT | {field_name}={value}"
        )
    return value


def validate_status(status: str) -> str:
    normalized = str(status).strip().upper()
    if normalized in BLOCKED_STATUSES:
        raise DeploymentGateViolation(f"blocked runtime promotion status: {status}")
    if normalized not in ALLOWED_STATUSES:
        raise DeploymentGateViolation(f"unsupported status for local dry-run: {status}")
    return normalized


def validate_local_dry_run_state(status: str, routing: str, deployment_gate: str) -> None:
    validate_status(status)
    if routing != "LOCAL_DRY_RUN_ONLY":
        raise DeploymentGateViolation("routing must remain LOCAL_DRY_RUN_ONLY")
    if deployment_gate != "CLOSED":
        raise DeploymentGateViolation("deployment_gate must remain CLOSED")


def scan_for_leakage(payload: bytes | str) -> None:
    if isinstance(payload, bytes):
        text = payload.decode("utf-8", errors="ignore")
    else:
        text = payload

    patterns = [
        r"BEGIN\s+(RSA\s+)?PRIVATE\s+KEY",
        r"OPENSSH\s+PRIVATE\s+KEY",
        r"FOUNDERS_SEED",
        r"seed[_\s-]?phrase",
        r"\bmnemonic\b",
        r'"d"\s*:',
        r'"p"\s*:',
        r'"q"\s*:',
        r'"dp"\s*:',
        r'"dq"\s*:',
        r'"qi"\s*:',
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.I):
            raise LeakageViolation(f"leakage pattern detected: {pattern}")
