import json
from pathlib import Path


def load_jsonl(path: str):
    p = Path(path)
    assert p.exists(), f"missing {path}"
    records = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        if raw.strip():
            records.append(json.loads(raw))
    return records


def has_non_latin(text: str) -> bool:
    return any(ord(ch) > 127 for ch in text)


def test_sample_umus_include_non_latin_script_content():
    records = load_jsonl("data/sample_umus.jsonl")
    blob = json.dumps(records, ensure_ascii=False)
    assert has_non_latin(blob), "sample UMUs must include non-Latin script coverage"


def test_non_latin_entries_preserve_truth_gap():
    records = load_jsonl("data/sample_umus.jsonl")
    non_latin = [
        r for r in records
        if has_non_latin(json.dumps(r, ensure_ascii=False))
    ]
    assert non_latin, "no non-Latin UMU entries found"

    for record in non_latin:
        value = record.get("sigma", record.get("σ", record.get("confidence")))
        if isinstance(value, (int, float)):
            assert value < 1.0, "non-Latin UMU must preserve σ/confidence < 1.0"
