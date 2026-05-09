import pytest

from core.tetrad_core_v4_2 import (
    DEPLOYMENT_GATE,
    ROUTING,
    STATUS,
    attest_fragment_metadata_only,
    build_default_tetrad,
    runtime_state,
    validate_public_crypto_metadata,
)
from gdl.validation import LeakageViolation, TruthGapViolation, validate_confidence


def test_default_tetrad_validates_local_dry_run_only():
    result = build_default_tetrad().validate()
    assert result["status"] == "CODE_NEEDS_TEST"
    assert result["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert result["deployment_gate"] == "CLOSED"
    assert result["release_allowed"] is False
    assert result["human_review_required"] is True


def test_confidence_strictly_below_one():
    assert validate_confidence(0.94) == 0.94
    with pytest.raises(TruthGapViolation):
        validate_confidence(1.0)
    with pytest.raises(TruthGapViolation):
        validate_confidence(1.01)


def test_attestation_digest_only_no_raw_payload():
    raw = b"safe local test fragment"
    output = attest_fragment_metadata_only(raw)
    rendered = str(output)

    assert output["payload_mode"] == "METADATA_ONLY"
    assert output["raw_fragment"] is None
    assert output["raw_payload_hex"] is None
    assert raw.decode() not in rendered
    assert output["release_allowed"] is False
    assert "arweave_upload" in output["blocked_actions"]
    assert "ipfs_pinning" in output["blocked_actions"]


def test_leakage_rejected_before_hashing():
    with pytest.raises(LeakageViolation):
        attest_fragment_metadata_only(b"-----BEGIN PRIVATE KEY-----\nabc")


def test_ed25519_public_key_length_validation():
    valid = bytes([1]) * 32
    result = validate_public_crypto_metadata(ed25519_public_key=valid)
    assert result["ed25519_public_key_valid"] is True
    assert result["private_key_loaded"] is False
    assert result["signing_enabled"] is False

    with pytest.raises(ValueError):
        validate_public_crypto_metadata(ed25519_public_key=b"too-short")


def test_bad_rsa_modulus_rejected():
    with pytest.raises(ValueError):
        validate_public_crypto_metadata(rsa_public_modulus_n=b"short")


def test_runtime_state_locked():
    state = runtime_state()
    assert state["status"] == "CODE_NEEDS_TEST"
    assert state["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert state["deployment_gate"] == "CLOSED"
    assert state["human_review_required"] is True
    assert state["confidence_sigma"] < 1.0
