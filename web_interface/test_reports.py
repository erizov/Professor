#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test results reporting web interface.

Provides a web page to view test results with search, sorting,
and state change highlighting.
"""

from flask import Blueprint, render_template, request, jsonify
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

test_reports_bp = Blueprint("test_reports", __name__)


def get_db_connection():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


@test_reports_bp.route("/test-reports")
def test_reports():
    """Main test reports page."""
    return render_template("test_reports.html")


@test_reports_bp.route("/api/test-results")
def get_test_results():
    """Get test results as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get query parameters
    search = request.args.get("search", "").lower()
    status_filter = request.args.get("status", "")
    language_filter = request.args.get("language", "")
    sort_by = request.args.get("sort", "timestamp")  # timestamp, algorithm_path, status, duration
    sort_order = request.args.get("order", "desc")  # asc, desc

    # Build query
    query = """
        WITH recent_results AS (
            SELECT 
                algorithm_path,
                language,
                status,
                duration,
                timestamp,
                error_message,
                previous_status,
                state_changed,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
            WHERE 1=1
    """

    params = []

    if search:
        query += " AND algorithm_path LIKE ?"
        params.append(f"%{search}%")

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)

    if language_filter:
        query += " AND language = ?"
        params.append(language_filter)

    query += """
        )
        SELECT 
            algorithm_path,
            language,
            status,
            duration,
            timestamp,
            error_message,
            previous_status,
            state_changed
        FROM recent_results
        WHERE rn <= 5
        ORDER BY 
    """

    # Validate sort column
    valid_sorts = {
        "timestamp": "timestamp",
        "algorithm_path": "algorithm_path",
        "status": "status",
        "duration": "duration",
    }
    sort_column = valid_sorts.get(sort_by, "timestamp")

    query += f" {sort_column} {sort_order.upper()}"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Group by algorithm_path:language and get up to 5 most recent
    results_by_algorithm = {}
    for row in rows:
        key = f"{row[0]}:{row[1]}"
        if key not in results_by_algorithm:
            results_by_algorithm[key] = []

        results_by_algorithm[key].append(
            {
                "algorithm_path": row[0],
                "language": row[1],
                "status": row[2],
                "duration": row[3],
                "timestamp": row[4],
                "error_message": row[5],
                "previous_status": row[6],
                "state_changed": bool(row[7]),
            }
        )

    # Convert to list format
    results = []
    for key, test_results in results_by_algorithm.items():
        # Get the most recent result
        latest = test_results[0]
        results.append(
            {
                "algorithm_path": latest["algorithm_path"],
                "language": latest["language"],
                "latest_status": latest["status"],
                "latest_timestamp": latest["timestamp"],
                "latest_duration": latest["duration"],
                "state_changed": latest["state_changed"],
                "previous_status": latest["previous_status"],
                "recent_results": test_results[:5],  # Max 5 results
            }
        )

    conn.close()

    return jsonify({"results": results})


@test_reports_bp.route("/api/test-statistics")
def get_test_statistics():
    """Get test statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get overall statistics
    cursor.execute(
        """
        SELECT 
            status,
            COUNT(*) as count
        FROM (
            SELECT 
                algorithm_path,
                language,
                status,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
        ) recent
        WHERE rn = 1
        GROUP BY status
    """
    )

    status_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Get language breakdown
    cursor.execute(
        """
        SELECT 
            language,
            status,
            COUNT(*) as count
        FROM (
            SELECT 
                algorithm_path,
                language,
                status,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
        ) recent
        WHERE rn = 1
        GROUP BY language, status
    """
    )

    language_stats = {}
    for row in cursor.fetchall():
        lang, status, count = row
        if lang not in language_stats:
            language_stats[lang] = {}
        language_stats[lang][status] = count

    # Get state changes
    cursor.execute(
        """
        SELECT COUNT(*) 
        FROM test_results 
        WHERE state_changed = 1 
        AND timestamp > datetime('now', '-24 hours')
    """
    )

    recent_changes = cursor.fetchone()[0]

    conn.close()

    return jsonify(
        {
            "status_counts": status_counts,
            "language_stats": language_stats,
            "recent_changes": recent_changes,
        }
    )


