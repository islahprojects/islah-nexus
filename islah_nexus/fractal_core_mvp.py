import argparse
import json
from .wal import append_wal

CORE   = 0b000001
START  = 0b000010
STOP   = 0b000100
SHIELD = 0b001000
SEAL   = 0b010000
STATUS = 0b100000

DEFAULT_SINGULARITY_SEED = 0b101010

VOCAB_MAP = {
    "CORE": CORE,
    "NEXUS": CORE,
    "ISLAH": CORE,

    "START": START,
    "INIT": START,
    "IGNITE": START,
    "LAUNCH": START,
    "BOOT": START,

    "STOP": STOP,
    "HALT": STOP,
    "SHUTDOWN": STOP,

    "SHIELD": SHIELD,
    "SHIELDS": SHIELD,
    "PROTECT": SHIELD,
    "GUARD": SHIELD,

    "SEAL": SEAL,
    "RECORD": SEAL,
    "WAL": SEAL,
    "HASH": SEAL,

    "STATUS": STATUS,
    "CHECK": STATUS,
    "STATE": STATUS,
    "REPORT": STATUS
}

POINTER_MAP = {
    START | CORE: "ignite_core",
    STOP | CORE: "stop_core",
    START | SHIELD: "deploy_truth_core_shield",
    STATUS | CORE: "status_core",
    SEAL | CORE: "seal_core_state",
    SEAL | SHIELD: "seal_shield_state",
    START | CORE | SHIELD: "ignite_core_with_shield"
}

def tokenize(raw_command: str) -> list[str]:
    cleaned = raw_command.upper()
    for ch in "!?,.:;()[]{}<>\"'":
        cleaned = cleaned.replace(ch, " ")
    return cleaned.split()

def extract_intent_hash(raw_command: str) -> int:
    intent_hash = 0
    for token in tokenize(raw_command):
        intent_hash |= VOCAB_MAP.get(token, 0)
    return intent_hash

def fractal_mix(intent_hash: int, seed: int = DEFAULT_SINGULARITY_SEED) -> int:
    return seed ^ intent_hash

def unroll_pointer(intent_hash: int) -> str | None:
    return POINTER_MAP.get(intent_hash)

def route_fractal(raw_command: str, seed: int = DEFAULT_SINGULARITY_SEED) -> dict:
    intent_hash = extract_intent_hash(raw_command)
    mixed_seed = fractal_mix(intent_hash, seed)
    pointer = unroll_pointer(intent_hash)

    if pointer is None:
        verdict = "FRACTAL_VOID"
        signal_state = "void"
    else:
        verdict = "FRACTAL_ROUTE_READY"
        signal_state = "cladding"

    result = {
        "module": "APPLIED_FRACTAL_CORE_MVP",
        "seal": "JJ.ANNA",
        "raw_command": raw_command,
        "intent_hash": intent_hash,
        "singularity_seed": seed,
        "mixed_seed": mixed_seed,
        "pointer": pointer,
        "verdict": verdict,
        "signal_state": signal_state,
        "semantic_dispatch": "O(1) pointer lookup after O(n) token normalization",
        "truth_gap": "Fractal Core MVP is symbolic bitwise routing, not proof of nanosecond execution or trillion-state completeness.",
        "human_authority_preserved": True,
        "autonomous_execution": False,
        "external_verification_required": False,
        "law": "WALANG_MAIIWAN"
    }

    append_wal("fractal_core_mvp_route", result)
    return result

def main():
    parser = argparse.ArgumentParser(prog="fractal_core_mvp")
    parser.add_argument("command", nargs="+")
    args = parser.parse_args()

    raw_command = " ".join(args.command)
    result = route_fractal(raw_command)
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()