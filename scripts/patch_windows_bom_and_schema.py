from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path.cwd()


def strip_bom(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False

    raw = path.read_bytes()
    bom = b"\xef\xbb\xbf"

    if raw.startswith(bom):
        path.write_bytes(raw[len(bom):])
        return True

    return False


def strip_all_boms() -> list[str]:
    changed = []

    patterns = [
        "data/*.json",
        "data/*.jsonl",
        "logs/*.json",
        "logs/*.jsonl",
        "schemas/*.json",
        "docs/*.md",
        "tests/*.py",
        "gdl/*.py",
        "core/*.py",
    ]

    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if strip_bom(path):
                changed.append(str(path))

    return changed


def patch_omnisyntax_schema() -> bool:
    path = ROOT / "schemas/omnisyntax_layer_model.schema.json"
    if not path.exists():
        return False

    schema = json.loads(path.read_text(encoding="utf-8-sig"))

    props = schema.setdefault("properties", {})
    required = schema.setdefault("required", [])

    if "constraints" not in required:
        required.append("constraints")

    props["constraints"] = {
        "type": "object",
        "required": [
            "L2_truth_gap",
            "L3_jj_final",
            "L6_local_first",
            "L7_walang_maiiwan",
            "L8_intelligence_for_human_good",
            "no_private_key_handling",
            "no_arweave_upload",
            "no_ipfs_pin",
            "no_autonomous_execution"
        ],
        "properties": {
            "L2_truth_gap": {"const": "confidence_sigma < 1.0"},
            "L3_jj_final": {"const": True},
            "L6_local_first": {"const": True},
            "L7_walang_maiiwan": {"const": True},
            "L8_intelligence_for_human_good": {"const": True},
            "no_private_key_handling": {"const": True},
            "no_arweave_upload": {"const": True},
            "no_ipfs_pin": {"const": True},
            "no_autonomous_execution": {"const": True}
        },
        "additionalProperties": False
    }

    path.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return True


def patch_constitutional_audit_windows() -> bool:
    path = ROOT / "tests/test_constitutional_audit.py"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8-sig")

    # Add imports if missing.
    if "import sys" not in text:
        text = text.replace("import subprocess", "import subprocess\nimport sys")

    # Safer subprocess capture on Windows. This handles tests that currently use
    # subprocess.run(..., capture_output=True, text=True).
    text = text.replace(
        "capture_output=True, text=True",
        "stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True"
    )

    # If tests call plain python instead of current interpreter, make it deterministic.
    text = text.replace('["python", "-m", "islah_nexus.cli"', '[sys.executable, "-m", "islah_nexus.cli"')
    text = text.replace("['python', '-m', 'islah_nexus.cli'", "[sys.executable, '-m', 'islah_nexus.cli'")

    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = {
        "bom_stripped": strip_all_boms(),
        "schema_patched": patch_omnisyntax_schema(),
        "constitutional_audit_windows_patched": patch_constitutional_audit_windows(),
    }

    out = ROOT / "logs/windows_bom_schema_patch_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(changed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(changed, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
