import argparse
import json
from pathlib import Path

from .wal import append_wal

CORE   = 0b000001
START  = 0b000010
STOP   = 0b000100
SHIELD = 0b001000
SEAL   = 0b010000
STATUS = 0b100000

EXPERTS = {
    START | CORE: {
        "route": "ignite_core",
        "risk": "medium",
        "requires_human_confirm": True
    },
    STOP | CORE: {
        "route": "stop_core",
        "risk": "medium",
        "requires_human_confirm": True
    },
    START | SHIELD: {
        "route": "deploy_truth_core_shield",
        "risk": "low",
        "requires_human_confirm": False
    },
    STATUS | CORE: {
        "route": "status_core",
        "risk": "low",
        "requires_human_confirm": False
    },
    SEAL | CORE: {
        "route": "seal_core_state",
        "risk": "medium",
        "requires_human_confirm": True
    },
    SEAL | SHIELD: {
        "route": "seal_shield_state",
        "risk": "low",
        "requires_human_confirm": False
    }
}

def normalize(raw_command: str) -> int:
    cleaned = (
        raw_command
        .upper()
        .replace("!", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("?", " ")
        .replace(":", " ")
        .replace(";", " ")
    )
    words = set(cleaned.split())
    intent_hash = 0

    if {"START", "INIT", "IGNITE", "LAUNCH", "BOOT", "OPEN"} & words:
        intent_hash |= START

    if {"STOP", "HALT", "SHUTDOWN", "CLOSE", "KILL"} & words:
        intent_hash |= STOP

    if {"CORE", "NEXUS", "ISLAH"} & words:
        intent_hash |= CORE

    if {"SHIELD", "PROTECT", "GUARD", "DEFEND"} & words:
        intent_hash |= SHIELD

    if {"SEAL", "RECORD", "WAL", "HASH"} & words:
        intent_hash |= SEAL

    if {"STATUS", "CHECK", "STATE", "REPORT"} & words:
        intent_hash |= STATUS

    return intent_hash

def law_gate(route_obj, intent_hash: int, raw_command: str) -> dict:
    if route_obj is None:
        return {
            "verdict": "UNKNOWN_INTENT",
            "raw_command": raw_command,
            "intent_hash": intent_hash,
            "signal_state": "void",
            "route": None,
            "risk": "unknown",
            "requires_human_confirm": True,
            "truth_gap": "No mapped expert for this exact semantic bitfield.",
            "human_authority_preserved": True,
            "external_verification_required": False,
            "autonomous_execution": False,
            "law": "WALANG_MAIIWAN"
        }

    return {
        "verdict": "DISPATCH_READY",
        "raw_command": raw_command,
        "intent_hash": intent_hash,
        "signal_state": "cladding",
        "route": route_obj["route"],
        "risk": route_obj["risk"],
        "requires_human_confirm": route_obj["requires_human_confirm"],
        "truth_gap": "Intent parsing is approximate; route is deterministic after normalization.",
        "human_authority_preserved": True,
        "external_verification_required": False,
        "autonomous_execution": False,
        "law": "WALANG_MAIIWAN"
    }

def route_command(raw_command: str) -> dict:
    intent_hash = normalize(raw_command)
    route_obj = EXPERTS.get(intent_hash)
    result = law_gate(route_obj, intent_hash, raw_command)
    append_wal("synaptic_route", result)
    return result

def main():
    parser = argparse.ArgumentParser(prog="synaptic_router")
    parser.add_argument("command", nargs="+")
    args = parser.parse_args()

    raw_command = " ".join(args.command)
    result = route_command(raw_command)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
