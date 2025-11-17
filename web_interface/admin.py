#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Admin and user management endpoints.
"""

from flask import Blueprint, request, jsonify, session
import sqlite3
from pathlib import Path

from web_interface.auth import require_role, hash_password, log_audit

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def get_connection() -> sqlite3.Connection:
    """Return database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@admin_bp.route("/users", methods=["GET"])
@require_role("admin", "professor")
def list_users():
    """Return all users."""
    conn = get_connection()
    users = conn.execute(
        """
        SELECT id, username, email, full_name, role, is_active,
               created_at, last_login
        FROM users
        ORDER BY created_at DESC
        """
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])


@admin_bp.route("/users", methods=["POST"])
@require_role("admin", "professor")
def create_user():
    """Create a new user."""
    data = request.get_json()
    required_fields = ["username", "email", "password", "role"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    role = data["role"]
    if role not in ("admin", "professor", "student", "reader"):
        return jsonify({"error": "Invalid role"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check duplicates
    cursor.execute(
        "SELECT 1 FROM users WHERE username = ? OR email = ?",
        (data["username"], data["email"]),
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 400

    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, full_name, role)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["username"],
            data["email"],
            hash_password(data["password"]),
            data.get("full_name"),
            role,
        ),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_audit(
        session.get("user_id"),
        "admin_create_user",
        "user",
        user_id,
        f"Created user {data['username']} ({role})",
        request.remote_addr,
    )

    return jsonify({"success": True, "user_id": user_id}), 201


@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@require_role("admin")
def update_user(user_id: int):
    """Update user role or status."""
    data = request.get_json()
    fields = []
    params = []

    if "role" in data:
        if data["role"] not in ("admin", "professor", "student", "reader"):
            return jsonify({"error": "Invalid role"}), 400
        fields.append("role = ?")
        params.append(data["role"])

    if "is_active" in data:
        fields.append("is_active = ?")
        params.append(int(bool(data["is_active"])))

    if "password" in data:
        fields.append("password_hash = ?")
        params.append(hash_password(data["password"]))

    if not fields:
        return jsonify({"error": "No fields to update"}), 400

    params.append(user_id)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET {', '.join(fields)}, updated_at = datetime('now') WHERE id = ?",
        params,
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    if not updated:
        return jsonify({"error": "User not found"}), 404

    log_audit(
        session.get("user_id"),
        "admin_update_user",
        "user",
        user_id,
        f"Updated user {user_id}",
        request.remote_addr,
    )

    return jsonify({"success": True})


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@require_role("admin")
def delete_user(user_id: int):
    """Delete a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    log_audit(
        session.get("user_id"),
        "admin_delete_user",
        "user",
        user_id,
        f"Deleted user {user_id}",
        request.remote_addr,
    )

    return jsonify({"success": True})

