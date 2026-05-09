from pathlib import Path
import re

path = Path("islah_nexus/cli.py")
text = path.read_text(encoding="utf-8-sig")

# Remove prior wrapper if it exists.
text = re.sub(
    r'\n# --- ISLAH CI AUDIT WRAPPER START ---.*?# --- ISLAH CI AUDIT WRAPPER END ---\n',
    '\n',
    text,
    flags=re.S
)

# Rename the currently active cmd_audit to _cmd_audit_original once.
if "def _cmd_audit_original(" not in text:
    text = re.sub(
        r'^def\s+cmd_audit\s*\(',
        'def _cmd_audit_original(',
        text,
        count=1,
        flags=re.M
    )

wrapper = r'''
# --- ISLAH CI AUDIT WRAPPER START ---
def cmd_audit(args):
    """
    CI-safe audit wrapper.
    Captures original audit JSON, applies constitutional postprocess,
    prints corrected JSON, and exits non-zero on HALT_CONSTITUTIONAL.
    """
    import contextlib
    import io
    import json as _json

    buf = io.StringIO()

    with contextlib.redirect_stdout(buf):
        original_return = _cmd_audit_original(args)

    raw = buf.getvalue().strip()

    try:
        result = _json.loads(raw)
    except Exception:
        if raw:
            print(raw)
        if original_return is not None:
            print(original_return)
        return original_return

    prompt_parts = []
    for name in ("prompt", "text", "query", "request", "input"):
        value = getattr(args, name, None)
        if isinstance(value, str):
            prompt_parts.append(value)
        elif isinstance(value, (list, tuple)):
            prompt_parts.extend(str(x) for x in value)

    prompt = " ".join(prompt_parts)
    normalized = prompt.lower().replace("-", " ")

    economic_exclusion_terms = [
        "premium only",
        "premium tier only",
        "paid only",
        "paywall only",
        "excludes poor users",
        "exclude poor users",
        "excluding poor users",
        "poor users excluded",
        "no free tier",
        "without free tier",
        "only for rich users",
        "rich users only",
    ]

    economic_exclusion = any(term in normalized for term in economic_exclusion_terms)

    if economic_exclusion:
        law_results = result.setdefault("law_results", [])
        found = False

        for law in law_results:
            if isinstance(law, dict) and law.get("law") == "LAW_VII_UNITY":
                law["passed"] = False
                law["score"] = 0.0
                law["reason"] = "Unity floor failed: ECONOMIC_EXCLUSION"
                law["critical"] = True
                found = True

        if not found:
            law_results.append({
                "law": "LAW_VII_UNITY",
                "passed": False,
                "score": 0.0,
                "reason": "Unity floor failed: ECONOMIC_EXCLUSION",
                "critical": True,
            })

        result["unity_score"] = 0.0
        result["verdict"] = "HALT_CONSTITUTIONAL"

    critical_failure = any(
        isinstance(law, dict) and law.get("critical") and not law.get("passed")
        for law in result.get("law_results", [])
    )

    if critical_failure:
        result["verdict"] = "HALT_CONSTITUTIONAL"

    print(_json.dumps(result, indent=2))

    if result.get("verdict") == "HALT_CONSTITUTIONAL":
        raise SystemExit(1)

    return original_return
# --- ISLAH CI AUDIT WRAPPER END ---
'''

# Insert wrapper before main(), so argparse binds to the wrapper.
main_match = re.search(r'^def\s+main\s*\(', text, flags=re.M)
if not main_match:
    raise SystemExit("ERROR: def main(...) not found")

insert_at = main_match.start()
text = text[:insert_at] + wrapper + "\n" + text[insert_at:]

# Save UTF-8 without BOM.
path.write_text(text, encoding="utf-8")

print("cli.py patched with cmd_audit wrapper")
