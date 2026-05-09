from islah_nexus.wal import append_wal

def test_wal_append_returns_hash():
    record = append_wal("test_action", {"ok": True})
    assert "sha256" in record
    assert record["walang_maiiwan"] is True
