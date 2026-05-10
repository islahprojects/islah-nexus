from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path

@dataclass(frozen=True)
class OfflineBundleManifest:
    bundle_id: str
    language_code: str
    language_name: str
    local_first: bool = True
    offline_first: bool = True
    raw_identity_storage: bool = False
    perfect_translation_claim: bool = False
    community_validation: str = "REQUIRED"
    files: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors = []
        if not self.bundle_id:
            errors.append("bundle_id_required")
        if not self.language_code:
            errors.append("language_code_required")
        if not self.language_name:
            errors.append("language_name_required")
        if not self.local_first:
            errors.append("local_first_required")
        if not self.offline_first:
            errors.append("offline_first_required")
        if self.raw_identity_storage:
            errors.append("raw_identity_storage_forbidden")
        if self.perfect_translation_claim:
            errors.append("perfect_translation_claim_forbidden")
        return errors

    def hash_manifest(self) -> str:
        return sha256(repr(sorted(self.__dict__.items())).encode("utf-8")).hexdigest()

def expected_bundle_paths(root: str):
    root = Path(root)
    return [
        root / "language_profiles",
        root / "script_profiles",
        root / "phonology_maps",
        root / "morphology_rules",
        root / "semantic_atoms",
        root / "cultural_notes",
        root / "validation_records",
        root / "law_gate_tests",
    ]
