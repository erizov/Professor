#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User administration blueprint.
Handles user management (add, delete students) for professors and admins.
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
import sqlite3
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

user_admin_bp = Blueprint("user_admin", __name__, url_prefix="/api/user-admin")


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


def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


@user_admin_bp.route("/users", methods=["GET"])
@require_role("admin", "professor")
def list_users():
    """List all users, optionally filtered by role."""
    role_filter = request.args.get("role", "")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        if role_filter:
            cursor.execute("""
                SELECT id, username, email, full_name, role, is_active, created_at, last_login
                FROM users
                WHERE role = ?
                ORDER BY created_at DESC
            """, (role_filter,))
        else:
            cursor.execute("""
                SELECT id, username, email, full_name, role, is_active, created_at, last_login
                FROM users
                ORDER BY created_at DESC
            """)
        
        users = [dict(row) for row in cursor.fetchall()]
        return jsonify({"success": True, "users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@user_admin_bp.route("/users", methods=["POST"])
@require_role("admin", "professor")
def create_user():
    """Create a new user (student)."""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name", "")
    role = data.get("role", "student")
    
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400
    
    # Only allow creating students (or other roles if admin)
    if session.get("role") == "professor" and role != "student":
        return jsonify({"error": "Professors can only create students"}), 403
    
    if role not in ["admin", "professor", "student", "reader"]:
        return jsonify({"error": "Invalid role"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            return jsonify({"error": "Username or email already exists"}), 400
        
        # Create user
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (username, email, password_hash, full_name, role))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "user_id": user_id
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@user_admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_role("admin", "professor")
def delete_user(user_id):
    """Delete a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get user info
        cursor.execute("SELECT id, role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Professors can only delete students
        if session.get("role") == "professor" and user[1] != "student":
            return jsonify({"error": "Professors can only delete students"}), 403
        
        # Prevent self-deletion
        if user_id == session.get("user_id"):
            return jsonify({"error": "Cannot delete your own account"}), 400
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "User deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

