from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

CURRENT_RELEASE_SET = {
    "docs/omnisyntax_evolving_v1_2.md",
    "docs/origin_intent_to_omnisyntax.md",
    "docs/mirror_partnership_boundary_protocol.md",
    "docs/omnisyntax_library_compression_v1.md",
    "docs/nexus_security_layers.md",
    "data/omnisyntax_library_capsule.json",
    "data/omnisyntax_qubit_registry.jsonl",
    "data/arweave_rsa_provisioning_qubits.json",
    "data/arweave_identity_attestation_schema.json",
    "schemas/omnisyntax_layer_model.schema.json",
    "schemas/umu_min_refined.schema.json",
    "gdl/__init__.py",
    "gdl/validation.py",
    "core/__init__.py",
    "core/tetrad_core_v4_2.py",
    "tests/test_no_pass_verified_sealed_deploy_claims.py",
    "tests/test_omnisyntax_boundary_capsule_schema.py",
    "tests/test_master_builder_local_dry_run_only.py",
    "tests/test_gdl_core_validation.py",
    "tests/test_tetrad_v4_2.py",
    "tests/test_identity_attestation_bridge.py",
    "tests/test_arweave_rsa_qubits_schema.py",
    "scripts/bootstrap_omnisyntax_v1_2.py",
    "logs/library_compression_report.json",
    "logs/validation_report.json",
    "logs/build_log.jsonl",
}

TEXT_SUFFIXES = {
    ".py", ".md", ".json", ".jsonl", ".txt", ".ps1", ".sh",
    ".yml", ".yaml", ".toml", ".tsx", ".ts", ".js", ".css", ".html",
}

BLOCKED_PATH_HINTS = [
    ".env",
    "dist/",
    "archive/",
    "core/vault/",
    "core/logs/",
    "target/",
    "node_modules/",
    ".next/",
    ".zip",
    ".bak",
    "secret",
    "vault",
]

CONTENT_PATTERNS = [
    ("PRIVATE_KEY", r"BEGIN\s+(RSA\s+)?PRIVATE\s+KEY|OPENSSH\s+PRIVATE\s+KEY"),
    ("FOUNDERS_SEED", r"FOUNDERS_SEED"),
    ("SEED_OR_MNEMONIC", r"seed[\s_-]?phrase|\bmnemonic\b"),
    ("JWK_PRIVATE_FIELDS", r'"(d|p|q|dp|dq|qi)"\s*:'),
    ("API_SECRET_TOKEN", r"api[\s_-]?key|secret[\s_-]?key|private[\s_-]?key|bearer\s+[A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,}"),
    ("FORBIDDEN_PROMOTION", r"\b(PASS|VERIFIED|SEALED|RUNTIME_SEALED|WAL_COMMIT_READY|PRODUCTION_READY)\b"),
    ("DEPLOYMENT_WORDING", r"\bproduction\s+ready\b|\bdeployment\s*[:=]\s*true\b|\bdeployed\s*[:=]\s*true\b"),
    ("CONFIDENCE_GE_1", r"(confidence_sigma|confidence|sigma|σ)\s*[:=]\s*1(\.0+)?\b"),
    ("NETWORK_PERSISTENCE", r"(arweave_upload|ipfs_pin|transaction_signing)\s*[:=]\s*(true|allowed)"),
]

COMPILED_PATTERNS = []
PATTERN_ERRORS = []

for name, pattern in CONTENT_PATTERNS:
    try:
        COMPILED_PATTERNS.append((name, re.compile(pattern, re.IGNORECASE)))
    except re.error as exc:
        PATTERN_ERRORS.append({"name": name, "pattern": pattern, "error": str(exc)})


def norm(path: str) -> str:
    return path.replace("\\", "/").strip()


def run_git_status() -> list[dict]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1"],
        text=True,
        capture_output=True,
        check=True,
    )
    items = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2]
        path = norm(line[3:])
        if " -> " in path:
            path = norm(path.split(" -> ", 1)[1])
        items.append({"status": status, "path": path})
    return items


def is_blocked_path(path: str) -> bool:
    lower = path.lower()
    return any(hint.lower() in lower for hint in BLOCKED_PATH_HINTS)


def sha256_file(path: Path, max_bytes: int = 2_000_000) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def scan_content(path: str) -> list[str]:
    p = ROOT / path
    if not p.exists() or not p.is_file():
        return ["MISSING_ON_DISK"]

    if p.suffix.lower() not in TEXT_SUFFIXES:
        return []

    try:
        if p.stat().st_size > 512_000:
            return ["SKIPPED_LARGE_TEXT_FILE"]
        text = p.read_text(encoding="utf-8-sig", errors="ignore")
    except OSError as exc:
        return [f"READ_ERROR:{exc}"]

    hits = []
    for name, regex in COMPILED_PATTERNS:
        if regex.search(text):
            hits.append(name)
    return hits


def classify(item: dict) -> dict:
    path = item["path"]
    status = item["status"]
    risks = scan_content(path)
    blocked_path = is_blocked_path(path)

    secret_risks = {
        "PRIVATE_KEY",
        "FOUNDERS_SEED",
        "SEED_OR_MNEMONIC",
        "JWK_PRIVATE_FIELDS",
        "API_SECRET_TOKEN",
    }
    claim_risks = {
        "FORBIDDEN_PROMOTION",
        "DEPLOYMENT_WORDING",
        "CONFIDENCE_GE_1",
        "NETWORK_PERSISTENCE",
    }

    if blocked_path or any(r in risks for r in secret_risks):
        bucket = "BLOCKED_DO_NOT_STAGE"
    elif path in CURRENT_RELEASE_SET:
        bucket = "CURRENT_OMNISYNTAX_RELEASE_CANDIDATE"
    elif status.strip().startswith("M"):
        bucket = "TRACKED_MODIFIED_REVIEW_BEFORE_COMMIT"
    elif path.startswith("docs/"):
        bucket = "DOCS_FUTURE_REVIEW"
    elif path.startswith(("tests/", "scripts/", "schemas/", "gdl/", "core/", "data/")):
        bucket = "CODE_OR_VALIDATION_FUTURE_REVIEW"
    elif path.startswith("logs/"):
        bucket = "LOCAL_EVIDENCE_LOG_REVIEW"
    elif path.startswith(("nexus-ui/", "sovereign-ui/", "mirror_app/", "experiments/", "registry/", "ollama/", "ginto_core/")):
        bucket = "FUTURE_CHAMBER_NOT_THIS_RELEASE"
    else:
        bucket = "UNSORTED_LOCAL_REVIEW"

    if any(r in risks for r in claim_risks):
        if bucket == "CURRENT_OMNISYNTAX_RELEASE_CANDIDATE":
            bucket = "CURRENT_CANDIDATE_NEEDS_REVIEW"
        elif bucket != "BLOCKED_DO_NOT_STAGE":
            bucket = "NEEDS_CLAIM_BOUNDARY_REVIEW"

    p = ROOT / path
    return {
        "status": status,
        "path": path,
        "bucket": bucket,
        "risks": risks,
        "sha256": sha256_file(p),
    }


def main() -> int:
    items = [classify(item) for item in run_git_status()]

    buckets = {}
    for item in items:
        buckets.setdefault(item["bucket"], []).append(item)

    report = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "status": "LOCAL_SCAN_ONLY",
        "deployment_gate": "CLOSED",
        "git_add_dot_allowed": False,
        "pattern_compile_errors": PATTERN_ERRORS,
        "total_items": len(items),
        "bucket_counts": {k: len(v) for k, v in sorted(buckets.items())},
        "items": items,
        "recommended_current_release_stage_list": [
            item["path"]
            for item in items
            if item["bucket"] == "CURRENT_OMNISYNTAX_RELEASE_CANDIDATE"
        ],
        "blocked_do_not_stage": [
            item["path"]
            for item in items
            if item["bucket"] == "BLOCKED_DO_NOT_STAGE"
        ],
        "needs_review": [
            item
            for item in items
            if item["bucket"] in {
                "CURRENT_CANDIDATE_NEEDS_REVIEW",
                "TRACKED_MODIFIED_REVIEW_BEFORE_COMMIT",
                "NEEDS_CLAIM_BOUNDARY_REVIEW",
                "UNSORTED_LOCAL_REVIEW",
            }
        ],
    }

    Path("logs").mkdir(exist_ok=True)
    Path("logs/local_file_candidate_scan.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Local File Candidate Scan",
        "",
        f"Status: {report['status']}",
        f"Deployment gate: {report['deployment_gate']}",
        f"Total items: {report['total_items']}",
        "",
        "## Bucket counts",
        "",
    ]

    for bucket, count in sorted(report["bucket_counts"].items()):
        lines.append(f"- {bucket}: {count}")

    lines += ["", "## Recommended current release candidates", ""]
    for path in report["recommended_current_release_stage_list"]:
        lines.append(f"- {path}")

    lines += ["", "## Blocked / do not stage", ""]
    for path in report["blocked_do_not_stage"][:200]:
        lines.append(f"- {path}")

    lines += ["", "## Needs review", ""]
    for item in report["needs_review"][:200]:
        risk = ", ".join(item["risks"]) if item["risks"] else "none"
        lines.append(f"- {item['path']} [{item['status']}] bucket={item['bucket']} risks={risk}")

    Path("logs/local_file_candidate_scan.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "status": report["status"],
        "deployment_gate": report["deployment_gate"],
        "total_items": report["total_items"],
        "bucket_counts": report["bucket_counts"],
        "recommended_current_release_count": len(report["recommended_current_release_stage_list"]),
        "blocked_count": len(report["blocked_do_not_stage"]),
        "needs_review_count": len(report["needs_review"]),
        "pattern_compile_errors": PATTERN_ERRORS,
        "outputs": [
            "logs/local_file_candidate_scan.json",
            "logs/local_file_candidate_scan.md",
        ],
    }, ensure_ascii=False, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
