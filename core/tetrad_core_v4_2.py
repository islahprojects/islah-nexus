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
