from dataclasses import dataclass, field
from hashlib import sha256

@dataclass(frozen=True)
class MeaningUnit:
    source_language: str
    source_script: str
    source_text: str
    uncertainty_band: str = "MEDIUM"
    community_validation: str = "REQUIRED"
    risk_flags: list[str] = field(default_factory=list)
    law_flags: list[str] = field(default_factory=list)

    @property
    def umu_id(self) -> str:
        raw = "|".join([self.source_language, self.source_script, self.source_text])
        return "umu_" + sha256(raw.encode("utf-8")).hexdigest()[:24]

    def validate(self) -> list[str]:
        errors = []
        if not self.source_language:
            errors.append("source_language_required")
        if not self.source_script:
            errors.append("source_script_required")
        if not self.source_text:
            errors.append("source_text_required")
        if self.uncertainty_band not in {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}:
            errors.append("invalid_uncertainty_band")
        if self.community_validation not in {"REQUIRED", "PENDING", "APPROVED", "REJECTED"}:
            errors.append("invalid_community_validation")
        return errors
