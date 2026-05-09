from islah_nexus.chronos_mvp import chronos_route

def test_chronos_detects_past_shannon():
    result = chronos_route("route SHANNON into the past house")
    assert result["verdict"] == "CHRONOS_ROUTE_READY"
    assert result["autonomous_execution"] is False
    assert any(hit["house"] == "PAST" for hit in result["hits"])

def test_chronos_detects_present_ghost():
    result = chronos_route("check GHOST and WAL present state")
    assert result["verdict"] == "CHRONOS_ROUTE_READY"
    routes = [hit["route"] for hit in result["hits"]]
    assert "present_ghost_bridge" in routes
    assert "present_wal_trace" in routes

def test_chronos_detects_future_deploy():
    result = chronos_route("future DEPLOY path")
    assert result["verdict"] == "CHRONOS_ROUTE_READY"
    assert any(hit["house"] == "FUTURE" for hit in result["hits"])
    assert "not future certainty" in result["truth_gap"]

def test_chronos_void_unknown():
    result = chronos_route("banana nebula no time key")
    assert result["verdict"] == "CHRONOS_VOID"
    assert result["signal_state"] == "void"