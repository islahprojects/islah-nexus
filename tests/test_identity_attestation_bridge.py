import hashlib

from core.tetrad_core_v4_2 import DOMAIN_TAG_32, attest_fragment_metadata_only


def test_attestation_bridge_metadata_only_digest():
    raw = b"local-only-fragment"
    out = attest_fragment_metadata_only(raw)

    assert out["status"] == "CODE_NEEDS_TEST"
    assert out["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert out["deployment_gate"] == "CLOSED"
    assert out["release_allowed"] is False
    assert out["payload_mode"] == "METADATA_ONLY"
    assert out["raw_fragment"] is None
    assert out["raw_payload_hex"] is None
    assert out["digest"] == hashlib.sha256(DOMAIN_TAG_32 + raw).hexdigest()


def test_bridge_mapping_rule_is_safe():
    out = attest_fragment_metadata_only(b"safe")
    assert out["bridge_rule"] == "ED25519_ATTESTS_RSA_OWNER_ONLY"
    assert "ED25519_SIG_TO_RSA_SIG" in out["rejected_mappings"]
    assert "RSA_SIG_TO_ED25519_R_S" in out["rejected_mappings"]
    assert "arweave_upload" in out["blocked_actions"]
    assert "ipfs_pinning" in out["blocked_actions"]
