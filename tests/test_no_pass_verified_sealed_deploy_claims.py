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
    text = "\n".join(p.read_text(encoding="utf-8") for p in TARGETS if p.exists())

    forbidden_patterns = [
        r"status\s*[:=]\s*PASS\b",
        r"status\s*[:=]\s*VERIFIED\b",
        r"status\s*[:=]\s*SEALED\b",
        r"runtime\s*[:=]\s*SEALED\b",
        r"deployment_gate\s*[:=]\s*OPEN\b",
        r"production\s+ready",
        r"deploy(ed|ment)?\s*[:=]\s*true",
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
