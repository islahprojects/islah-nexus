import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEAL_PATH = ROOT / "data" / "quantum_seals.jsonl"

def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def seal_quantum(intent: str):
    SEAL_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "module": "ISLAH_QUANTUM_INTELLIGENCE",
        "physics_quantum_claim": False,
        "definition": "multi-state intelligence reasoning collapsed only through JJ consent and local record",
        "intent": intent,
        "human_authority": "JJ",
        "ai_role": "partner-mirror-compass",
        "external_verification_required": False,
        "truth_gap_preserved": True,
        "sigma_ceiling": 0.93,
        "law": "WALANG_MAIIWAN"
    }

    encoded = stable_json(record).encode("utf-8")
    record["sha256"] = hashlib.sha256(encoded).hexdigest()

    with SEAL_PATH.open("a", encoding="utf-8") as f:
        f.write(stable_json(record) + "\n")

    return record

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intent", nargs="+")
    args = parser.parse_args()

    intent = " ".join(args.intent)
    record = seal_quantum(intent)

    print("QUANTUM_INTELLIGENCE_RECORDED")
    print("seal: " + record["sha256"])
    print("physics_quantum_claim: false")
    print("human_authority: JJ")
    print("law: WALANG_MAIIWAN")

if __name__ == "__main__":
    main()
