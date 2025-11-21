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
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from framework.sandbox_manager import (
    get_sandbox_path,
    save_version_code,
    load_version_code,
    get_sandbox_dir
)
import shutil

# Import require_role from auth module
try:
    from web_interface.auth import require_role
except ImportError:
    # Fallback if auth module not available
    from functools import wraps
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

sandbox_bp = Blueprint('sandbox', __name__, url_prefix='/api/sandbox')

DB_PATH = ROOT / "database" / "users.db"


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
    
    # Normalize algorithm_path: convert absolute to relative, remove filename if present
    algorithm_path_str = str(algorithm_path)
    
    # If it's an absolute path, convert to relative
    try:
        path_obj = Path(algorithm_path_str)
        if path_obj.is_absolute():
            try:
                # Try to get relative path from ROOT
                algorithm_path_str = str(path_obj.relative_to(ROOT))
            except ValueError:
                # If not relative to ROOT, try to extract just the path part
                # Remove common prefixes
                for prefix in [str(ROOT), str(ROOT).replace('\\', '/')]:
                    if algorithm_path_str.startswith(prefix):
                        algorithm_path_str = algorithm_path_str[len(prefix):].lstrip('/\\')
                        break
    except Exception:
        pass
    
    # Normalize path separators
    algorithm_path_str = algorithm_path_str.replace('\\', '/')
    
    # Remove filename if present (algorithm.py, Algorithm.java, etc.)
    if algorithm_path_str.endswith('/algorithm.py'):
        algorithm_path_str = algorithm_path_str[:-len('/algorithm.py')]
    elif algorithm_path_str.endswith('/Algorithm.java'):
        algorithm_path_str = algorithm_path_str[:-len('/Algorithm.java')]
    elif algorithm_path_str.endswith('algorithm.py'):
        algorithm_path_str = algorithm_path_str[:-len('algorithm.py')].rstrip('/')
    elif algorithm_path_str.endswith('Algorithm.java'):
        algorithm_path_str = algorithm_path_str[:-len('Algorithm.java')].rstrip('/')
    elif algorithm_path_str.endswith('.py'):
        algorithm_path_str = algorithm_path_str[:-3].rstrip('/')
    elif algorithm_path_str.endswith('.java'):
        algorithm_path_str = algorithm_path_str[:-5].rstrip('/')
    
    # Remove trailing slashes
    algorithm_path_str = algorithm_path_str.rstrip('/\\')
    
    # Normalize path separators again after filename removal
    algorithm_path_str = algorithm_path_str.replace('\\', '/')
    
    # Determine original file path - try multiple variations
    original_file = None
    paths_to_try = [algorithm_path_str]
    
    # Generate semester number variations
    import re
    semester_match = re.search(r'semester_(\d+)', algorithm_path_str)
    if semester_match:
        semester_num = semester_match.group(1)
        if len(semester_num) == 1:
            # semester_9 -> semester_09
            alt_path = algorithm_path_str.replace(f'semester_{semester_num}', f'semester_0{semester_num}')
            paths_to_try.append(alt_path)
        elif len(semester_num) == 2 and semester_num.startswith('0'):
            # semester_09 -> semester_9
            alt_path = algorithm_path_str.replace(f'semester_{semester_num}', f'semester_{semester_num[1]}')
            paths_to_try.append(alt_path)
    
    # Try each path variation
    for path_to_try in paths_to_try:
        if language == 'python':
            candidate_file = ROOT / path_to_try / "algorithm.py"
        else:
            candidate_file = ROOT / path_to_try / "Algorithm.java"
        
        if candidate_file.exists():
            original_file = candidate_file
            algorithm_path_str = path_to_try  # Use the working path
            break
    
    if not original_file:
        # Last attempt: search for the algorithm directory
        algorithm_name = algorithm_path_str.split('/')[-1] if '/' in algorithm_path_str else algorithm_path_str.split('\\')[-1]
        search_pattern = f"**/{algorithm_name}/algorithm.py" if language == 'python' else f"**/{algorithm_name}/Algorithm.java"
        
        found_files = list(ROOT.glob(search_pattern))
        if found_files:
            original_file = found_files[0]
            # Extract the relative path
            try:
                algorithm_path_str = str(original_file.parent.relative_to(ROOT))
            except ValueError:
                pass
        
        if not original_file:
            return jsonify({
                'error': f'Algorithm not found. Tried paths: {", ".join(paths_to_try)}. Searched for: {algorithm_name}'
            }), 404
    
    # Use normalized path for database
    algorithm_path = algorithm_path_str
    
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
@require_role('student', 'professor', 'admin')
def list_sandboxes():
    """List all sandboxes for current user."""
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
@require_role('student', 'professor', 'admin')
def get_sandbox(sandbox_id):
    """Get sandbox details and current code."""
    
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
@require_role('student', 'professor', 'admin')
def list_versions(sandbox_id):
    """List all versions of a sandbox."""
    
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
@require_role('student', 'professor', 'admin')
def get_version(sandbox_id, version_number):
    """Get specific version of sandbox code."""
    
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


@sandbox_bp.route('/<int:sandbox_id>/execute', methods=['POST'])
@require_role('student', 'professor', 'admin')
def execute_sandbox(sandbox_id):
    """Execute sandbox code."""
    data = request.get_json()
    use_custom_code = data.get('use_custom_code', True)
    custom_code = data.get('code')
    timeout = data.get('timeout', 30)
    input_data = data.get('input_data')
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get sandbox and code
        cursor.execute("""
            SELECT s.algorithm_path, s.language, sv.code_content
            FROM sandboxes s
            JOIN sandbox_versions sv ON s.id = sv.sandbox_id
            WHERE s.id = ? AND s.user_id = ?
            ORDER BY sv.version_number DESC
            LIMIT 1
        """, (sandbox_id, user_id))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Sandbox not found'}), 404
        
        algorithm_path, language, saved_code = result
        
        # Use custom code if provided, otherwise use saved version
        code_to_execute = custom_code if (use_custom_code and custom_code) else saved_code
        
        # Execute using existing executors
        import tempfile
        import os
        
        if language == 'python':
            from framework.python_executor import PythonExecutor, AlgorithmInfo
            
            # Create temporary file for execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code_to_execute)
                temp_file = Path(f.name)
            
            try:
                # Create AlgorithmInfo-like object
                algo_info = AlgorithmInfo(
                    name=algorithm_path,
                    path=temp_file,
                    module_name=None,
                    function_name=None,
                    class_name=None,
                    semester='',
                    lecture='',
                    algorithm='',
                    full_path=str(temp_file)
                )
                
                executor = PythonExecutor()
                success, stdout, stderr, exec_time = executor.execute_algorithm(
                    algo_info, timeout=timeout, input_data=input_data
                )
                
                return jsonify({
                    'success': success,
                    'stdout': stdout,
                    'stderr': stderr,
                    'execution_time': exec_time
                })
            finally:
                # Clean up temp file
                if temp_file.exists():
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass
                        
        elif language == 'java':
            from framework.java_executor import JavaExecutor, AlgorithmInfo
            import shutil
            
            # Extract class name from code to determine correct filename
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code_to_execute)
            class_name = class_match.group(1) if class_match else 'Algorithm'
            
            # Create temporary directory for Java file
            temp_dir = Path(tempfile.mkdtemp())
            temp_java_file = temp_dir / f"{class_name}.java"
            
            try:
                # Write code to file with correct name
                temp_java_file.write_text(code_to_execute, encoding='utf-8')
                
                # Extract package
                package_match = re.search(r'^\s*package\s+([^;]+);', code_to_execute, re.MULTILINE)
                package = package_match.group(1) if package_match else None
                
                # Create AlgorithmInfo-like object
                algo_info = AlgorithmInfo(
                    name=algorithm_path,
                    path=temp_java_file,
                    package=package,
                    class_name=class_name,
                    semester='',
                    lecture='',
                    algorithm='',
                    full_path=str(temp_java_file)
                )
                
                executor = JavaExecutor()
                success, stdout, stderr, exec_time = executor.execute_algorithm(
                    algo_info, timeout=timeout, input_data=input_data
                )
                
                return jsonify({
                    'success': success,
                    'stdout': stdout,
                    'stderr': stderr,
                    'execution_time': exec_time
                })
            finally:
                # Clean up temp directory and all files
                if temp_dir.exists():
                    try:
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    except Exception:
                        pass
        else:
            return jsonify({
                'error': f'Unsupported language: {language}'
            }), 400
                    
    except Exception as e:
        import traceback
        return jsonify({
            'error': f'Execution error: {str(e)}',
            'traceback': traceback.format_exc() if __debug__ else None
        }), 500
    finally:
        conn.close()


@sandbox_bp.route('/<int:sandbox_id>', methods=['DELETE'])
@require_role('student', 'professor', 'admin')
def delete_sandbox(sandbox_id):
    """Delete a sandbox and all its versions."""
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verify ownership
        cursor.execute("""
            SELECT id, algorithm_path, language
            FROM sandboxes
            WHERE id = ? AND user_id = ?
        """, (sandbox_id, user_id))
        
        sandbox = cursor.fetchone()
        if not sandbox:
            return jsonify({'error': 'Sandbox not found or access denied'}), 404
        
        # Delete sandbox directory from file system
        try:
            sandbox_dir = get_sandbox_dir(user_id, sandbox_id)
            if sandbox_dir.exists():
                shutil.rmtree(sandbox_dir, ignore_errors=True)
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Warning: Could not delete sandbox directory: {e}")
        
        # Delete from database (CASCADE will delete versions and executions)
        cursor.execute("DELETE FROM sandboxes WHERE id = ?", (sandbox_id,))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sandbox deleted successfully'
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Error deleting sandbox: {str(e)}'}), 500
    finally:
        conn.close()

