#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student dashboard for progress tracking.
Flask routes for dashboard functionality.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)
from database.student_progress import StudentProgressTracker
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def _get_request_student_id(source: str = "args"):
    """Extract student_id from request source."""
    if source == "json":
        payload = request.get_json(silent=True) or {}
        return payload.get("student_id")
    return request.args.get("student_id")


def _resolve_student_id(source: str = "args"):
    """Resolve which student_id the current user may access."""
    if "user_id" not in session:
        return None, (jsonify({"error": "Authentication required"}), 401)
    role = session.get("role")
    if role == "student":
        student_id = session.get("student_id") or str(session.get("user_id"))
        return student_id, None
    if role in ("admin", "professor"):
        requested = _get_request_student_id(source)
        if not requested:
            return None, (
                jsonify({"error": "student_id required for instructor view"}),
                400,
            )
        return requested, None
    return None, (
        jsonify({"error": "Reader access is limited to the public overview"}),
        403,
    )


@dashboard_bp.route("/")
def index():
    """Dashboard main page."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    role = session.get("role")
    if role not in ("student", "admin", "professor"):
        return redirect(url_for("index"))
    student_id = ""
    if role == "student":
        student_id = session.get("student_id") or str(session.get("user_id"))
    return render_template(
        "dashboard.html",
        student_id=student_id,
        read_only=role != "student",
        user_role=role,
        username=session.get("full_name") or session.get("username"),
    )


@dashboard_bp.route("/api/progress")
def get_progress():
    """Get student progress summary."""
    student_id, error = _resolve_student_id("args")
    if error:
        return error
    tracker = StudentProgressTracker(str(student_id))
    summary = tracker.get_progress_summary()
    tracker.close()
    return jsonify(summary)


@dashboard_bp.route("/api/recent")
def get_recent_activity():
    """Get recent activity."""
    student_id, error = _resolve_student_id("args")
    if error:
        return error
    limit = int(request.args.get("limit", 10))
    tracker = StudentProgressTracker(str(student_id))
    activity = tracker.get_recent_activity(limit)
    tracker.close()
    return jsonify(activity)


@dashboard_bp.route("/api/algorithm/<int:algorithm_id>", methods=["POST"])
def update_algorithm_progress(algorithm_id):
    """Update algorithm progress."""
    if "user_id" not in session or session.get("role") != "student":
        return jsonify({"error": "Only students may update progress"}), 403
    action = request.json.get("action")  # 'start', 'complete'
    time_spent = request.json.get("time_spent_minutes", 0)

    student_id = session.get("student_id") or str(session.get("user_id"))
    tracker = StudentProgressTracker(student_id)

    if action == "start":
        tracker.start_algorithm(algorithm_id)
    elif action == "complete":
        tracker.complete_algorithm(algorithm_id, time_spent)

    tracker.close()
    return jsonify({"status": "success"})


@dashboard_bp.route("/api/test_result", methods=["POST"])
def record_test_result():
    """Record test result."""
    if "user_id" not in session or session.get("role") != "student":
        return jsonify({"error": "Only students may record results"}), 403
    algorithm_id = request.json.get("algorithm_id")
    test_score = request.json.get("test_score")
    total_tests = request.json.get("total_tests")
    passed_tests = request.json.get("passed_tests")

    student_id = session.get("student_id") or str(session.get("user_id"))
    tracker = StudentProgressTracker(student_id)
    tracker.record_test_result(algorithm_id, test_score, total_tests, passed_tests)
    tracker.close()

    return jsonify({"status": "success"})


@dashboard_bp.route("/api/achievements")
def get_achievements():
    """Get student achievements."""
    student_id, error = _resolve_student_id("args")
    if error:
        return error
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM achievements
        WHERE student_id = ?
        ORDER BY earned_at DESC
    """,
        (student_id,),
    )

    achievements = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(achievements)


@dashboard_bp.route("/api/statistics")
def get_statistics():
    """Get detailed statistics."""
    student_id, error = _resolve_student_id("args")
    if error:
        return error
    tracker = StudentProgressTracker(str(student_id))

    # Progress by category
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            a.category,
            COUNT(*) as total,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id AND ap.student_id = ?
        GROUP BY a.category
    """,
        (student_id,),
    )

    by_category = [dict(row) for row in cursor.fetchall()]

    # Progress by semester
    cursor.execute(
        """
        SELECT 
            a.semester_number,
            COUNT(*) as total,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id AND ap.student_id = ?
        WHERE a.semester_number IS NOT NULL
        GROUP BY a.semester_number
        ORDER BY a.semester_number
    """,
        (student_id,),
    )

    by_semester = [dict(row) for row in cursor.fetchall()]

    conn.close()
    tracker.close()

    return jsonify({"by_category": by_category, "by_semester": by_semester})
