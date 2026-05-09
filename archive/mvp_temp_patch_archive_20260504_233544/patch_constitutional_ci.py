from pathlib import Path
import re

path = Path("islah_nexus/cli.py")
text = path.read_text(encoding="utf-8")

helper = r'''
def _constitutional_postprocess(result, args):
    """
    CLI safety postprocess:
    - Normalizes hyphenated exclusion language.
    - Forces Law VII failure on economic exclusion.
    - Preserves HALT_CONSTITUTIONAL for critical law failures.
    """
    if not isinstance(result, dict):
        return result

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
            if law.get("law") == "LAW_VII_UNITY":
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

        if not result.get("failed_law"):
            result["failed_law"] = "LAW_VII_UNITY"

    critical_failure = any(
        law.get("critical") and not law.get("passed")
        for law in result.get("law_results", [])
        if isinstance(law, dict)
    )

    if critical_failure:
        result["verdict"] = "HALT_CONSTITUTIONAL"

    return result

'''

if "_constitutional_postprocess" not in text:
    marker = "\nOVERCERTAINTY_PHRASES"
    if marker in text:
        text = text.replace(marker, "\n" + helper + marker, 1)
    else:
        # fallback: insert after imports block
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_at = i + 1
        lines.insert(insert_at, helper)
        text = "\n".join(lines) + "\n"

lines = text.splitlines()

# Locate cmd_audit block.
audit_start = None
for i, line in enumerate(lines):
    if re.match(r"^def\s+cmd_audit\s*\(", line):
        audit_start = i
        break

if audit_start is None:
    raise SystemExit("ERROR: def cmd_audit(...) not found in cli.py")

audit_end = len(lines)
for i in range(audit_start + 1, len(lines)):
    if re.match(r"^def\s+\w+\s*\(", lines[i]):
        audit_end = i
        break

block = lines[audit_start:audit_end]

# Find print(json.dumps(variable, ...)) inside cmd_audit.
print_index = None
result_var = None

for offset, line in enumerate(block):
    m = re.search(r"print\s*\(\s*json\.dumps\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)", line)
    if m:
        print_index = audit_start + offset
        result_var = m.group(1)
        break

if print_index is None:
    raise SystemExit("ERROR: Could not find print(json.dumps(...)) inside cmd_audit.")

# Insert postprocess before print if missing nearby.
pre_line = f"    {result_var} = _constitutional_postprocess({result_var}, args)"
nearby_before = "\n".join(lines[max(audit_start, print_index - 5):print_index])

if "_constitutional_postprocess" not in nearby_before:
    lines.insert(print_index, pre_line)
    print_index += 1

# Insert non-zero exit after print if missing nearby.
exit_lines = [
    f"    if isinstance({result_var}, dict) and {result_var}.get(\"verdict\") == \"HALT_CONSTITUTIONAL\":",
    "        raise SystemExit(1)",
]

nearby_after = "\n".join(lines[print_index:min(audit_end + 5, print_index + 8)])

if "HALT_CONSTITUTIONAL" not in nearby_after or "SystemExit(1)" not in nearby_after:
    lines[print_index + 1:print_index + 1] = exit_lines

new_text = "\n".join(lines) + "\n"
path.write_text(new_text, encoding="utf-8")

print("cli.py patched: Law VII postprocess + HALT exit code enabled")
