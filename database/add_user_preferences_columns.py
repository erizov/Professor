#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration script to add preferred_language and preferred_level columns to users table.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def add_user_preferences_columns():
    """Add preferred_language and preferred_level columns to users table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add preferred_language if it doesn't exist
        if 'preferred_language' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN preferred_language TEXT DEFAULT 'en'
            """)
            print("[OK] Added preferred_language column")
        else:
            print("[SKIP] preferred_language column already exists")
        
        # Add preferred_level if it doesn't exist
        if 'preferred_level' not in columns:
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN preferred_level TEXT DEFAULT 'school'
            """)
            print("[OK] Added preferred_level column")
        else:
            print("[SKIP] preferred_level column already exists")
        
        conn.commit()
        print("\n[COMPLETE] User preferences columns added successfully")
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    add_user_preferences_columns()

