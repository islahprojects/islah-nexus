import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAL_PATH = ROOT / "data" / "wal.jsonl"

def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def append_wal(action, payload):
    WAL_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": "JJ+Partner",
        "action": action,
        "payload": payload,
        "human_authority": "JJ",
        "walang_maiiwan": True
    }

    encoded = stable_json(record).encode("utf-8")
    record["sha256"] = hashlib.sha256(encoded).hexdigest()

    with WAL_PATH.open("a", encoding="utf-8") as f:
        f.write(stable_json(record) + "\n")

    return record
