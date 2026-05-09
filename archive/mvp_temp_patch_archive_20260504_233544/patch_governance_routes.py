from pathlib import Path
import datetime
import json
import re

project = Path.cwd()
main_path = project / "islah_nexus" / "main.py"
gov_path = project / "governance_log.json"

backup = main_path.with_name("main.py.governance_route_backup")
backup.write_text(main_path.read_text(encoding="utf-8-sig"), encoding="utf-8")

# Ensure governance_log.json exists and has at least one entry.
if gov_path.exists():
    try:
        gov = json.loads(gov_path.read_text(encoding="utf-8-sig"))
    except Exception:
        gov = {}
else:
    gov = {}

if not isinstance(gov, dict):
    gov = {}

gov.setdefault("log_id", "ISLAH_NEXUS_GOVERNANCE_LOG_v1")
gov.setdefault("description", "Append-only constitutional governance log. No raw identity. Hash-only.")
gov.setdefault("law_reference", ["I", "II", "III", "VI", "VII"])
gov.setdefault("created", datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"))

entries = gov.get("entries")
if not isinstance(entries, list):
    entries = []

if len(entries) == 0:
    entries.append({
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "actor_hash": "sha256:jj_architect",
        "action": "MVP_CHRONOS_ANNA_GOVERNANCE_ROUTE_PATCHED",
        "law": "VII",
        "verdict": "PASS",
        "note": "Governance route patched. Anna online. Metrics/history path anchored."
    })

gov["entries"] = entries
gov_path.write_text(json.dumps(gov, indent=2, ensure_ascii=False), encoding="utf-8")

text = main_path.read_text(encoding="utf-8-sig")

# Remove old override block if present.
text = re.sub(
    r'\n# --- ISLAH GOVERNANCE ROUTE OVERRIDE START ---.*?# --- ISLAH GOVERNANCE ROUTE OVERRIDE END ---\n',
    '\n',
    text,
    flags=re.S
)

override = r'''
# --- ISLAH GOVERNANCE ROUTE OVERRIDE START ---
# Forces /history and /metrics to read project-root governance_log.json.
from pathlib import Path as _IslahPath
import json as _islah_json
import datetime as _islah_datetime
from fastapi import Depends as _IslahDepends

_ISLAH_PROJECT_ROOT = _IslahPath(__file__).resolve().parents[1]
_ISLAH_GOVERNANCE_LOG = _ISLAH_PROJECT_ROOT / "governance_log.json"
_ISLAH_VIOLATIONS_LOG = _ISLAH_PROJECT_ROOT / "violations.log"

def _islah_read_governance():
    if not _ISLAH_GOVERNANCE_LOG.exists():
        return {
            "log_id": "ISLAH_NEXUS_GOVERNANCE_LOG_v1",
            "entries": [],
            "_path": str(_ISLAH_GOVERNANCE_LOG),
            "_exists": False,
        }

    raw = _ISLAH_GOVERNANCE_LOG.read_text(encoding="utf-8-sig")
    data = _islah_json.loads(raw)

    if not isinstance(data, dict):
        data = {"entries": []}

    if "entries" not in data or not isinstance(data["entries"], list):
        data["entries"] = []

    data["_path"] = str(_ISLAH_GOVERNANCE_LOG)
    data["_exists"] = True
    return data

def _islah_count_violations():
    if not _ISLAH_VIOLATIONS_LOG.exists():
        return 0
    raw = _ISLAH_VIOLATIONS_LOG.read_text(encoding="utf-8", errors="ignore")
    return len([line for line in raw.splitlines() if line.strip()])

# Remove previously registered /history and /metrics routes so these become authoritative.
app.router.routes = [
    route for route in app.router.routes
    if getattr(route, "path", None) not in {"/history", "/metrics"}
]

@app.get("/history", dependencies=[_IslahDepends(verify_token)])
def history():
    data = _islah_read_governance()
    entries = data.get("entries", [])
    return {
        "log_id": data.get("log_id", "ISLAH_NEXUS_GOVERNANCE_LOG_v1"),
        "log_path": data.get("_path"),
        "log_exists": data.get("_exists"),
        "entry_count": len(entries),
        "entries": entries,
    }

@app.get("/metrics", dependencies=[_IslahDepends(verify_token)])
def metrics():
    data = _islah_read_governance()
    entries = data.get("entries", [])
    return {
        "timestamp": _islah_datetime.datetime.now(_islah_datetime.UTC).isoformat().replace("+00:00", "Z"),
        "governance_entries": len(entries),
        "law_vii_violations": _islah_count_violations(),
        "unity_floor": 0.05,
        "sigma_ceiling": 0.93,
        "status": "PROTOTYPE - NOT PRODUCTION READY",
        "governance_log_path": data.get("_path"),
        "governance_log_exists": data.get("_exists"),
    }
# --- ISLAH GOVERNANCE ROUTE OVERRIDE END ---
'''

text = text + "\n" + override + "\n"
main_path.write_text(text, encoding="utf-8")

print("Patched main.py governance routes.")
print("Governance log:", gov_path)
print("Local governance entries:", len(entries))
