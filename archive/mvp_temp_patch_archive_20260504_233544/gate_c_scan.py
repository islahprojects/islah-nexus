import re
from pathlib import Path

PATTERNS = [
    "AIza",
    "sk-",
    "JWT_SECRET",
    "auth_secret",
    "hardcoded_key",
    "FOUNDERS_SEED",
]

EXCLUDE = ["gate_c_scan.py", "gate_c_scan.py.bak"]

root = Path(".")
hits = []

for f in root.rglob("*.py"):
    if "__pycache__" in str(f):
        continue
    if f.name in EXCLUDE:
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    for pat in PATTERNS:
        if pat.lower() in text.lower():
            hits.append((str(f), pat))

if hits:
    for path, pat in hits:
        print("LAW_VI_WARNING:", path, "|", pat)
else:
    print("Gate C: PASSED — no hardcoded secrets found")
