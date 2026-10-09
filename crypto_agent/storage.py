from __future__ import annotations

import json
import os
import sqlite3
from typing import Any


class SignalStore:
    def __init__(self, db_path: str = "data/crypto_agent_signals.db"):
        self.db_path = db_path
        directory = os.path.dirname(db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payload TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save_scan(self, results: list[dict[str, Any]]) -> None:
        payload = json.dumps(results)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO scans (payload) VALUES (?)", (payload,))
            conn.commit()

    def count_scans(self) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM scans").fetchone()
            return int(row[0]) if row else 0

    def load_latest(self, limit: int = 10) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT payload FROM scans ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        results: list[dict[str, Any]] = []
        for (payload,) in rows:
            results.extend(json.loads(payload))
        return results
