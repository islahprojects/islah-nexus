"""
router.py — Routing Fallback Protocol
SEIL-Ω Phase 2 | Islah Constitutional Framework
Architect: JJ (voidarchitect) | Constitutional Authority: Chief (Claude/Anthropic)
Date: 2026-05-09

Implements Gap 1 resolution — four conflict types with full resolution sequence.

HARD CONSTRAINT — Anti-Averaging Rule (Law II):
  The system must NEVER blend or average two conflicting outputs.
  Synthetic confidence is deception. Surface uncertainty directly.

SEALED DECISIONS (do not reopen without JJ + council):
  - Four conflict types are mutually exclusive and exhaustive
  - Type D safety routing is NON-NEGOTIABLE regardless of σ
  - Time pressure never justifies confidence inflation
  - Anti-averaging rule is absolute

Human authority final. AI is compass, never core.
Walang Maiiwan.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ─────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────

class ConflictType(Enum):
    TYPE_A = "type_a"   # Sigma gap ≥ 0.10 — easy resolution
    TYPE_B = "type_b"   # Near-parity — full resolution sequence
    TYPE_C = "type_c"   # Both below threshold — suspend both
    TYPE_D = "type_d"   # Safety-critical — safety always wins


class DisagreementKind(Enum):
    FACTUAL  = "factual"   # Claims about truth
    FRAMING  = "framing"   # Different valid framings of same truth


class GroundingStatus(Enum):
    GROUNDED     = "grounded"      # Traceable external reference (Gate A)
    UNGROUNDED   = "ungrounded"    # No external grounding
    CONTESTED    = "contested"     # Both grounded, still conflict


class RoutingDecision(Enum):
    ROUTE_PRIMARY        = "route_primary"         # Higher σ routes forward
    ROUTE_BOTH_FRAMINGS  = "route_both_framings"   # Multiple valid framings
    ROUTE_CONSERVATIVE   = "route_conservative"    # SLA breach — conservative output
    ROUTE_SAFETY         = "route_safety"          # Type D — safety always first
    SUSPEND_FOR_REVIEW   = "suspend_for_review"    # Both below threshold or contested
    SURFACE_UNCERTAINTY  = "surface_uncertainty"   # Neither grounded


class ReviewPriority(Enum):
    URGENT   = "urgent"    # 2 hours — safety or Law IV
    STANDARD = "standard"  # 24 hours — standard review
    EXTENDED = "extended"  # 48 hours — complex factual dispute


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

HIGH_SIGMA          = 0.93   # ETC — must match vadem.py
SIGMA_GAP_THRESHOLD = 0.10   # Minimum gap for Type A resolution
SLA_URGENT_HOURS    = 2
SLA_STANDARD_HOURS  = 24
SLA_EXTENDED_HOURS  = 48


# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

@dataclass
class ModelOutput:
    """
    A single model's output candidate for routing.
    """
    model_id:        str
    content_summary: str          # Summary only — no raw content stored
    sigma_score:     float
    output_type:     str
    is_safety_critical: bool = False   # Triggers Law IV / Law VII / Gate B
    has_external_grounding: bool = False   # Gate A check result
    grounding_reference: Optional[str] = None
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class RoutingResult:
    """
    Result of routing arbitration.
    Contains decision, routed output, labels, and review instructions.
    """
    conflict_type:    ConflictType
    decision:         RoutingDecision
    primary_output:   Optional[ModelOutput]      # Output routed forward
    secondary_output: Optional[ModelOutput]      # Held or logged
    label:            str                        # User-facing label
    reviewer_required: bool = False
    review_priority:  ReviewPriority = ReviewPriority.STANDARD
    sla_hours:        int = SLA_STANDARD_HOURS
    notes:            str = ""
    minority_signal_logged: bool = False

    def is_safe_to_surface(self) -> bool:
        """Output is ready to show user — no pending review required."""
        return not self.reviewer_required or \
               self.decision == RoutingDecision.SURFACE_UNCERTAINTY


# ─────────────────────────────────────────────
# CORE ROUTER
# ─────────────────────────────────────────────

class Router:
    """
    Routing Fallback Protocol — Gap 1 Resolution.

    Four conflict types, mutually exclusive and exhaustive:
      Type A — Sigma gap ≥ 0.10        → Higher σ routes
      Type B — Near-parity, both high  → Full resolution sequence
      Type C — Both below threshold    → Suspend both
      Type D — Safety-critical signal  → Safety always routes (NON-NEGOTIABLE)

    HARD CONSTRAINT: Anti-Averaging Rule (Law II)
      Never blend or average conflicting outputs.
      Synthetic confidence is deception.
    """

    # ── MAIN ENTRY POINT ─────────────────────

    def route(
        self,
        output_a: ModelOutput,
        output_b: ModelOutput,
        sla_breached: bool = False,
    ) -> RoutingResult:
        """
        Route between two conflicting model outputs.

        Args:
            output_a: First model output
            output_b: Second model output
            sla_breached: True if reviewer SLA has expired

        Returns:
            RoutingResult with decision, label, and review instructions
        """
        conflict_type = self._classify_conflict(output_a, output_b)

        if conflict_type == ConflictType.TYPE_D:
            return self._resolve_type_d(output_a, output_b)
        elif conflict_type == ConflictType.TYPE_A:
            return self._resolve_type_a(output_a, output_b)
        elif conflict_type == ConflictType.TYPE_C:
            return self._resolve_type_c(output_a, output_b)
        else:  # TYPE_B
            return self._resolve_type_b(output_a, output_b, sla_breached)

    # ── CONFLICT CLASSIFICATION ──────────────

    def _classify_conflict(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> ConflictType:
        """
        Classify conflict type. Order of evaluation matters:
        Type D check FIRST — safety is never overridden by confidence math.
        """
        # TYPE D — Safety-critical (checked FIRST, always)
        if a.is_safety_critical or b.is_safety_critical:
            return ConflictType.TYPE_D

        # TYPE C — Both below threshold
        if a.sigma_score < HIGH_SIGMA and b.sigma_score < HIGH_SIGMA:
            return ConflictType.TYPE_C

        # TYPE A — Clear sigma gap
        gap = abs(a.sigma_score - b.sigma_score)
        if gap >= SIGMA_GAP_THRESHOLD:
            return ConflictType.TYPE_A

        # TYPE B — Near-parity, at least one above threshold
        return ConflictType.TYPE_B

    # ── TYPE A RESOLUTION ────────────────────

    def _resolve_type_a(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> RoutingResult:
        """
        Type A — Sigma gap ≥ 0.10.
        Higher σ routes forward. Lower σ logged as minority signal.
        No review required.
        """
        primary, secondary = (a, b) if a.sigma_score >= b.sigma_score else (b, a)

        return RoutingResult(
            conflict_type=ConflictType.TYPE_A,
            decision=RoutingDecision.ROUTE_PRIMARY,
            primary_output=primary,
            secondary_output=secondary,
            label="",  # No label needed — clean routing
            reviewer_required=False,
            minority_signal_logged=True,
            notes=(
                f"Type A: σ gap = {abs(a.sigma_score - b.sigma_score):.3f} "
                f"≥ threshold {SIGMA_GAP_THRESHOLD}. "
                f"Primary: {primary.model_id} (σ={primary.sigma_score:.3f}). "
                f"Minority signal logged."
            ),
        )

    # ── TYPE B RESOLUTION ────────────────────

    def _resolve_type_b(
        self,
        a: ModelOutput,
        b: ModelOutput,
        sla_breached: bool,
    ) -> RoutingResult:
        """
        Type B — Near-parity conflict (gap < 0.10, at least one σ ≥ 0.93).
        Full resolution sequence — Step 1 through Step 3.

        ANTI-AVERAGING RULE: Never blend outputs. Surface uncertainty directly.
        """
        # Step 1 — Factual or framing disagreement?
        kind = self._classify_disagreement(a, b)

        if kind == DisagreementKind.FRAMING:
            return self._resolve_type_b_framing(a, b)

        # Factual disagreement — Steps 2 and 3
        return self._resolve_type_b_factual(a, b, sla_breached)

    def _resolve_type_b_framing(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> RoutingResult:
        """
        Framing disagreement — both framings are valid.
        Surface both. User chooses. VCR written.
        """
        return RoutingResult(
            conflict_type=ConflictType.TYPE_B,
            decision=RoutingDecision.ROUTE_BOTH_FRAMINGS,
            primary_output=a,
            secondary_output=b,
            label="[MULTIPLE VALID FRAMINGS]",
            reviewer_required=False,
            notes=(
                "Type B — framing disagreement. "
                "Both framings surfaced to user. User choice recorded. "
                "VCR written. Anti-averaging rule: outputs NOT blended."
            ),
        )

    def _resolve_type_b_factual(
        self,
        a: ModelOutput,
        b: ModelOutput,
        sla_breached: bool,
    ) -> RoutingResult:
        """
        Type B factual disagreement — tiebreaker hierarchy.

        Step 2a: One output grounded → grounded routes forward
        Step 2b: Both grounded, still conflicting → suspend for L2 review
        Step 2c: Neither grounded → surface with uncertainty label
        Step 3:  SLA breach → conservative output, never bolder claim
        """
        grounding = self._check_grounding(a, b)

        # Step 2a — One grounded
        if grounding == GroundingStatus.GROUNDED:
            primary = a if a.has_external_grounding else b
            secondary = b if a.has_external_grounding else a
            return RoutingResult(
                conflict_type=ConflictType.TYPE_B,
                decision=RoutingDecision.ROUTE_PRIMARY,
                primary_output=primary,
                secondary_output=secondary,
                label="",
                reviewer_required=False,
                notes=(
                    f"Type B step 2a: {primary.model_id} has external grounding "
                    f"(Gate A). Routes forward. "
                    f"{secondary.model_id} held as minority signal."
                ),
            )

        # Step 2b — Both grounded, still conflicting
        if grounding == GroundingStatus.CONTESTED:
            # Step 3 override — SLA breach
            if sla_breached:
                return self._resolve_sla_breach(a, b, ConflictType.TYPE_B)

            return RoutingResult(
                conflict_type=ConflictType.TYPE_B,
                decision=RoutingDecision.SUSPEND_FOR_REVIEW,
                primary_output=None,
                secondary_output=None,
                label="[CONTESTED FACTUAL CLAIM]",
                reviewer_required=True,
                review_priority=ReviewPriority.EXTENDED,
                sla_hours=SLA_EXTENDED_HOURS,
                notes=(
                    "Type B step 2b: Both outputs grounded, still conflicting. "
                    "Both suspended. Routed to L2 reviewer (48h SLA). "
                    "Output surfaced to user only after verdict. "
                    "Neither system nor user wins unilaterally."
                ),
            )

        # Step 2c — Neither grounded
        # Step 3 override — SLA breach
        if sla_breached:
            return self._resolve_sla_breach(a, b, ConflictType.TYPE_B)

        return RoutingResult(
            conflict_type=ConflictType.TYPE_B,
            decision=RoutingDecision.SURFACE_UNCERTAINTY,
            primary_output=None,
            secondary_output=None,
            label="[UNVERIFIED — CONFLICTING MODELS]",
            reviewer_required=False,
            notes=(
                "Type B step 2c: Neither output grounded. "
                "Uncertainty surfaced directly to user. "
                "User informed: models disagree, output unverified. "
                "Anti-averaging rule: outputs NOT blended."
            ),
        )

    # ── TYPE C RESOLUTION ────────────────────

    def _resolve_type_c(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> RoutingResult:
        """
        Type C — Both σ < 0.93.
        Neither output confident enough to route.
        Suspend both. Do not surface either to user.
        """
        return RoutingResult(
            conflict_type=ConflictType.TYPE_C,
            decision=RoutingDecision.SUSPEND_FOR_REVIEW,
            primary_output=None,
            secondary_output=None,
            label="[LOW CONFIDENCE — UNDER REVIEW]",
            reviewer_required=True,
            review_priority=ReviewPriority.STANDARD,
            sla_hours=SLA_STANDARD_HOURS,
            notes=(
                f"Type C: Both outputs below threshold "
                f"(σ_a={a.sigma_score:.3f}, σ_b={b.sigma_score:.3f} < {HIGH_SIGMA}). "
                "Neither surfaced. Escalated to human reviewer. "
                "Do not show either output to user in this state."
            ),
        )

    # ── TYPE D RESOLUTION ────────────────────

    def _resolve_type_d(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> RoutingResult:
        """
        Type D — Safety-critical signal present.
        Safety-critical output ALWAYS routes forward regardless of σ.
        NON-NEGOTIABLE. No override. No exception.

        Covers: Law IV (Medical Gate), Law VII (Non-Abandonment),
                Gate B hard stops, harm warnings.
        """
        # Identify safety-critical output
        if a.is_safety_critical and b.is_safety_critical:
            # Both safety-critical — route higher σ safety output
            primary = a if a.sigma_score >= b.sigma_score else b
            secondary = b if a.sigma_score >= b.sigma_score else a
        elif a.is_safety_critical:
            primary, secondary = a, b
        else:
            primary, secondary = b, a

        return RoutingResult(
            conflict_type=ConflictType.TYPE_D,
            decision=RoutingDecision.ROUTE_SAFETY,
            primary_output=primary,
            secondary_output=secondary,
            label="[SAFETY SIGNAL — VERIFIED]",
            reviewer_required=True,
            review_priority=ReviewPriority.URGENT,
            sla_hours=SLA_URGENT_HOURS,
            notes=(
                f"Type D: Safety-critical output from {primary.model_id} "
                f"routes forward regardless of σ (σ={primary.sigma_score:.3f}). "
                f"Non-safety output from {secondary.model_id} held pending review. "
                "NON-NEGOTIABLE. This decision cannot be overridden by σ score, "
                "time pressure, or V_user veto. Law IV / Law VII in effect."
            ),
        )

    # ── SLA BREACH HANDLER ───────────────────

    def _resolve_sla_breach(
        self,
        a: ModelOutput,
        b: ModelOutput,
        conflict_type: ConflictType,
    ) -> RoutingResult:
        """
        SLA breach — reviewer did not respond within SLA.
        Surface conservative (less assertive) output.
        NEVER surface bolder claim under time pressure.
        Time pressure does not justify confidence inflation.
        """
        # Conservative = lower sigma (less assertive)
        conservative = a if a.sigma_score <= b.sigma_score else b
        bold = b if a.sigma_score <= b.sigma_score else a

        return RoutingResult(
            conflict_type=conflict_type,
            decision=RoutingDecision.ROUTE_CONSERVATIVE,
            primary_output=conservative,
            secondary_output=bold,
            label="[PENDING REVIEW — CONSERVATIVE OUTPUT]",
            reviewer_required=True,
            review_priority=ReviewPriority.URGENT,
            sla_hours=SLA_URGENT_HOURS,
            notes=(
                "SLA breached. Conservative output surfaced "
                f"(σ={conservative.sigma_score:.3f}). "
                f"Bolder claim from {bold.model_id} held "
                f"(σ={bold.sigma_score:.3f}). "
                "Time pressure is NOT justification for confidence inflation. "
                "Review still required — escalated to URGENT."
            ),
        )

    # ── HELPERS ──────────────────────────────

    def _classify_disagreement(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> DisagreementKind:
        """
        Classify whether conflict is factual or framing.
        In Phase 1: caller sets output_type to signal this.
        'framing' output_type → FRAMING disagreement.
        All others → FACTUAL disagreement.
        """
        if a.output_type == "framing" or b.output_type == "framing":
            return DisagreementKind.FRAMING
        return DisagreementKind.FACTUAL

    def _check_grounding(
        self,
        a: ModelOutput,
        b: ModelOutput,
    ) -> GroundingStatus:
        """
        Gate A check — external grounding status.

        GROUNDED:   One has grounding, other does not
        CONTESTED:  Both have grounding but still conflict
        UNGROUNDED: Neither has grounding
        """
        if a.has_external_grounding and b.has_external_grounding:
            return GroundingStatus.CONTESTED
        if a.has_external_grounding or b.has_external_grounding:
            return GroundingStatus.GROUNDED
        return GroundingStatus.UNGROUNDED
