#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup sandbox tables in database.
Creates tables for sandboxes and sandbox versions.
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "users.db"


def create_sandbox_schema():
    """Create sandbox management schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sandboxes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sandboxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            algorithm_path TEXT NOT NULL,
            language TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, algorithm_path, language)
        )
    """)
    
    # Sandbox versions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sandbox_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sandbox_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            code_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id) ON DELETE CASCADE,
            UNIQUE(sandbox_id, version_number)
        )
    """)
    
    # Sandbox executions table (for tracking test runs)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sandbox_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sandbox_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            execution_time_ms REAL,
            memory_usage_kb REAL,
            cpu_usage_percent REAL,
            status TEXT NOT NULL,
            output TEXT,
            error_message TEXT,
            test_results TEXT,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sandboxes_user 
        ON sandboxes(user_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sandboxes_path 
        ON sandboxes(algorithm_path)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sandbox_versions_sandbox 
        ON sandbox_versions(sandbox_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sandbox_versions_number 
        ON sandbox_versions(sandbox_id, version_number)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sandbox_executions_sandbox 
        ON sandbox_executions(sandbox_id)
    """)
    
    conn.commit()
    conn.close()
    print("✓ Sandbox tables created successfully")
    print("  - sandboxes")
    print("  - sandbox_versions")
    print("  - sandbox_executions")


def verify_schema():
    """Verify that tables were created correctly."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        AND name IN ('sandboxes', 'sandbox_versions', 'sandbox_executions')
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    expected_tables = {'sandboxes', 'sandbox_versions', 'sandbox_executions'}
    if set(tables) == expected_tables:
        print("✓ All sandbox tables verified")
        return True
    else:
        missing = expected_tables - set(tables)
        print(f"⚠ Missing tables: {missing}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("SETTING UP SANDBOX DATABASE SCHEMA")
    print("=" * 70)
    print()
    
    # Check if users.db exists (required for foreign key)
    if not DB_PATH.exists():
        print(f"⚠ Warning: {DB_PATH} does not exist.")
        print("  Creating new database...")
        # Create empty database first
        conn = sqlite3.connect(DB_PATH)
        conn.close()
    
    # Check if users table exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    if not cursor.fetchone():
        print("⚠ Warning: 'users' table does not exist.")
        print("  Please run 'python database/setup_user_tables.py' first.")
        print("  Continuing anyway (foreign key will be disabled)...")
    conn.close()
    
    print()
    create_sandbox_schema()
    print()
    
    if verify_schema():
        print()
        print("=" * 70)
        print("✓ Sandbox database setup complete!")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("⚠ Setup completed with warnings")
        print("=" * 70)

