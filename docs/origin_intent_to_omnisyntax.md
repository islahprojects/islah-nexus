# Origin Intent to OMNISYNTAX
## Islah Constitutional Framework | JAJIS 2026
## Classification: SPECIFICATION — Not runtime-evaluated

---

## Why OMNISYNTAX Exists

OMNISYNTAX exists because natural language cannot directly trigger execution.

The gap between intent and action is not a limitation to be overcome.
It is a safety boundary to be preserved.

The intent of OMNISYNTAX is to formalize that boundary:
every request must pass through normalization, schema validation,
DAG validation, canonicalization, hashing, signing, and authorization
before any execution is permitted.

This is not bureaucracy. This is the engineering expression of
human authority over machine action.

---

## Constitutional Origin

The origin of OMNISYNTAX traces to three constitutional requirements:

**Law II — Truth:** Outputs must declare their signal state.
No synthetic confidence. No blending of conflicting signals.
OMNISYNTAX enforces this by requiring explicit signal_state
on every IR payload before it can be routed.

**Law III — Authority:** AI is compass, never core.
OMNISYNTAX enforces this by separating intent generation
from authorization. OMNISYNTAX normalizes and generates IR only.
It does not authorize. It does not execute.

**Law VI — Sovereignty:** User data and consent are inviolable.
OMNISYNTAX enforces this by requiring idempotency keys,
anonymized session references, and append-only event lineage.
No silent overwrites. No speculative state changes.

---

## What OMNISYNTAX Is Not

OMNISYNTAX is not an autonomous agent.
OMNISYNTAX is not a reasoning engine.
OMNISYNTAX is not a deployment mechanism.
OMNISYNTAX does not self-authorize.
OMNISYNTAX does not self-modify.
OMNISYNTAX does not handle private keys.
OMNISYNTAX does not upload to Arweave or pin to IPFS.

Any implementation that adds these capabilities
without explicit human authorization is a boundary violation.

---

## Required Pipeline

Intent must travel this path before execution:

```
Intent
  → Normalize (OMNISYNTAX)
  → Generate IR (OMNISYNTAX)
  → Schema Validate
  → DAG Validate
  → JCS Canonicalize
  → SHA256 Hash
  → Ed25519 Sign
  → WAL Append
  → Authorization (Constraint Runtime)
  → Dispatch
  → Execute
  → Replay Verification
```

Skipping any step is a protocol violation.
Shortcuts under time pressure are not permitted.
The pipeline is deterministic or it is not the pipeline.

---

## Determinism Requirements

Every step must produce identical output for identical input.

Forbidden in OMNISYNTAX context:
- `datetime.now()` — use externally supplied timestamps only
- Implicit runtime state — all state must be explicit in payload
- Speculative execution — no action before authorization
- Non-deterministic ordering — DAG must enforce stable ordering

---

## Local-First Principle (L6)

OMNISYNTAX operates locally first.
No network dependency for core IR generation.
No cloud dependency for schema validation.
No external service for canonicalization or hashing.

Local-first is not a performance optimization.
It is a sovereignty protection.
A system that requires external authorization for every operation
is a system that can be denied to underserved communities.
Walang Maiiwan.

---

## Current Implementation State

This document describes intent and specification.
Implementation state is tracked in the refinement report.
No runtime claims are made here.
No deployment has occurred.
Human review is required before any merge or deployment.

Human authority final.
AI is compass, never core.
Walang Maiiwan.
