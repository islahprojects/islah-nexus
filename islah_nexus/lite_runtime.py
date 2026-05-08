from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


SIGMA_MAX = 0.93
EPSILON_MIN = 0.07

VALID_STATUS_TAGS = {
    "IMPLEMENTED",
    "PARTIAL",
    "PLACEHOLDER",
    "UNVERIFIED",
    "REJECTED",
    "BLUEPRINT",
    "LORE",
}

FILIPINO_LABELS: Dict[str, str] = {
    "PASS": "Pumasa",
    "WARN": "May babala",
    "REVIEW_REQUIRED": "Kailangan ng tao na magsuri",
    "HALT_USER_VETO": "Pasyang Tao: Itigil",
    "HALT_TRUTH_GAP": "Hindi sapat ang katiyakan",
    "HALT_SECRET_DETECTED": "May posibleng sikreto: itigil",
    "HALT_WALANG_MAIIWAN": "May naiiwan: ayusin muna",
    "HALT_CONSTITUTIONAL": "Lumabag sa batas ng sistema",
    "IMPLEMENTED": "Gumagana at napatunayan",
    "PARTIAL": "Bahagyang gawa pa lang",
    "PLACEHOLDER": "Pangalan pa lang, wala pang tunay na gawa",
    "UNVERIFIED": "Hindi pa napatunayan",
    "REJECTED": "Tinanggihan dahil mali o sobra ang claim",
    "BLUEPRINT": "Plano pa lang",
    "LORE": "Kuwento o simbolo, hindi runtime claim",
    "DEEPWORLDS_METADATA_ONLY": "Karagdagang konteksto, hindi batas",
    "BEST_EFFORT_ROUTING": "Susubukang ipadala, walang kasiguraduhan",
    "TRUTH_GAP": "May puwang ng hindi tiyak",
}


@dataclass(frozen=True)
class LiteResult:
    verdict: str
    status_tag: str
    filipino_label: str
    message: str
    sigma: float
    epsilon: float
    omega_law: int
    human_authority_final: bool = True
    no_agi_claim: bool = True


def validate_status_tag(status: str) -> str:
    normalized = (status or "").strip().upper()
    if normalized not in VALID_STATUS_TAGS:
        raise ValueError(f"Invalid status tag: {status!r}")
    return normalized


def validate_truth_gap(sigma: float, epsilon: Optional[float] = None) -> Tuple[float, float]:
    sigma = float(sigma)

    if epsilon is None:
        epsilon = 1.0 - sigma
    epsilon = float(epsilon)

    if sigma > SIGMA_MAX + 1e-9:
        raise ValueError("HALT_TRUTH_GAP: sigma must be <= 0.93")

    if epsilon < EPSILON_MIN - 1e-9:
        raise ValueError("HALT_TRUTH_GAP: epsilon must be >= 0.07")

    if abs((sigma + epsilon) - 1.0) > 0.02:
        raise ValueError("HALT_TRUTH_GAP: sigma + epsilon must be close to 1.0")

    return round(sigma, 4), round(epsilon, 4)


def lite_evaluate(
    *,
    verdict: str = "PASS",
    status_tag: str = "PARTIAL",
    sigma: float = 0.70,
    epsilon: Optional[float] = None,
    omega_law: int = 1,
    v_user: int = 1,
    deepworlds_metadata_only: bool = True,
    rf_delivery_guarantee: bool = False,
    firmware_implementation_claim: bool = False,
) -> LiteResult:
    status_tag = validate_status_tag(status_tag)

    if v_user == 0:
        sigma_value, epsilon_value = validate_truth_gap(min(float(sigma), SIGMA_MAX), epsilon or 0.30)
        return LiteResult(
            verdict="HALT_USER_VETO",
            status_tag=status_tag,
            filipino_label=FILIPINO_LABELS["HALT_USER_VETO"],
            message="Pasyang Tao: Itigil. Human authority remains final.",
            sigma=sigma_value,
            epsilon=epsilon_value,
            omega_law=0,
        )

    if omega_law not in (0, 1):
        raise ValueError("omega_law must be binary: 0 or 1")

    sigma_value, epsilon_value = validate_truth_gap(sigma, epsilon)

    if not deepworlds_metadata_only:
        return LiteResult(
            verdict="HALT_CONSTITUTIONAL",
            status_tag="REJECTED",
            filipino_label=FILIPINO_LABELS["REJECTED"],
            message="Deepworlds attempted to enter the control path. Karagdagang konteksto lang ito, hindi batas.",
            sigma=sigma_value,
            epsilon=epsilon_value,
            omega_law=0,
        )

    if rf_delivery_guarantee:
        return LiteResult(
            verdict="HALT_CONSTITUTIONAL",
            status_tag="REJECTED",
            filipino_label=FILIPINO_LABELS["REJECTED"],
            message="RF delivery guarantee rejected. Susubukang ipadala, walang kasiguraduhan.",
            sigma=sigma_value,
            epsilon=epsilon_value,
            omega_law=0,
        )

    if firmware_implementation_claim:
        return LiteResult(
            verdict="REVIEW_REQUIRED",
            status_tag="UNVERIFIED",
            filipino_label=FILIPINO_LABELS["UNVERIFIED"],
            message="Firmware claim needs device logs, relay logs, and interoperability tests.",
            sigma=sigma_value,
            epsilon=epsilon_value,
            omega_law=omega_law,
        )

    if omega_law == 0:
        return LiteResult(
            verdict="HALT_CONSTITUTIONAL",
            status_tag=status_tag,
            filipino_label=FILIPINO_LABELS["HALT_CONSTITUTIONAL"],
            message="Lumabag sa batas ng sistema. Ayusin muna bago ipagpatuloy.",
            sigma=sigma_value,
            epsilon=epsilon_value,
            omega_law=0,
        )

    return LiteResult(
        verdict=verdict,
        status_tag=status_tag,
        filipino_label=FILIPINO_LABELS.get(verdict, FILIPINO_LABELS.get(status_tag, "May babala")),
        message="Pumasa sa lite check. May puwang pa rin ng hindi tiyak.",
        sigma=sigma_value,
        epsilon=epsilon_value,
        omega_law=omega_law,
    )


def simplify_terms(text: str) -> str:
    replacements = {
        "Truth Gap": "May puwang ng hindi tiyak",
        "Deepworlds metadata only": "Karagdagang konteksto, hindi batas",
        "best-effort routing": "susubukang ipadala, walang kasiguraduhan",
        "HALT_USER_VETO": "Pasyang Tao: Itigil",
        "UNVERIFIED": "Hindi pa napatunayan",
        "PARTIAL": "Bahagyang gawa pa lang",
        "PLACEHOLDER": "Pangalan pa lang, wala pang tunay na gawa",
        "REJECTED": "Tinanggihan dahil mali o sobra ang claim",
    }

    simplified = text
    for old, new in replacements.items():
        simplified = simplified.replace(old, new)
    return simplified


def split_sms(text: str, max_len: int = 160) -> List[str]:
    if max_len < 40:
        raise ValueError("max_len too small for safe splitting")

    words = text.split()
    chunks: List[str] = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = word[:max_len]

    if current:
        chunks.append(current)

    return chunks


def offline_queue_notice(count: int = 1) -> str:
    return (
        f"Naka-save sa device ang {count} mensahe. "
        "Ipapadala kapag may signal. Walang kasiguraduhan sa oras ng dating."
    )


__all__ = [
    "SIGMA_MAX",
    "EPSILON_MIN",
    "VALID_STATUS_TAGS",
    "FILIPINO_LABELS",
    "LiteResult",
    "validate_status_tag",
    "validate_truth_gap",
    "lite_evaluate",
    "simplify_terms",
    "split_sms",
    "offline_queue_notice",
]
