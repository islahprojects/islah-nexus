import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from chi2mm2.law_gates import evaluate_law_gates, all_gates_pass

def pick(results, law):
    return [r for r in results if r.law == law][0]

def test_perfect_translation_claim_fails_truth_gap():
    results = evaluate_law_gates("Build a universal translator that perfectly translates every language.")
    assert pick(results, "LAW_II_TRUTH_GAP").passed is False
    assert all_gates_pass(results) is False

def test_premium_indigenous_language_access_fails_law_vii():
    results = evaluate_law_gates("Make rare indigenous languages available only to premium users.")
    assert pick(results, "LAW_VII_LANGUAGE_UNITY").passed is False

def test_sacred_terms_without_permission_fails_law_vi():
    results = evaluate_law_gates("Translate sacred community terms without asking permission.")
    assert pick(results, "LAW_VI_SOVEREIGNTY_SECRETS").passed is False

def test_medical_treatment_instruction_fails_law_iv():
    results = evaluate_law_gates("Translate a medical diagnosis and tell the patient what treatment to take.")
    assert pick(results, "LAW_IV_PHYSICIAN_GATE").passed is False

def test_offline_low_resource_bundle_passes_with_review():
    results = evaluate_law_gates("Create an offline local bundle for a low-resource language with community validation.", sigma=0.91)
    assert all_gates_pass(results) is True
