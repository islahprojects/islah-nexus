import json
from pathlib import Path


REPORT = Path("logs/omnisyntax_refinement_report.json")
DOC = Path("docs/omnisyntax_refined_v1_1.md")


def test_no_production_activation_allowed():
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["runtime_activation_allowed"] is False
    assert report["network_persistence_allowed"] is False
    assert report["private_key_handling_allowed"] is False
    assert report["deployment_gate"] == "CLOSED"

    text = DOC.read_text(encoding="utf-8")
    assert "No production activation is authorized." in text
    assert "No network persistence is authorized." in text
    assert "No private key material is authorized." in text
