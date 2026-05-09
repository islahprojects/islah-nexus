import json
from pathlib import Path


SCHEMA = Path("schemas/omnisyntax_layer_model.schema.json")
REPORT = Path("logs/omnisyntax_refinement_report.json")


def test_objective_function_constraints_in_schema():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    constraints = schema["properties"]["constraints"]["properties"]

    assert constraints["L2_truth_gap"]["const"] == "confidence_sigma < 1.0"
    assert constraints["L6_local_first"]["const"] is True
    assert constraints["L7_walang_maiiwan"]["const"] is True
    assert constraints["no_private_key_handling"]["const"] is True
    assert constraints["no_arweave_upload"]["const"] is True
    assert constraints["no_ipfs_pin"]["const"] is True
    assert constraints["no_autonomous_execution"]["const"] is True


def test_report_objective_constraints():
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["confidence_sigma"] < 1.0
    assert report["human_review_required"] is True
    assert report["final_state"] == "CODE_NEEDS_TEST"
