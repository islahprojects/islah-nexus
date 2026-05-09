import argparse
import json
from datetime import datetime, timezone

from .wal import append_wal

PAST_HOUSE = {
    "SHANNON": {
        "era": "1948_1957",
        "meaning": "information, channel, noise, bits",
        "route": "past_information_theory"
    },
    "ARPANET": {
        "era": "1969",
        "meaning": "packet network origin",
        "route": "past_networking"
    },
    "DEEP": {
        "era": "2012_plus",
        "meaning": "deep learning acceleration",
        "route": "past_ai_acceleration"
    }
}

PRESENT_HOUSE = {
    "GHOST": {
        "state": "active",
        "meaning": "Ghost PowerShell local bridge",
        "route": "present_ghost_bridge"
    },
    "WAL": {
        "state": "active",
        "meaning": "append-only local trace",
        "route": "present_wal_trace"
    },
    "TESTS": {
        "state": "94_passed_plus",
        "meaning": "local test green milestone",
        "route": "present_test_state"
    }
}

FUTURE_HOUSE = {
    "2056": {
        "type": "symbolic_trajectory",
        "meaning": "long-range Islah/Chronos direction, not prediction",
        "route": "future_symbolic_trajectory"
    },
    "DEPLOY": {
        "type": "roadmap",
        "meaning": "make local-first deployable components",
        "route": "future_deployment_path"
    },
    "LEARN": {
        "type": "roadmap",
        "meaning": "continue quantum, language, routing, and Omnisyntax learning",
        "route": "future_learning_path"
    }
}

HOUSES = {
    "PAST": PAST_HOUSE,
    "PRESENT": PRESENT_HOUSE,
    "FUTURE": FUTURE_HOUSE
}

def normalize(raw_command: str) -> set[str]:
    cleaned = raw_command.upper()
    for ch in "!?,.:;()[]{}":
        cleaned = cleaned.replace(ch, " ")
    return set(cleaned.split())

def scan_house(words: set[str], house_name: str, house: dict) -> list[dict]:
    hits = []
    for key, payload in house.items():
        if key in words:
            item = {
                "house": house_name,
                "key": key,
                "route": payload["route"],
                "meaning": payload["meaning"],
                "signal_state": "cladding"
            }
            if "era" in payload:
                item["era"] = payload["era"]
            if "state" in payload:
                item["state"] = payload["state"]
            if "type" in payload:
                item["type"] = payload["type"]
            hits.append(item)
    return hits

def chronos_route(raw_command: str) -> dict:
    words = normalize(raw_command)

    hits = []
    for house_name, house in HOUSES.items():
        hits.extend(scan_house(words, house_name, house))

    if hits:
        verdict = "CHRONOS_ROUTE_READY"
        signal_state = "cladding"
    else:
        verdict = "CHRONOS_VOID"
        signal_state = "void"

    result = {
        "module": "CHRONOS_ENGINE_MVP",
        "seal": "JJ.ANNA",
        "verifier_mode": "INTELLIGENCE_ONLY_MVP",
        "human_verifier_required": False,
        "human_authority_preserved": True,
        "autonomous_execution": False,
        "raw_command": raw_command,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "signal_state": signal_state,
        "houses_scanned": ["PAST", "PRESENT", "FUTURE"],
        "hits": hits,
        "truth_gap": "Chronos MVP is symbolic temporal routing, not future certainty or physical time control.",
        "law": "WALANG_MAIIWAN"
    }

    append_wal("chronos_engine_mvp_route", result)
    return result

def main():
    parser = argparse.ArgumentParser(prog="chronos_mvp")
    parser.add_argument("command", nargs="+")
    args = parser.parse_args()

    raw_command = " ".join(args.command)
    result = chronos_route(raw_command)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()