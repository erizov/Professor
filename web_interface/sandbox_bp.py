#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sandbox management blueprint.
Handles sandbox creation, code editing, and version management.
"""

from flask import Blueprint, request, jsonify, session
from pathlib import Path
import sqlite3
from datetime import datetime
from functools import wraps
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.sandbox_manager import (
    get_sandbox_path,
    save_version_code,
    load_version_code
)

sandbox_bp = Blueprint('sandbox', __name__, url_prefix='/api/sandbox')

DB_PATH = ROOT / "database" / "users.db"


def require_role(*allowed_roles):
    """Decorator to require specific role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Not authenticated'}), 401
            if session.get('role') not in allowed_roles:
                return jsonify({
                    'error': 'Insufficient permissions. '
                            f'Required roles: {", ".join(allowed_roles)}'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@sandbox_bp.route('/create', methods=['POST'])
@require_role('student', 'professor', 'admin')
def create_sandbox():
    """Create a new sandbox for an algorithm."""
    data = request.get_json()
    algorithm_path = data.get('algorithm_path')
    language = data.get('language', 'python')
    
    if not algorithm_path:
        return jsonify({'error': 'algorithm_path required'}), 400
    
    if language not in ['python', 'java']:
        return jsonify({'error': 'language must be python or java'}), 400
    
    user_id = session['user_id']
    
    # Determine original file path
    if language == 'python':
        original_file = ROOT / algorithm_path / "algorithm.py"
    else:
        original_file = ROOT / algorithm_path / "Algorithm.java"
    
    if not original_file.exists():
        return jsonify({
            'error': f'Algorithm not found: {original_file}'
        }), 404
    
    try:
        original_code = original_file.read_text(encoding='utf-8')
    except Exception as e:
        return jsonify({
            'error': f'Could not read original file: {str(e)}'
        }), 500
    
    # Create sandbox in database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if sandbox already exists
        cursor.execute("""
            SELECT id FROM sandboxes
            WHERE user_id = ? AND algorithm_path = ? AND language = ?
        """, (user_id, algorithm_path, language))
        
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return jsonify({
                'error': 'Sandbox already exists',
                'sandbox_id': existing[0]
            }), 409
        
        # Create new sandbox
        cursor.execute("""
            INSERT INTO sandboxes (user_id, algorithm_path, language, last_modified)
            VALUES (?, ?, ?, datetime('now'))
        """, (user_id, algorithm_path, language))
        
        sandbox_id = cursor.lastrowid
        
        # Create first version with original code
        cursor.execute("""
            INSERT INTO sandbox_versions 
            (sandbox_id, version_number, code_content, description)
            VALUES (?, 1, ?, 'Original copy')
        """, (sandbox_id, original_code))
        
        conn.commit()
        
        # Create file system structure
        save_version_code(user_id, algorithm_path, language, 1, original_code)
        
        return jsonify({
            'success': True,
            'sandbox_id': sandbox_id,
            'message': 'Sandbox created successfully'
        })
        
    except sqlite3.Error as e:
        conn.rollback()
        conn.close()
        return jsonify({
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({
            'error': f'Unexpected error: {str(e)}'
        }), 500
    finally:
        if conn:
            conn.close()


@sandbox_bp.route('/list', methods=['GET'])
def list_sandboxes():
    """List all sandboxes for current user."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                s.id,
                s.algorithm_path,
                s.language,
                s.created_at,
                s.last_modified,
                (SELECT MAX(version_number) 
                 FROM sandbox_versions 
                 WHERE sandbox_id = s.id) as latest_version
            FROM sandboxes s
            WHERE s.user_id = ? AND s.is_active = 1
            ORDER BY s.last_modified DESC
        """, (user_id,))
        
        sandboxes = []
        for row in cursor.fetchall():
            sandboxes.append({
                'id': row['id'],
                'algorithm_path': row['algorithm_path'],
                'language': row['language'],
                'created_at': row['created_at'],
                'last_modified': row['last_modified'],
                'latest_version': row['latest_version'] or 0
            })
        
        return jsonify({
            'success': True,
            'sandboxes': sandboxes,
            'count': len(sandboxes)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error listing sandboxes: {str(e)}'
        }), 500
    finally:
        conn.close()


@sandbox_bp.route('/<int:sandbox_id>', methods=['GET'])
def get_sandbox(sandbox_id):
    """Get sandbox details and current code."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get sandbox info
        cursor.execute("""
            SELECT id, algorithm_path, language, created_at, last_modified
            FROM sandboxes
            WHERE id = ? AND user_id = ?
        """, (sandbox_id, user_id))
        
        sandbox = cursor.fetchone()
        if not sandbox:
            return jsonify({'error': 'Sandbox not found'}), 404
        
        # Get all versions
        cursor.execute("""
            SELECT 
                version_number,
                code_content,
                created_at,
                description
            FROM sandbox_versions
            WHERE sandbox_id = ?
            ORDER BY version_number DESC
        """, (sandbox_id,))
        
        versions = []
        for row in cursor.fetchall():
            versions.append({
                'version_number': row['version_number'],
                'code_content': row['code_content'],
                'created_at': row['created_at'],
                'description': row['description']
            })
        
        current_version = versions[0] if versions else None
        
        return jsonify({
            'success': True,
            'sandbox': {
                'id': sandbox['id'],
                'algorithm_path': sandbox['algorithm_path'],
                'language': sandbox['language'],
                'created_at': sandbox['created_at'],
                'last_modified': sandbox['last_modified']
            },
            'current_version': current_version,
            'all_versions': versions,
            'version_count': len(versions)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error getting sandbox: {str(e)}'
        }), 500
    finally:
        conn.close()


@sandbox_bp.route('/<int:sandbox_id>/code', methods=['PUT'])
@require_role('student', 'professor', 'admin')
def save_code(sandbox_id):
    """Save code to sandbox (creates new version)."""
    data = request.get_json()
    code = data.get('code')
    description = data.get('description', 'Updated code')
    
    if not code:
        return jsonify({'error': 'code required'}), 400
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verify ownership and get sandbox info
        cursor.execute("""
            SELECT id, algorithm_path, language
            FROM sandboxes
            WHERE id = ? AND user_id = ?
        """, (sandbox_id, user_id))
        
        sandbox = cursor.fetchone()
        if not sandbox:
            return jsonify({'error': 'Sandbox not found'}), 404
        
        sandbox_id_db, algorithm_path, language = sandbox
        
        # Get next version number
        cursor.execute("""
            SELECT MAX(version_number) FROM sandbox_versions
            WHERE sandbox_id = ?
        """, (sandbox_id_db,))
        
        max_version = cursor.fetchone()[0] or 0
        next_version = max_version + 1
        
        # Create new version
        cursor.execute("""
            INSERT INTO sandbox_versions 
            (sandbox_id, version_number, code_content, description)
            VALUES (?, ?, ?, ?)
        """, (sandbox_id_db, next_version, code, description))
        
        # Update sandbox last_modified
        cursor.execute("""
            UPDATE sandboxes
            SET last_modified = datetime('now')
            WHERE id = ?
        """, (sandbox_id_db,))
        
        conn.commit()
        
        # Save to file system
        save_version_code(user_id, algorithm_path, language, next_version, code)
        
        return jsonify({
            'success': True,
            'version_number': next_version,
            'message': 'Code saved successfully'
        })
        
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        conn.rollback()
        return jsonify({
            'error': f'Unexpected error: {str(e)}'
        }), 500
    finally:
        conn.close()


@sandbox_bp.route('/<int:sandbox_id>/versions', methods=['GET'])
def list_versions(sandbox_id):
    """List all versions of a sandbox."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Verify ownership
        cursor.execute("""
            SELECT id FROM sandboxes
            WHERE id = ? AND user_id = ?
        """, (sandbox_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({'error': 'Sandbox not found'}), 404
        
        # Get all versions
        cursor.execute("""
            SELECT 
                version_number,
                created_at,
                description
            FROM sandbox_versions
            WHERE sandbox_id = ?
            ORDER BY version_number DESC
        """, (sandbox_id,))
        
        versions = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            'success': True,
            'versions': versions,
            'count': len(versions)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error listing versions: {str(e)}'
        }), 500
    finally:
        conn.close()


@sandbox_bp.route('/<int:sandbox_id>/version/<int:version_number>', methods=['GET'])
def get_version(sandbox_id, version_number):
    """Get specific version of sandbox code."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Verify ownership and get sandbox info
        cursor.execute("""
            SELECT id, algorithm_path, language
            FROM sandboxes
            WHERE id = ? AND user_id = ?
        """, (sandbox_id, user_id))
        
        sandbox = cursor.fetchone()
        if not sandbox:
            return jsonify({'error': 'Sandbox not found'}), 404
        
        # Get version
        cursor.execute("""
            SELECT 
                version_number,
                code_content,
                created_at,
                description
            FROM sandbox_versions
            WHERE sandbox_id = ? AND version_number = ?
        """, (sandbox_id, version_number))
        
        version = cursor.fetchone()
        if not version:
            return jsonify({'error': 'Version not found'}), 404
        
        return jsonify({
            'success': True,
            'version': dict(version)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error getting version: {str(e)}'
        }), 500
    finally:
        conn.close()

