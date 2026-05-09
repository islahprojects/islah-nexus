import json
from pathlib import Path


def test_arweave_rsa_qubits_block_private_key_paths():
    data = json.loads(Path("data/arweave_rsa_provisioning_qubits.json").read_text(encoding="utf-8"))

    assert data["status"] == "CODE_NEEDS_TEST"
    assert data["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert data["deployment_gate"] == "CLOSED"
    assert data["release_allowed"] is False
    assert data["confidence_sigma"] < 1.0
    assert data["private_jwk_loading"] == "BLOCKED"
    assert data["key_generation"] == "BLOCKED"
    assert data["transaction_signing"] == "BLOCKED"
    assert data["arweave_upload"] == "BLOCKED"
    assert data["human_review_required"] is True


def test_arweave_identity_attestation_schema_metadata_only():
    data = json.loads(Path("data/arweave_identity_attestation_schema.json").read_text(encoding="utf-8"))

    assert data["attestation_mode"] == "METADATA_ONLY"
    assert data["raw_payload_allowed"] is False
    assert data["private_jwk_allowed"] is False
    assert data["transaction_signing_allowed"] is False
    assert data["arweave_upload_allowed"] is False
    assert data["ipfs_pin_allowed"] is False
