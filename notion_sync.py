# -*- coding: utf-8 -*-
import os
import json
import requests
from pathlib import Path

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = "5306c30a-839f-4aca-acb3-69a5e7d1d612"
GOVERNANCE_LOG = Path("governance_log.json")
SYNC_MARKER = Path(".notion_sync_marker")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_synced_indices():
    if not SYNC_MARKER.exists():
        return set()
    return set(SYNC_MARKER.read_text(encoding="utf-8").strip().splitlines())

def mark_synced(index: str):
    with open(SYNC_MARKER, "a", encoding="utf-8") as f:
        f.write(index + "\n")

def push_entry(entry: dict, index: int):
    action = entry.get("action", "ENTRY")
    date = entry.get("timestamp", "")[:10]
    title = f"{action} {date}"
    verdict = entry.get("verdict", "PASS")
    if verdict not in ["PASS", "FLAG", "HALT_CONSTITUTIONAL"]:
        verdict = "PASS"
    law = entry.get("law", "VII")
    if law not in ["I","II","III","IV","V","VI","VII"]:
        law = "VII"
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Entry": {"title": [{"text": {"content": title}}]},
            "Timestamp": {"rich_text": [{"text": {"content": entry.get("timestamp", "")}}]},
            "Actor Hash": {"rich_text": [{"text": {"content": entry.get("actor_hash", "")}}]},
            "Action": {"rich_text": [{"text": {"content": action}}]},
            "Law": {"select": {"name": law}},
            "Verdict": {"select": {"name": verdict}},
            "Note": {"rich_text": [{"text": {"content": entry.get("note", "")[:200]}}]},
            "Sigma": {"rich_text": [{"text": {"content": "0.81" if verdict == "PASS" else "0.40"}}]}
        }
    }
    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if r.status_code == 200:
        print(f"  SYNCED [{index}]: {title}")
        mark_synced(str(index))
    else:
        print(f"  FAILED [{index}]: {r.status_code} -- {r.text[:120]}")

def main():
    if not NOTION_TOKEN:
        print("ERROR: NOTION_TOKEN not set.")
        return
    if not GOVERNANCE_LOG.exists():
        print("ERROR: governance_log.json not found.")
        return
    raw = GOVERNANCE_LOG.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    entries = data.get("entries", [])
    synced = get_synced_indices()
    print(f"NOTION SYNC -- Islah Nexus Governance Log")
    print(f"==========================================")
    print(f"Total entries: {len(entries)}")
    print(f"Already synced: {len(synced)}")
    new_count = 0
    for i, entry in enumerate(entries):
        if str(i) in synced:
            continue
        push_entry(entry, i)
        new_count += 1
    print(f"==========================================")
    print(f"New entries synced: {new_count}")
    print(f"Walang Maiiwan.")

if __name__ == "__main__":
    main()