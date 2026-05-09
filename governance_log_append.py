import json
import sys
import datetime
from pathlib import Path

GOVERNANCE_LOG = Path("governance_log.json")

def append_entry(actor_hash, action, law, verdict, note=""):
    if not GOVERNANCE_LOG.exists():
        print("ERROR: governance_log.json not found.")
        sys.exit(1)
    raw = GOVERNANCE_LOG.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    entry = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "actor_hash": actor_hash,
        "action": action,
        "law": law,
        "verdict": verdict,
        "note": note
    }
    data["entries"].append(entry)
    GOVERNANCE_LOG.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"GOVERNANCE_LOG: entry appended")
    print(f"  actor: {actor_hash}")
    print(f"  action: {action}")
    print(f"  law: {law} | verdict: {verdict}")

if __name__ == "__main__":
    append_entry(
        actor_hash="sha256:jj_architect",
        action="GOVERNANCE_LOG_APPEND_PATCHED",
        law="II",
        verdict="PASS",
        note="Fixed utcnow deprecation. Now using datetime.UTC."
    )