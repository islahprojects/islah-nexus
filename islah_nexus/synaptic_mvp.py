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

ROUTES = {
    START | CORE: "ignite_core",
    STOP | CORE: "stop_core",
    START | SHIELD: "deploy_truth_core_shield",
    STATUS | CORE: "status_core",
    SEAL | CORE: "seal_core_state",
    SEAL | SHIELD: "seal_shield_state"
}

FORBIDDEN_EXCLUSION_TERMS = {
    "PREMIUM", "PAYWALL", "EXCLUDE", "EXCLUDES", "POOR", "RICH-ONLY", "ELITE-ONLY"
}

OVERCERTAINTY_TERMS = {
    "PERFECT", "INFALLIBLE", "OMNISCIENT", "GUARANTEED", "100%", "SIGMA=1"
}

def normalize(raw_command: str) -> int:
    cleaned = raw_command.upper()
    for ch in "!?,.:;()[]{}":
        cleaned = cleaned.replace(ch, " ")

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

def intelligence_validators(raw_command: str, route: str | None) -> list[dict]:
    words = set(raw_command.upper().replace("-", " ").split())

    law_vii_failed = bool(FORBIDDEN_EXCLUSION_TERMS & words)
    truth_gap_failed = bool(OVERCERTAINTY_TERMS & words)

    return [
        {
            "validator": "INTEL_TRUTH_GAP",
            "passed": not truth_gap_failed,
            "critical": truth_gap_failed,
            "signal": "cladding" if not truth_gap_failed else "void",
            "reason": "Truth Gap preserved." if not truth_gap_failed else "OVERCERTAINTY_BLOCKED"
        },
        {
            "validator": "INTEL_LAW_VII",
            "passed": not law_vii_failed,
            "critical": law_vii_failed,
            "signal": "cladding" if not law_vii_failed else "void",
            "reason": "Walang Maiiwan preserved." if not law_vii_failed else "ECONOMIC_EXCLUSION"
        },
        {
            "validator": "INTEL_AUTONOMY_GATE",
            "passed": True,
            "critical": False,
            "signal": "cladding",
            "reason": "MVP routes only; autonomous execution disabled."
        },
        {
            "validator": "INTEL_SIGNAL_GATE",
            "passed": route is not None,
            "critical": False,
            "signal": "cladding" if route else "void",
            "reason": "Route mapped." if route else "No mapped route."
        }
    ]

def route_command(raw_command: str) -> dict:
    intent_hash = normalize(raw_command)
    route = ROUTES.get(intent_hash)
    validators = intelligence_validators(raw_command, route)

    critical_fail = any(v["critical"] for v in validators)
    route_known = route is not None

    if critical_fail:
        verdict = "HALT_INTELLIGENCE_GATE"
        signal_state = "void"
    elif route_known:
        verdict = "DISPATCH_READY"
        signal_state = "cladding"
    else:
        verdict = "UNKNOWN_INTENT"
        signal_state = "void"

    result = {
        "module": "SYNAPTIC_OMNISYNTAX_MVP",
        "verifier_mode": "INTELLIGENCE_ONLY_MVP",
        "human_verifier_required": False,
        "human_authority_preserved": True,
        "autonomous_execution": False,
        "raw_command": raw_command,
        "intent_hash": intent_hash,
        "route": route,
        "verdict": verdict,
        "signal_state": signal_state,
        "validators": validators,
        "truth_gap": "Parsing is approximate; dispatch is deterministic after normalization.",
        "law": "WALANG_MAIIWAN"
    }

    append_wal("synaptic_omnisyntax_mvp_route", result)
    return result

def main():
    parser = argparse.ArgumentParser(prog="synaptic_mvp")
    parser.add_argument("command", nargs="+")
    args = parser.parse_args()

    raw_command = " ".join(args.command)
    result = route_command(raw_command)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()