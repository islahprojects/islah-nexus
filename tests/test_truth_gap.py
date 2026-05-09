from islah_nexus.constitution import SIGMA_CEILING

def test_sigma_below_one():
    assert SIGMA_CEILING < 1.0
