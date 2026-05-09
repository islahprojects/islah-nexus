import hashlib
import json
from pathlib import Path

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def make_entry(index, content, previous_hash):
    entry = {
        "index": index,
        "content": content,
        "previous_hash": previous_hash,
    }
    entry["hash"] = sha256(json.dumps(entry, sort_keys=True))
    return entry

def verify_chain(ledger):
    for i, entry in enumerate(ledger):
        expected = sha256(json.dumps(
            {k: v for k, v in entry.items() if k != "hash"},
            sort_keys=True
        ))
        if entry["hash"] != expected:
            return False, f"TAMPER DETECTED at index {i}"
        if i > 0 and entry["previous_hash"] != ledger[i-1]["hash"]:
            return False, f"CHAIN BROKEN at index {i}"
    return True, "Chain intact"

# Build ledger
ledger = []
prev = "0" * 64
for i, content in enumerate([
    "Genesis — Walang Maiiwan",
    "Law II — Truth gap preserved",
    "Law VII — Unity floor active",
]):
    entry = make_entry(i, content, prev)
    ledger.append(entry)
    prev = entry["hash"]

# Verify clean chain
ok, msg = verify_chain(ledger)
print("Clean chain:", msg)

# Tamper test
ledger[1]["content"] = "TAMPERED"
ok2, msg2 = verify_chain(ledger)
print("Tamper test:", msg2)

if ok and not ok2:
    print("Gate D: PASSED — tamper detection working")
else:
    print("Gate D: FAILED")
