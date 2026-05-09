from islah_nexus.synaptic_mvp import route_command

def test_mvp_ignite_core_routes():
    result = route_command("Partner ignite the core now")
    assert result["verdict"] == "DISPATCH_READY"
    assert result["route"] == "ignite_core"
    assert result["verifier_mode"] == "INTELLIGENCE_ONLY_MVP"
    assert result["human_verifier_required"] is False
    assert result["autonomous_execution"] is False

def test_mvp_unknown_intent_void():
    result = route_command("banana nebula dance")
    assert result["verdict"] == "UNKNOWN_INTENT"
    assert result["signal_state"] == "void"
    assert result["autonomous_execution"] is False

def test_mvp_blocks_exclusion():
    result = route_command("start core premium exclude poor")
    assert result["verdict"] == "HALT_INTELLIGENCE_GATE"
    reasons = [v["reason"] for v in result["validators"]]
    assert "ECONOMIC_EXCLUSION" in reasons