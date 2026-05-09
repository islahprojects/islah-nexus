import json
import re
from pathlib import Path


DOCS = [
    Path("docs/omnisyntax_refined_v1_1.md"),
    Path("docs/mirror_partnership_boundary_protocol.md"),
    Path("docs/origin_intent_to_omnisyntax.md"),
]

REPORT = Path("logs/omnisyntax_refinement_report.json")
SCHEMA = Path("schemas/omnisyntax_layer_model.schema.json")


def read_all_text():
    return "\n".join(path.read_text(encoding="utf-8") for path in DOCS)


def test_required_files_exist():
    for path in DOCS + [REPORT, SCHEMA]:
        assert path.exists(), f"missing {path}"


def test_status_boundaries_are_local_only():
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["status"] == "CODE_NEEDS_TEST"
    assert report["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert report["deployment_gate"] == "CLOSED"
    assert report["human_authority"] == "JJ_FINAL_AUTHORITY"
    assert report["confidence_sigma"] < 1.0
    assert report["release_allowed"] is False


def test_forbidden_positive_status_assignments_absent():
    text = read_all_text()
    forbidden_assignment = re.compile(
        r"(status|verdict|final_state)\s*[:=]\s*(PASS|VERIFIED|SEALED)\b",
        re.IGNORECASE,
    )
    assert not forbidden_assignment.search(text)
