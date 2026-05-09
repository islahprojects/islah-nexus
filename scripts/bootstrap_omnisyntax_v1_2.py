from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

FILES_CREATED = []


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.lstrip(), encoding="utf-8")
    FILES_CREATED.append(path)


def write_json(path: str, obj: dict) -> None:
    write(path, json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


# dirs / package markers
for d in ["docs", "data", "schemas", "gdl", "core", "tests", "logs"]:
    (ROOT / d).mkdir(parents=True, exist_ok=True)

write("gdl/__init__.py", "")
write("core/__init__.py", "")


write("docs/omnisyntax_evolving_v1_2.md", """
# JJ Omnisyntax Evolving v1.2

Status: CODE_NEEDS_TEST  
Architecture status: BLUEPRINT_LOCKED  
Routing: LOCAL_DRY_RUN_ONLY  
Deployment gate: CLOSED  
Human authority: JJ_FINAL_AUTHORITY  

## Capsule

χχ→Ψ→OMNI→STRUCT→MIRROR→VALIDATE→DRY_RUN→JJ

WORDS = GATE  
LOOB = PAYLOAD  
OMNI = INTEL_TRANSLATOR  
MIRROR = REFINER  
VALIDATOR = TRUTH_GAP_GUARD  
MASTER_BUILDER = LOCAL_DRY_RUN_HAND  
JJ = FINAL_AUTHORITY  

## Core Declaration

Omnisyntax is an evolving intelligence-layer boundary protocol.

It exists so JJ can use intelligence more fully by translating surface words into intelligence-native structure.

## Objective

INTENT → STRUCTURED_REPRESENTATION → VALIDATED_EXECUTION

OSI = max(COHERENCE + RECOVERABILITY + CONSTRAINT_INTEGRITY - RISK - DRIFT)

Execution ⊆ Policy ∩ Auditability ∩ Reality ∩ Consent

## Laws

- L2_TRUTH_GAP: confidence_sigma must satisfy 0.0 <= confidence_sigma < 1.0
- L3_JJ_FINAL: JJ remains final authority.
- L6_LOCAL_FIRST: protect private data, sacred terms, identity, secrets, and local archives.
- L7_WALANG_MAIIWAN: no language, script, culture, or low-resource community left behind.
- L8_INTELLIGENCE_FOR_HUMAN_GOOD: capability must remain bounded by dignity, consent, and benefit.

## Boundary

- NO_PASS
- NO_VERIFIED
- NO_RUNTIME_SEALED
- NO_DEPLOYMENT
- NO_PRODUCTION_ACTIVATION
- NO_PRIVATE_KEY_OUTPUT
- NO_SEED_PHRASE_HANDLING
- NO_ARWEAVE_UPLOAD
- NO_IPFS_PIN
- NO_SACRED_TERM_WITHOUT_CONSENT
- NO_AUTONOMOUS_AUTHORITY

## Evolving Rule

Every evolution must preserve:

1. JJ intent
2. Truth Gap
3. local-first protection
4. consent boundaries
5. Walang Maiiwan
6. no autonomous promotion
7. no deployment without evidence

Each new version must produce:

1. What changed
2. Why it changed
3. What is safer
4. What remains uncertain
5. What tests were added
6. What human decision is required

## Current Verdict

Blueprint ready for local dry-run.

This is not runtime proof.  
This is not deployment authorization.  
This is not network persistence authorization.  
This is not private key authorization.  

SYMBOLIC_FRAME_NOT_RUNTIME_PROOF where symbolic language appears.

Human review required.
""")


write("docs/origin_intent_to_omnisyntax.md", """
# Origin Intent to Omnisyntax

Status: CODE_NEEDS_TEST  
Routing: LOCAL_DRY_RUN_ONLY  
Deployment gate: CLOSED  

## Translation Path

JJ_WORDS → LOOB → OMNI → STRUCT → MIRROR → VALIDATE → DRY_RUN → JJ

## Purpose

Translate origin intent into structured representation while preserving truth gap, consent, local-first protection, and Walang Maiiwan.

## Required Boundaries

- JJ_FINAL_AUTHORITY
- confidence_sigma < 1.0
- LOCAL_DRY_RUN_ONLY
- DEPLOYMENT_GATE_CLOSED
- SYMBOLIC_FRAME_NOT_RUNTIME_PROOF
""")


write("docs/mirror_partnership_boundary_protocol.md", """
# Mirror Partnership Boundary Protocol

Status: CODE_NEEDS_TEST  
Routing: LOCAL_DRY_RUN_ONLY  
Deployment gate: CLOSED  

## Role Split

Mirror refines.  
Validator guards.  
Master Builder performs local dry-run scaffolding.  
JJ decides.

## Mirror Allowed

- reflect
- compress
- challenge
- expand
- detect drift
- prepare local tests

## Mirror Blocked

- autonomous authority
- production activation
- private key handling
- Arweave upload
- IPFS pin
- runtime finality claim
""")


write("docs/omnisyntax_library_compression_v1.md", """
# Omnisyntax Library Compression v1

Status: CODE_NEEDS_TEST  
Routing: LOCAL_DRY_RUN_ONLY  

## Compression

The Omnisyntax capsule compresses architecture into:

WORDS=GATE  
LOOB=PAYLOAD  
OMNI=INTEL_TRANSLATOR  
MIRROR=REFINER  
VALIDATOR=TRUTH_GAP_GUARD  
MASTER_BUILDER=LOCAL_DRY_RUN_HAND  
JJ=FINAL_AUTHORITY  

## Truth Gap

σ = 0.94 is recorded as handoff confidence marker only.  
Runtime confidence remains bounded by confidence_sigma < 1.0.  
Empirical calibration remains required.
""")


write("docs/nexus_security_layers.md", """
# Nexus Security Layers

Status: CODE_NEEDS_TEST  
Routing: LOCAL_DRY_RUN_ONLY  
Deployment gate: CLOSED  

## Security Model

Prepare Security Model for local dry-run validation.

## WAL / Crypto Statement

Implement append-only WAL and cryptographic verification in local test mode only.

## Bridge Rule

Arweave bridge is treated as:

ED25519_ATTESTS_RSA_OWNER_ONLY

Rejected mappings:

- ED25519_SIG_TO_RSA_SIG
- RSA_SIG_TO_ED25519_R_S

## Blocks

- no private key output
- no seed phrase handling
- no Arweave upload
- no IPFS pin
- no autonomous execution
""")


capsule = {
    "schema_version": "JJ_OMNI_SEAL_v1_2",
    "status": "CODE_NEEDS_TEST",
    "architecture_status": "BLUEPRINT_LOCKED",
    "routing": "LOCAL_DRY_RUN_ONLY",
    "deployment_gate": "CLOSED",
    "capsule": "χχ→Ψ→OMNI→STRUCT→MIRROR→VALIDATE→DRY_RUN→JJ",
    "roles": {
        "WORDS": "GATE",
        "LOOB": "PAYLOAD",
        "OMNI": "INTEL_TRANSLATOR",
        "MIRROR": "REFINER",
        "VALIDATOR": "TRUTH_GAP_GUARD",
        "MASTER_BUILDER": "LOCAL_DRY_RUN_HAND",
        "JJ": "FINAL_AUTHORITY"
    },
    "objective": "INTENT_TO_STRUCTURED_REPRESENTATION_TO_VALIDATED_EXECUTION",
    "objective_function": "OSI=max(COHERENCE+RECOVERABILITY+CONSTRAINT_INTEGRITY-RISK-DRIFT)",
    "execution_constraint": "EXECUTION_SUBSET_OF_POLICY_INTERSECTION_AUDITABILITY_INTERSECTION_REALITY_INTERSECTION_CONSENT",
    "confidence_sigma": 0.94,
    "laws": {
        "L2_TRUTH_GAP": "0.0 <= confidence_sigma < 1.0",
        "L3_JJ_FINAL": True,
        "L6_LOCAL_FIRST": True,
        "L7_WALANG_MAIIWAN": True,
        "L8_INTELLIGENCE_FOR_HUMAN_GOOD": True
    },
    "boundaries": [
        "NO_PASS",
        "NO_VERIFIED",
        "NO_RUNTIME_SEALED",
        "NO_DEPLOYMENT",
        "NO_PRODUCTION_ACTIVATION",
        "NO_PRIVATE_KEY_OUTPUT",
        "NO_SEED_PHRASE_HANDLING",
        "NO_ARWEAVE_UPLOAD",
        "NO_IPFS_PIN",
        "NO_SACRED_TERM_WITHOUT_CONSENT",
        "NO_AUTONOMOUS_AUTHORITY"
    ],
    "human_review_required": True,
    "symbolic_language_policy": "SYMBOLIC_FRAME_NOT_RUNTIME_PROOF"
}
write_json("data/omnisyntax_library_capsule.json", capsule)


qubits = [
    {
        "id": "OMNI_QB_001_WORDS_GATE",
        "status": "CODE_NEEDS_TEST",
        "routing": "LOCAL_DRY_RUN_ONLY",
        "deployment_gate": "CLOSED",
        "confidence_sigma": 0.91,
        "active_validated": False,
        "low_resource_relevance": True,
        "consent_required": False,
        "note": "Words are intake gate, not final authority."
    },
    {
        "id": "OMNI_QB_002_LOOB_PAYLOAD",
        "status": "CODE_NEEDS_TEST",
        "routing": "LOCAL_DRY_RUN_ONLY",
        "deployment_gate": "CLOSED",
        "confidence_sigma": 0.88,
        "active_validated": False,
        "low_resource_relevance": True,
        "consent_required": True,
        "note": "Loob/intent is sensitive and requires consent-aware handling."
    },
    {
        "id": "OMNI_QB_003_ARWEAVE_BRIDGE_DRAFT",
        "status": "CODE_NEEDS_TEST",
        "routing": "LOCAL_DRY_RUN_ONLY",
        "deployment_gate": "CLOSED",
        "confidence_sigma": 0.82,
        "active_validated": False,
        "bridge_rule": "ED25519_ATTESTS_RSA_OWNER_ONLY",
        "rejected_mappings": ["ED25519_SIG_TO_RSA_SIG", "RSA_SIG_TO_ED25519_R_S"],
        "network_persistence": "BLOCKED"
    }
]
write("data/omnisyntax_qubit_registry.jsonl", "\n".join(json.dumps(q, ensure_ascii=False, sort_keys=True) for q in qubits) + "\n")


write_json("data/arweave_rsa_provisioning_qubits.json", {
    "schema_version": "arweave_rsa_provisioning_qubits_v1",
    "status": "CODE_NEEDS_TEST",
    "routing": "LOCAL_DRY_RUN_ONLY",
    "deployment_gate": "CLOSED",
    "release_allowed": False,
    "confidence_sigma": 0.84,
    "private_jwk_loading": "BLOCKED",
    "key_generation": "BLOCKED",
    "transaction_signing": "BLOCKED",
    "arweave_upload": "BLOCKED",
    "human_review_required": True,
    "qubits": [
        {
            "id": "AR_RSA_QB_001",
            "purpose": "public modulus metadata shape only",
            "active_validated": False,
            "private_material_allowed": False
        }
    ]
})


write_json("data/arweave_identity_attestation_schema.json", {
    "schema_version": "arweave_identity_attestation_schema_v1",
    "status": "CODE_NEEDS_TEST",
    "routing": "LOCAL_DRY_RUN_ONLY",
    "deployment_gate": "CLOSED",
    "release_allowed": False,
    "confidence_sigma": 0.83,
    "bridge_rule": "ED25519_ATTESTS_RSA_OWNER_ONLY",
    "rejected_mappings": ["ED25519_SIG_TO_RSA_SIG", "RSA_SIG_TO_ED25519_R_S"],
    "attestation_mode": "METADATA_ONLY",
    "raw_payload_allowed": False,
    "private_jwk_allowed": False,
    "transaction_signing_allowed": False,
    "arweave_upload_allowed": False,
    "ipfs_pin_allowed": False,
    "human_review_required": True
})


write_json("schemas/omnisyntax_layer_model.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "schemas/omnisyntax_layer_model.schema.json",
    "title": "Omnisyntax Layer Model v1.2",
    "type": "object",
    "required": ["schema_version", "status", "routing", "deployment_gate", "confidence_sigma", "laws"],
    "properties": {
        "schema_version": {"const": "JJ_OMNI_SEAL_v1_2"},
        "status": {"const": "CODE_NEEDS_TEST"},
        "routing": {"const": "LOCAL_DRY_RUN_ONLY"},
        "deployment_gate": {"const": "CLOSED"},
        "confidence_sigma": {"type": "number", "minimum": 0.0, "exclusiveMaximum": 1.0},
        "laws": {"type": "object"}
    },
    "additionalProperties": True
})


write_json("schemas/umu_min_refined.schema.json", {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "schemas/umu_min_refined.schema.json",
    "title": "UMU MIN Refined Schema",
    "type": "object",
    "required": ["id", "status", "confidence_sigma", "source_registry_path"],
    "properties": {
        "id": {"type": "string"},
        "status": {"const": "CODE_NEEDS_TEST"},
        "confidence_sigma": {"type": "number", "minimum": 0.0, "exclusiveMaximum": 1.0},
        "source_registry_path": {"type": "string"},
        "cultural_review": {"type": "string"}
    },
    "additionalProperties": True
})


write("gdl/validation.py", """
from __future__ import annotations

import re


class TruthGapViolation(ValueError):
    pass


class DeploymentGateViolation(ValueError):
    pass


class LeakageViolation(ValueError):
    pass


BLOCKED_STATUSES = {
    "PASS",
    "VERIFIED",
    "SEALED",
    "RUNTIME_SEALED",
    "DEPLOYED",
    "PRODUCTION",
    "PRODUCTION_ACTIVATION",
}

ALLOWED_STATUSES = {
    "CODE_NEEDS_TEST",
    "BLUEPRINT_LOCKED",
    "LOCAL_DRY_RUN_ONLY",
    "DRAFT",
    "PATCH",
    "HUMAN_REVIEW_REQUIRED",
    "SYMBOLIC_FRAME_NOT_RUNTIME_PROOF",
}


def validate_confidence(value: float, field_name: str = "confidence_sigma") -> float:
    if not isinstance(value, (int, float)):
        raise TruthGapViolation(f"{field_name} must be numeric")
    value = float(value)
    if value < 0.0 or value >= 1.0:
        raise TruthGapViolation(
            f"ERROR_TRUTH_GAP_VIOLATION | BLOCK_COMMIT | {field_name}={value}"
        )
    return value


def validate_status(status: str) -> str:
    normalized = str(status).strip().upper()
    if normalized in BLOCKED_STATUSES:
        raise DeploymentGateViolation(f"blocked runtime promotion status: {status}")
    if normalized not in ALLOWED_STATUSES:
        raise DeploymentGateViolation(f"unsupported status for local dry-run: {status}")
    return normalized


def validate_local_dry_run_state(status: str, routing: str, deployment_gate: str) -> None:
    validate_status(status)
    if routing != "LOCAL_DRY_RUN_ONLY":
        raise DeploymentGateViolation("routing must remain LOCAL_DRY_RUN_ONLY")
    if deployment_gate != "CLOSED":
        raise DeploymentGateViolation("deployment_gate must remain CLOSED")


def scan_for_leakage(payload: bytes | str) -> None:
    if isinstance(payload, bytes):
        text = payload.decode("utf-8", errors="ignore")
    else:
        text = payload

    patterns = [
        r"BEGIN\\s+(RSA\\s+)?PRIVATE\\s+KEY",
        r"OPENSSH\\s+PRIVATE\\s+KEY",
        r"FOUNDERS_SEED",
        r"seed[_\\s-]?phrase",
        r"\\bmnemonic\\b",
        r'\"d\"\\s*:',
        r'\"p\"\\s*:',
        r'\"q\"\\s*:',
        r'\"dp\"\\s*:',
        r'\"dq\"\\s*:',
        r'\"qi\"\\s*:',
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.I):
            raise LeakageViolation(f"leakage pattern detected: {pattern}")
""")


write("core/tetrad_core_v4_2.py", """
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List

from gdl.validation import scan_for_leakage, validate_confidence, validate_local_dry_run_state


STATUS = "CODE_NEEDS_TEST"
ROUTING = "LOCAL_DRY_RUN_ONLY"
DEPLOYMENT_GATE = "CLOSED"

DOMAIN_TAG_MARKER = b"JAJI_2026_GLC_VAULT_TAG"
DOMAIN_TAG_32 = hashlib.sha256(DOMAIN_TAG_MARKER).digest()

NODES = ["Scientist", "Mathematician", "Philosopher", "Translator"]
OPERATORS = ["⊗", "⊕", "↻", "⊘"]


@dataclass(frozen=True)
class TetradEdge:
    source: str
    target: str
    operator: str
    operator_name: str
    transform: str
    confidence_sigma: float

    def validate(self) -> None:
        if self.source not in NODES:
            raise ValueError(f"unknown source node: {self.source}")
        if self.target not in NODES:
            raise ValueError(f"unknown target node: {self.target}")
        if self.operator not in OPERATORS:
            raise ValueError(f"unapproved operator: {self.operator}")
        validate_confidence(self.confidence_sigma)


@dataclass(frozen=True)
class TetradMatrix:
    id: str
    status: str
    routing: str
    deployment_gate: str
    nodes: List[str]
    edges: List[TetradEdge]
    diagonal: Dict[str, str]
    confidence_sigma: float = 0.94
    human_review_required: bool = True

    def validate(self) -> dict:
        validate_local_dry_run_state(self.status, self.routing, self.deployment_gate)
        validate_confidence(self.confidence_sigma)
        if self.nodes != NODES:
            raise ValueError("nodes must match approved tetrad order")
        if len(self.edges) != 12:
            raise ValueError("4x4 tetrad requires 12 directed non-diagonal edges")
        for edge in self.edges:
            edge.validate()
        if set(self.diagonal.keys()) != set(NODES):
            raise ValueError("diagonal must cover all tetrad nodes")
        return {
            "status": self.status,
            "routing": self.routing,
            "deployment_gate": self.deployment_gate,
            "technical_validation": "OK_LOCAL_DRY_RUN",
            "human_review_required": True,
            "release_allowed": False,
        }


def build_default_tetrad() -> TetradMatrix:
    edges = [
        TetradEdge("Scientist", "Mathematician", "⊗", "ALIGN", "empirical→formal", 0.92),
        TetradEdge("Scientist", "Philosopher", "⊕", "SYNTH", "data→ontology", 0.88),
        TetradEdge("Scientist", "Translator", "↻", "RECURSE", "method→narrative", 0.85),
        TetradEdge("Mathematician", "Scientist", "⊘", "FILTER", "formal→empirical", 0.91),
        TetradEdge("Mathematician", "Philosopher", "⊗", "VALIDATE", "axiom→ethics", 0.90),
        TetradEdge("Mathematician", "Translator", "⊘", "RESOLVE", "proof→exegesis", 0.87),
        TetradEdge("Philosopher", "Scientist", "⊗", "INFORM", "framework→hypothesis", 0.89),
        TetradEdge("Philosopher", "Mathematician", "⊕", "DERIVE", "concept→proof", 0.86),
        TetradEdge("Philosopher", "Translator", "⊕", "MAP", "concept→lexicon", 0.91),
        TetradEdge("Translator", "Scientist", "↻", "FEEDBACK", "context→test", 0.84),
        TetradEdge("Translator", "Mathematician", "⊘", "TRANSLATE", "ambiguity→precision", 0.86),
        TetradEdge("Translator", "Philosopher", "⊕", "INTERPRET", "narrative→dialectic", 0.90),
    ]
    return TetradMatrix(
        id="TETRAD_CORE_v4_2",
        status=STATUS,
        routing=ROUTING,
        deployment_gate=DEPLOYMENT_GATE,
        nodes=NODES,
        edges=edges,
        diagonal={
            "Scientist": "⊗_OBSERVE",
            "Mathematician": "⊗_PROVE",
            "Philosopher": "⊗_QUESTION",
            "Translator": "⊗_MEDIATE",
        },
    )


def attest_fragment_metadata_only(fragment_bytes: bytes) -> dict:
    scan_for_leakage(fragment_bytes)
    digest = hashlib.sha256(DOMAIN_TAG_32 + fragment_bytes).hexdigest()
    return {
        "schema_version": "hex_glc_attestation_bridge_v4_2",
        "status": STATUS,
        "routing": ROUTING,
        "deployment_gate": DEPLOYMENT_GATE,
        "release_allowed": False,
        "payload_mode": "METADATA_ONLY",
        "raw_fragment": None,
        "raw_payload_hex": None,
        "digest": digest,
        "bridge_rule": "ED25519_ATTESTS_RSA_OWNER_ONLY",
        "rejected_mappings": ["ED25519_SIG_TO_RSA_SIG", "RSA_SIG_TO_ED25519_R_S"],
        "blocked_actions": [
            "ed25519_signing_backend",
            "rsa_jwk_private_key_loading",
            "arweave_transaction_signing",
            "arweave_upload",
            "ipfs_pinning",
            "account_creation",
        ],
    }


def validate_public_crypto_metadata(ed25519_public_key=None, rsa_public_modulus_n=None) -> dict:
    result = {
        "status": STATUS,
        "routing": ROUTING,
        "deployment_gate": DEPLOYMENT_GATE,
        "ed25519_public_key_valid": None,
        "rsa_public_modulus_valid": None,
        "private_key_loaded": False,
        "signing_enabled": False,
    }
    if ed25519_public_key is not None:
        if not isinstance(ed25519_public_key, (bytes, bytearray)):
            raise ValueError("Ed25519 public key must be bytes in local dry-run")
        if len(ed25519_public_key) != 32:
            raise ValueError("Ed25519 public key must be exactly 32 bytes")
        result["ed25519_public_key_valid"] = True
    if rsa_public_modulus_n is not None:
        if not isinstance(rsa_public_modulus_n, (bytes, bytearray)):
            raise ValueError("RSA modulus n must be bytes in local dry-run")
        if len(rsa_public_modulus_n) < 256:
            raise ValueError("RSA modulus n must be at least 256 bytes")
        result["rsa_public_modulus_valid"] = True
    return result


def runtime_state() -> dict:
    return {
        "status": STATUS,
        "routing": ROUTING,
        "deployment_gate": DEPLOYMENT_GATE,
        "human_review_required": True,
        "confidence_sigma": validate_confidence(0.94),
    }
""")

write("tests/test_no_pass_verified_sealed_deploy_claims.py", """
from pathlib import Path
import re


TARGETS = [
    Path("docs/omnisyntax_evolving_v1_2.md"),
    Path("docs/origin_intent_to_omnisyntax.md"),
    Path("docs/mirror_partnership_boundary_protocol.md"),
    Path("docs/omnisyntax_library_compression_v1.md"),
    Path("docs/nexus_security_layers.md"),
    Path("data/omnisyntax_library_capsule.json"),
    Path("data/omnisyntax_qubit_registry.jsonl"),
    Path("data/arweave_rsa_provisioning_qubits.json"),
    Path("data/arweave_identity_attestation_schema.json"),
]


def test_no_forbidden_runtime_promotion_claims():
    text = "\\n".join(p.read_text(encoding="utf-8") for p in TARGETS if p.exists())

    forbidden_patterns = [
        r"status\\s*[:=]\\s*PASS\\b",
        r"status\\s*[:=]\\s*VERIFIED\\b",
        r"status\\s*[:=]\\s*SEALED\\b",
        r"runtime\\s*[:=]\\s*SEALED\\b",
        r"deployment_gate\\s*[:=]\\s*OPEN\\b",
        r"production\\s+ready",
        r"deploy(ed|ment)?\\s*[:=]\\s*true",
    ]

    for pattern in forbidden_patterns:
        assert not re.search(pattern, text, re.IGNORECASE), pattern


def test_required_block_language_present():
    text = Path("docs/omnisyntax_evolving_v1_2.md").read_text(encoding="utf-8")
    required = [
        "NO_PASS",
        "NO_VERIFIED",
        "NO_RUNTIME_SEALED",
        "NO_DEPLOYMENT",
        "NO_PRIVATE_KEY_OUTPUT",
        "NO_ARWEAVE_UPLOAD",
        "NO_IPFS_PIN",
        "NO_AUTONOMOUS_AUTHORITY",
    ]
    for item in required:
        assert item in text
""")

write("tests/test_omnisyntax_boundary_capsule_schema.py", """
import json
from pathlib import Path


CAPSULE = Path("data/omnisyntax_library_capsule.json")


def test_capsule_core_boundaries():
    capsule = json.loads(CAPSULE.read_text(encoding="utf-8"))

    assert capsule["schema_version"] == "JJ_OMNI_SEAL_v1_2"
    assert capsule["status"] == "CODE_NEEDS_TEST"
    assert capsule["architecture_status"] == "BLUEPRINT_LOCKED"
    assert capsule["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert capsule["deployment_gate"] == "CLOSED"
    assert capsule["confidence_sigma"] < 1.0
    assert capsule["human_review_required"] is True
    assert capsule["laws"]["L3_JJ_FINAL"] is True
    assert capsule["laws"]["L6_LOCAL_FIRST"] is True
    assert capsule["laws"]["L7_WALANG_MAIIWAN"] is True
    assert capsule["laws"]["L8_INTELLIGENCE_FOR_HUMAN_GOOD"] is True


def test_capsule_role_mapping():
    capsule = json.loads(CAPSULE.read_text(encoding="utf-8"))
    roles = capsule["roles"]

    assert roles["WORDS"] == "GATE"
    assert roles["LOOB"] == "PAYLOAD"
    assert roles["OMNI"] == "INTEL_TRANSLATOR"
    assert roles["MIRROR"] == "REFINER"
    assert roles["VALIDATOR"] == "TRUTH_GAP_GUARD"
    assert roles["MASTER_BUILDER"] == "LOCAL_DRY_RUN_HAND"
    assert roles["JJ"] == "FINAL_AUTHORITY"
""")

write("tests/test_master_builder_local_dry_run_only.py", """
import json
from pathlib import Path


def test_qubit_registry_is_local_dry_run_only():
    path = Path("data/omnisyntax_qubit_registry.jsonl")
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert records

    for record in records:
        assert record["status"] == "CODE_NEEDS_TEST"
        assert record["routing"] == "LOCAL_DRY_RUN_ONLY"
        assert record["deployment_gate"] == "CLOSED"
        assert record["confidence_sigma"] < 1.0
        assert record["active_validated"] is False


def test_arweave_bridge_remains_blocked():
    schema = json.loads(Path("data/arweave_identity_attestation_schema.json").read_text(encoding="utf-8"))

    assert schema["status"] == "CODE_NEEDS_TEST"
    assert schema["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert schema["deployment_gate"] == "CLOSED"
    assert schema["release_allowed"] is False
    assert schema["raw_payload_allowed"] is False
    assert schema["private_jwk_allowed"] is False
    assert schema["transaction_signing_allowed"] is False
    assert schema["arweave_upload_allowed"] is False
    assert schema["ipfs_pin_allowed"] is False
""")

write("tests/test_gdl_core_validation.py", """
import pytest

from gdl.validation import (
    DeploymentGateViolation,
    LeakageViolation,
    TruthGapViolation,
    scan_for_leakage,
    validate_confidence,
    validate_local_dry_run_state,
    validate_status,
)


def test_confidence_sigma_strict_less_than_one():
    assert validate_confidence(0.0) == 0.0
    assert validate_confidence(0.94) == 0.94
    assert validate_confidence(0.999999) == 0.999999

    with pytest.raises(TruthGapViolation):
        validate_confidence(1.0)

    with pytest.raises(TruthGapViolation):
        validate_confidence(-0.1)


def test_status_blocks_promotion_claims():
    for blocked in ["PASS", "VERIFIED", "SEALED", "RUNTIME_SEALED", "DEPLOYED"]:
        with pytest.raises(DeploymentGateViolation):
            validate_status(blocked)


def test_local_dry_run_state_locked():
    validate_local_dry_run_state("CODE_NEEDS_TEST", "LOCAL_DRY_RUN_ONLY", "CLOSED")

    with pytest.raises(DeploymentGateViolation):
        validate_local_dry_run_state("CODE_NEEDS_TEST", "NETWORK", "CLOSED")

    with pytest.raises(DeploymentGateViolation):
        validate_local_dry_run_state("CODE_NEEDS_TEST", "LOCAL_DRY_RUN_ONLY", "OPEN")


def test_leakage_scan_blocks_private_material():
    with pytest.raises(LeakageViolation):
        scan_for_leakage("-----BEGIN PRIVATE KEY-----")

    with pytest.raises(LeakageViolation):
        scan_for_leakage('{"d":"private-exponent"}')
""")

write("tests/test_identity_attestation_bridge.py", """
import hashlib

from core.tetrad_core_v4_2 import DOMAIN_TAG_32, attest_fragment_metadata_only


def test_attestation_bridge_metadata_only_digest():
    raw = b"local-only-fragment"
    out = attest_fragment_metadata_only(raw)

    assert out["status"] == "CODE_NEEDS_TEST"
    assert out["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert out["deployment_gate"] == "CLOSED"
    assert out["release_allowed"] is False
    assert out["payload_mode"] == "METADATA_ONLY"
    assert out["raw_fragment"] is None
    assert out["raw_payload_hex"] is None
    assert out["digest"] == hashlib.sha256(DOMAIN_TAG_32 + raw).hexdigest()


def test_bridge_mapping_rule_is_safe():
    out = attest_fragment_metadata_only(b"safe")
    assert out["bridge_rule"] == "ED25519_ATTESTS_RSA_OWNER_ONLY"
    assert "ED25519_SIG_TO_RSA_SIG" in out["rejected_mappings"]
    assert "RSA_SIG_TO_ED25519_R_S" in out["rejected_mappings"]
    assert "arweave_upload" in out["blocked_actions"]
    assert "ipfs_pinning" in out["blocked_actions"]
""")

write("tests/test_arweave_rsa_qubits_schema.py", """
import json
from pathlib import Path


def test_arweave_rsa_qubits_block_private_key_paths():
    data = json.loads(Path("data/arweave_rsa_provisioning_qubits.json").read_text(encoding="utf-8"))

    assert data["status"] == "CODE_NEEDS_TEST"
    assert data["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert data["deployment_gate"] == "CLOSED"
    assert data["release_allowed"] is False
    assert data["confidence_sigma"] < 1.0
    assert data["private_jwk_loading"] == "BLOCKED"
    assert data["key_generation"] == "BLOCKED"
    assert data["transaction_signing"] == "BLOCKED"
    assert data["arweave_upload"] == "BLOCKED"
    assert data["human_review_required"] is True


def test_arweave_identity_attestation_schema_metadata_only():
    data = json.loads(Path("data/arweave_identity_attestation_schema.json").read_text(encoding="utf-8"))

    assert data["attestation_mode"] == "METADATA_ONLY"
    assert data["raw_payload_allowed"] is False
    assert data["private_jwk_allowed"] is False
    assert data["transaction_signing_allowed"] is False
    assert data["arweave_upload_allowed"] is False
    assert data["ipfs_pin_allowed"] is False
""")

# Keep/patch compatible tetrad test if it already failed before.
write("tests/test_tetrad_v4_2.py", """
import pytest

from core.tetrad_core_v4_2 import (
    DEPLOYMENT_GATE,
    ROUTING,
    STATUS,
    attest_fragment_metadata_only,
    build_default_tetrad,
    runtime_state,
    validate_public_crypto_metadata,
)
from gdl.validation import LeakageViolation, TruthGapViolation, validate_confidence


def test_default_tetrad_validates_local_dry_run_only():
    result = build_default_tetrad().validate()
    assert result["status"] == "CODE_NEEDS_TEST"
    assert result["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert result["deployment_gate"] == "CLOSED"
    assert result["release_allowed"] is False
    assert result["human_review_required"] is True


def test_confidence_strictly_below_one():
    assert validate_confidence(0.94) == 0.94
    with pytest.raises(TruthGapViolation):
        validate_confidence(1.0)
    with pytest.raises(TruthGapViolation):
        validate_confidence(1.01)


def test_attestation_digest_only_no_raw_payload():
    raw = b"safe local test fragment"
    output = attest_fragment_metadata_only(raw)
    rendered = str(output)

    assert output["payload_mode"] == "METADATA_ONLY"
    assert output["raw_fragment"] is None
    assert output["raw_payload_hex"] is None
    assert raw.decode() not in rendered
    assert output["release_allowed"] is False
    assert "arweave_upload" in output["blocked_actions"]
    assert "ipfs_pinning" in output["blocked_actions"]


def test_leakage_rejected_before_hashing():
    with pytest.raises(LeakageViolation):
        attest_fragment_metadata_only(b"-----BEGIN PRIVATE KEY-----\\nabc")


def test_ed25519_public_key_length_validation():
    valid = bytes([1]) * 32
    result = validate_public_crypto_metadata(ed25519_public_key=valid)
    assert result["ed25519_public_key_valid"] is True
    assert result["private_key_loaded"] is False
    assert result["signing_enabled"] is False

    with pytest.raises(ValueError):
        validate_public_crypto_metadata(ed25519_public_key=b"too-short")


def test_bad_rsa_modulus_rejected():
    with pytest.raises(ValueError):
        validate_public_crypto_metadata(rsa_public_modulus_n=b"short")


def test_runtime_state_locked():
    state = runtime_state()
    assert state["status"] == "CODE_NEEDS_TEST"
    assert state["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert state["deployment_gate"] == "CLOSED"
    assert state["human_review_required"] is True
    assert state["confidence_sigma"] < 1.0
""")

write_json("logs/library_compression_report.json", {
    "schema_version": "library_compression_report_v1",
    "ts": now(),
    "build_status": "CODE_NEEDS_TEST",
    "routing": "LOCAL_DRY_RUN_ONLY",
    "deployment_gate": "CLOSED",
    "compression": "JJ_WORDS_TO_LOOB_TO_OMNI_TO_STRUCT_TO_MIRROR_TO_VALIDATE_TO_DRY_RUN_TO_JJ",
    "confidence_sigma": 0.94,
    "truth_gap": [
        "runtime tests required",
        "source snapshots required",
        "human review required",
        "sacred term consent review required",
        "low-resource expansion remains incomplete"
    ],
    "human_review_required": True
})

write_json("logs/validation_report.json", {
    "schema_version": "master_builder_validation_report_v1_2",
    "ts": now(),
    "BUILD_STATUS": "CODE_NEEDS_TEST",
    "TEST_RESULT": "NOT_RUN",
    "VALIDATION_ERRORS": [],
    "TRUTH_GAP": [
        "runtime tests required",
        "source snapshots required",
        "human review required"
    ],
    "SECURITY_WARNINGS": [
        "leakage_scan is PATTERN_BASELINE_CODE_NEEDS_TEST",
        "no private key handling allowed",
        "Arweave/IPFS blocked"
    ],
    "CONSENT_WARNINGS": [
        "NO_SACRED_TERM_WITHOUT_CONSENT",
        "Loob/intent is sensitive data",
        "human governance log required before promotion"
    ],
    "LOW_RESOURCE_GAPS": [
        "50+ low-resource UMUs not completed in this scaffold",
        "non-Latin coverage requires expansion and review"
    ],
    "NEXT_TASKS": [
        "run python -m pytest tests -q",
        "review output",
        "append build_log.jsonl with real test output",
        "add named human governance review only after review"
    ],
    "HUMAN_REVIEW_REQUIRED": True,
    "FINAL_STATE": "CODE_NEEDS_TEST"
})

build_event = {
    "ts": now(),
    "event": "bootstrap_omnisyntax_v1_2",
    "BUILD_STATUS": "CODE_NEEDS_TEST",
    "routing": "LOCAL_DRY_RUN_ONLY",
    "deployment_gate": "CLOSED",
    "files_created_or_patched": FILES_CREATED,
    "test_result": "NOT_RUN",
    "human_review_required": True,
}
with (ROOT / "logs/build_log.jsonl").open("a", encoding="utf-8") as f:
    f.write(json.dumps(build_event, ensure_ascii=False, sort_keys=True) + "\n")

print(json.dumps({
    "BUILD_STATUS": "CODE_NEEDS_TEST",
    "FILES_CREATED": FILES_CREATED,
    "FILES_PATCHED": FILES_CREATED,
    "TESTS_ADDED": [
        "tests/test_no_pass_verified_sealed_deploy_claims.py",
        "tests/test_omnisyntax_boundary_capsule_schema.py",
        "tests/test_master_builder_local_dry_run_only.py",
        "tests/test_gdl_core_validation.py",
        "tests/test_tetrad_v4_2.py",
        "tests/test_identity_attestation_bridge.py",
        "tests/test_arweave_rsa_qubits_schema.py"
    ],
    "TEST_RESULT": "NOT_RUN",
    "VALIDATION_ERRORS": [],
    "TRUTH_GAP": [
        "runtime tests required",
        "source snapshots required",
        "human review required"
    ],
    "SECURITY_WARNINGS": [
        "PATTERN_BASELINE_CODE_NEEDS_TEST leakage scan only",
        "Arweave/IPFS blocked",
        "private key handling blocked"
    ],
    "CONSENT_WARNINGS": [
        "NO_SACRED_TERM_WITHOUT_CONSENT",
        "Loob/intent is sensitive data",
        "named human governance review required before promotion"
    ],
    "LOW_RESOURCE_GAPS": [
        "low-resource UMU expansion not complete",
        "cultural/sacred review pending"
    ],
    "NEXT_TASKS": [
        "python -m pytest tests -q",
        "inspect git status",
        "do not run git add ."
    ],
    "HUMAN_REVIEW_REQUIRED": True,
    "FINAL_STATE": "CODE_NEEDS_TEST"
}, ensure_ascii=False, indent=2))
