#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web interface for algorithm course.
Provides sorting, searching, and preview functionality.
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

app = Flask(__name__)

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/algorithms')
def get_algorithms():
    """Get algorithms with filtering and sorting."""
    conn = get_db_connection()
    
    # Get query parameters
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    semester = request.args.get('semester', '')
    sort_by = request.args.get('sort', 'name')  # name, semester, category, complexity
    sort_order = request.args.get('order', 'asc')  # asc, desc
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    # Build query
    query = '''
        SELECT 
            a.id, a.name, a.display_name, a.semester_number, a.lecture_name,
            a.category, a.time_complexity, a.space_complexity, a.description,
            a.short_description, a.folder_path,
            GROUP_CONCAT(DISTINCT fw.framework_name) as frameworks,
            COUNT(DISTINCT tf.id) as test_count,
            COUNT(DISTINCT af.id) as file_count
        FROM algorithms a
        LEFT JOIN framework_usage fw ON a.id = fw.algorithm_id
        LEFT JOIN test_files tf ON a.id = tf.algorithm_id
        LEFT JOIN algorithm_files af ON a.id = af.algorithm_id
        WHERE 1=1
    '''
    
    params = []
    
    if search:
        query += ' AND (a.name LIKE ? OR a.display_name LIKE ? OR a.description LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    if category:
        query += ' AND a.category = ?'
        params.append(category)
    
    if semester:
        query += ' AND a.semester_number = ?'
        params.append(int(semester))
    
    query += ' GROUP BY a.id'
    
    # Sorting
    valid_sorts = {'name': 'a.name', 'semester': 'a.semester_number', 
                   'category': 'a.category', 'complexity': 'a.time_complexity'}
    if sort_by in valid_sorts:
        query += f' ORDER BY {valid_sorts[sort_by]} {sort_order.upper()}'
    else:
        query += ' ORDER BY a.name ASC'
    
    # Execute query
    cursor = conn.execute(query, params)
    all_algorithms = cursor.fetchall()
    
    # Pagination
    total = len(all_algorithms)
    start = (page - 1) * per_page
    end = start + per_page
    algorithms = all_algorithms[start:end]
    
    # Convert to dict
    result = {
        'algorithms': [dict(row) for row in algorithms],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }
    
    conn.close()
    return jsonify(result)

@app.route('/api/algorithm/<int:algorithm_id>')
def get_algorithm_detail(algorithm_id):
    """Get detailed algorithm information."""
    conn = get_db_connection()
    
    # Get algorithm
    algorithm = conn.execute(
        'SELECT * FROM algorithms WHERE id = ?', (algorithm_id,)
    ).fetchone()
    
    if not algorithm:
        conn.close()
        return jsonify({'error': 'Algorithm not found'}), 404
    
    result = dict(algorithm)
    
    # Get files
    files = conn.execute(
        'SELECT * FROM algorithm_files WHERE algorithm_id = ?', (algorithm_id,)
    ).fetchall()
    result['files'] = [dict(f) for f in files]
    
    # Get test files
    tests = conn.execute(
        'SELECT * FROM test_files WHERE algorithm_id = ?', (algorithm_id,)
    ).fetchall()
    result['tests'] = [dict(t) for t in tests]
    
    # Get frameworks
    frameworks = conn.execute(
        'SELECT * FROM framework_usage WHERE algorithm_id = ?', (algorithm_id,)
    ).fetchall()
    result['frameworks'] = [dict(f) for f in frameworks]
    
    # Get advantages
    advantages = conn.execute(
        'SELECT advantage FROM algorithm_advantages WHERE algorithm_id = ?', (algorithm_id,)
    ).fetchall()
    result['advantages'] = [a['advantage'] for a in advantages]
    
    # Get shortcomings
    shortcomings = conn.execute(
        'SELECT shortcoming FROM algorithm_shortcomings WHERE algorithm_id = ?', (algorithm_id,)
    ).fetchall()
    result['shortcomings'] = [s['shortcoming'] for s in shortcomings]
    
    # Get performance metrics
    performance = conn.execute(
        'SELECT * FROM performance_metrics WHERE algorithm_id = ? ORDER BY test_date DESC LIMIT 10',
        (algorithm_id,)
    ).fetchall()
    result['performance'] = [dict(p) for p in performance]
    
    conn.close()
    return jsonify(result)

@app.route('/api/categories')
def get_categories():
    """Get all categories."""
    conn = get_db_connection()
    categories = conn.execute(
        'SELECT DISTINCT category FROM algorithms WHERE category IS NOT NULL ORDER BY category'
    ).fetchall()
    conn.close()
    return jsonify([c['category'] for c in categories])

@app.route('/api/semesters')
def get_semesters():
    """Get all semesters."""
    conn = get_db_connection()
    semesters = conn.execute(
        'SELECT DISTINCT semester_number FROM algorithms WHERE semester_number IS NOT NULL ORDER BY semester_number'
    ).fetchall()
    conn.close()
    return jsonify([s['semester_number'] for s in semesters])

@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics."""
    conn = get_db_connection()
    stats = conn.execute('SELECT * FROM algorithm_statistics').fetchone()
    conn.close()
    return jsonify(dict(stats))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
