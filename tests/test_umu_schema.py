import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from chi2mm2.umu import MeaningUnit

def test_umu_has_stable_id():
    a = MeaningUnit("Tagalog", "Latin", "Walang maiiwan")
    b = MeaningUnit("Tagalog", "Latin", "Walang maiiwan")
    assert a.umu_id == b.umu_id
    assert a.umu_id.startswith("umu_")

def test_umu_requires_core_fields():
    unit = MeaningUnit("", "", "")
    errors = unit.validate()
    assert "source_language_required" in errors
    assert "source_script_required" in errors
    assert "source_text_required" in errors

def test_umu_preserves_uncertainty_and_review():
    unit = MeaningUnit("Tagalog", "Latin", "loob", uncertainty_band="HIGH", community_validation="REQUIRED")
    assert unit.validate() == []
    assert unit.uncertainty_band == "HIGH"
    assert unit.community_validation == "REQUIRED"
