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
ALGORITHMS_DB_PATH = ROOT / "database" / "algorithms.db"

test_reports_bp = Blueprint("test_reports", __name__)


def get_db_connection():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


def get_algorithms_db_connection():
    """Get algorithms database connection."""
    if ALGORITHMS_DB_PATH.exists():
        return sqlite3.connect(ALGORITHMS_DB_PATH)
    return None


@test_reports_bp.route("/test-reports")
def test_reports():
    """Main test reports page."""
    # Get available algorithm types for filter dropdown
    algo_conn = get_algorithms_db_connection()
    algorithm_types = ["All Types"]
    
    if algo_conn:
        cursor = algo_conn.cursor()
        cursor.execute("""
            SELECT DISTINCT algorithm_type 
            FROM algorithms 
            WHERE algorithm_type IS NOT NULL 
            ORDER BY algorithm_type
        """)
        types = [row[0] for row in cursor.fetchall()]
        algorithm_types.extend(types)
        algo_conn.close()
    
    return render_template("test_reports.html", algorithm_types=algorithm_types)


@test_reports_bp.route("/api/test-results")
def get_test_results():
    """Get test results as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()
    algo_conn = get_algorithms_db_connection()

    # Get query parameters
    search = request.args.get("search", "").lower()
    status_filter = request.args.get("status", "")
    language_filter = request.args.get("language", "")
    algorithm_type_filter = request.args.get("algorithm_type", "")
    sort_by = request.args.get("sort", "timestamp")  # timestamp, algorithm_path, status, duration
    sort_order = request.args.get("order", "desc")  # asc, desc

    # Build query - join with algorithms DB if available
    if algo_conn:
        # Join with algorithms database to get algorithm_type
        query = """
            WITH recent_results AS (
                SELECT 
                    tr.algorithm_path,
                    tr.language,
                    tr.status,
                    tr.duration,
                    tr.timestamp,
                    tr.error_message,
                    tr.previous_status,
                    tr.state_changed,
                    COALESCE(a.algorithm_type, 'unknown') as algorithm_type,
                    ROW_NUMBER() OVER (
                        PARTITION BY tr.algorithm_path, tr.language 
                        ORDER BY tr.timestamp DESC
                    ) as rn
                FROM test_results tr
                LEFT JOIN (
                    SELECT folder_path, algorithm_type 
                    FROM algorithms
                ) a ON tr.algorithm_path = a.folder_path
                WHERE 1=1
        """
    else:
        # Fallback if algorithms DB doesn't exist
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
                    'unknown' as algorithm_type,
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

    if algorithm_type_filter:
        query += " AND algorithm_type = ?"
        params.append(algorithm_type_filter)

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
                "algorithm_type": row[8] if len(row) > 8 else "unknown",
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
                "algorithm_type": latest.get("algorithm_type", "unknown"),
                "recent_results": test_results[:5],  # Max 5 results
            }
        )

    conn.close()
    if algo_conn:
        algo_conn.close()

    return jsonify({"results": results})


@test_reports_bp.route("/api/test-statistics")
def get_test_statistics():
    """Get test statistics with filter support."""
    conn = get_db_connection()
    cursor = conn.cursor()
    algo_conn = get_algorithms_db_connection()

    # Get filter parameters
    search = request.args.get("search", "").lower()
    status_filter = request.args.get("status", "")
    language_filter = request.args.get("language", "")
    algorithm_type_filter = request.args.get("algorithm_type", "")

    # Build base query with filters
    if algo_conn:
        base_query = """
            FROM test_results tr
            LEFT JOIN (
                SELECT folder_path, algorithm_type 
                FROM algorithms
            ) a ON tr.algorithm_path = a.folder_path
            WHERE 1=1
        """
    else:
        base_query = """
            FROM test_results tr
            WHERE 1=1
        """

    params = []
    filter_conditions = []

    if search:
        filter_conditions.append("tr.algorithm_path LIKE ?")
        params.append(f"%{search}%")

    if status_filter:
        filter_conditions.append("tr.status = ?")
        params.append(status_filter)

    if language_filter:
        filter_conditions.append("tr.language = ?")
        params.append(language_filter)

    if algorithm_type_filter and algo_conn:
        filter_conditions.append("COALESCE(a.algorithm_type, 'unknown') = ?")
        params.append(algorithm_type_filter)

    if filter_conditions:
        base_query += " AND " + " AND ".join(filter_conditions)

    # Get overall statistics with filters
    query = f"""
        SELECT 
            status,
            COUNT(*) as count
        FROM (
            SELECT 
                tr.algorithm_path,
                tr.language,
                tr.status,
                ROW_NUMBER() OVER (
                    PARTITION BY tr.algorithm_path, tr.language 
                    ORDER BY tr.timestamp DESC
                ) as rn
            {base_query}
        ) recent
        WHERE rn = 1
        GROUP BY status
    """

    cursor.execute(query, params)
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}

    # Get language breakdown with filters
    query = f"""
        SELECT 
            language,
            status,
            COUNT(*) as count
        FROM (
            SELECT 
                tr.algorithm_path,
                tr.language,
                tr.status,
                ROW_NUMBER() OVER (
                    PARTITION BY tr.algorithm_path, tr.language 
                    ORDER BY tr.timestamp DESC
                ) as rn
            {base_query}
        ) recent
        WHERE rn = 1
        GROUP BY language, status
    """

    cursor.execute(query, params)
    language_stats = {}
    for row in cursor.fetchall():
        lang, status, count = row
        if lang not in language_stats:
            language_stats[lang] = {}
        language_stats[lang][status] = count

    # Get state changes with filters
    state_change_params = params.copy()
    state_change_query = f"""
        SELECT COUNT(*) 
        FROM (
            SELECT DISTINCT tr.algorithm_path, tr.language
            {base_query}
            AND tr.state_changed = 1 
            AND tr.timestamp > datetime('now', '-24 hours')
        )
    """
    cursor.execute(state_change_query, state_change_params)
    recent_changes = cursor.fetchone()[0]

    conn.close()
    if algo_conn:
        algo_conn.close()

    return jsonify(
        {
            "status_counts": status_counts,
            "language_stats": language_stats,
            "recent_changes": recent_changes,
        }
    )


