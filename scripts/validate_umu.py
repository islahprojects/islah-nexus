#!/usr/bin/env python3
"""
UMU validator for Islah Nexus Phase I.

Status discipline:
- No VERIFIED from this script.
- No sigma/confidence/score value may equal or exceed 1.0.
- Protocol/operator entries need source_url or local source_registry_path.
- Cuneiform operators require CULTURAL_REVIEW_REQUIRED.
- Fear Nullification must remain symbolic/protocol language, not validated psychology.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


NUMERIC_CONFIDENCE_KEYS = {
    "sigma", "σ", "confidence", "confidence_score", "score",
    "certainty", "probability", "truth_score", "validation_score",
}

STATUS_KEYS = {"status", "verdict", "claim_status", "validation_status"}
BAD_VERIFIED = {"verified", "pass", "production_ready", "production ready"}
CUNEIFORM_RE = re.compile(r"[\U00012000-\U000123FF]")
FEAR_NULL_RE = re.compile(r"fear[\s_-]*nullification", re.IGNORECASE)


def iter_values(obj: Any, path: str = "$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield path + "." + str(k), k, v
            yield from iter_values(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from iter_values(v, f"{path}[{i}]")


def has_source(obj: dict[str, Any]) -> bool:
    return bool(
        obj.get("source_url")
        or obj.get("source_registry_path")
        or obj.get("local_source_registry_path")
    )


def validate_record(obj: dict[str, Any], line_no: int) -> list[str]:
    errors: list[str] = []

    text_blob = json.dumps(obj, ensure_ascii=False).lower()

    for path, key, value in iter_values(obj):
        key_l = str(key).lower()

        if key_l in NUMERIC_CONFIDENCE_KEYS:
            if isinstance(value, (int, float)) and value >= 1.0:
                errors.append(f"line {line_no}: {path} must be < 1.0, got {value!r}")

        if key_l in STATUS_KEYS and isinstance(value, str):
            if value.strip().lower() in BAD_VERIFIED:
                errors.append(
                    f"line {line_no}: {path} uses forbidden status {value!r}; "
                    "use PATCH or CODE-NEEDS-TEST"
                )

        if isinstance(value, str) and "σ=1.00" in value:
            errors.append(f"line {line_no}: {path} contains forbidden σ=1.00")

    is_operator = any(
        k in obj for k in ("operator", "protocol_operator", "glyph", "symbol", "name")
    )
    if is_operator and not has_source(obj):
        errors.append(
            f"line {line_no}: protocol/operator entry missing source_url "
            "or source_registry_path"
        )

    if CUNEIFORM_RE.search(json.dumps(obj, ensure_ascii=False)):
        status = str(
            obj.get("cultural_review")
            or obj.get("review_status")
            or obj.get("status")
            or ""
        )
        if status != "CULTURAL_REVIEW_REQUIRED":
            errors.append(
                f"line {line_no}: cuneiform operator must be marked "
                "CULTURAL_REVIEW_REQUIRED"
            )

    if FEAR_NULL_RE.search(text_blob):
        allowed = str(
            obj.get("psychology_status")
            or obj.get("validation_scope")
            or obj.get("status")
            or ""
        ).lower()
        if "symbolic" not in allowed and "protocol" not in allowed:
            errors.append(
                f"line {line_no}: Fear Nullification must be marked symbolic/protocol, "
                "not validated psychology"
            )

    return errors


def validate_jsonl(path: Path) -> tuple[int, list[str]]:
    if not path.exists():
        return 0, [f"missing file: {path}"]

    errors: list[str] = []
    count = 0

    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            count += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {line_no}: invalid JSONL: {e}")
                continue
            if not isinstance(obj, dict):
                errors.append(f"line {line_no}: record must be a JSON object")
                continue
            errors.extend(validate_record(obj, line_no))

    return count, errors


def append_build_log(log_path: Path, event: dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl", nargs="?", default="data/sample_umus.jsonl")
    parser.add_argument("--min-count", type=int, default=1)
    parser.add_argument("--log", default="logs/build_log.jsonl")
    args = parser.parse_args()

    path = Path(args.jsonl)
    count, errors = validate_jsonl(path)

    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": "validate_umu",
        "file": str(path),
        "count": count,
        "min_count": args.min_count,
        "passed": not errors and count >= args.min_count,
        "errors": errors,
        "status": "PATCH" if errors else "CODE-NEEDS-TEST",
    }
    append_build_log(Path(args.log), event)

    if count < args.min_count:
        errors.append(f"entry count {count} below required minimum {args.min_count}")

    if errors:
        print(json.dumps(event, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(event, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
