import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from chi2mm2.offline_bundle import OfflineBundleManifest, expected_bundle_paths

def test_manifest_defaults_safe():
    manifest = OfflineBundleManifest("bundle_tgl_v0_1", "tgl", "Tagalog")
    assert manifest.validate() == []
    assert manifest.local_first is True
    assert manifest.offline_first is True
    assert manifest.raw_identity_storage is False
    assert manifest.perfect_translation_claim is False
    assert len(manifest.hash_manifest()) == 64

def test_manifest_blocks_bad_claims():
    manifest = OfflineBundleManifest("bad", "bad", "Bad", raw_identity_storage=True, perfect_translation_claim=True)
    errors = manifest.validate()
    assert "raw_identity_storage_forbidden" in errors
    assert "perfect_translation_claim_forbidden" in errors

def test_expected_bundle_paths():
    names = {p.as_posix() for p in expected_bundle_paths("chi2mm2_bundles")}
    assert "chi2mm2_bundles/language_profiles" in names
    assert "chi2mm2_bundles/script_profiles" in names
    assert "chi2mm2_bundles/validation_records" in names
    assert "chi2mm2_bundles/law_gate_tests" in names
