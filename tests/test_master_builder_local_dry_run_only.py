import json
from pathlib import Path


def test_qubit_registry_is_local_dry_run_only():
    path = Path("data/omnisyntax_qubit_registry.jsonl")
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert records

    for record in records:
        assert record["status"] == "CODE_NEEDS_TEST"
        assert record["routing"] == "LOCAL_DRY_RUN_ONLY"
        assert record["deployment_gate"] == "CLOSED"
        assert record["confidence_sigma"] < 1.0
        assert record["active_validated"] is False


def test_arweave_bridge_remains_blocked():
    schema = json.loads(Path("data/arweave_identity_attestation_schema.json").read_text(encoding="utf-8"))

    assert schema["status"] == "CODE_NEEDS_TEST"
    assert schema["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert schema["deployment_gate"] == "CLOSED"
    assert schema["release_allowed"] is False
    assert schema["raw_payload_allowed"] is False
    assert schema["private_jwk_allowed"] is False
    assert schema["transaction_signing_allowed"] is False
    assert schema["arweave_upload_allowed"] is False
    assert schema["ipfs_pin_allowed"] is False
