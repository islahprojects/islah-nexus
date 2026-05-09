from islah_nexus.fractal_core_mvp import (
    START,
    CORE,
    SHIELD,
    DEFAULT_SINGULARITY_SEED,
    extract_intent_hash,
    fractal_mix,
    route_fractal
)

def test_fractal_extract_ignite_core():
    assert extract_intent_hash("Partner ignite the core now") == (START | CORE)

def test_fractal_xor_mix():
    intent = START | CORE
    assert fractal_mix(intent, DEFAULT_SINGULARITY_SEED) == (DEFAULT_SINGULARITY_SEED ^ intent)

def test_fractal_route_ignite_core():
    result = route_fractal("Partner ignite the core now")
    assert result["verdict"] == "FRACTAL_ROUTE_READY"
    assert result["pointer"] == "ignite_core"
    assert result["autonomous_execution"] is False
    assert result["human_authority_preserved"] is True

def test_fractal_route_core_shield():
    result = route_fractal("ignite core shield")
    assert result["verdict"] == "FRACTAL_ROUTE_READY"
    assert result["pointer"] == "ignite_core_with_shield"

def test_fractal_unknown_void():
    result = route_fractal("banana nebula dance")
    assert result["verdict"] == "FRACTAL_VOID"
    assert result["signal_state"] == "void"