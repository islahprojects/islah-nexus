from islah_nexus.synaptic_router import route_command

def test_route_ignite_core():
    result = route_command("Partner, ignite the core now!")
    assert result["verdict"] == "DISPATCH_READY"
    assert result["route"] == "ignite_core"
    assert result["requires_human_confirm"] is True
    assert result["autonomous_execution"] is False
    assert result["human_authority_preserved"] is True

def test_route_start_shield():
    result = route_command("Start shield")
    assert result["verdict"] == "DISPATCH_READY"
    assert result["route"] == "deploy_truth_core_shield"
    assert result["autonomous_execution"] is False

def test_unknown_intent_void():
    result = route_command("dance banana nebula")
    assert result["verdict"] == "UNKNOWN_INTENT"
    assert result["signal_state"] == "void"
    assert result["autonomous_execution"] is False
