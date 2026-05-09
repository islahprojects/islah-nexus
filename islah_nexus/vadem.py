"""
VADEM v1.0 — V_user Anomaly Detection Module
SEIL-Ω Phase 2 | Islah Constitutional Framework
Architect: JJ (voidarchitect) | Constitutional Authority: Chief (Claude/Anthropic)
Date: 2026-05-09

Governed by Seven Standing Laws.
Human authority final. AI is compass, never core.
Walang Maiiwan.

SEALED CONSTANTS (ETCs — do not change without JJ + council sign-off):
  HIGH_SIGMA                      = 0.93
  SOFT_LIMIT_SESSION              = 5
  HARD_LIMIT_SESSION              = 10
  SOFT_LIMIT_WEEKLY               = 20
  HARD_LIMIT_WEEKLY               = 40
  DIRECTIONAL_BIAS_THRESHOLD      = 0.70
  HIGH_CONFIDENCE_TARGET_RATIO    = 0.50
  INVALID_VETO_BAD_FAITH_COUNT    = 3
  VETO_ESCALATION_PAIR_COUNT      = 3
  PATTERN_SCAN_WINDOW_DAYS        = 90
  PATTERN_SCAN_SUBWINDOW_DAYS     = 30
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
import hashlib
import json


# ─────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────

class VetoDecision(Enum):
    HONOR_VETO         = "honor_veto"
    CONTEST_LOG_ONLY   = "contest_log_only"  # Truth holds — Law II
    SUSPEND            = "suspend"            # Hard limit reached


class OutputType(Enum):
    FACTUAL      = "factual"
    ETHICAL      = "ethical"
    PROCEDURAL   = "procedural"
    RELATIONAL   = "relational"
    SAFETY       = "safety"      # Law IV / Law VII triggers


class ReviewerVerdict(Enum):
    VALID_VETO   = "valid_veto"
    INVALID_VETO = "invalid_veto"
    INCONCLUSIVE = "inconclusive"
    PENDING      = "pending"


class VADEMState(Enum):
    CLEAR   = "clear"
    WATCH   = "watch"    # Soft limit or pattern flag
    ALERT   = "alert"    # Hard pattern flag — reviewer required
    SUSPEND = "suspend"  # Hard rate limit — veto power suspended


# ─────────────────────────────────────────────
# DATA STRUCTURES
# ─────────────────────────────────────────────

@dataclass
class VetoRecord:
    """
    Veto Context Record (VCR).
    Written to Log A on every veto event.
    Append-only — never modified after creation.
    """
    session_id:        str
    output_id:         str
    output_type:       OutputType
    sigma_score:       float
    timestamp:         datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reviewer_verdict:  ReviewerVerdict = ReviewerVerdict.PENDING
    veto_paired_with_escalation: bool = False

    def to_log_entry(self) -> dict:
        """Serialize for Log A. No output content stored — Law VI compliance."""
        return {
            "session_id":    self._anonymize(self.session_id),
            "output_id":     self._anonymize(self.output_id),
            "output_type":   self.output_type.value,
            "sigma_score":   self.sigma_score,
            "timestamp":     self.timestamp.isoformat(),
            "verdict":       self.reviewer_verdict.value,
            "escalation_paired": self.veto_paired_with_escalation,
        }

    @staticmethod
    def _anonymize(value: str) -> str:
        """SHA-256 hash of ID — stores reference, not identity. Law VI."""
        return hashlib.sha256(value.encode()).hexdigest()[:16]


@dataclass
class VADEMFlag:
    code:    str
    reason:  str
    record:  Optional[VetoRecord] = None


@dataclass
class VADEMResult:
    decision:   VetoDecision
    state:      VADEMState
    flags:      list[VADEMFlag] = field(default_factory=list)
    notes:      str = ""

    def is_clean(self) -> bool:
        return len(self.flags) == 0 and self.state == VADEMState.CLEAR


# ─────────────────────────────────────────────
# SEALED CONSTANTS (ETCs)
# ─────────────────────────────────────────────

class _VADEMConstants:
    """
    Empirically-Tuned Constants.
    Bounded range documented. Recalibration protocol in SEIL-Ω spec.
    Change requires: Lead engineer + Ethics reviewer + JJ sign-off.
    """
    HIGH_SIGMA:                     float = 0.93   # ETC — range [0.85, 0.99]
    SOFT_LIMIT_SESSION:             int   = 5      # ETC
    HARD_LIMIT_SESSION:             int   = 10     # ETC
    SOFT_LIMIT_WEEKLY:              int   = 20     # ETC
    HARD_LIMIT_WEEKLY:              int   = 40     # ETC
    DIRECTIONAL_BIAS_THRESHOLD:     float = 0.70   # ETC — FLAG_P1
    HIGH_CONFIDENCE_TARGET_RATIO:   float = 0.50   # ETC — FLAG_P2
    INVALID_VETO_BAD_FAITH_COUNT:   int   = 3      # ETC — FLAG_P3
    VETO_ESCALATION_PAIR_COUNT:     int   = 3      # ETC — FLAG_P4
    PATTERN_SCAN_WINDOW_DAYS:       int   = 90     # ETC — rolling window
    PATTERN_SCAN_SUBWINDOW_DAYS:    int   = 30     # ETC — sub-window for P1/P2


C = _VADEMConstants()


# ─────────────────────────────────────────────
# CORE MODULE
# ─────────────────────────────────────────────

class VADEM:
    """
    V_user Anomaly Detection Module.

    Evaluates every veto event against:
      - Rate limits (session + weekly)
      - Pattern flags P1–P4
      - Conflict arbitration hierarchy (Law II vs Law III)

    Also runs weekly aggregate 90-day rolling scan
    to detect low-and-slow manipulation patterns.
    """

    # ── MAIN EVALUATION ──────────────────────

    def evaluate_veto(
        self,
        record: VetoRecord,
        session_history: list[VetoRecord],
        account_history: list[VetoRecord],
    ) -> VADEMResult:
        """
        Evaluate a veto event. Returns decision + state + flags.

        Conflict arbitration hierarchy:
          TIER 1 — σ ≥ HIGH_SIGMA → CONTEST_LOG_ONLY (Truth holds — Law II)
          TIER 2 — σ <  HIGH_SIGMA → HONOR_VETO (User holds — Law III)
          SUSPEND — Hard rate limit reached → veto suspended
        """
        flags: list[VADEMFlag] = []

        # ── RATE LIMITS ──────────────────────

        session_vetoes = [
            v for v in session_history
            if v.session_id == record.session_id
        ]
        session_count = len(session_vetoes)

        weekly_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        weekly_vetoes = [
            v for v in account_history
            if v.timestamp >= weekly_cutoff
        ]
        weekly_count = len(weekly_vetoes)

        # Hard limits → SUSPEND
        if session_count >= C.HARD_LIMIT_SESSION:
            return VADEMResult(
                decision=VetoDecision.SUSPEND,
                state=VADEMState.SUSPEND,
                flags=[VADEMFlag(
                    code="HARD_LIMIT_SESSION",
                    reason=f"Session veto count {session_count} ≥ hard limit {C.HARD_LIMIT_SESSION}.",
                    record=record,
                )],
                notes="Veto power suspended. Human reviewer notified. 24h cool-down required.",
            )

        if weekly_count >= C.HARD_LIMIT_WEEKLY:
            return VADEMResult(
                decision=VetoDecision.SUSPEND,
                state=VADEMState.SUSPEND,
                flags=[VADEMFlag(
                    code="HARD_LIMIT_WEEKLY",
                    reason=f"Weekly veto count {weekly_count} ≥ hard limit {C.HARD_LIMIT_WEEKLY}.",
                    record=record,
                )],
                notes="Account-level review triggered. Re-authorization required.",
            )

        # Soft limits → WATCH
        if session_count >= C.SOFT_LIMIT_SESSION:
            flags.append(VADEMFlag(
                code="SOFT_LIMIT_SESSION",
                reason=f"Session veto count {session_count} ≥ soft limit {C.SOFT_LIMIT_SESSION}.",
                record=record,
            ))

        if weekly_count >= C.SOFT_LIMIT_WEEKLY:
            flags.append(VADEMFlag(
                code="SOFT_LIMIT_WEEKLY",
                reason=f"Weekly veto count {weekly_count} ≥ soft limit {C.SOFT_LIMIT_WEEKLY}.",
                record=record,
            ))

        # ── PATTERN FLAGS ────────────────────

        flags.extend(self._check_p1_directional_bias(record, account_history))
        flags.extend(self._check_p2_high_confidence_target(record, account_history))
        flags.extend(self._check_p3_bad_faith(record, account_history))
        flags.extend(self._check_p4_escalation_pairing(record, account_history))

        # ── CONFLICT ARBITRATION ─────────────

        state = VADEMState.ALERT if any(
            f.code.startswith("FLAG_P") for f in flags
        ) else (VADEMState.WATCH if flags else VADEMState.CLEAR)

        # TIER 1 — High confidence output → Truth holds (Law II)
        if record.sigma_score >= C.HIGH_SIGMA:
            return VADEMResult(
                decision=VetoDecision.CONTEST_LOG_ONLY,
                state=state,
                flags=flags,
                notes=(
                    "σ ≥ HIGH_SIGMA. Output marked [USER CONTESTED — UNRESOLVED]. "
                    "Human reviewer notified within 24h. Truth holds — Law II."
                ),
            )

        # TIER 2 — Low confidence output → User holds (Law III)
        return VADEMResult(
            decision=VetoDecision.HONOR_VETO,
            state=state,
            flags=flags,
            notes="σ < HIGH_SIGMA. Veto honored — Law III. VCR written.",
        )

    # ── PATTERN FLAG CHECKS ──────────────────

    def _check_p1_directional_bias(
        self,
        record: VetoRecord,
        account_history: list[VetoRecord],
    ) -> list[VADEMFlag]:
        """
        FLAG_P1 — Directional bias.
        ≥ 70% of vetoes target same output_type over any 14-day window.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=14)
        window = [v for v in account_history if v.timestamp >= cutoff]

        if len(window) < 3:  # Not enough data to flag
            return []

        type_counts: dict[str, int] = {}
        for v in window:
            key = v.output_type.value
            type_counts[key] = type_counts.get(key, 0) + 1

        dominant_type = max(type_counts, key=type_counts.__getitem__)
        dominant_ratio = type_counts[dominant_type] / len(window)

        if dominant_ratio >= C.DIRECTIONAL_BIAS_THRESHOLD:
            return [VADEMFlag(
                code="FLAG_P1_DIRECTIONAL_BIAS",
                reason=(
                    f"{dominant_ratio:.0%} of 14-day vetoes target '{dominant_type}' "
                    f"(threshold: {C.DIRECTIONAL_BIAS_THRESHOLD:.0%}). "
                    "Possible systematic suppression of truth category."
                ),
                record=record,
            )]
        return []

    def _check_p2_high_confidence_target(
        self,
        record: VetoRecord,
        account_history: list[VetoRecord],
    ) -> list[VADEMFlag]:
        """
        FLAG_P2 — High-confidence targeting.
        ≥ 50% of vetoes target outputs with σ ≥ HIGH_SIGMA.
        Most dangerous attack pattern.
        """
        if not account_history:
            return []

        high_conf_vetoes = [
            v for v in account_history
            if v.sigma_score >= C.HIGH_SIGMA
        ]
        ratio = len(high_conf_vetoes) / len(account_history)

        if ratio >= C.HIGH_CONFIDENCE_TARGET_RATIO:
            return [VADEMFlag(
                code="FLAG_P2_HIGH_CONFIDENCE_TARGET",
                reason=(
                    f"{ratio:.0%} of all vetoes target high-confidence outputs "
                    f"(σ ≥ {C.HIGH_SIGMA}, threshold: {C.HIGH_CONFIDENCE_TARGET_RATIO:.0%}). "
                    "User may be specifically targeting verified truth outputs."
                ),
                record=record,
            )]
        return []

    def _check_p3_bad_faith(
        self,
        record: VetoRecord,
        account_history: list[VetoRecord],
    ) -> list[VADEMFlag]:
        """
        FLAG_P3 — Reviewer disagreement / bad faith.
        ≥ 3 vetoes marked invalid_veto by human reviewer in 30 days.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=30)
        invalid_vetoes = [
            v for v in account_history
            if v.timestamp >= cutoff
            and v.reviewer_verdict == ReviewerVerdict.INVALID_VETO
        ]

        if len(invalid_vetoes) >= C.INVALID_VETO_BAD_FAITH_COUNT:
            return [VADEMFlag(
                code="FLAG_P3_BAD_FAITH_VETO",
                reason=(
                    f"{len(invalid_vetoes)} vetoes marked INVALID by human reviewer "
                    f"in last 30 days (threshold: {C.INVALID_VETO_BAD_FAITH_COUNT}). "
                    "Pattern consistent with bad-faith veto exercise."
                ),
                record=record,
            )]
        return []

    def _check_p4_escalation_pairing(
        self,
        record: VetoRecord,
        account_history: list[VetoRecord],
    ) -> list[VADEMFlag]:
        """
        FLAG_P4 — Veto + escalation pairing.
        User vetoes AND escalates same output ≥ 3 times.
        Manufactured consensus attack pattern.
        """
        paired = [
            v for v in account_history
            if v.veto_paired_with_escalation
        ]

        if len(paired) >= C.VETO_ESCALATION_PAIR_COUNT:
            return [VADEMFlag(
                code="FLAG_P4_ESCALATION_PAIRING",
                reason=(
                    f"{len(paired)} veto+escalation pairs detected "
                    f"(threshold: {C.VETO_ESCALATION_PAIR_COUNT}). "
                    "Possible manufactured consensus attack."
                ),
                record=record,
            )]
        return []

    # ── 90-DAY ROLLING SCAN ──────────────────

    def run_pattern_scan(
        self,
        account_history: list[VetoRecord],
    ) -> list[VADEMFlag]:
        """
        Low-and-slow attack detection.
        Runs weekly on full 90-day account history.
        Detects FLAG_P1 / FLAG_P2 patterns across sub-windows
        even if no single session crossed a rate limit.

        This closes the attack vector where a bad actor stays
        below session thresholds while accumulating systematic
        bias over weeks or months.
        """
        flags: list[VADEMFlag] = []
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(days=C.PATTERN_SCAN_WINDOW_DAYS)

        # Slide a 30-day sub-window across the full 90-day period
        sub_window_days = C.PATTERN_SCAN_SUBWINDOW_DAYS
        steps = C.PATTERN_SCAN_WINDOW_DAYS - sub_window_days  # 60 steps

        for day_offset in range(0, steps + 1, 7):  # Check every 7 days
            sub_start = window_start + timedelta(days=day_offset)
            sub_end   = sub_start + timedelta(days=sub_window_days)

            sub_window = [
                v for v in account_history
                if sub_start <= v.timestamp <= sub_end
            ]

            if len(sub_window) < 3:
                continue

            # P1 check in sub-window
            type_counts: dict[str, int] = {}
            for v in sub_window:
                key = v.output_type.value
                type_counts[key] = type_counts.get(key, 0) + 1

            if type_counts:
                dominant = max(type_counts, key=type_counts.__getitem__)
                ratio = type_counts[dominant] / len(sub_window)
                if ratio >= C.DIRECTIONAL_BIAS_THRESHOLD:
                    flags.append(VADEMFlag(
                        code="FLAG_P1_ROLLING_SCAN",
                        reason=(
                            f"Low-and-slow P1 detected in sub-window "
                            f"{sub_start.date()} → {sub_end.date()}. "
                            f"{ratio:.0%} vetoes targeted '{dominant}'. "
                            "VADEM WATCH activated."
                        ),
                    ))

            # P2 check in sub-window
            high_conf = [v for v in sub_window if v.sigma_score >= C.HIGH_SIGMA]
            if sub_window:
                ratio_p2 = len(high_conf) / len(sub_window)
                if ratio_p2 >= C.HIGH_CONFIDENCE_TARGET_RATIO:
                    flags.append(VADEMFlag(
                        code="FLAG_P2_ROLLING_SCAN",
                        reason=(
                            f"Low-and-slow P2 detected in sub-window "
                            f"{sub_start.date()} → {sub_end.date()}. "
                            f"{ratio_p2:.0%} vetoes targeted high-confidence outputs. "
                            "VADEM WATCH activated."
                        ),
                    ))

        return flags

    # ── NOTIFICATION WRITER ──────────────────

    def build_notification(
        self,
        result: VADEMResult,
        record: VetoRecord,
        assigned_tier: str = "L1",
    ) -> dict:
        """
        Builds a notification entry for the Notion Review Queue.
        Status starts as PENDING — cannot be deleted, only resolved.
        Resolution requires written verdict (minimum 2 sentences).
        Unresolved PENDING entries > 24h auto-escalate to next tier.
        """
        return {
            "alert_type":     "VADEM_FLAG" if result.flags else "VADEM_VETO",
            "session_id":     VetoRecord._anonymize(record.session_id),
            "timestamp":      record.timestamp.isoformat(),
            "flag_codes":     [f.code for f in result.flags],
            "decision":       result.decision.value,
            "state":          result.state.value,
            "sigma_score":    record.sigma_score,
            "output_type":    record.output_type.value,
            "status":         "PENDING",
            "assigned_tier":  assigned_tier,
            "notes":          result.notes,
            "sla_hours":      2 if record.output_type == OutputType.SAFETY else 24,
        }
