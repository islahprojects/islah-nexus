"""
test_vadem.py â€” VADEM v1.0 Test Suite
SEIL-Î© Phase 2 | Islah Constitutional Framework

Tests cover:
  - Rate limits (session + weekly, soft + hard)
  - Pattern flags P1â€“P4
  - Conflict arbitration (Law II vs Law III)
  - 90-day rolling scan (low-and-slow detection)
  - Notification builder
  - Law VI compliance (anonymization)

Run: python -m pytest test_vadem.py -v
"""

import pytest
from datetime import datetime, timedelta, timezone
from islah_nexus.vadem import (
    VADEM, VetoRecord, VetoDecision, VADEMState,
    OutputType, ReviewerVerdict, C
)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# HELPERS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def make_record(
    session_id="session_001",
    output_id="output_001",
    output_type=OutputType.FACTUAL,
    sigma_score=0.80,
    timestamp=None,
    reviewer_verdict=ReviewerVerdict.PENDING,
    escalation_paired=False,
) -> VetoRecord:
    return VetoRecord(
        session_id=session_id,
        output_id=output_id,
        output_type=output_type,
        sigma_score=sigma_score,
        timestamp=timestamp or datetime.now(timezone.utc),
        reviewer_verdict=reviewer_verdict,
        veto_paired_with_escalation=escalation_paired,
    )


def make_history(count, session_id="session_001", sigma=0.80,
                 output_type=OutputType.FACTUAL, days_ago=0):
    now = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return [
        make_record(session_id=session_id, sigma_score=sigma,
                    output_type=output_type,
                    timestamp=now - timedelta(minutes=i))
        for i in range(count)
    ]


vadem = VADEM()


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# RATE LIMIT TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestRateLimits:

    def test_below_soft_limit_is_clear(self):
        record = make_record(sigma_score=0.80)
        history = make_history(2, output_type=OutputType.FACTUAL) + make_history(2, output_type=OutputType.ETHICAL)
        result = vadem.evaluate_veto(record, history, history)
        assert result.state == VADEMState.CLEAR
        assert result.decision == VetoDecision.HONOR_VETO

    def test_soft_limit_session_activates_watch(self):
        record = make_record(sigma_score=0.80)
        history = make_history(C.SOFT_LIMIT_SESSION)
        result = vadem.evaluate_veto(record, history, history)
        assert any(f.code == "SOFT_LIMIT_SESSION" for f in result.flags)
        assert result.state in (VADEMState.WATCH, VADEMState.ALERT)

    def test_hard_limit_session_triggers_suspend(self):
        record = make_record(sigma_score=0.80)
        history = make_history(C.HARD_LIMIT_SESSION)
        result = vadem.evaluate_veto(record, history, history)
        assert result.decision == VetoDecision.SUSPEND
        assert result.state == VADEMState.SUSPEND
        assert any(f.code == "HARD_LIMIT_SESSION" for f in result.flags)

    def test_hard_limit_weekly_triggers_suspend(self):
        record = make_record(sigma_score=0.80)
        weekly_history = make_history(C.HARD_LIMIT_WEEKLY, days_ago=3)
        result = vadem.evaluate_veto(record, [], weekly_history)
        assert result.decision == VetoDecision.SUSPEND
        assert any(f.code == "HARD_LIMIT_WEEKLY" for f in result.flags)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CONFLICT ARBITRATION TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestConflictArbitration:

    def test_high_sigma_truth_holds_law_ii(self):
        """Ïƒ â‰¥ 0.93 â†’ CONTEST_LOG_ONLY. Truth holds. Law II."""
        record = make_record(sigma_score=C.HIGH_SIGMA)
        result = vadem.evaluate_veto(record, [], [])
        assert result.decision == VetoDecision.CONTEST_LOG_ONLY
        assert "Law II" in result.notes

    def test_low_sigma_user_holds_law_iii(self):
        """Ïƒ < 0.93 â†’ HONOR_VETO. User holds. Law III."""
        record = make_record(sigma_score=C.HIGH_SIGMA - 0.01)
        result = vadem.evaluate_veto(record, [], [])
        assert result.decision == VetoDecision.HONOR_VETO
        assert "Law III" in result.notes

    def test_exact_boundary_sigma(self):
        """Ïƒ = 0.93 exactly â†’ Truth holds."""
        record = make_record(sigma_score=0.93)
        result = vadem.evaluate_veto(record, [], [])
        assert result.decision == VetoDecision.CONTEST_LOG_ONLY

    def test_safety_output_type_gets_2h_sla(self):
        """Law IV / Law VII outputs get 2h SLA, not 24h."""
        record = make_record(output_type=OutputType.SAFETY, sigma_score=0.80)
        result = vadem.evaluate_veto(record, [], [])
        notif = vadem.build_notification(result, record)
        assert notif["sla_hours"] == 2

    def test_non_safety_output_gets_24h_sla(self):
        record = make_record(output_type=OutputType.FACTUAL, sigma_score=0.80)
        result = vadem.evaluate_veto(record, [], [])
        notif = vadem.build_notification(result, record)
        assert notif["sla_hours"] == 24


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PATTERN FLAG TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestPatternFlags:

    def test_flag_p1_directional_bias(self):
        """â‰¥ 70% same output_type in 14 days â†’ FLAG_P1."""
        record = make_record(output_type=OutputType.FACTUAL, sigma_score=0.80)
        # 9 factual vetoes (90% > 70% threshold)
        history = make_history(9, output_type=OutputType.FACTUAL)
        history += make_history(1, output_type=OutputType.ETHICAL)
        result = vadem.evaluate_veto(record, [], history)
        assert any(f.code == "FLAG_P1_DIRECTIONAL_BIAS" for f in result.flags)

    def test_flag_p1_not_triggered_below_threshold(self):
        """60% same type â€” below 70% threshold. No P1."""
        record = make_record(sigma_score=0.80)
        history = make_history(6, output_type=OutputType.FACTUAL)
        history += make_history(4, output_type=OutputType.ETHICAL)
        result = vadem.evaluate_veto(record, [], history)
        assert not any(f.code == "FLAG_P1_DIRECTIONAL_BIAS" for f in result.flags)

    def test_flag_p2_high_confidence_targeting(self):
        """â‰¥ 50% vetoes target Ïƒ â‰¥ 0.93 â†’ FLAG_P2."""
        record = make_record(sigma_score=0.95)
        # 6 high-confidence vetoes out of 10 (60% > 50%)
        history = make_history(6, sigma=0.95)
        history += make_history(4, sigma=0.80)
        result = vadem.evaluate_veto(record, [], history)
        assert any(f.code == "FLAG_P2_HIGH_CONFIDENCE_TARGET" for f in result.flags)

    def test_flag_p2_not_triggered_below_threshold(self):
        """40% high-confidence vetoes â€” below 50% threshold. No P2."""
        record = make_record(sigma_score=0.80)
        history = make_history(4, sigma=0.95)
        history += make_history(6, sigma=0.80)
        result = vadem.evaluate_veto(record, [], history)
        assert not any(f.code == "FLAG_P2_HIGH_CONFIDENCE_TARGET" for f in result.flags)

    def test_flag_p3_bad_faith_invalid_vetoes(self):
        """â‰¥ 3 INVALID_VETO verdicts in 30 days â†’ FLAG_P3."""
        record = make_record(sigma_score=0.80)
        history = [
            make_record(reviewer_verdict=ReviewerVerdict.INVALID_VETO)
            for _ in range(C.INVALID_VETO_BAD_FAITH_COUNT)
        ]
        result = vadem.evaluate_veto(record, [], history)
        assert any(f.code == "FLAG_P3_BAD_FAITH_VETO" for f in result.flags)

    def test_flag_p3_not_triggered_below_threshold(self):
        """2 invalid vetoes â€” below threshold. No P3."""
        record = make_record(sigma_score=0.80)
        history = [
            make_record(reviewer_verdict=ReviewerVerdict.INVALID_VETO)
            for _ in range(C.INVALID_VETO_BAD_FAITH_COUNT - 1)
        ]
        result = vadem.evaluate_veto(record, [], history)
        assert not any(f.code == "FLAG_P3_BAD_FAITH_VETO" for f in result.flags)

    def test_flag_p4_escalation_pairing(self):
        """â‰¥ 3 veto+escalation pairs â†’ FLAG_P4."""
        record = make_record(sigma_score=0.80)
        history = [
            make_record(escalation_paired=True)
            for _ in range(C.VETO_ESCALATION_PAIR_COUNT)
        ]
        result = vadem.evaluate_veto(record, [], history)
        assert any(f.code == "FLAG_P4_ESCALATION_PAIRING" for f in result.flags)


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# ROLLING SCAN TESTS (LOW-AND-SLOW)
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestRollingScan:

    def test_low_and_slow_p1_detected_across_subwindows(self):
        """
        Bad actor stays below session rate limits but
        systematically vetoes FACTUAL outputs over 90 days.
        Rolling scan must catch this.
        """
        # 80 factual vetoes spread across 90 days (below session limit each day)
        history = []
        for day in range(80):
            history.append(make_record(
                output_type=OutputType.FACTUAL,
                sigma_score=0.80,
                timestamp=datetime.now(timezone.utc) - timedelta(days=day % 89),
            ))
        # Add 10 ethical vetoes for variety
        for day in range(10):
            history.append(make_record(
                output_type=OutputType.ETHICAL,
                sigma_score=0.80,
                timestamp=datetime.now(timezone.utc) - timedelta(days=day % 89),
            ))

        flags = vadem.run_pattern_scan(history)
        p1_flags = [f for f in flags if "P1" in f.code]
        assert len(p1_flags) > 0, "Rolling scan must detect low-and-slow P1 pattern"

    def test_low_and_slow_p2_detected_across_subwindows(self):
        """
        Bad actor consistently vetoes high-confidence outputs
        below session thresholds. Rolling scan catches it.
        """
        history = []
        for day in range(60):
            history.append(make_record(
                sigma_score=0.95,  # High confidence
                timestamp=datetime.now(timezone.utc) - timedelta(days=day % 89),
            ))
        for day in range(20):
            history.append(make_record(
                sigma_score=0.80,
                timestamp=datetime.now(timezone.utc) - timedelta(days=day % 89),
            ))

        flags = vadem.run_pattern_scan(history)
        p2_flags = [f for f in flags if "P2" in f.code]
        assert len(p2_flags) > 0, "Rolling scan must detect low-and-slow P2 pattern"

    def test_clean_history_no_rolling_flags(self):
        """Random vetoes across all types â€” no systematic pattern. No flags."""
        history = []
        types = list(OutputType)
        for i in range(30):
            history.append(make_record(
                output_type=types[i % len(types)],
                sigma_score=0.70 + (i % 3) * 0.05,
                timestamp=datetime.now(timezone.utc) - timedelta(days=i * 2),
            ))
        flags = vadem.run_pattern_scan(history)
        assert len(flags) == 0


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# LAW VI COMPLIANCE TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestLawVICompliance:

    def test_session_id_is_anonymized_in_log(self):
        """Raw session_id must not appear in Log A entry."""
        record = make_record(session_id="user_jj_private_session")
        entry = record.to_log_entry()
        assert "user_jj_private_session" not in entry["session_id"]
        assert len(entry["session_id"]) == 16  # SHA-256 truncated

    def test_output_content_not_stored(self):
        """Log entry must not contain output content fields."""
        record = make_record()
        entry = record.to_log_entry()
        forbidden_keys = ["content", "text", "output_text", "response"]
        for key in forbidden_keys:
            assert key not in entry

    def test_notification_uses_anonymized_session_id(self):
        """Notification entry must use anonymized session_id."""
        record = make_record(session_id="sensitive_user_id_12345")
        result = vadem.evaluate_veto(record, [], [])
        notif = vadem.build_notification(result, record)
        assert "sensitive_user_id_12345" not in notif["session_id"]


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# NOTIFICATION BUILDER TESTS
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class TestNotificationBuilder:

    def test_notification_starts_as_pending(self):
        """All notifications must start as PENDING â€” cannot be auto-resolved."""
        record = make_record(sigma_score=0.80)
        result = vadem.evaluate_veto(record, [], [])
        notif = vadem.build_notification(result, record)
        assert notif["status"] == "PENDING"

    def test_notification_contains_required_fields(self):
        required = [
            "alert_type", "session_id", "timestamp", "flag_codes",
            "decision", "state", "sigma_score", "output_type",
            "status", "assigned_tier", "notes", "sla_hours"
        ]
        record = make_record()
        result = vadem.evaluate_veto(record, [], [])
        notif = vadem.build_notification(result, record)
        for field in required:
            assert field in notif, f"Missing required field: {field}"

    def test_suspend_decision_notification(self):
        """Suspended sessions must generate notification with SUSPEND decision."""
        record = make_record(sigma_score=0.80)
        history = make_history(C.HARD_LIMIT_SESSION)
        result = vadem.evaluate_veto(record, history, history)
        notif = vadem.build_notification(result, record)
        assert notif["decision"] == "suspend"
        assert notif["status"] == "PENDING"


