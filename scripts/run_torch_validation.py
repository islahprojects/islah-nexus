from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


LOG = Path("logs/build_log.jsonl")
REPORT = Path("logs/validation_report.json")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_log(event: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": now(), **event}, ensure_ascii=False, sort_keys=True) + "\n")


def run_pytest() -> tuple[int, str]:
    cmd = [sys.executable, "-m", "pytest", "tests/test_tetrad_v4_2.py", "-q"]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def main() -> int:
    pytest_code, pytest_output = run_pytest()

    technical_pass = pytest_code == 0
    human_review_required = True

    if not technical_pass:
        exit_code = 1
        status = "TECHNICAL_VALIDATION_FAILURE"
    elif human_review_required:
        exit_code = 2
        status = "TECHNICAL_PASS_GOVERNANCE_HOLD"
    else:
        exit_code = 0
        status = "TECHNICAL_PASS_NO_REVIEW_HOLD"

    report = {
        "schema_version": "torch_validation_report_v1",
        "ts": now(),
        "status": status,
        "architecture_status": "BLUEPRINT_LOCKED",
        "code_status": "CODE_NEEDS_TEST",
        "routing": "LOCAL_DRY_RUN_ONLY",
        "deployment_gate": "CLOSED",
        "technical_pass": technical_pass,
        "human_review_required": human_review_required,
        "release_allowed": False,
        "pytest_exit_code": pytest_code,
        "expected_exit_code": exit_code,
        "pytest_output": pytest_output,
        "blocked": [
            "real_ed25519_signing_backend",
            "real_rsa_jwk_private_key_loading",
            "arweave_transaction_signing",
            "arweave_upload",
            "ipfs_pinning",
            "account_creation"
        ],
        "truth_gap": {
            "confidence_sigma": 0.94,
            "rule": "confidence_sigma < 1.0"
        }
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    append_log({
        "event": "torch_validation",
        "status": status,
        "technical_pass": technical_pass,
        "human_review_required": human_review_required,
        "exit_code": exit_code,
        "report": str(REPORT),
    })

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
