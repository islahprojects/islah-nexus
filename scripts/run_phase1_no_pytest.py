#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

UMU = Path("data/sample_umus.jsonl")
LOG = Path("logs/build_log.jsonl")

CONFIDENCE_KEYS = {
    "sigma", "σ", "confidence", "confidence_score", "score",
    "certainty", "probability", "truth_score", "validation_score",
}

BAD_STATUS = {"verified", "pass", "production ready", "production_ready"}
CUNEIFORM_RE = re.compile(r"[\U00012000-\U000123FF]")
FEAR_NULL_RE = re.compile(r"fear[\s_-]*nullification", re.IGNORECASE)


def walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def load_jsonl(path: Path):
    records = []
    if not path.exists():
        raise AssertionError(f"missing {path}")
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            raise AssertionError(f"line {line_no}: invalid JSONL: {e}") from e
        if not isinstance(obj, dict):
            raise AssertionError(f"line {line_no}: record must be object")
        records.append((line_no, obj))
    return records


def has_source(obj):
    return bool(obj.get("source_url") or obj.get("source_registry_path") or obj.get("local_source_registry_path"))


def main():
    errors = []

    try:
        records = load_jsonl(UMU)
    except AssertionError as e:
        records = []
        errors.append(str(e))

    if len(records) < 1:
        errors.append("sample_umus.jsonl has fewer than 1 entry")

    blob = json.dumps([r for _, r in records], ensure_ascii=False)

    if not any(ord(ch) > 127 for ch in blob):
        errors.append("no non-Latin script coverage found")

    for line_no, record in records:
        text = json.dumps(record, ensure_ascii=False)

        for key, value in walk(record):
            key_l = str(key).lower()

            if key_l in CONFIDENCE_KEYS and isinstance(value, (int, float)) and value >= 1.0:
                errors.append(f"line {line_no}: {key} must be < 1.0, got {value}")

            if key_l in {"status", "verdict", "claim_status", "validation_status"} and isinstance(value, str):
                if value.strip().lower() in BAD_STATUS:
                    errors.append(f"line {line_no}: forbidden status {value!r}; use PATCH or CODE-NEEDS-TEST")

        if "σ=1.00" in text or '"sigma": 1.0' in text or '"confidence": 1.0' in text:
            errors.append(f"line {line_no}: forbidden confidence/sigma equals 1.0")

        if any(k in record for k in ("operator", "protocol_operator", "glyph", "symbol", "name")) and not has_source(record):
            errors.append(f"line {line_no}: operator/protocol entry missing source_url or source_registry_path")

        if CUNEIFORM_RE.search(text):
            review = str(record.get("cultural_review") or record.get("review_status") or "")
            if review != "CULTURAL_REVIEW_REQUIRED":
                errors.append(f"line {line_no}: cuneiform requires CULTURAL_REVIEW_REQUIRED")

        if FEAR_NULL_RE.search(text):
            scope = str(record.get("psychology_status") or record.get("validation_scope") or record.get("status") or "").lower()
            if "symbolic" not in scope and "protocol" not in scope:
                errors.append(f"line {line_no}: Fear Nullification must be symbolic/protocol only")

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": "phase1_no_pytest_fallback",
        "runner": "stdlib_only",
        "file": str(UMU),
        "count": len(records),
        "passed": not errors,
        "errors": errors,
        "status": "CODE-NEEDS-TEST" if not errors else "PATCH",
        "note": "Local fallback only; does not replace CI/pytest."
    }

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")

    print(json.dumps(event, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
