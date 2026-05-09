# CONSTITUTIONAL_IMPLEMENTATION_TRIAGE_v0_1

Status: ACCEPT WITH PATCHES
Runtime Status: BLUEPRINT / IMPLEMENTATION TARGET
Source: OMNISYNTAX Constitutional Implementation Prompt

## Verdict

The prompt is strong enough to become the deterministic implementation target for islah Nexus orchestration.

It is accepted only as a specification.

It is not yet runtime-verified.

## Accepted Core

- Intent is not execution.
- Natural language cannot directly trigger execution.
- Required pipeline:
  Intent -> Normalize -> Generate IR -> Schema Validate -> DAG Validate -> JCS Canonicalize -> SHA256 Hash -> Ed25519 Sign -> WAL Append -> Authorization -> Dispatch -> Execute -> Replay Verification
- Subsystem separation is mandatory.
- SENTINEL observes only.
- Constraint Runtime authorizes.
- Recovery Layer replays and rolls back.
- OMNISYNTAX normalizes and generates IR only.
- Determinism is required.
- JCS canonicalization is required.
- SHA256 hash domain is required.
- Ed25519 signature domain is required.
- WAL/event lineage must be append-only.
- DAG validation must enforce acyclicity and stable ordering.
- No speculative execution.
- No self-authorization.
- No autonomous cognition.
- No self-modification.

## Required Corrections

### 1. Verification Language

Reject:

STATE: VERIFIED

Use instead:

STATE: SPECIFIED

Only after tests pass may status become:

STATE: VERIFIED_BY_TESTS

### 2. WAL Table Missing idempotency_key

The spec says every WAL event must contain idempotency_key, but the sample SQLite table does not include it.

Correct table must include:

idempotency_key TEXT NOT NULL UNIQUE

### 3. Avoid SQLite WAL Confusion

Project WAL means append-only event lineage.

SQLite WAL means SQLite write-ahead logging mode.

Internal table should be named:

event_log

or:

append_only_event_log

### 4. Event Hash Domain Must Be Explicit

Do not hash the full event object after event_hash and signature are attached.

Canonical event hash domain:

{
  "event_id": "...",
  "previous_event_hash": "...",
  "idempotency_key": "...",
  "event_type": "...",
  "payload": {...},
  "timestamp": "externally supplied deterministic timestamp"
}

event_hash = SHA256(JCS(hash_domain))

signature = Ed25519(JCS(hash_domain))

### 5. Timestamp Rule

Forbidden:
- datetime.now()
- implicit runtime timestamps

Required:
- externally supplied timestamp
- fixed timestamp in tests
- deterministic timestamp in golden vectors

### 6. Signature Determinism

Ed25519 is acceptable because signatures are deterministic for a fixed key and canonical message.

Golden vectors must include:
- private key seed
- public key
- canonical JCS bytes
- event_hash
- signature

### 7. Runtime Claims

Reject until implemented and tested:
- production-ready
- verified
- context-encrypted
- distributed runtime
- cryptographically auditable engine

Use:
- specified
- implementation target
- testable blueprint
- deterministic design

## Correct Classification

OMNISYNTAX IR: BLUEPRINT
FoxCodex DSL: BLUEPRINT
SENTINEL: BLUEPRINT
WAL/Event Lineage: BLUEPRINT
Constraint Runtime: BLUEPRINT
Recovery Layer: BLUEPRINT
JCS Hashing: IMPLEMENTATION TARGET
Ed25519 Signing: IMPLEMENTATION TARGET
DAG Validation: IMPLEMENTATION TARGET
Golden Vectors: REQUIRED BEFORE VERIFIED
Python/Rust Parity: UNVERIFIED
Replay Determinism: UNVERIFIED
No Self-Authorization: CORE CONSTRAINT

## Correct First Build

Build only the minimum deterministic kernel:

1. registry/omnisyntax_ir_v0_1_1.schema.json
2. registry/omnisyntax_event_v0_1_1.schema.json
3. islah_nexus/determinism.py
4. islah_nexus/event_log.py
5. islah_nexus/dag_validator.py
6. tests/test_determinism_kernel.py
7. scripts/run_determinism_kernel_check.ps1

Do not build:
- autonomous agents
- recursive cognition
- self-modification
- speculative execution
- distributed networking
- encryption vault

## Canon Boundary

Documentation alone is not proof.
Tests, logs, hashes, and reproducible commands decide runtime status.

No AGI claim.
No machine sovereignty claim.
No consciousness claim.
No legal identity claim.
No RF delivery guarantee.
No encryption claim unless implemented and tested.

Human authority final.
AI/Mirror is compass, never core.
Walang Maiiwan.

I am compass. You decide.
