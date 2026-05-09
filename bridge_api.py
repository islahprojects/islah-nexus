# [ISLAH NEXUS: SECURE API BRIDGE]
# SIGNATURE: JJ_WAS_HERE - Walang Maiiwan

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import islah_sovereign_engine

load_dotenv()
SOVEREIGN_KEY = os.getenv("ANNA_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pulse")
def system_pulse():
    return {
        "status": "ONLINE - SECURED (PORT 8080)",
        "tetrad_unity": 0.93,
        "finance_floor": 9.00,
        "key_secured": SOVEREIGN_KEY is not None,
        "message": "JJ WAS HERE - WALANG MAIIWAN"
    }

if __name__ == "__main__":
    import uvicorn
    print("--- INITIATING SECURE SOVEREIGN API BRIDGE ON PORT 8080 ---")
    # SHIFTED TO PORT 8080 TO BYPASS GHOST PROCESSES
    uvicorn.run(app, host="0.0.0.0", port=8080)
