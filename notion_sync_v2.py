# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: python -m pip install requests")
    sys.exit(1)


def load_env_file():
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

GOVERNANCE_LOG = Path("governance_log.json")
SYNC_MARKER = Path(".notion_sync_marker_v2")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

ALLOWED_LAWS = {"I", "II", "III", "IV", "V", "VI", "VII"}
ALLOWED_VERDICTS = {"PASS", "FLAG", "HALT_CONSTITUTIONAL"}


def normalize_law(value):
    raw = str(value or "VII")
    parts = [p.strip() for p in raw.replace("/", ",").split(",") if p.strip()]
    for part in parts:
        if part in ALLOWED_LAWS:
            return part
    return "VII"


def normalize_verdict(value):
    verdict = str(value or "PASS")
    if verdict in ALLOWED_VERDICTS:
        return verdict
    return "PASS"


def get_synced_indices():
    if not SYNC_MARKER.exists():
        return set()

    return {
        line.strip()
        for line in SYNC_MARKER.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    }


def mark_synced(index):
    with SYNC_MARKER.open("a", encoding="utf-8") as f:
        f.write(str(index) + "\n")


def load_entries():
    if not GOVERNANCE_LOG.exists():
        print("ERROR: governance_log.json not found.")
        sys.exit(1)

    data = json.loads(GOVERNANCE_LOG.read_text(encoding="utf-8-sig"))
    entries = data.get("entries", [])

    if not isinstance(entries, list):
        print("ERROR: governance_log.json entries is not a list.")
        sys.exit(1)

    return entries


def build_payload(entry, index):
    action = str(entry.get("action", "ENTRY"))
    timestamp = str(entry.get("timestamp", ""))
    actor_hash = str(entry.get("actor_hash", ""))
    law = normalize_law(entry.get("law", "VII"))
    verdict = normalize_verdict(entry.get("verdict", "PASS"))
    note = str(entry.get("note", ""))[:1800]

    title = f"{index:04d} {action}"

    return {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Entry": {"title": [{"text": {"content": title[:2000]}}]},
            "Timestamp": {"rich_text": [{"text": {"content": timestamp[:2000]}}]},
            "Actor Hash": {"rich_text": [{"text": {"content": actor_hash[:2000]}}]},
            "Action": {"rich_text": [{"text": {"content": action[:2000]}}]},
            "Law": {"select": {"name": law}},
            "Verdict": {"select": {"name": verdict}},
            "Note": {"rich_text": [{"text": {"content": note}}]},
            "Sigma": {"rich_text": [{"text": {"content": "0.81" if verdict == "PASS" else "0.40"}}]},
        },
    }


def push_entry(entry, index):
    payload = build_payload(entry, index)

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )

    if response.status_code in (200, 201):
        mark_synced(index)
        print(f"SYNCED [{index}]: {entry.get('action', 'ENTRY')}")
        return True

    print(f"FAILED [{index}]: HTTP {response.status_code}")
    print(response.text[:900])
    return False


def main():
    if not NOTION_TOKEN:
        print("ERROR: NOTION_TOKEN missing.")
        print("Set it locally or in .env. Do not paste it into chat.")
        sys.exit(1)

    if not DATABASE_ID:
        print("ERROR: NOTION_DATABASE_ID missing.")
        print("Set it locally or in .env.")
        sys.exit(1)

    entries = load_entries()
    synced = get_synced_indices()

    print("NOTION BRIDGE V2 - Islah Nexus Governance Sync")
    print("================================================")
    print(f"Entries found: {len(entries)}")
    print(f"Already synced: {len(synced)}")
    print(f"Database ID: {DATABASE_ID}")
    print("================================================")

    success = 0
    failed = 0

    for index, entry in enumerate(entries):
        if str(index) in synced:
            continue

        if push_entry(entry, index):
            success += 1
        else:
            failed += 1

    print("================================================")
    print(f"New synced: {success}")
    print(f"Failed: {failed}")

    if failed:
        print("RESULT: NOTION_SYNC_PARTIAL_OR_FAILED")
        print("401 = invalid token.")
        print("404 = valid token, but database/page is not shared with islahprojects or ID is wrong.")
        sys.exit(1)

    print("RESULT: NOTION_SYNC_PASS")
    print("Walang Maiiwan.")


if __name__ == "__main__":
    main()
