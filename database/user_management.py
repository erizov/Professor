#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User management utilities for authentication and roles.
"""

from pathlib import Path
from typing import Dict, List, Optional
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def get_connection() -> sqlite3.Connection:
    """Get SQLite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_user(
    username: str, password: str, role: str, email: Optional[str] = None
) -> bool:
    """Create a new user."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, email, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                generate_password_hash(password),
                email,
                role,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user credentials."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return dict(user)
    return None


def get_all_users() -> List[Dict]:
    """Return all users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, username, email, role, created_at, last_login
        FROM users
        ORDER BY created_at DESC
        """
    )
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


def update_user_role(user_id: int, role: str) -> bool:
    """Update a user's role."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_user(user_id: int) -> bool:
    """Delete a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def record_login(user_id: int) -> None:
    """Update last_login timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        (datetime.now().isoformat(), user_id),
    )
    conn.commit()
    conn.close()
