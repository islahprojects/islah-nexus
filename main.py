from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Any, Dict
from engine import SovereignCommunityNervousSystem, ICF_CONSTANTS

app = FastAPI(title="Islah Nexus", version="4.0.0-GOD-TIER")

nervous_system = SovereignCommunityNervousSystem({
    "provenance_origin": "10.5281/zenodo.18989894"
})

@app.get("/", response_model=None)
def read_root() -> FileResponse | Dict[str, Any]:
    try:
        result = nervous_system.run({"action": "ping", "architect": "Krimerra13"})
        return {"status": "ONLINE", "gate_check": result, "message": "Walang Maiiwan."}
    except Exception as e:
        return {"status": "CONSTITUTIONAL_HALT", "error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "ok", "constants": ICF_CONSTANTS()}
