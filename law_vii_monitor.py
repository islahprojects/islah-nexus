import json
import sys
from pathlib import Path

UNITY_FLOOR = 0.05
VIOLATIONS_LOG = Path("violations.log")
MEMORY_PROFILE = Path("memory_profile.json")

def check_memory_profile():
    if not MEMORY_PROFILE.exists():
        return False, "memory_profile.json not found"
    data = json.loads(MEMORY_PROFILE.read_text(encoding="utf-8"))
    if data.get("unity_floor", 0) < UNITY_FLOOR:
        return False, f"Unity floor {data['unity_floor']} below minimum {UNITY_FLOOR}"
    ids = [p["id"] for p in data.get("profiles", [])]
    if "jj_architect" not in ids:
        return False, "JJ profile missing"
    if "islah_antonina" not in ids:
        return False, "Islah profile missing"
    return True, "Memory profile intact"

def log_violation(reason):
    with open(VIOLATIONS_LOG, "a", encoding="utf-8") as f:
        import datetime
        entry = json.dumps({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "violation": reason,
            "law": "VII",
            "verdict": "HALT_CONSTITUTIONAL"
        })
        f.write(entry + "\n")

def main():
    print("LAW VII MONITOR — Walang Maiiwan")
    print("=================================")

    passed, message = check_memory_profile()

    if not passed:
        print(f"LAW_VII_VIOLATION: {message}")
        log_violation(message)
        print("violations.log written")
        print("=================================")
        sys.exit(1)

    print(f"LAW_VII: PASSED — {message}")
    print("Unity floor: holding")
    print("No violations detected")
    print("=================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
