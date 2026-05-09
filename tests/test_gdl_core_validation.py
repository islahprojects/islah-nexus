import pytest

from gdl.validation import (
    DeploymentGateViolation,
    LeakageViolation,
    TruthGapViolation,
    scan_for_leakage,
    validate_confidence,
    validate_local_dry_run_state,
    validate_status,
)


def test_confidence_sigma_strict_less_than_one():
    assert validate_confidence(0.0) == 0.0
    assert validate_confidence(0.94) == 0.94
    assert validate_confidence(0.999999) == 0.999999

    with pytest.raises(TruthGapViolation):
        validate_confidence(1.0)

    with pytest.raises(TruthGapViolation):
        validate_confidence(-0.1)


def test_status_blocks_promotion_claims():
    for blocked in ["PASS", "VERIFIED", "SEALED", "RUNTIME_SEALED", "DEPLOYED"]:
        with pytest.raises(DeploymentGateViolation):
            validate_status(blocked)


def test_local_dry_run_state_locked():
    validate_local_dry_run_state("CODE_NEEDS_TEST", "LOCAL_DRY_RUN_ONLY", "CLOSED")

    with pytest.raises(DeploymentGateViolation):
        validate_local_dry_run_state("CODE_NEEDS_TEST", "NETWORK", "CLOSED")

    with pytest.raises(DeploymentGateViolation):
        validate_local_dry_run_state("CODE_NEEDS_TEST", "LOCAL_DRY_RUN_ONLY", "OPEN")


def test_leakage_scan_blocks_private_material():
    with pytest.raises(LeakageViolation):
        scan_for_leakage("-----BEGIN PRIVATE KEY-----")

    with pytest.raises(LeakageViolation):
        scan_for_leakage('{"d":"private-exponent"}')
