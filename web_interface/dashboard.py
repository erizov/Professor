#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student dashboard for progress tracking.
Flask routes for dashboard functionality.
"""

from flask import Blueprint, render_template, request, jsonify, session
from database.student_progress import StudentProgressTracker
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
def index():
    """Dashboard main page."""
    student_id = session.get('student_id', 'guest')
    return render_template('dashboard.html', student_id=student_id)


@dashboard_bp.route('/api/progress')
def get_progress():
    """Get student progress summary."""
    student_id = request.args.get('student_id', 'guest')
    tracker = StudentProgressTracker(student_id)
    summary = tracker.get_progress_summary()
    tracker.close()
    return jsonify(summary)


@dashboard_bp.route('/api/recent')
def get_recent_activity():
    """Get recent activity."""
    student_id = request.args.get('student_id', 'guest')
    limit = int(request.args.get('limit', 10))
    tracker = StudentProgressTracker(student_id)
    activity = tracker.get_recent_activity(limit)
    tracker.close()
    return jsonify(activity)


@dashboard_bp.route('/api/algorithm/<int:algorithm_id>', methods=['POST'])
def update_algorithm_progress(algorithm_id):
    """Update algorithm progress."""
    student_id = request.json.get('student_id', 'guest')
    action = request.json.get('action')  # 'start', 'complete'
    time_spent = request.json.get('time_spent_minutes', 0)
    
    tracker = StudentProgressTracker(student_id)
    
    if action == 'start':
        tracker.start_algorithm(algorithm_id)
    elif action == 'complete':
        tracker.complete_algorithm(algorithm_id, time_spent)
    
    tracker.close()
    return jsonify({'status': 'success'})


@dashboard_bp.route('/api/test_result', methods=['POST'])
def record_test_result():
    """Record test result."""
    student_id = request.json.get('student_id', 'guest')
    algorithm_id = request.json.get('algorithm_id')
    test_score = request.json.get('test_score')
    total_tests = request.json.get('total_tests')
    passed_tests = request.json.get('passed_tests')
    
    tracker = StudentProgressTracker(student_id)
    tracker.record_test_result(algorithm_id, test_score, total_tests, passed_tests)
    tracker.close()
    
    return jsonify({'status': 'success'})


@dashboard_bp.route('/api/achievements')
def get_achievements():
    """Get student achievements."""
    student_id = request.args.get('student_id', 'guest')
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM achievements
        WHERE student_id = ?
        ORDER BY earned_at DESC
    ''', (student_id,))
    
    achievements = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(achievements)


@dashboard_bp.route('/api/statistics')
def get_statistics():
    """Get detailed statistics."""
    student_id = request.args.get('student_id', 'guest')
    tracker = StudentProgressTracker(student_id)
    
    # Progress by category
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            a.category,
            COUNT(*) as total,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id AND ap.student_id = ?
        GROUP BY a.category
    ''', (student_id,))
    
    by_category = [dict(row) for row in cursor.fetchall()]
    
    # Progress by semester
    cursor.execute('''
        SELECT 
            a.semester_number,
            COUNT(*) as total,
            SUM(CASE WHEN ap.status = 'completed' THEN 1 ELSE 0 END) as completed
        FROM algorithms a
        LEFT JOIN algorithm_progress ap ON a.id = ap.algorithm_id AND ap.student_id = ?
        WHERE a.semester_number IS NOT NULL
        GROUP BY a.semester_number
        ORDER BY a.semester_number
    ''', (student_id,))
    
    by_semester = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    tracker.close()
    
    return jsonify({
        'by_category': by_category,
        'by_semester': by_semester
    })

