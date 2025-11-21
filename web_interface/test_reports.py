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


def has_algorithm_type_column(conn):
    """Check if algorithms table has algorithm_type column."""
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(algorithms)")
        columns = [row[1] for row in cursor.fetchall()]
        return "algorithm_type" in columns
    except Exception:
        return False


def ensure_algorithm_type_column(conn):
    """Add algorithm_type column if it doesn't exist."""
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        if not has_algorithm_type_column(conn):
            cursor.execute(
                "ALTER TABLE algorithms ADD COLUMN algorithm_type TEXT"
            )
            conn.commit()
        return True
    except Exception:
        return False


def load_algorithm_types() -> Dict[str, str]:
    """Load mapping of algorithm_path -> algorithm_type."""
    if not ALGORITHMS_DB_PATH.exists():
        return {}

    conn = get_algorithms_db_connection()
    if not conn:
        return {}

    try:
        ensure_algorithm_type_column(conn)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT folder_path, COALESCE(algorithm_type, 'unknown')
            FROM algorithms
        """
        )
        mapping = {row[0]: row[1] for row in cursor.fetchall()}
        return mapping
    except Exception:
        return {}
    finally:
        conn.close()


@test_reports_bp.route("/test-reports")
def test_reports():
    """Main test reports page."""
    algorithm_types = ["All Types"]
    algo_conn = get_algorithms_db_connection()
    
    if algo_conn:
        try:
            ensure_algorithm_type_column(algo_conn)
            cursor = algo_conn.cursor()
            cursor.execute("""
                SELECT DISTINCT algorithm_type 
                FROM algorithms 
                WHERE algorithm_type IS NOT NULL 
                ORDER BY algorithm_type
            """)
            types = [row[0] for row in cursor.fetchall()]
            algorithm_types.extend(types)
        except Exception:
            pass
        finally:
            algo_conn.close()

    return render_template("test_reports.html", algorithm_types=algorithm_types)


@test_reports_bp.route("/api/test-results")
def get_test_results():
    """Get test results as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()
    algorithm_types = load_algorithm_types()

    # Get query parameters
    search = request.args.get("search", "").lower()
    status_filter = request.args.get("status", "")
    language_filter = request.args.get("language", "")
    algorithm_type_filter = request.args.get("algorithm_type", "")
    sort_by = request.args.get("sort", "timestamp")
    sort_order = request.args.get("order", "desc")

    # Build query - no cross-database join, we'll add algorithm_type in Python
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
        # Handle "failure" filter to include both "failure" and "error"
        if status_filter == "failure":
            query += " AND (status = ? OR status = ?)"
            params.append("failure")
            params.append("error")
        else:
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

        # Normalize path separators for lookup (Windows uses backslashes)
        algo_path = row[0].replace("\\", "/")
        algo_type = algorithm_types.get(algo_path, "unknown")

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
                "algorithm_type": algo_type,
            }
        )

    # Convert to list format
    results = []
    for key, test_results in results_by_algorithm.items():
        latest = test_results[0]
        algo_type = latest.get("algorithm_type", "unknown")

        if algorithm_type_filter and algo_type != algorithm_type_filter:
            continue

        results.append(
            {
                "algorithm_path": latest["algorithm_path"],
                "language": latest["language"],
                "latest_status": latest["status"],
                "latest_timestamp": latest["timestamp"],
                "latest_duration": latest["duration"],
                "state_changed": latest["state_changed"],
                "previous_status": latest["previous_status"],
                "algorithm_type": algo_type,
                "recent_results": test_results[:5],
            }
        )

    conn.close()

    return jsonify({"results": results})


@test_reports_bp.route("/api/test-statistics")
def get_test_statistics():
    """Get test statistics with filter support."""
    conn = get_db_connection()
    cursor = conn.cursor()
    algorithm_types = load_algorithm_types()

    # Get filter parameters
    search = request.args.get("search", "").lower()
    status_filter = request.args.get("status", "")
    language_filter = request.args.get("language", "")
    algorithm_type_filter = request.args.get("algorithm_type", "")

    # Build base query WITHOUT status filter for statistics
    # Status filter should only affect displayed results, not statistics counts
    base_query = """
        FROM test_results tr
        WHERE 1=1
    """

    params = []
    filter_conditions = []

    if search:
        filter_conditions.append("tr.algorithm_path LIKE ?")
        params.append(f"%{search}%")

    # NOTE: status_filter is NOT applied here for statistics
    # Statistics should show counts for all statuses in the filtered dataset

    if language_filter:
        filter_conditions.append("tr.language = ?")
        params.append(language_filter)

    if filter_conditions:
        base_query += " AND " + " AND ".join(filter_conditions)

    # Get overall statistics with filters (excluding status filter)
    # First get all recent results with paths for algorithm_type filtering
    query_with_paths = f"""
        SELECT 
            recent.algorithm_path,
            recent.language,
            recent.status
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
        WHERE recent.rn = 1
    """
    
    cursor.execute(query_with_paths, params)
    all_path_rows = cursor.fetchall()
    
    # Filter by algorithm_type if specified, then count by status
    status_counts = {}
    for row in all_path_rows:
        algo_path, lang, status = row
        algo_path_normalized = algo_path.replace("\\", "/")
        algo_type = algorithm_types.get(algo_path_normalized, "unknown")
        
        if algorithm_type_filter and algo_type != algorithm_type_filter:
            continue
            
        status_counts[status] = status_counts.get(status, 0) + 1

    # Get language breakdown with filters (reuse path_rows from above)
    language_stats = {}
    for row in all_path_rows:
        algo_path, lang, status = row
        algo_path_normalized = algo_path.replace("\\", "/")
        algo_type = algorithm_types.get(algo_path_normalized, "unknown")
        
        if algorithm_type_filter and algo_type != algorithm_type_filter:
            continue
            
        if lang not in language_stats:
            language_stats[lang] = {}
        language_stats[lang][status] = language_stats[lang].get(status, 0) + 1

    # Get state changes with filters (excluding status filter)
    state_change_base = base_query + " AND tr.state_changed = 1 AND tr.timestamp > datetime('now', '-24 hours')"
    state_change_query = f"""
        SELECT COUNT(DISTINCT recent.algorithm_path || ':' || recent.language)
        FROM (
            SELECT 
                tr.algorithm_path,
                tr.language,
                ROW_NUMBER() OVER (
                    PARTITION BY tr.algorithm_path, tr.language 
                    ORDER BY tr.timestamp DESC
                ) as rn
            {state_change_base}
        ) recent
        WHERE recent.rn = 1
    """
    cursor.execute(state_change_query, params)
    recent_changes = cursor.fetchone()[0] or 0

    conn.close()

    return jsonify(
        {
            "status_counts": status_counts,
            "language_stats": language_stats,
            "recent_changes": recent_changes,
        }
    )


