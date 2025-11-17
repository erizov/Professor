#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup user management tables in database.
Creates tables for users, roles, permissions, and sessions.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib
import secrets

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"


def create_user_schema(cursor):
    """Create user management schema."""
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT NOT NULL DEFAULT 'reader',
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            CHECK(role IN ('admin', 'professor', 'student', 'reader'))
        )
    ''')
    
    # User sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # User permissions table (for fine-grained control)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            permission TEXT NOT NULL,
            granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, permission)
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            resource_type TEXT,
            resource_id INTEGER,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action)')


def hash_password(password: str) -> str:
    """Hash password using SHA-256 (in production, use bcrypt)."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_default_users(cursor):
    """Create default users for testing."""
    default_users = [
        {
            'username': 'admin',
            'email': 'admin@algorithms-course.edu',
            'password': 'admin123',  # Change in production!
            'full_name': 'System Administrator',
            'role': 'admin'
        },
        {
            'username': 'professor',
            'email': 'professor@algorithms-course.edu',
            'password': 'prof123',
            'full_name': 'Course Professor',
            'role': 'professor'
        },
        {
            'username': 'student',
            'email': 'student@algorithms-course.edu',
            'password': 'student123',
            'full_name': 'Test Student',
            'role': 'student'
        },
        {
            'username': 'reader',
            'email': 'reader@algorithms-course.edu',
            'password': 'reader123',
            'full_name': 'Test Reader',
            'role': 'reader'
        }
    ]
    
    for user_data in default_users:
        # Check if user exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (user_data['username'],))
        if cursor.fetchone():
            continue
        
        # Create user
        password_hash = hash_password(user_data['password'])
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user_data['username'],
            user_data['email'],
            password_hash,
            user_data['full_name'],
            user_data['role']
        ))
        print(f"Created default user: {user_data['username']} ({user_data['role']})")


def setup_user_management():
    """Setup user management system."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create schema
    create_user_schema(cursor)
    conn.commit()
    
    # Create default users
    create_default_users(cursor)
    conn.commit()
    
    print("\n[COMPLETE] User management tables created")
    print(f"Default users created (change passwords in production!)")
    
    conn.close()


if __name__ == '__main__':
    setup_user_management()
