#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report generation system based on database usage cases.
Generates various reports for different user roles.
"""

from flask import Blueprint, request, jsonify, render_template
from functools import wraps
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json
import csv
import io

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

from web_interface.auth import require_role


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@reports_bp.route('/student-progress/<student_id>')
@require_role('admin', 'professor', 'student')
def student_progress_report(student_id):
    """Generate student progress report."""
    conn = get_db_connection()
    
    # Get student info
    student = conn.execute('''
        SELECT * FROM users WHERE id = ? AND role = 'student'
    ''', (student_id,)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
    
    # Get progress summary
    progress = conn.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'not_started' THEN 1 ELSE 0 END) as not_started,
            AVG(time_spent_minutes) as avg_time,
            SUM(time_spent_minutes) as total_time
        FROM algorithm_progress
        WHERE student_id = ?
    ''', (student_id,)).fetchone()
    
    # Get progress by category
    by_category = conn.execute('''
        SELECT 
            a.category,
            COUNT(*) as total,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id AND ap.student_id = ?
        GROUP BY a.category
        ORDER BY a.category
    ''', (student_id,)).fetchall()
    
    # Get test scores
    test_scores = conn.execute('''
        SELECT 
            a.name,
            AVG(tr.test_score) as avg_score,
            COUNT(tr.id) as test_count
        FROM test_results tr
        JOIN algorithms a ON tr.algorithm_id = a.id
        WHERE tr.student_id = ?
        GROUP BY a.id
        ORDER BY avg_score DESC
        LIMIT 20
    ''', (student_id,)).fetchall()
    
    # Get recent activity
    recent = conn.execute('''
        SELECT a.name, ap.status, ap.last_accessed
        FROM algorithm_progress ap
        JOIN algorithms a ON ap.algorithm_id = a.id
        WHERE ap.student_id = ?
        ORDER BY ap.last_accessed DESC
        LIMIT 10
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'student': dict(student),
        'progress': dict(progress),
        'by_category': [dict(row) for row in by_category],
        'test_scores': [dict(row) for row in test_scores],
        'recent_activity': [dict(row) for row in recent]
    })


@reports_bp.route('/class-performance')
@require_role('admin', 'professor')
def class_performance_report():
    """Generate class performance report."""
    conn = get_db_connection()
    
    # Overall statistics
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT u.id) as total_students,
            COUNT(DISTINCT ap.algorithm_id) as algorithms_attempted,
            AVG(ap.time_spent_minutes) as avg_time_per_algorithm,
            AVG(tr.test_score) as avg_test_score
        FROM users u
        LEFT JOIN algorithm_progress ap ON u.id = ap.student_id
        LEFT JOIN test_results tr ON u.id = tr.student_id
        WHERE u.role = 'student'
    ''').fetchone()
    
    # Progress by algorithm
    algorithm_progress = conn.execute('''
        SELECT 
            a.name,
            a.category,
            COUNT(DISTINCT ap.student_id) as students_attempted,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completions,
            AVG(ap.time_spent_minutes) as avg_time,
            AVG(tr.test_score) as avg_score
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id
        LEFT JOIN test_results tr ON a.id = tr.algorithm_id
        GROUP BY a.id
        HAVING students_attempted > 0
        ORDER BY completions DESC
        LIMIT 50
    ''').fetchall()
    
    # Difficulty analysis
    difficulty = conn.execute('''
        SELECT 
            a.name,
            AVG(ap.attempts) as avg_attempts,
            AVG(ap.time_spent_minutes) as avg_time,
            AVG(tr.test_score) as avg_score,
            COUNT(CASE WHEN ap.status = 'completed' THEN 1 END) * 100.0 / COUNT(*) as completion_rate
        FROM algorithms a
        JOIN algorithm_progress ap ON a.id = ap.algorithm_id
        LEFT JOIN test_results tr ON a.id = tr.algorithm_id
        GROUP BY a.id
        HAVING COUNT(ap.id) > 5
        ORDER BY avg_attempts DESC
        LIMIT 20
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'statistics': dict(stats),
        'algorithm_progress': [dict(row) for row in algorithm_progress],
        'difficult_algorithms': [dict(row) for row in difficulty]
    })


@reports_bp.route('/algorithm-performance')
@require_role('admin', 'professor')
def algorithm_performance_report():
    """Generate algorithm performance benchmark report."""
    conn = get_db_connection()
    
    # Performance metrics
    performance = conn.execute('''
        SELECT 
            a.name,
            a.category,
            pm.input_size,
            AVG(pm.execution_time_ms) as avg_time,
            AVG(pm.memory_usage_mb) as avg_memory,
            AVG(pm.operations_per_sec) as avg_ops,
            pm.language,
            COUNT(*) as test_count
        FROM performance_metrics pm
        JOIN algorithms a ON pm.algorithm_id = a.id
        GROUP BY a.id, pm.input_size, pm.language
        ORDER BY a.name, pm.input_size
    ''').fetchall()
    
    # Comparison by language
    language_comparison = conn.execute('''
        SELECT 
            a.name,
            pm.language,
            AVG(pm.execution_time_ms) as avg_time,
            AVG(pm.memory_usage_mb) as avg_memory
        FROM performance_metrics pm
        JOIN algorithms a ON pm.algorithm_id = a.id
        WHERE pm.input_size = 1000
        GROUP BY a.id, pm.language
        ORDER BY a.name, pm.language
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'performance_metrics': [dict(row) for row in performance],
        'language_comparison': [dict(row) for row in language_comparison]
    })


@reports_bp.route('/content-quality')
@require_role('admin', 'professor')
def content_quality_report():
    """Generate content quality report."""
    conn = get_db_connection()
    
    # Algorithms without tests
    no_tests = conn.execute('''
        SELECT a.name, a.category, a.semester_number
        FROM algorithms a
        LEFT JOIN test_files tf ON a.id = tf.algorithm_id
        WHERE tf.id IS NULL
        ORDER BY a.semester_number, a.category
    ''').fetchall()
    
    # Algorithms without framework examples
    no_frameworks = conn.execute('''
        SELECT a.name, a.category
        FROM algorithms a
        LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id
        WHERE fw.id IS NULL
        ORDER BY a.category
    ''').fetchall()
    
    # Algorithms with incomplete files
    incomplete = conn.execute('''
        SELECT 
            a.name,
            COUNT(DISTINCT CASE WHEN af.file_type = 'python' THEN af.id END) as has_python,
            COUNT(DISTINCT CASE WHEN af.file_type = 'java' THEN af.id END) as has_java,
            COUNT(DISTINCT CASE WHEN af.file_type = 'readme' THEN af.id END) as has_readme
        FROM algorithms a
        LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
        GROUP BY a.id
        HAVING has_python = 0 OR has_java = 0 OR has_readme = 0
        ORDER BY a.name
    ''').fetchall()
    
    # Overall statistics
    stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT a.id) as total_algorithms,
            COUNT(DISTINCT tf.id) as total_tests,
            COUNT(DISTINCT fw.id) as total_frameworks,
            COUNT(DISTINCT af.id) FILTER (WHERE af.file_type = 'python') as python_files,
            COUNT(DISTINCT af.id) FILTER (WHERE af.file_type = 'java') as java_files
        FROM algorithms a
        LEFT JOIN test_files tf ON a.id = tf.algorithm_id
        LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id
        LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
    ''').fetchone()
    
    conn.close()
    
    return jsonify({
        'statistics': dict(stats),
        'algorithms_without_tests': [dict(row) for row in no_tests],
        'algorithms_without_frameworks': [dict(row) for row in no_frameworks],
        'incomplete_algorithms': [dict(row) for row in incomplete]
    })


@reports_bp.route('/usage-statistics')
@require_role('admin', 'professor')
def usage_statistics_report():
    """Generate usage statistics report."""
    conn = get_db_connection()
    
    # Algorithm popularity
    popularity = conn.execute('''
        SELECT 
            a.name,
            COUNT(DISTINCT ap.student_id) as student_count,
            COUNT(ap.id) as total_attempts,
            AVG(ap.time_spent_minutes) as avg_time
        FROM algorithms a
        JOIN algorithm_progress ap ON a.id = ap.algorithm_id
        GROUP BY a.id
        ORDER BY student_count DESC
        LIMIT 30
    ''').fetchall()
    
    # Activity over time
    activity = conn.execute('''
        SELECT 
            DATE(ap.last_accessed) as date,
            COUNT(DISTINCT ap.student_id) as active_students,
            COUNT(ap.id) as total_activities
        FROM algorithm_progress ap
        WHERE ap.last_accessed >= DATE('now', '-30 days')
        GROUP BY DATE(ap.last_accessed)
        ORDER BY date DESC
    ''').fetchall()
    
    # Category usage
    category_usage = conn.execute('''
        SELECT 
            a.category,
            COUNT(DISTINCT ap.student_id) as students,
            COUNT(ap.id) as attempts,
            AVG(ap.time_spent_minutes) as avg_time
        FROM algorithms a
        JOIN algorithm_progress ap ON a.id = ap.algorithm_id
        GROUP BY a.category
        ORDER BY students DESC
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'popular_algorithms': [dict(row) for row in popularity],
        'activity_over_time': [dict(row) for row in activity],
        'category_usage': [dict(row) for row in category_usage]
    })


@reports_bp.route('/export/<report_type>')
@require_role('admin', 'professor')
def export_report(report_type):
    """Export report as CSV."""
    # Get report data based on type
    if report_type == 'student-progress':
        data = student_progress_report(request.args.get('student_id'))
        # Convert to CSV format
        # ... implementation
        pass
    
    # Return CSV file
    output = io.StringIO()
    writer = csv.writer(output)
    # Write CSV data
    # ...
    
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename={report_type}.csv'
    }

