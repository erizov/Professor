#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify dry run results."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithm_prompts.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM algorithm_prompts")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT algorithm_name) FROM algorithm_prompts")
unique = cursor.fetchone()[0]

cursor.execute("SELECT algorithm_name FROM algorithm_prompts ORDER BY date_updated DESC LIMIT 10")
recent = [row[0] for row in cursor.fetchall()]

print(f"Total rows in database: {total}")
print(f"Unique algorithms: {unique}")
print(f"\nMost recently updated algorithms:")
for name in recent:
    print(f"  - {name}")

conn.close()

