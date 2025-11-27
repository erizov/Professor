#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web interface for algorithm course.
Provides sorting, searching, and preview functionality.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
import sqlite3
from pathlib import Path
import json
import markdown
import os
import sys
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "algorithms.db"

# Add project root to Python path for imports
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "your-secret-key-here"  # Change in production
CORS(app)


@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests to avoid 404 errors."""
    return '', 204  # Return No Content status

# Register blueprints
# Use relative imports when running from web_interface directory
try:
    from web_interface.dashboard import dashboard_bp
    from web_interface.auth import auth_bp
    from web_interface.reports import reports_bp
    from web_interface.admin import admin_bp
    from web_interface.test_reports import test_reports_bp
    from web_interface.java_executor_bp import java_executor_bp
    from web_interface.algorithm_executor_bp import algorithm_executor_bp
    from web_interface.sandbox_bp import sandbox_bp
    from web_interface.user_admin_bp import user_admin_bp
    from web_interface.algorithm_index_bp import algorithm_index_bp
except ImportError:
    # Fallback to relative imports when running from web_interface directory
    from dashboard import dashboard_bp
    from auth import auth_bp
    from reports import reports_bp
    from admin import admin_bp
    from test_reports import test_reports_bp
    from java_executor_bp import java_executor_bp
    from sandbox_bp import sandbox_bp
    from user_admin_bp import user_admin_bp
    from algorithm_index_bp import algorithm_index_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(test_reports_bp)
app.register_blueprint(java_executor_bp)
app.register_blueprint(algorithm_executor_bp)
app.register_blueprint(sandbox_bp)
app.register_blueprint(user_admin_bp)
app.register_blueprint(algorithm_index_bp)

# Register database query routes from load/web_query.py
try:
    # Database path resolution for algos.db
    def get_algos_db_path():
        """Find algos.db - prioritize main database in root directory."""
        # Check main database first (has more data)
        db_path = ROOT / "algos.db"
        if not db_path.exists():
            db_path = ROOT / "load" / "algos.db"
        return str(db_path)
    
    def get_algos_connection():
        """Get connection to algos.db."""
        return sqlite3.connect(get_algos_db_path())
    
    # Extract templates from web_query.py by parsing the file
    import re
    web_query_path = ROOT / "load" / "web_query.py"
    if web_query_path.exists():
        with open(web_query_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract HTML_TEMPLATE (raw string between HTML_TEMPLATE = r""" and """)
        html_match = re.search(r'HTML_TEMPLATE = r"""([\s\S]*?)"""', content)
        if html_match:
            HTML_TEMPLATE = html_match.group(1).replace('action="/"', 'action="/load"')
        else:
            raise ValueError("Could not find HTML_TEMPLATE in web_query.py")
        
        # Extract STATS_TEMPLATE
        stats_match = re.search(r'STATS_TEMPLATE = r"""([\s\S]*?)"""', content)
        if stats_match:
            STATS_TEMPLATE = stats_match.group(1)
        else:
            raise ValueError("Could not find STATS_TEMPLATE in web_query.py")
    else:
        raise FileNotFoundError(f"web_query.py not found at {web_query_path}")
    
    from flask import render_template_string
    from pathlib import Path as PathLib
    import sqlite3
    
    # Register /load route (Algorithm Descriptions Database Query)
    @app.route('/load')
    def load_query_page():
        """Algorithm Descriptions Database Query page."""
        # Get query parameters
        search = request.args.get('search', '').strip()
        language = request.args.get('language', '').strip()
        level = request.args.get('level', '').strip()
        source = request.args.get('source', '').strip()
        order_by = request.args.get('order_by', 'fetched_at').strip()
        order_dir = request.args.get('order_dir', 'DESC').strip()
        limit = request.args.get('limit', '200').strip()
        
        # Validate order_by to prevent SQL injection
        valid_columns = ['algorithm_name', 'language', 'level', 'title', 'source_site', 
                         'quality_score', 'fetched_at', 'id', 'short_description', 'long_description']
        if order_by not in valid_columns:
            order_by = 'fetched_at'
        
        # Validate order_dir
        if order_dir.upper() not in ['ASC', 'DESC']:
            order_dir = 'DESC'
        
        # Validate limit
        try:
            limit = max(1, min(1000, int(limit)))
        except ValueError:
            limit = 200
        
        # Build query
        conn = get_algos_connection()
        cursor = conn.cursor()
        
        # Build WHERE clause
        where_conditions = []
        params = []
        
        if search:
            where_conditions.append("""
                (algorithm_name LIKE ? OR title LIKE ? OR 
                 short_description LIKE ? OR long_description LIKE ?)
            """)
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])
        
        if language:
            where_conditions.append("language = ?")
            params.append(language)
        
        if level:
            where_conditions.append("level = ?")
            params.append(level)
        
        if source:
            where_conditions.append("source_site = ?")
            params.append(source)
        
        # Filter out rows with no meaningful data
        # Only show rows that have at least one non-empty description field
        # and exclude placeholder patterns
        data_condition = """(
            (short_description IS NOT NULL AND short_description != '' AND 
             short_description NOT LIKE '%[конкретн%' AND 
             short_description NOT LIKE '%[specific%' AND
             short_description NOT LIKE '%placeholder%' AND
             short_description NOT LIKE '%заполнитель%') OR
            (long_description IS NOT NULL AND long_description != '' AND 
             long_description NOT LIKE '%[конкретн%' AND 
             long_description NOT LIKE '%[specific%' AND
             long_description NOT LIKE '%placeholder%' AND
             long_description NOT LIKE '%заполнитель%') OR
            (simple_explanation IS NOT NULL AND simple_explanation != '' AND 
             simple_explanation NOT LIKE '%[конкретн%' AND 
             simple_explanation NOT LIKE '%[specific%' AND
             simple_explanation NOT LIKE '%placeholder%' AND
             simple_explanation NOT LIKE '%заполнитель%') OR
            (where_its_used IS NOT NULL AND where_its_used != '' AND 
             where_its_used NOT LIKE '%[конкретн%' AND 
             where_its_used NOT LIKE '%[specific%' AND
             where_its_used NOT LIKE '%placeholder%' AND
             where_its_used NOT LIKE '%заполнитель%') OR
            (example IS NOT NULL AND example != '' AND 
             example NOT LIKE '%[конкретн%' AND 
             example NOT LIKE '%[specific%' AND
             example NOT LIKE '%placeholder%' AND
             example NOT LIKE '%заполнитель%') OR
            (algorithm_definition IS NOT NULL AND algorithm_definition != '' AND 
             algorithm_definition NOT LIKE '%[конкретн%' AND 
             algorithm_definition NOT LIKE '%[specific%' AND
             algorithm_definition NOT LIKE '%placeholder%' AND
             algorithm_definition NOT LIKE '%заполнитель%') OR
            (technical_description IS NOT NULL AND technical_description != '' AND 
             technical_description NOT LIKE '%[конкретн%' AND 
             technical_description NOT LIKE '%[specific%' AND
             technical_description NOT LIKE '%placeholder%' AND
             technical_description NOT LIKE '%заполнитель%') OR
            (application IS NOT NULL AND application != '' AND 
             application NOT LIKE '%[конкретн%' AND 
             application NOT LIKE '%[specific%' AND
             application NOT LIKE '%placeholder%' AND
             application NOT LIKE '%заполнитель%') OR
            (step_by_step IS NOT NULL AND step_by_step != '' AND 
             step_by_step NOT LIKE '%[конкретн%' AND 
             step_by_step NOT LIKE '%[specific%' AND
             step_by_step NOT LIKE '%placeholder%' AND
             step_by_step NOT LIKE '%заполнитель%')
        )"""
        where_conditions.append(data_condition)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # Get total count
        count_query = f"SELECT COUNT(*) FROM algorithm_descriptions{where_clause}"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]
        
        # Get results with all columns for static display
        query = f"""
            SELECT id, algorithm_name, language, level, title, source_site, 
                   quality_score, fetched_at,
                   short_description, long_description,
                   simple_explanation, where_its_used, example,
                   algorithm_definition, technical_description,
                   application, step_by_step
            FROM algorithm_descriptions
            {where_clause}
            ORDER BY {order_by} {order_dir}
            LIMIT ?
        """
        params.append(limit)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        # Get column names from cursor description
        columns = [description[0] for description in cursor.description]
        # Convert rows (tuples) to dictionaries
        results = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        # Get database path for display
        db_path = PathLib(get_algos_db_path()).absolute()
        
        return render_template_string(
            HTML_TEMPLATE,
            results=results,
            total_count=total_count,
            showing_count=len(results),
            db_path=str(db_path)
        )
    
    # Register /stats route
    @app.route('/stats')
    def stats_page():
        """Database Statistics page."""
        conn = get_algos_connection()
        cursor = conn.cursor()
        
        # Get total algorithms
        cursor.execute("SELECT COUNT(DISTINCT algorithm_name) FROM algorithms")
        total_algorithms = cursor.fetchone()[0]
        
        # Get total descriptions
        cursor.execute("SELECT COUNT(*) FROM algorithm_descriptions")
        total_descriptions = cursor.fetchone()[0]
        
        # Get web vs local counts (SQLite compatible)
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN source_site != 'local_markdown' THEN 1 ELSE 0 END) as web_count,
                SUM(CASE WHEN source_site = 'local_markdown' THEN 1 ELSE 0 END) as local_count
            FROM algorithm_descriptions
        """)
        row = cursor.fetchone()
        web_descriptions = row[0] if row else 0
        local_descriptions = row[1] if row else 0
        
        # Get breakdown by source
        cursor.execute("""
            SELECT source_site, COUNT(*) 
            FROM algorithm_descriptions 
            GROUP BY source_site
            ORDER BY COUNT(*) DESC
        """)
        sources = cursor.fetchall()
        
        # Get breakdown by language
        cursor.execute("""
            SELECT language, COUNT(*) 
            FROM algorithm_descriptions 
            GROUP BY language
            ORDER BY language
        """)
        languages = cursor.fetchall()
        
        # Get breakdown by level
        cursor.execute("""
            SELECT level, COUNT(*) 
            FROM algorithm_descriptions 
            GROUP BY level
            ORDER BY level
        """)
        levels = cursor.fetchall()
        
        # Get last updated time
        cursor.execute("""
            SELECT MAX(fetched_at) 
            FROM algorithm_descriptions
        """)
        last_updated_row = cursor.fetchone()
        last_updated = str(last_updated_row[0])[:19] if last_updated_row[0] else "N/A"
        
        conn.close()
        
        db_path = PathLib(get_algos_db_path()).absolute()
        
        return render_template_string(
            STATS_TEMPLATE,
            total_algorithms=total_algorithms,
            total_descriptions=total_descriptions,
            web_descriptions=web_descriptions,
            local_descriptions=local_descriptions,
            sources=sources,
            languages=languages,
            levels=levels,
            db_path=str(db_path),
            last_updated=last_updated
        )
    
    # Register API endpoint for algorithm details
    @app.route('/api/algorithm-details/<int:desc_id>')
    def algorithm_details_api(desc_id):
        """API endpoint to get full algorithm description details."""
        conn = get_algos_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                title, short_description, long_description, simple_explanation,
                algorithm_definition, technical_description, where_its_used,
                application, step_by_step, example, discipline,
                self_check_basic, self_check_intermediate, self_check_advanced,
                practical_tasks_basic, practical_tasks_applied, practical_tasks_research,
                ethical_reasoning, example_result
            FROM algorithm_descriptions
            WHERE id = ?
        """, (desc_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Not found'}), 404
        
        # Map to dictionary
        details = {
            'title': row[0],
            'short_description': row[1],
            'long_description': row[2],
            'simple_explanation': row[3],
            'algorithm_definition': row[4],
            'technical_description': row[5],
            'where_its_used': row[6],
            'application': row[7],
            'step_by_step': row[8],
            'example': row[9],
            'discipline': row[10],
            'self_check_basic': row[11],
            'self_check_intermediate': row[12],
            'self_check_advanced': row[13],
            'practical_tasks_basic': row[14],
            'practical_tasks_applied': row[15],
            'practical_tasks_research': row[16],
            'ethical_reasoning': row[17],
            'example_result': row[18]
        }
        
        # Remove None values and return as JSON
        return jsonify({k: v for k, v in details.items() if v})
    
except ImportError as e:
    print(f"Warning: Could not import database query routes: {e}")
    print("Routes /load and /stats will not be available")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Warning: Error setting up database query routes: {e}")
    print("Routes /load and /stats will not be available")
    import traceback
    traceback.print_exc()


# Login route
@app.route("/login")
def login_page():
    """Login page."""
    return render_template("login.html")


def require_session(roles=None):
    """Ensure user logged in and optionally has allowed role."""
    if "user_id" not in session:
        return False
    if roles and session.get("role") not in roles:
        return False
    return True


@app.route("/admin")
def admin_page():
    """Admin dashboard page."""
    if not require_session(["admin", "professor"]):
        return redirect(url_for("login_page"))
    return render_template("admin_dashboard.html")


@app.route("/user-admin")
def user_admin_page():
    """User administration page."""
    if not require_session(["admin", "professor"]):
        return redirect(url_for("login_page"))
    return render_template("user_admin.html")


@app.route("/reports")
def reports_page():
    """Reports dashboard page."""
    if not require_session(["admin", "professor"]):
        return redirect(url_for("login_page"))
    return render_template("reports_dashboard.html")


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    """Main page."""
    return render_template("index.html")


@app.route("/java-executor")
def java_executor_page():
    """Java algorithm executor page."""
    return render_template("java_executor.html")


@app.route("/algorithm-executor")
def algorithm_executor_page():
    """Unified algorithm executor page (Java and Python)."""
    return render_template("algorithm_executor.html")


@app.route("/sandbox")
def sandbox_page():
    """Sandbox page for students to edit algorithms."""
    # Check authentication and role
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    user_role = session.get("role", "reader")
    # Only allow student, professor, and admin roles
    if user_role not in ("student", "professor", "admin"):
        return render_template(
            "sandbox.html",
            error_message="Access denied. Sandbox is only available for students, professors, and administrators.",
            user_role=user_role,
            read_only=True
        )
    
    return render_template(
        "sandbox.html",
        user_role=user_role,
        username=session.get("full_name") or session.get("username"),
        read_only=False
    )


@app.route("/api/algorithms")
def get_algorithms():
    """Get algorithms with filtering and sorting."""
    conn = get_db_connection()

    # Get query parameters
    search = request.args.get("search", "").strip()
    level = request.args.get("level", "").strip()  # school, univer
    language = request.args.get("language", "").strip()  # ru, en
    category = request.args.get("category", "")
    semester = request.args.get("semester", "")
    sort_by = request.args.get("sort", "name")  # name, semester, category, complexity
    sort_order = request.args.get("order", "asc")  # asc, desc
    
    # Handle limit parameter (for sandbox and other use cases that need all algorithms)
    limit_param = request.args.get("limit")
    if limit_param:
        try:
            limit = int(limit_param)
            # If limit is specified, return all algorithms up to that limit
            page = 1
            per_page = limit
        except ValueError:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 50))
    else:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))

    # Build query
    query = """
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
    """

    params = []
    
    # If level is "school", filter out advanced algorithms (semesters 9-16)
    if level == "school":
        query += " AND (a.semester_number IS NULL OR a.semester_number <= 8)"

    if search:
        query += " AND (a.name LIKE ? OR a.display_name LIKE ? OR a.description LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    if category:
        query += " AND a.category = ?"
        params.append(category)

    if semester:
        query += " AND a.semester_number = ?"
        params.append(int(semester))

    query += " GROUP BY a.id"

    # Sorting
    valid_sorts = {
        "name": "a.name",
        "semester": "a.semester_number",
        "category": "a.category",
        "complexity": "a.time_complexity",
    }
    if sort_by in valid_sorts:
        query += f" ORDER BY {valid_sorts[sort_by]} {sort_order.upper()}"
    else:
        query += " ORDER BY a.name ASC"

    # Execute query
    cursor = conn.execute(query, params)
    all_algorithms = cursor.fetchall()

    # Filter by level and language (check if MD files exist)
    # Ensure same number of algorithms are shown regardless of language choice
    if level or language:
        filtered_algorithms = []
        for algo in all_algorithms:
            folder_path = Path(ROOT / algo['folder_path']) if algo['folder_path'] else None
            
            if folder_path and folder_path.exists():
                # Check if required MD file exists
                if level and language:
                    # First, check for specific level.language.md file
                    md_file = folder_path / f"{level}.{language}.md"
                    if md_file.exists():
                        filtered_algorithms.append(algo)
                    else:
                        # If specific language file doesn't exist, check if any language file exists for this level
                        # This ensures same algorithms are shown regardless of language choice
                        ru_file = folder_path / f"{level}.ru.md"
                        en_file = folder_path / f"{level}.en.md"
                        if ru_file.exists() or en_file.exists():
                            filtered_algorithms.append(algo)
                elif level:
                    # Check if any language file exists for this level
                    # This ensures same algorithms are shown regardless of language choice
                    ru_file = folder_path / f"{level}.ru.md"
                    en_file = folder_path / f"{level}.en.md"
                    if ru_file.exists() or en_file.exists():
                        filtered_algorithms.append(algo)
                elif language:
                    # Check if any level file exists for this language
                    # This ensures same algorithms are shown regardless of level choice
                    school_file = folder_path / f"school.{language}.md"
                    univer_file = folder_path / f"univer.{language}.md"
                    if school_file.exists() or univer_file.exists():
                        filtered_algorithms.append(algo)
            else:
                # If folder doesn't exist, don't include algorithm when filtering by level/language
                pass
        
        all_algorithms = filtered_algorithms
    else:
        # If no level and no language filter, show all algorithms (but still respect school level semester filter from SQL)
        pass

    # Pagination
    total = len(all_algorithms)
    start = (page - 1) * per_page
    end = start + per_page
    algorithms = all_algorithms[start:end]

    # Convert to dict
    result = {
        "algorithms": [dict(row) for row in algorithms],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        },
    }

    conn.close()
    return jsonify(result)


@app.route("/api/algorithm/<int:algorithm_id>")
def get_algorithm_detail(algorithm_id):
    """Get detailed algorithm information."""
    conn = get_db_connection()

    # Get algorithm
    algorithm = conn.execute(
        "SELECT * FROM algorithms WHERE id = ?", (algorithm_id,)
    ).fetchone()

    if not algorithm:
        conn.close()
        return jsonify({"error": "Algorithm not found"}), 404

    result = dict(algorithm)

    # Get files
    files = conn.execute(
        "SELECT * FROM algorithm_files WHERE algorithm_id = ?", (algorithm_id,)
    ).fetchall()
    result["files"] = [dict(f) for f in files]

    # Get test files
    tests = conn.execute(
        "SELECT * FROM test_files WHERE algorithm_id = ?", (algorithm_id,)
    ).fetchall()
    result["tests"] = [dict(t) for t in tests]

    # Get frameworks
    frameworks = conn.execute(
        "SELECT * FROM framework_usage WHERE algorithm_id = ?", (algorithm_id,)
    ).fetchall()
    result["frameworks"] = [dict(f) for f in frameworks]

    # Get advantages
    advantages = conn.execute(
        "SELECT advantage FROM algorithm_advantages WHERE algorithm_id = ?",
        (algorithm_id,),
    ).fetchall()
    result["advantages"] = [a["advantage"] for a in advantages]

    # Get shortcomings
    shortcomings = conn.execute(
        "SELECT shortcoming FROM algorithm_shortcomings WHERE algorithm_id = ?",
        (algorithm_id,),
    ).fetchall()
    result["shortcomings"] = [s["shortcoming"] for s in shortcomings]

    # Get performance metrics
    performance = conn.execute(
        "SELECT * FROM performance_metrics WHERE algorithm_id = ? ORDER BY test_date DESC LIMIT 10",
        (algorithm_id,),
    ).fetchall()
    result["performance"] = [dict(p) for p in performance]

    conn.close()
    return jsonify(result)


@app.route("/api/categories")
def get_categories():
    """Get all categories."""
    conn = get_db_connection()
    categories = conn.execute(
        "SELECT DISTINCT category FROM algorithms WHERE category IS NOT NULL ORDER BY category"
    ).fetchall()
    conn.close()
    return jsonify([c["category"] for c in categories])


@app.route("/api/semesters")
def get_semesters():
    """Get all semesters."""
    conn = get_db_connection()
    semesters = conn.execute(
        "SELECT DISTINCT semester_number FROM algorithms WHERE semester_number IS NOT NULL ORDER BY semester_number"
    ).fetchall()
    conn.close()
    return jsonify([s["semester_number"] for s in semesters])


@app.route("/api/user/preferences", methods=["GET", "POST"])
def user_preferences():
    """Get or set user preferences for language and level."""
    if "user_id" not in session:
        # Return defaults if not authenticated
        if request.method == "GET":
            return jsonify({"language": "en", "level": "school"})
        return jsonify({"error": "Not authenticated"}), 401
    
    conn = get_db_connection()
    user_id = session["user_id"]
    
    if request.method == "GET":
        # Get preferences from database
        user = conn.execute(
            "SELECT preferred_language, preferred_level FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        
        if user:
            preferences = {
                "language": user["preferred_language"] or "en",
                "level": user["preferred_level"] or "school"
            }
            # Also update session
            session["preferred_language"] = preferences["language"]
            session["preferred_level"] = preferences["level"]
        else:
            preferences = {
                "language": "en",
                "level": "school"
            }
        
        conn.close()
        return jsonify(preferences)
    
    else:  # POST
        data = request.get_json()
        language = data.get("language", "en")
        level = data.get("level", "school")
        
        # Validate
        if language not in ["en", "ru"]:
            language = "en"
        if level not in ["school", "univer", "university"]:
            level = "school"
        
        # Normalize level
        if level == "university":
            level = "univer"
        
        # Update database
        conn.execute(
            """
            UPDATE users 
            SET preferred_language = ?, preferred_level = ?
            WHERE id = ?
            """,
            (language, level, user_id)
        )
        conn.commit()
        conn.close()
        
        # Update session
        session["preferred_language"] = language
        session["preferred_level"] = level
        
        # Update README.md files for the chosen language (in background)
        # This ensures all README files show links for the chosen language
        try:
            script_path = ROOT / "scripts" / "update_readme_educational_materials.py"
            if script_path.exists():
                def update_readmes():
                    try:
                        subprocess.run(
                            [sys.executable, str(script_path), language],
                            cwd=str(ROOT),
                            capture_output=True,
                            timeout=300
                        )
                    except Exception as e:
                        print(f"Error updating README files: {e}")
                
                # Run in background thread
                thread = threading.Thread(target=update_readmes, daemon=True)
                thread.start()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error starting README update thread: {e}")
        
        return jsonify({"success": True, "language": language, "level": level})


@app.route("/api/statistics")
def get_statistics():
    """Get overall statistics."""
    conn = get_db_connection()
    
    # Calculate real-time statistics
    total_algorithms = conn.execute("SELECT COUNT(*) FROM algorithms").fetchone()[0]
    total_tests = conn.execute("SELECT COUNT(*) FROM test_files").fetchone()[0]
    total_frameworks = conn.execute("SELECT COUNT(DISTINCT framework_name) FROM framework_usage").fetchone()[0]
    total_semesters = conn.execute("SELECT COUNT(DISTINCT semester_number) FROM algorithms WHERE semester_number IS NOT NULL").fetchone()[0]
    
    stats = {
        "total_algorithms": total_algorithms,
        "total_tests": total_tests,
        "total_framework_examples": total_frameworks,
        "total_semesters": total_semesters
    }
    
    conn.close()
    return jsonify(stats)


@app.route("/readme/<path:file_path>")
def serve_readme(file_path):
    """Serve README files as rendered HTML."""
    try:
        # Normalize path separators and handle semester number variations
        # Convert forward slashes to OS-specific separators
        normalized_path = file_path.replace('/', '\\' if os.name == 'nt' else '/')
        
        # Try to find the file with the given path
        readme_path = ROOT / normalized_path
        
        # If not found, try to find matching semester directory (handle semester_6 vs semester_06)
        if not readme_path.exists():
            # Extract semester number and try both formats
            parts = normalized_path.split('\\' if os.name == 'nt' else '/')
            if len(parts) > 0 and parts[0].startswith('semester_'):
                semester_part = parts[0]
                # Try with leading zero
                if not semester_part.endswith('_0') and not semester_part.endswith('_00'):
                    alt_semester = semester_part.replace('semester_', 'semester_0')
                    alt_path = '\\'.join([alt_semester] + parts[1:]) if os.name == 'nt' else '/'.join([alt_semester] + parts[1:])
                    alt_readme_path = ROOT / alt_path
                    if alt_readme_path.exists():
                        readme_path = alt_readme_path
                # Try without leading zero
                elif semester_part.endswith('_0') and not semester_part.endswith('_00'):
                    alt_semester = semester_part.replace('semester_0', 'semester_')
                    alt_path = '\\'.join([alt_semester] + parts[1:]) if os.name == 'nt' else '/'.join([alt_semester] + parts[1:])
                    alt_readme_path = ROOT / alt_path
                    if alt_readme_path.exists():
                        readme_path = alt_readme_path
        
        # Security: ensure path is within project root
        if not str(readme_path.resolve()).startswith(str(ROOT.resolve())):
            return jsonify({"error": "Invalid path"}), 400
        
        if not readme_path.exists() or not readme_path.is_file():
            return jsonify({"error": f"File not found: {file_path}"}), 404
        
        # Get user's preferred language
        user_language = 'en'
        if "user_id" in session:
            conn = get_db_connection()
            user = conn.execute(
                "SELECT preferred_language FROM users WHERE id = ?",
                (session["user_id"],)
            ).fetchone()
            if user and user["preferred_language"]:
                user_language = user["preferred_language"]
            conn.close()
        else:
            # Check query parameter or use default
            user_language = request.args.get('lang', 'en')
        
        # Read and render markdown
        with open(readme_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Update Educational Materials section based on user language
        folder_path = readme_path.parent
        has_ru_school = (folder_path / "school.ru.md").exists()
        has_ru_univer = (folder_path / "univer.ru.md").exists()
        has_en_school = (folder_path / "school.en.md").exists()
        has_en_univer = (folder_path / "univer.en.md").exists()
        
        # Update Educational Materials section with language-specific links
        import re
        pattern = r'(## Educational Materials / Учебные материалы\s*\n\n|## Учебные материалы\s*\n\n|## Educational Materials\s*\n\n)(.*?)(?=\n##|\Z)'
        
        def replace_section(match):
            if user_language == 'ru':
                header = "## Учебные материалы\n\n"
                links = []
                if has_ru_school:
                    links.append("- [Школьный уровень](school.ru.md)")
                if has_ru_univer:
                    links.append("- [Университетский уровень](univer.ru.md)")
                if not links:
                    content = "*Учебные материалы недоступны.*\n"
                else:
                    content = '\n'.join(links) + '\n'
            else:  # en
                header = "## Educational Materials\n\n"
                links = []
                if has_en_school:
                    links.append("- [School Level](school.en.md)")
                if has_en_univer:
                    links.append("- [University Level](univer.en.md)")
                if not links:
                    content = "*No educational materials available.*\n"
                else:
                    content = '\n'.join(links) + '\n'
            return header + content + '\n'
        
        md_content = re.sub(pattern, replace_section, md_content, flags=re.DOTALL)
        
        # Update Educational Materials section based on user language
        folder_path = readme_path.parent
        has_ru_school = (folder_path / "school.ru.md").exists()
        has_ru_univer = (folder_path / "univer.ru.md").exists()
        has_en_school = (folder_path / "school.en.md").exists()
        has_en_univer = (folder_path / "univer.en.md").exists()
        
        # Update Educational Materials section with language-specific links
        import re
        pattern = r'(## Educational Materials / Учебные материалы\s*\n\n|## Учебные материалы\s*\n\n|## Educational Materials\s*\n\n)(.*?)(?=\n##|\Z)'
        
        def replace_section(match):
            if user_language == 'ru':
                header = "## Учебные материалы\n\n"
                links = []
                if has_ru_school:
                    links.append("- [Школьный уровень](school.ru.md)")
                if has_ru_univer:
                    links.append("- [Университетский уровень](univer.ru.md)")
                if not links:
                    content = "*Учебные материалы недоступны.*\n"
                else:
                    content = '\n'.join(links) + '\n'
            else:  # en
                header = "## Educational Materials\n\n"
                links = []
                if has_en_school:
                    links.append("- [School Level](school.en.md)")
                if has_en_univer:
                    links.append("- [University Level](univer.en.md)")
                if not links:
                    content = "*No educational materials available.*\n"
                else:
                    content = '\n'.join(links) + '\n'
            return header + content + '\n'
        
        md_content = re.sub(pattern, replace_section, md_content, flags=re.DOTALL)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['fenced_code', 'tables', 'codehilite']
        )
        
        # Wrap in a simple HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>README - {file_path}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }}
                pre {{
                    background: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                code {{
                    background: #f4f4f4;
                    padding: 2px 5px;
                    border-radius: 3px;
                }}
                pre code {{
                    background: none;
                    padding: 0;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div style="margin-bottom: 20px;">
                <a href="/" style="color: #667eea;">← Back to Index</a>
            </div>
            {html_content}
        </body>
        </html>
        """
        
        return html
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/code/<path:file_path>")
def serve_code(file_path):
    """Serve code files (Python, Java, etc.) with syntax highlighting."""
    try:
        # Security: ensure path is within project root
        code_path = ROOT / file_path
        if not str(code_path).startswith(str(ROOT)):
            return jsonify({"error": "Invalid path"}), 400
        
        if not code_path.exists() or not code_path.is_file():
            return jsonify({"error": "File not found"}), 404
        
        # Read file content
        with open(code_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Determine language from extension
        ext = code_path.suffix.lower()
        lang_map = {
            '.py': 'python',
            '.java': 'java',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.md': 'markdown',
        }
        language = lang_map.get(ext, 'text')
        
        # Escape HTML
        from html import escape
        escaped_code = escape(code_content)
        
        # Wrap in HTML with syntax highlighting
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{code_path.name}</title>
            <style>
                body {{
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    line-height: 1.5;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                pre {{
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 5px;
                    overflow-x: auto;
                    border: 1px solid #ddd;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                code {{
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 14px;
                }}
                .header {{
                    margin-bottom: 20px;
                    padding: 10px;
                    background: #fff;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }}
                .header a {{
                    color: #667eea;
                    text-decoration: none;
                }}
                .header a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <a href="/" style="color: #667eea;">← Back to Index</a>
                <span style="margin: 0 10px;">|</span>
                <strong>{code_path.name}</strong>
                <span style="margin: 0 10px;">|</span>
                <span style="color: #666;">{language}</span>
            </div>
            <pre><code class="language-{language}">{escaped_code}</code></pre>
        </body>
        </html>
        """
        
        return html
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
