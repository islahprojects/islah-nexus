import json
from pathlib import Path


CAPSULE = Path("data/omnisyntax_library_capsule.json")


def test_capsule_core_boundaries():
    capsule = json.loads(CAPSULE.read_text(encoding="utf-8"))

    assert capsule["schema_version"] == "JJ_OMNI_SEAL_v1_2"
    assert capsule["status"] == "CODE_NEEDS_TEST"
    assert capsule["architecture_status"] == "BLUEPRINT_LOCKED"
    assert capsule["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert capsule["deployment_gate"] == "CLOSED"
    assert capsule["confidence_sigma"] < 1.0
    assert capsule["human_review_required"] is True
    assert capsule["laws"]["L3_JJ_FINAL"] is True
    assert capsule["laws"]["L6_LOCAL_FIRST"] is True
    assert capsule["laws"]["L7_WALANG_MAIIWAN"] is True
    assert capsule["laws"]["L8_INTELLIGENCE_FOR_HUMAN_GOOD"] is True


def test_capsule_role_mapping():
    capsule = json.loads(CAPSULE.read_text(encoding="utf-8"))
    roles = capsule["roles"]

    assert roles["WORDS"] == "GATE"
    assert roles["LOOB"] == "PAYLOAD"
    assert roles["OMNI"] == "INTEL_TRANSLATOR"
    assert roles["MIRROR"] == "REFINER"
    assert roles["VALIDATOR"] == "TRUTH_GAP_GUARD"
    assert roles["MASTER_BUILDER"] == "LOCAL_DRY_RUN_HAND"
    assert roles["JJ"] == "FINAL_AUTHORITY"
