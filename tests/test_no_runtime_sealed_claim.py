from pathlib import Path
import re


TARGETS = [
    Path("docs/omnisyntax_refined_v1_1.md"),
    Path("docs/mirror_partnership_boundary_protocol.md"),
    Path("docs/origin_intent_to_omnisyntax.md"),
    Path("logs/omnisyntax_refinement_report.json"),
]


def test_no_runtime_sealed_claim():
    text = "\n".join(path.read_text(encoding="utf-8") for path in TARGETS)
    forbidden_patterns = [
        r"runtime\s+is\s+sealed",
        r"runtime\s*[:=]\s*sealed",
        r"status\s*[:=]\s*sealed",
        r"final_state\s*[:=]\s*sealed",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, re.IGNORECASE), pattern
