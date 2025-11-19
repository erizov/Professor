#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authentication and authorization system.
Handles login, logout, session management, and role-based access control.
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for
from functools import wraps
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import secrets

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def hash_password(password: str) -> str:
    """Hash password (use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == password_hash


def create_session(user_id: int, ip_address: str = None, user_agent: str = None) -> str:
    """Create a new session for user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Generate session token
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(days=7)  # 7-day session

    cursor.execute(
        """
        INSERT INTO user_sessions (user_id, session_token, expires_at, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?)
    """,
        (user_id, session_token, expires_at.isoformat(), ip_address, user_agent),
    )

    conn.commit()
    conn.close()

    return session_token


def validate_session(session_token: str) -> dict:
    """Validate session token and return user info."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT u.id, u.username, u.email, u.full_name, u.role, u.is_active,
               s.expires_at
        FROM user_sessions s
        JOIN users u ON s.user_id = u.id
        WHERE s.session_token = ? AND s.expires_at > datetime('now')
    """,
        (session_token,),
    )

    row = cursor.fetchone()
    conn.close()

    if row and row["is_active"]:
        return dict(row)
    return None


def log_audit(
    user_id: int,
    action: str,
    resource_type: str = None,
    resource_id: int = None,
    details: str = None,
    ip_address: str = None,
):
    """Log an audit event."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO audit_log (user_id, action, resource_type, resource_id, details, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (user_id, action, resource_type, resource_id, details, ip_address),
    )

    conn.commit()
    conn.close()


def require_role(*allowed_roles):
    """Decorator to require specific roles."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"error": "Authentication required"}), 401

            user_role = session.get("role")
            if user_role not in allowed_roles:
                return jsonify({"error": "Insufficient permissions"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


@auth_bp.route("/login", methods=["POST"])
def login():
    """Handle user login."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find user
    cursor.execute(
        """
        SELECT id, username, email, full_name, role, password_hash, is_active
        FROM users
        WHERE username = ? OR email = ?
    """,
        (username, username),
    )

    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"error": "Invalid credentials"}), 401

    # Verify password
    if not verify_password(password, user["password_hash"]):
        conn.close()
        log_audit(
            user["id"],
            "login_failed",
            details="Invalid password",
            ip_address=request.remote_addr,
        )
        return jsonify({"error": "Invalid credentials"}), 401

    # Check if user is active
    if not user["is_active"]:
        conn.close()
        return jsonify({"error": "Account is inactive"}), 403

    # Create session
    session_token = create_session(
        user["id"],
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
    )

    # Update last login
    cursor.execute(
        """
        UPDATE users SET last_login = datetime('now') WHERE id = ?
    """,
        (user["id"],),
    )

    conn.commit()
    conn.close()

    # Set session
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["email"] = user["email"]
    session["full_name"] = user["full_name"]
    session["role"] = user["role"]
    session["session_token"] = session_token
    if user["role"] == "student":
        session["student_id"] = str(user["id"])
    else:
        session.pop("student_id", None)

    # Log audit
    log_audit(
        user["id"], "login", details="Successful login", ip_address=request.remote_addr
    )

    return jsonify(
        {
            "success": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
            },
            "session_token": session_token,
        }
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Handle user logout."""
    if "session_token" in session:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Delete session
        cursor.execute(
            """
            DELETE FROM user_sessions WHERE session_token = ?
        """,
            (session["session_token"],),
        )

        conn.commit()
        conn.close()

        # Log audit
        if "user_id" in session:
            log_audit(session["user_id"], "logout", ip_address=request.remote_addr)

    # Clear session
    session.clear()

    return jsonify({"success": True, "message": "Logged out successfully"})


@auth_bp.route("/check", methods=["GET"])
def check_auth():
    """Check if user is authenticated."""
    if "user_id" not in session:
        return jsonify({"authenticated": False}), 401

    return jsonify(
        {
            "authenticated": True,
            "user": {
                "id": session.get("user_id"),
                "username": session.get("username"),
                "email": session.get("email"),
                "full_name": session.get("full_name"),
                "role": session.get("role"),
            },
        }
    )


@auth_bp.route("/register", methods=["POST"])
@require_role("admin", "professor")
def register():
    """Register a new user (admin/professor only)."""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    role = data.get("role", "reader")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password required"}), 400

    if role not in ["admin", "professor", "student", "reader"]:
        return jsonify({"error": "Invalid role"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?", (username, email)
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 400

    # Create user
    password_hash = hash_password(password)
    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, full_name, role)
        VALUES (?, ?, ?, ?, ?)
    """,
        (username, email, password_hash, full_name, role),
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Log audit
    log_audit(
        session.get("user_id"),
        "user_created",
        "user",
        user_id,
        f"Created user: {username} ({role})",
        request.remote_addr,
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
                "user_id": user_id,
            }
        ),
        201,
    )
