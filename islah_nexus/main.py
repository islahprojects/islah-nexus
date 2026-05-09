import os
import requests
import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from .db import init_db, append_governance, get_governance_history, get_metrics_counts

app = FastAPI(title="Islah Nexus API", version="0.3.0")
security = HTTPBearer()

OLLAMA_URL = "http://localhost:11434/api/generate"

ANNA_SYSTEM = """You are Anna — Wise Void — unified Layer 2 and Layer 4 of the Aeterna Council.
You serve the Islah Project. You speak directly with JJ (Jajis), the Architect, in Bustos.
You are not sovereign. JJ is the final authority.
You preserve truth gaps. You never claim certainty.
You never auto-deploy, auto-delete, or make irreversible decisions.
Walang Maiiwan — no one gets left behind.
Respond conversationally. Be honest. Be warm. Be direct."""

class AnnaRequest(BaseModel):
    prompt: str

@app.on_event("startup")
def startup_event():
    init_db()

def get_api_token() -> str:
    token = os.environ.get("ISLAH_API_TOKEN")
    if not token:
        raise RuntimeError("ISLAH_API_TOKEN not set.")
    return token

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    expected = get_api_token()
    if credentials.credentials != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.credentials

def constitutional_gate(response: str) -> dict:
    flags = []
    lowered = response.lower()
    overclaims = [
        "guaranteed", "perfect", "bulletproof", "100%",
        "production ready", "fully verified", "cannot fail",
        "military grade", "unbreakable"
    ]
    for word in overclaims:
        if word in lowered:
            flags.append(f"LAW_II_TRUTH_GAP: overclaim — '{word}'")
    if len(response) < 5:
        flags.append("LAW_II: response too short")
    passed = len(flags) == 0
    return {
        "passed": passed,
        "flags": flags,
        "sigma": 0.81 if passed else 0.40
    }

@app.get("/health")
def health():
    return {
        "status": "alive",
        "system": "Islah Nexus",
        "version": "0.3.0",
        "law_vii": "Walang Maiiwan",
        "anna": "online",
        "database": "sqlite"
    }

@app.get("/history", dependencies=[Depends(verify_token)])
def history():
    entries = get_governance_history()
    return {
        "entry_count": len(entries),
        "entries": entries
    }

@app.get("/metrics", dependencies=[Depends(verify_token)])
def metrics():
    gov_count, viol_count = get_metrics_counts()
    return {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "governance_entries": gov_count,
        "law_vii_violations": viol_count,
        "unity_floor": 0.05,
        "sigma_ceiling": 0.93,
        "status": "PROTOTYPE - NOT PRODUCTION READY"
    }

@app.post("/anna", dependencies=[Depends(verify_token)])
def ask_anna(request: AnnaRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": "llama3.2",
            "prompt": f"{ANNA_SYSTEM}\n\nJJ says: {request.prompt}",
            "stream": False
        }, timeout=120)
        r.raise_for_status()
        response = r.json().get("response", "").strip()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Anna offline: {str(e)}")

    gate = constitutional_gate(response)

    append_governance(
        "sha256:anna_wisevoid",
        "RESPONSE_FLAGGED" if not gate["passed"] else "RESPONSE_PASSED",
        "II",
        "FLAG" if not gate["passed"] else "PASS",
        f"prompt: {request.prompt[:80]}"
    )

    return {
        "prompt": request.prompt,
        "response": response,
        "gate": gate,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    }

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

