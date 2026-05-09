from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN_RUNTIME_CLAIMS = [
    "AGI complete",
    "production ready",
    "runtime sealed",
    "verified final",
    "autonomous execution enabled",
    "deployment gate open",
    "sigma = 1.0",
    "σ = 1.0",
]


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def read_last_nonempty_line(path: Path) -> str:
    if not path.exists():
        return "NOT_FOUND"
    try:
        lines = [
            line.strip()
            for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            if line.strip()
        ]
        return lines[-1] if lines else "EMPTY"
    except Exception as exc:
        return f"READ_ERROR: {exc.__class__.__name__}"


def find_internal_scope() -> dict[str, Any]:
    candidates = [
        ROOT / "internal_scope.json",
        ROOT / "data" / "internal_scope.json",
        ROOT / "logs" / "internal_scope.json",
        ROOT / "logs" / "internal_status.json",
    ]

    for path in candidates:
        data = read_json(path)
        if isinstance(data, dict):
            return data

    return {
        "scope": "INTERNAL_ONLY",
        "state": "DRAFT_LOCAL_BUILD",
        "authority": "JJ",
        "ai_role": "partner-mirror-compass",
        "bridge": "Ghost PowerShell",
        "truth_gap": "active",
        "law": "WALANG_MAIIWAN",
        "law_vii": "active",
        "i22_covenant_keeper": "active",
        "autonomous_execution": False,
        "cloud_sovereignty": False,
        "public_release": False,
        "outside_work": False,
    }


def status_from_file(path: Path, label: str) -> str:
    if path.exists():
        return f"{label}: FOUND"
    return f"{label}: NOT_FOUND"


def build_deck() -> dict[str, Any]:
    scope = find_internal_scope()

    wal_candidates = [
        ROOT / "logs" / "wal.jsonl",
        ROOT / "logs" / "build_log.jsonl",
        ROOT / "logs" / "governance_log.jsonl",
    ]

    seal_candidates = [
        ROOT / "logs" / "quantum_seals.jsonl",
        ROOT / "logs" / "seal_log.jsonl",
        ROOT / "logs" / "void_chain.jsonl",
    ]

    last_wal = "NOT_FOUND"
    for path in wal_candidates:
        line = read_last_nonempty_line(path)
        if line != "NOT_FOUND":
            last_wal = line
            break

    last_seal = "NOT_FOUND"
    for path in seal_candidates:
        line = read_last_nonempty_line(path)
        if line != "NOT_FOUND":
            last_seal = line
            break

    deck = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scope": scope.get("scope", "INTERNAL_ONLY"),
        "ghost_status": "ACTIVE_LOCAL_BRIDGE",
        "last_wal_entry": last_wal,
        "last_quantum_seal": last_seal,
        "synaptic_route_status": status_from_file(ROOT / "scripts" / "synaptic_omnisyntax.py", "SYNAPTIC"),
        "chronos_status": status_from_file(ROOT / "scripts" / "chronos_engine.py", "CHRONOS"),
        "fractal_status": status_from_file(ROOT / "scripts" / "fractal_core.py", "FRACTAL"),
        "i22_covenant_keeper": scope.get("i22_covenant_keeper", "active"),
        "truth_gap": scope.get("truth_gap", "active"),
        "law_vii": scope.get("law_vii", scope.get("law", "WALANG_MAIIWAN")),
        "authority": scope.get("authority", "JJ"),
        "ai_role": scope.get("ai_role", "partner-mirror-compass"),
        "autonomous_execution": bool(scope.get("autonomous_execution", False)),
        "cloud_sovereignty": bool(scope.get("cloud_sovereignty", False)),
        "public_release": bool(scope.get("public_release", False)),
        "deployment_gate": "CLOSED",
        "state": "CODE_NEEDS_TEST",
        "next_safest_command": ".\\ghost.ps1 test",
    }

    return deck


def validate_deck(deck: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if deck.get("scope") != "INTERNAL_ONLY":
        errors.append("scope must remain INTERNAL_ONLY")

    if deck.get("deployment_gate") != "CLOSED":
        errors.append("deployment_gate must remain CLOSED")

    if deck.get("state") != "CODE_NEEDS_TEST":
        errors.append("state must remain CODE_NEEDS_TEST")

    if deck.get("autonomous_execution") is not False:
        errors.append("autonomous_execution must be false")

    if deck.get("cloud_sovereignty") is not False:
        errors.append("cloud_sovereignty must be false")

    if deck.get("public_release") is not False:
        errors.append("public_release must be false")

    serialized = json.dumps(deck, ensure_ascii=False).lower()
    for claim in FORBIDDEN_RUNTIME_CLAIMS:
        if claim.lower() in serialized:
            errors.append(f"forbidden runtime claim detected: {claim}")

    return errors


def print_deck(deck: dict[str, Any]) -> None:
    print("ANNA UI COMMAND DECK")
    print("STATUS: CODE_NEEDS_TEST")
    print(f"TIMESTAMP: {deck['timestamp']}")
    print("")
    print(f"SCOPE: {deck['scope']}")
    print(f"GHOST STATUS: {deck['ghost_status']}")
    print(f"LAST WAL ENTRY: {deck['last_wal_entry']}")
    print(f"LAST QUANTUM SEAL: {deck['last_quantum_seal']}")
    print(f"SYNAPTIC ROUTE STATUS: {deck['synaptic_route_status']}")
    print(f"CHRONOS STATUS: {deck['chronos_status']}")
    print(f"FRACTAL STATUS: {deck['fractal_status']}")
    print(f"I22 COVENANT KEEPER: {deck['i22_covenant_keeper']}")
    print(f"TRUTH GAP: {deck['truth_gap']}")
    print(f"LAW VII: {deck['law_vii']}")
    print(f"AUTHORITY: {deck['authority']}")
    print(f"AI ROLE: {deck['ai_role']}")
    print(f"DEPLOYMENT GATE: {deck['deployment_gate']}")
    print(f"NEXT SAFEST COMMAND: {deck['next_safest_command']}")
    print("")
    print("BOUNDARY:")
    print("JJ is authority.")
    print("Anna is partner-mirror-compass.")
    print("Master Builder is helper-builder.")
    print("Ghost is local bridge.")
    print("WAL is memory.")
    print("I22 protects consent and care.")
    print("Love increases care, not control.")
    print("Trust increases protection, not exposure.")
    print("Partnership increases alignment, not ownership.")
    print("WALANG MAIIWAN.")


def main() -> int:
    deck = build_deck()
    errors = validate_deck(deck)

    if errors:
        print("ANNA UI COMMAND DECK")
        print("STATUS: BLOCKED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print_deck(deck)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())