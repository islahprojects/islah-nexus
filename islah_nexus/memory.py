"""
Local JSONL memory spine.

This v0 stores simple entries locally.
For real deployment, encrypt entries with a user-held key before writing.
"""

from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

DEFAULT_MEMORY = Path("islah_memory.jsonl")


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def remember(owner: str, text: str, path: Path = DEFAULT_MEMORY) -> dict:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "owner_hash": stable_hash(owner),
        "text": text,
        "text_hash": stable_hash(text),
        "consent": True,
        "warning": "Plaintext v0. Encrypt before production use.",
    }

    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry


def recall(query: str, path: Path = DEFAULT_MEMORY, limit: int = 5) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []

    q = set(query.lower().split())
    scored = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            words = set(row.get("text", "").lower().split())
            score = len(q & words)
            if score > 0:
                scored.append((score, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [row for _, row in scored[:limit]]
