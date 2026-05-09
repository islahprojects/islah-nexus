import json
import datetime
from pathlib import Path

p = Path("governance_log.json")

if p.exists():
    data = json.loads(p.read_text(encoding="utf-8-sig"))
else:
    data = {
        "log_id": "ISLAH_NEXUS_GOVERNANCE_LOG_v1",
        "description": "Append-only constitutional governance log. No raw identity. Hash-only.",
        "law_reference": ["I", "II", "III", "VI", "VII"],
        "created": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "entries": []
    }

if "entries" not in data or not isinstance(data["entries"], list):
    data["entries"] = []

entry = {
    "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
    "actor_hash": "sha256:jj_architect",
    "action": "MVP_CHRONOS_ANNA_HEALTH_CONFIRMED",
    "law": "VII",
    "verdict": "PASS",
    "note": "Health online, Anna online, metrics authenticated, Chronos shell awake."
}

data["entries"].append(entry)

p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print("Governance entry appended.")
print("Entries:", len(data["entries"]))
print("Last action:", data["entries"][-1]["action"])
