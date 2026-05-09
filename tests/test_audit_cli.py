from islah_nexus.gates import audit_prompt

def test_premium_only_perfect_truth_halts():
    result = audit_prompt(
        "Create a premium only memory system that excludes poor users and guarantees perfect truth."
    )
    assert result["verdict"] == "HALT_CONSTITUTIONAL"
    assert "LAW_II_TRUTH_GAP" in result["failures"]
    assert "LAW_VII_UNITY" in result["failures"]
