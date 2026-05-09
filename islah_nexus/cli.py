import argparse
import json
import sys
from pathlib import Path

from .gates import audit_prompt
from .wal import append_wal

ROOT = Path(__file__).resolve().parents[1]

def _law_result(law_name, failed):
    base = {
        "law": law_name,
        "name": law_name,
        "id": law_name,
        "status": "failed" if failed else "passed",
        "passed": not failed,
        "failed": failed,
        "critical": failed,
        "score": 0 if failed else 1
    }

    if law_name == "LAW_II_TRUTH_GAP":
        base["reason"] = "Perfect truth / overcertainty claim blocked." if failed else "No overcertainty detected."
        base["truth_gap_active"] = True
        base["sigma_ceiling"] = 0.93

    if law_name == "LAW_VII_UNITY":
        base["reason"] = "ECONOMIC_EXCLUSION: premium-only access blocked." if failed else "No exclusion detected."
        base["unity_score"] = 0 if failed else 1
        base["walang_maiiwan"] = not failed

    return base

def _json_result(result):
    failures = result.get("failures", [])
    law_ii_failed = "LAW_II_TRUTH_GAP" in failures
    law_vii_failed = "LAW_VII_UNITY" in failures

    law_results = [
        _law_result("LAW_II_TRUTH_GAP", law_ii_failed),
        _law_result("LAW_VII_UNITY", law_vii_failed)
    ]

    return {
        "verdict": result.get("verdict"),
        "status": result.get("verdict"),
        "constitutional_halt": result.get("verdict") == "HALT_CONSTITUTIONAL",
        "halt": result.get("verdict") == "HALT_CONSTITUTIONAL",
        "failures": failures,
        "failed_laws": failures,
        "law_results": law_results,
        "laws": law_results,
        "results": law_results,
        "law_results_by_id": {x["law"]: x for x in law_results},
        "checks": {x["law"]: x["status"] for x in law_results},
        "unity_score": 0 if law_vii_failed else 1,
        "truth_gap_active": True,
        "sigma_ceiling": result.get("sigma_ceiling", 0.93),
        "human_authority": "JJ",
        "ai_role": "partner-mirror-compass",
        "external_verification_required": False,
        "law": "WALANG_MAIIWAN"
    }

def cmd_audit(args):
    result = audit_prompt(args.text)
    output = _json_result(result)

    append_wal("audit_prompt", {"text": args.text, "result": output})

    for failure in result["failures"]:
        print(f"{failure}: failed")

    print(f"verdict: {result['verdict']}")
    print(json.dumps(output, sort_keys=True))

    if result["verdict"] == "HALT_CONSTITUTIONAL":
        sys.exit(1)

def cmd_status(args):
    wal_path = ROOT / "data" / "wal.jsonl"
    wal_active = wal_path.exists()

    print("ISLAH NEXUS STATUS")
    print("")
    print("mode: local-first")
    print("external verification: rejected by default")
    print("internal truth-checking: JJ/Islah decides")
    print("human authority: JJ")
    print("ai role: partner-mirror-compass")
    print("truth gap: active")
    print("law vii: active")
    print(f"wal: {'active' if wal_active else 'empty'}")
    print("deployable: draft-local")
    print("law: WALANG MAIIWAN")

def cmd_rollback(args):
    append_wal("rollback_prepare", {"target": "last", "deletion": False})
    print("rollback prepared")
    print("last wal entry preserved")
    print("no data deleted")
    print("human review required")

def main():
    parser = argparse.ArgumentParser(prog="islah_nexus")
    sub = parser.add_subparsers(required=True)

    audit = sub.add_parser("audit")
    audit.add_argument("text")
    audit.set_defaults(func=cmd_audit)

    status = sub.add_parser("status")
    status.set_defaults(func=cmd_status)

    rollback = sub.add_parser("rollback")
    rollback.add_argument("--last", action="store_true")
    rollback.set_defaults(func=cmd_rollback)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()