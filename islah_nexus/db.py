import sqlite3
import datetime
from pathlib import Path

DB_PATH = Path("islah_nexus.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS governance_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                actor_hash TEXT,
                action TEXT,
                law TEXT,
                verdict TEXT,
                note TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS violations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                violation_type TEXT,
                details TEXT
            )
        """)

def append_governance(actor: str, action: str, law: str, verdict: str, note: str = ""):
    timestamp = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO governance_log (timestamp, actor_hash, action, law, verdict, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, actor, action, law, verdict, note[:200]))

def get_governance_history():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM governance_log ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]

def get_metrics_counts():
    with sqlite3.connect(DB_PATH) as conn:
        gov_count = conn.execute("SELECT COUNT(*) FROM governance_log").fetchone()[0]
        viol_count = conn.execute("SELECT COUNT(*) FROM violations_log").fetchone()[0]
        return gov_count, viol_count