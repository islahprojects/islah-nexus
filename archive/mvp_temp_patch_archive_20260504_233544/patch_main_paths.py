from pathlib import Path

path = Path("islah_nexus/main.py")
text = path.read_text(encoding="utf-8-sig")

if "PROJECT_ROOT = Path(__file__).resolve().parents[1]" not in text:
    text = text.replace(
        "from pathlib import Path",
        "from pathlib import Path\n\nPROJECT_ROOT = Path(__file__).resolve().parents[1]"
    )

text = text.replace(
    'GOVERNANCE_LOG = Path("governance_log.json")',
    'GOVERNANCE_LOG = PROJECT_ROOT / "governance_log.json"'
)

text = text.replace(
    'VIOLATIONS_LOG = Path("violations.log")',
    'VIOLATIONS_LOG = PROJECT_ROOT / "violations.log"'
)

path.write_text(text, encoding="utf-8")
print("main.py path anchoring patched.")
