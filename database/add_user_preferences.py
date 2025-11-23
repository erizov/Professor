#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add user preferences columns to users table.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def add_user_preferences():
    """Add preferred_language and preferred_level columns to users table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add preferred_language column if it doesn't exist
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN preferred_language TEXT DEFAULT 'en'
        """)
        print("[OK] Added preferred_language column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("[SKIP] preferred_language column already exists")
        else:
            raise
    
    try:
        # Add preferred_level column if it doesn't exist
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN preferred_level TEXT DEFAULT 'school'
        """)
        print("[OK] Added preferred_level column")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("[SKIP] preferred_level column already exists")
        else:
            raise
    
    conn.commit()
    conn.close()
    print("\n[COMPLETE] User preferences columns added")


if __name__ == "__main__":
    add_user_preferences()

