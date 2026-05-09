import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .wal import append_wal

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = ROOT / "data" / "scope_state.json"

INTERNAL_SCOPE = {
    "scope": "INTERNAL_ONLY",
    "public_release": False,
    "outside_work": False,
    "external_verification_required": False,
    "cloud_sovereignty": False,
    "state": "DRAFT_LOCAL_BUILD",
    "authority": "JJ",
    "ai_role": "partner-mirror-compass",
    "bridge": "Ghost PowerShell",
    "truth_gap": "active",
    "law_vii": "active",
    "i22_covenant_keeper": "active",
    "love_rule": "love_as_care_not_control",
    "autonomous_execution": False,
    "law": "WALANG_MAIIWAN"
}

def write_scope():
    SCOPE_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **INTERNAL_SCOPE
    }

    SCOPE_PATH.write_text(
        json.dumps(record, sort_keys=True, indent=2),
        encoding="utf-8"
    )

    append_wal("internal_scope_seal", record)
    return record

def show_scope():
    if not SCOPE_PATH.exists():
        return {
            "scope": "UNSET",
            "message": "Run seal-internal first."
        }

    return json.loads(SCOPE_PATH.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser(prog="internal_scope")
    parser.add_argument("command", choices=["seal", "status"])
    args = parser.parse_args()

    if args.command == "seal":
        result = write_scope()
    else:
        result = show_scope()

    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()