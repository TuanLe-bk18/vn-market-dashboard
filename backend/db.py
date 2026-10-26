"""SQLite watchlist storage. DB file lives under data/ and is git-ignored."""
import json
import os
import sqlite3
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "data")
DB_PATH = os.environ.get("WATCHLIST_DB", os.path.join(DATA_DIR, "watchlist.db"))
SEED_PATH = os.path.join(DATA_DIR, "seed_watchlist.json")

SCHEMA = """
CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    thesis TEXT DEFAULT '',
    resistance TEXT DEFAULT '',
    support TEXT DEFAULT '',
    invalidate TEXT DEFAULT '',
    status TEXT DEFAULT 'watching',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL
);
"""


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    count = conn.execute("SELECT COUNT(*) FROM watchlist").fetchone()[0]
    if count == 0 and os.path.exists(SEED_PATH):
        with open(SEED_PATH) as f:
            seeds = json.load(f)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        for s in seeds:
            conn.execute(
                "INSERT INTO watchlist (code, thesis, resistance, support, invalidate, status, notes, created_at)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (s.get("code", ""), s.get("thesis", ""), s.get("resistance", ""),
                 s.get("support", ""), s.get("invalidate", ""), s.get("status", "watching"),
                 s.get("notes", ""), now),
            )
    conn.commit()
    conn.close()


def row_to_dict(r):
    return dict(r) if r else None


def list_entries():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM watchlist ORDER BY id").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def add_entry(data):
    conn = get_conn()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = conn.execute(
        "INSERT INTO watchlist (code, thesis, resistance, support, invalidate, status, notes, created_at)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (data.get("code", "").upper(), data.get("thesis", ""), data.get("resistance", ""),
         data.get("support", ""), data.get("invalidate", ""), data.get("status", "watching"),
         data.get("notes", ""), now),
    )
    entry_id = cur.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM watchlist WHERE id=?", (entry_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def delete_entry(entry_id):
    conn = get_conn()
    cur = conn.execute("DELETE FROM watchlist WHERE id=?", (entry_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted
