import pytest

from scripts.seil_boundary_engine_v1_3 import SEILBoundaryEngine


def test_rehabilitation_stays_below_one():
    engine = SEILBoundaryEngine()
    out = engine.rehabilitate("test", 0.01)

    assert out["status"] == "CODE_NEEDS_TEST"
    assert out["routing"] == "LOCAL_DRY_RUN_ONLY"
    assert out["deployment_gate"] == "CLOSED"
    assert 0.0 <= out["confidence"] < 1.0
    assert out["payload"].startswith("0xGOLD_")
    assert out["network_persistence"] == "BLOCKED"
    assert out["wal_commit"] == "BLOCKED"
    assert out["runtime_sealed_claim"] == "NONE"


def test_confidence_one_rejected():
    engine = SEILBoundaryEngine()

    with pytest.raises(ValueError):
        engine.rehabilitate("bad", 1.0)


def test_negative_confidence_rejected():
    engine = SEILBoundaryEngine()

    with pytest.raises(ValueError):
        engine.rehabilitate("bad", -0.01)
