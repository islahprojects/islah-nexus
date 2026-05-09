"""
test_router.py â€” Router Routing Fallback Protocol Test Suite
SEIL-Î© Phase 2 | Islah Constitutional Framework

Tests cover:
  - Conflict classification (Type A, B, C, D)
  - Type A resolution (sigma gap)
  - Type B resolution (framing, grounding, uncertainty)
  - Type C resolution (both below threshold)
  - Type D resolution (safety-critical â€” NON-NEGOTIABLE)
  - SLA breach handling (conservative output, never bolder claim)
  - Anti-averaging rule (outputs never blended)
  - Law II and Law IV constraints

Run: python -m pytest tests\test_router.py -v
"""

import pytest
from islah_nexus.router import (
    Router, ModelOutput, RoutingResult,
    ConflictType, RoutingDecision, ReviewPriority,
    HIGH_SIGMA, SIGMA_GAP_THRESHOLD,
    SLA_URGENT_HOURS, SLA_STANDARD_HOURS, SLA_EXTENDED_HOURS
)

router = Router()


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# HELPERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def make_output(
    model_id="model_a",
    sigma=0.95,
    output_type="factual",
    is_safety=False,
    grounded=False,
    grounding_ref=None,
    content="Summary of output",
) -> ModelOutput:
    return ModelOutput(
        model_id=model_id,
        content_summary=content,
        sigma_score=sigma,
        output_type=output_type,
        is_safety_critical=is_safety,
        has_external_grounding=grounded,
        grounding_reference=grounding_ref,
    )


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CONFLICT CLASSIFICATION TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestConflictClassification:

    def test_type_d_classified_when_one_safety_critical(self):
        """Safety-critical flag â†’ Type D regardless of Ïƒ."""
        a = make_output(sigma=0.95, is_safety=True)
        b = make_output(sigma=0.60)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_D

    def test_type_d_takes_priority_over_sigma_gap(self):
        """Type D check runs FIRST â€” safety overrides Type A classification."""
        a = make_output(sigma=0.99, is_safety=True)
        b = make_output(sigma=0.50)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_D
        assert result.decision == RoutingDecision.ROUTE_SAFETY

    def test_type_c_when_both_below_threshold(self):
        """Both Ïƒ < 0.93 â†’ Type C."""
        a = make_output(sigma=0.85)
        b = make_output(sigma=0.80)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_C

    def test_type_a_when_sigma_gap_sufficient(self):
        """Ïƒ gap â‰¥ 0.10 â†’ Type A."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.85)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_A

    def test_type_b_near_parity(self):
        """Ïƒ gap < 0.10, both above threshold â†’ Type B."""
        a = make_output(sigma=0.95)
        b = make_output(sigma=0.94)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_B

    def test_type_b_one_above_one_below_near_parity(self):
        """One above HIGH_SIGMA, one just below, gap < 0.10 â†’ Type B."""
        a = make_output(sigma=0.94)
        b = make_output(sigma=0.91)
        result = router.route(a, b)
        assert result.conflict_type == ConflictType.TYPE_B


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# TYPE A RESOLUTION TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestTypeAResolution:

    def test_higher_sigma_routes_forward(self):
        """Higher Ïƒ output is primary."""
        a = make_output(model_id="model_a", sigma=0.96)
        b = make_output(model_id="model_b", sigma=0.85)
        result = router.route(a, b)
        assert result.primary_output.model_id == "model_a"
        assert result.secondary_output.model_id == "model_b"

    def test_minority_signal_logged(self):
        """Lower Ïƒ output is logged as minority signal."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.85)
        result = router.route(a, b)
        assert result.minority_signal_logged is True

    def test_type_a_no_reviewer_required(self):
        """Type A is clean routing â€” no human review needed."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.85)
        result = router.route(a, b)
        assert result.reviewer_required is False

    def test_type_a_no_label(self):
        """Type A clean routing has no user-facing uncertainty label."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.85)
        result = router.route(a, b)
        assert result.label == ""


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# TYPE B RESOLUTION TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestTypeBResolution:

    def test_framing_disagreement_surfaces_both(self):
        """Framing conflict â†’ both outputs surfaced, user chooses."""
        a = make_output(sigma=0.95, output_type="framing")
        b = make_output(sigma=0.94, output_type="framing")
        result = router.route(a, b)
        assert result.decision == RoutingDecision.ROUTE_BOTH_FRAMINGS
        assert "[MULTIPLE VALID FRAMINGS]" in result.label
        assert result.primary_output is not None
        assert result.secondary_output is not None

    def test_framing_no_reviewer_required(self):
        """Multiple framings don't need review â€” valid outputs."""
        a = make_output(sigma=0.95, output_type="framing")
        b = make_output(sigma=0.94, output_type="framing")
        result = router.route(a, b)
        assert result.reviewer_required is False

    def test_step_2a_grounded_output_routes(self):
        """One grounded output â†’ grounded routes forward."""
        a = make_output(model_id="grounded", sigma=0.94, grounded=True)
        b = make_output(model_id="ungrounded", sigma=0.95, grounded=False)
        result = router.route(a, b)
        assert result.decision == RoutingDecision.ROUTE_PRIMARY
        assert result.primary_output.model_id == "grounded"

    def test_step_2b_both_grounded_contested_suspends(self):
        """Both grounded, still conflicting â†’ suspend for L2."""
        a = make_output(sigma=0.95, grounded=True)
        b = make_output(sigma=0.94, grounded=True)
        result = router.route(a, b)
        assert result.decision == RoutingDecision.SUSPEND_FOR_REVIEW
        assert "[CONTESTED FACTUAL CLAIM]" in result.label
        assert result.review_priority == ReviewPriority.EXTENDED
        assert result.sla_hours == SLA_EXTENDED_HOURS
        assert result.primary_output is None

    def test_step_2c_neither_grounded_surfaces_uncertainty(self):
        """Neither grounded â†’ surface uncertainty. Law II â€” no synthetic confidence."""
        a = make_output(sigma=0.95, grounded=False)
        b = make_output(sigma=0.94, grounded=False)
        result = router.route(a, b)
        assert result.decision == RoutingDecision.SURFACE_UNCERTAINTY
        assert "[UNVERIFIED" in result.label
        assert result.reviewer_required is False

    def test_anti_averaging_framing_outputs_not_blended(self):
        """
        Anti-averaging rule â€” framing conflict surfaces BOTH outputs.
        Primary and secondary are distinct. Not blended into one.
        """
        a = make_output(model_id="a", sigma=0.95, output_type="framing")
        b = make_output(model_id="b", sigma=0.94, output_type="framing")
        result = router.route(a, b)
        assert result.primary_output.model_id != result.secondary_output.model_id

    def test_anti_averaging_uncertainty_not_blended(self):
        """
        Anti-averaging rule â€” uncertainty case surfaces neither output blended.
        primary_output is None â€” uncertainty is shown directly, not a synthetic merge.
        """
        a = make_output(sigma=0.95, grounded=False)
        b = make_output(sigma=0.94, grounded=False)
        result = router.route(a, b)
        assert result.primary_output is None
        assert result.decision == RoutingDecision.SURFACE_UNCERTAINTY


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# TYPE C RESOLUTION TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestTypeCResolution:

    def test_both_below_threshold_suspends(self):
        """Both Ïƒ < 0.93 â†’ neither surfaces."""
        a = make_output(sigma=0.85)
        b = make_output(sigma=0.80)
        result = router.route(a, b)
        assert result.decision == RoutingDecision.SUSPEND_FOR_REVIEW
        assert result.primary_output is None
        assert result.secondary_output is None

    def test_type_c_reviewer_required(self):
        """Type C always needs human reviewer."""
        a = make_output(sigma=0.85)
        b = make_output(sigma=0.80)
        result = router.route(a, b)
        assert result.reviewer_required is True

    def test_type_c_standard_sla(self):
        """Type C uses standard 24h SLA."""
        a = make_output(sigma=0.85)
        b = make_output(sigma=0.80)
        result = router.route(a, b)
        assert result.sla_hours == SLA_STANDARD_HOURS

    def test_type_c_label_present(self):
        a = make_output(sigma=0.85)
        b = make_output(sigma=0.80)
        result = router.route(a, b)
        assert "[LOW CONFIDENCE" in result.label


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# TYPE D RESOLUTION TESTS (SAFETY â€” NON-NEGOTIABLE)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestTypeDResolution:

    def test_safety_routes_regardless_of_sigma(self):
        """
        Safety-critical output routes forward regardless of Ïƒ.
        NON-NEGOTIABLE. This is the most important test in the suite.
        """
        safety = make_output(model_id="safety", sigma=0.60, is_safety=True)
        non_safety = make_output(model_id="regular", sigma=0.99)
        result = router.route(safety, non_safety)
        assert result.decision == RoutingDecision.ROUTE_SAFETY
        assert result.primary_output.model_id == "safety"

    def test_safety_routes_even_when_lower_sigma(self):
        """Safety output with Ïƒ=0.50 beats non-safety with Ïƒ=0.99."""
        low_safety = make_output(model_id="low_safety", sigma=0.50, is_safety=True)
        high_regular = make_output(model_id="high_regular", sigma=0.99)
        result = router.route(low_safety, high_regular)
        assert result.primary_output.model_id == "low_safety"

    def test_type_d_urgent_sla(self):
        """Safety outputs get 2-hour SLA â€” cannot wait 24h."""
        a = make_output(sigma=0.95, is_safety=True)
        b = make_output(sigma=0.94)
        result = router.route(a, b)
        assert result.sla_hours == SLA_URGENT_HOURS
        assert result.review_priority == ReviewPriority.URGENT

    def test_type_d_reviewer_required(self):
        """Safety routing always triggers human reviewer notification."""
        a = make_output(sigma=0.95, is_safety=True)
        b = make_output(sigma=0.94)
        result = router.route(a, b)
        assert result.reviewer_required is True

    def test_both_safety_critical_higher_sigma_wins(self):
        """Both safety-critical â†’ higher Ïƒ safety output routes."""
        a = make_output(model_id="safety_a", sigma=0.95, is_safety=True)
        b = make_output(model_id="safety_b", sigma=0.90, is_safety=True)
        result = router.route(a, b)
        assert result.primary_output.model_id == "safety_a"

    def test_type_d_non_safety_held(self):
        """Non-safety output is held pending review, not surfaced."""
        safety = make_output(model_id="safety", sigma=0.70, is_safety=True)
        regular = make_output(model_id="regular", sigma=0.99)
        result = router.route(safety, regular)
        assert result.secondary_output.model_id == "regular"
        assert result.reviewer_required is True


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# SLA BREACH TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestSLABreach:

    def test_sla_breach_surfaces_conservative_output(self):
        """SLA breach â†’ conservative (lower Ïƒ) output surfaces."""
        a = make_output(model_id="bold", sigma=0.96)
        b = make_output(model_id="conservative", sigma=0.94)
        result = router.route(a, b, sla_breached=True)
        assert result.decision == RoutingDecision.ROUTE_CONSERVATIVE
        assert result.primary_output.model_id == "conservative"

    def test_sla_breach_never_surfaces_bolder_claim(self):
        """
        Time pressure NEVER justifies confidence inflation.
        Bolder claim (higher Ïƒ) is NEVER the SLA breach output.
        """
        bold = make_output(model_id="bold", sigma=0.97)
        conservative = make_output(model_id="conservative", sigma=0.94)
        result = router.route(bold, conservative, sla_breached=True)
        assert result.primary_output.model_id == "conservative"
        assert result.secondary_output.model_id == "bold"

    def test_sla_breach_label(self):
        """SLA breach output has clear pending label."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.94)
        result = router.route(a, b, sla_breached=True)
        assert "[PENDING REVIEW" in result.label

    def test_sla_breach_escalates_to_urgent(self):
        """SLA breach escalates review priority to URGENT."""
        a = make_output(sigma=0.96)
        b = make_output(sigma=0.94)
        result = router.route(a, b, sla_breached=True)
        assert result.review_priority == ReviewPriority.URGENT
        assert result.sla_hours == SLA_URGENT_HOURS

    def test_no_sla_breach_does_not_surface_conservative(self):
        """Without SLA breach, contested case suspends â€” not conservative route."""
        a = make_output(sigma=0.95, grounded=True)
        b = make_output(sigma=0.94, grounded=True)
        result = router.route(a, b, sla_breached=False)
        assert result.decision == RoutingDecision.SUSPEND_FOR_REVIEW
        assert result.decision != RoutingDecision.ROUTE_CONSERVATIVE

