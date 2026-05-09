# Islah Nexus MVP Recovery Guide

## If PowerShell says: import is not recognized

You typed Python directly into PowerShell.

Wrong:

    import json

Right:

    python -c "import json; print('ok')"

Or put `import json` inside a `.py` file.

## If Python says: SyntaxError near ```python

A Markdown code fence was pasted into a Python file.

Fix:
- Open the `.py` file.
- Delete ```python and ```.
- Save.
- Run:

    python -m py_compile file.py

## If Python says: Set-Content is invalid syntax

PowerShell wrapper text was pasted into a Python file.

Fix:
- Open the `.py` file.
- Delete lines like `Set-Content ... @'`.
- Keep only Python code.

## If Notion says 401

The token is invalid.

Likely causes:
- Wrong token.
- Stale token.
- Token from wrong/private workspace.
- Not the Installation Access Token.

Test:

    Invoke-RestMethod -Uri "https://api.notion.com/v1/users/me" -Headers $headers

## If Notion says 404

The token works, but the database/page is not shared with the integration, or the ID is wrong.

Fix:
- Open the Notion target database/page.
- Share / Add connection.
- Add `islahprojects`.

## If /metrics says governance_entries = 0

The API is reading the wrong governance log path or an old server process is running.

Fix:
- Stop port 8000.
- Restart API from project root.
- Run MVP check.

## Golden command

    powershell -ExecutionPolicy Bypass -File ".\scripts\run_mvp_check.ps1"

## Noob hand protocol

- Check shell type first.
- PowerShell commands go in PowerShell.
- Python code goes in `.py` files.
- Markdown fences do not go in `.py` files.
- Compile before claiming.
- Test before celebrating.
- Peanut butter remains.
