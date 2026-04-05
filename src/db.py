"""SQLite database layer for LLM leaderboard persistence."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data") / "leaderboard.sqlite"


def init_db() -> None:
    """Create database schema if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Source (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at TEXT NOT NULL,
            source_name TEXT NOT NULL,
            url TEXT NOT NULL,
            raw TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Source_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            extras TEXT NOT NULL,
            schema_version INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (source_id) REFERENCES Source(id)
        )
    """)
    conn.commit()
    conn.close()


def insert_source(source_name: str, url: str, raw: str) -> int:
    """Insert a raw source record. Returns the new Source.id."""
    conn = sqlite3.connect(DB_PATH)
    fetched_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor = conn.execute(
        "INSERT INTO Source (fetched_at, source_name, url, raw) VALUES (?, ?, ?, ?)",
        (fetched_at, source_name, url, raw),
    )
    conn.commit()
    source_id = cursor.lastrowid
    conn.close()
    return source_id


def insert_model_row(source_id: int, model_name: str, extras: dict, schema_version: int = 1) -> None:
    """Insert a parsed model row into Source_mapping."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO Source_mapping (source_id, model_name, extras, schema_version) VALUES (?, ?, ?, ?)",
        (source_id, model_name, json.dumps(extras), schema_version),
    )
    conn.commit()
    conn.close()


def source_exists(source_name: str) -> bool:
    """Check if a source name already exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT 1 FROM Source WHERE source_name = ? LIMIT 1", (source_name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
