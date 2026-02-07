#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithm index page with Level and Language filters.
"""

from flask import Blueprint, render_template, request, jsonify, session
from pathlib import Path
import re
import sqlite3
import uuid

try:
    from core.paths import PROJECT_ROOT, COURSE_ROOT, get_database_path
    from core.exceptions import ValidationError
except ImportError:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    COURSE_ROOT = PROJECT_ROOT / "course"
    ValidationError = ValueError  # type: ignore

    def get_database_path(db_name: str = "algorithms.db") -> Path:
        return PROJECT_ROOT / "database" / db_name

ROOT = PROJECT_ROOT
DB_PATH = get_database_path("algorithms.db")
LESSON_ASK_LIMIT_PER_LESSON = 25
LESSON_ASK_QUESTION_MAX_LEN = 1000

algorithm_index_bp = Blueprint("algorithm_index", __name__, url_prefix="/algorithm-index")


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def check_md_file_exists(folder_path: str, level: str, language: str) -> bool:
    """Check if MD file exists for given level and language.
    If specific language file doesn't exist, check if any language file exists for this level.
    This ensures same algorithms are shown regardless of language choice."""
    try:
        if not folder_path:
            return False
            
        folder = ROOT / folder_path
        if not folder.exists():
            return False
            
        if level == "school":
            # First check for specific language file
            filename = f"school.{language}.md"
            file_path = folder / filename
            if file_path.exists():
                return True
            # If not found, check if any language file exists for school level
            ru_file = folder / "school.ru.md"
            en_file = folder / "school.en.md"
            return ru_file.exists() or en_file.exists()
        else:  # university/univer
            # First check for specific language file
            filename = f"univer.{language}.md"
            file_path = folder / filename
            if file_path.exists():
                return True
            # If not found, check if any language file exists for univer level
            ru_file = folder / "univer.ru.md"
            en_file = folder / "univer.en.md"
            return ru_file.exists() or en_file.exists()
    except Exception as e:
        # Log error for debugging (can be removed in production)
        print(f"Error checking MD file for {folder_path}: {e}")
        return False


@algorithm_index_bp.route("/")
def index_page():
    """Algorithm index page with Level and Language filters."""
    # Get user preferences from session or defaults
    preferred_language = session.get("preferred_language", "en")
    preferred_level = session.get("preferred_level", "school")
    
    return render_template(
        "algorithm_index.html",
        preferred_language=preferred_language,
        preferred_level=preferred_level
    )


@algorithm_index_bp.route("/api/algorithms")
def get_algorithms():
    """Get algorithms with Level and Language filtering."""
    conn = get_db_connection()
    
    # Get query parameters
    level = request.args.get("level", "school")  # school or univer
    language = request.args.get("language", "en")  # en or ru
    
    # Normalize level value
    if level == "university":
        level = "univer"
    
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "")
    semester = request.args.get("semester", "")
    sort_by = request.args.get("sort", "name")
    sort_order = request.args.get("order", "asc")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 50))
    
    # Build query
    query = """
        SELECT 
            a.id, a.name, a.display_name, a.semester_number, a.lecture_name,
            a.category, a.time_complexity, a.space_complexity, a.description,
            a.short_description, a.folder_path
        FROM algorithms a
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
        params.append(semester)
    
    # Sort
    valid_sorts = {"name": "a.name", "semester": "a.semester_number", 
                   "category": "a.category", "complexity": "a.time_complexity"}
    sort_column = valid_sorts.get(sort_by, "a.name")
    order = "ASC" if sort_order == "asc" else "DESC"
    query += f" ORDER BY {sort_column} {order}"
    
    # Get total count
    count_query = f"SELECT COUNT(*) as total FROM ({query})"
    total = conn.execute(count_query, params).fetchone()["total"]
    
    # Pagination
    offset = (page - 1) * per_page
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    
    # Execute query
    algorithms = conn.execute(query, params).fetchall()
    
    # Filter by MD file existence and add file info
    result_algorithms = []
    for algo in algorithms:
        folder_path = algo["folder_path"]
        
        # Skip if folder_path is None or empty
        if not folder_path:
            continue
            
        # Check if MD file exists for the level (any language if specific language file doesn't exist)
        if check_md_file_exists(folder_path, level, language):
            algo_dict = dict(algo)
            # Add MD file path - try to find the best matching file
            folder = ROOT / folder_path
            md_filename = None
            # First try specific language file
            if level == "school":
                specific_file = folder / f"school.{language}.md"
                if specific_file.exists():
                    md_filename = f"school.{language}.md"
                else:
                    # Fallback to any language file for school level
                    if (folder / "school.ru.md").exists():
                        md_filename = "school.ru.md"
                    elif (folder / "school.en.md").exists():
                        md_filename = "school.en.md"
            else:  # univer
                specific_file = folder / f"univer.{language}.md"
                if specific_file.exists():
                    md_filename = f"univer.{language}.md"
                else:
                    # Fallback to any language file for univer level
                    if (folder / "univer.ru.md").exists():
                        md_filename = "univer.ru.md"
                    elif (folder / "univer.en.md").exists():
                        md_filename = "univer.en.md"
            
            if md_filename:
                algo_dict["md_file"] = str(folder / md_filename)
                algo_dict["md_url"] = f"/algorithm-index/api/md-file?path={folder_path}&level={level}&language={language}"
                result_algorithms.append(algo_dict)
    
    # Recalculate total based on filtered results
    # For now, we'll use the filtered count
    filtered_total = len(result_algorithms)
    
    conn.close()
    
    return jsonify({
        "algorithms": result_algorithms,
        "total": filtered_total,
        "page": page,
        "per_page": per_page,
        "total_pages": (filtered_total + per_page - 1) // per_page if filtered_total > 0 else 0
    })


@algorithm_index_bp.route("/api/md-file")
def get_md_file():
    """Get MD file content."""
    folder_path = request.args.get("path")
    level = request.args.get("level", "school")
    language = request.args.get("language", "en")
    
    if not folder_path:
        return jsonify({"error": "Path required"}), 400
    
    try:
        folder = ROOT / folder_path
        if level == "school":
            filename = f"school.{language}.md"
        else:
            filename = f"univer.{language}.md"
        
        file_path = folder / filename
        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404
        
        content = file_path.read_text(encoding='utf-8')
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _ensure_lesson_ask_table(conn: sqlite3.Connection) -> None:
    """Create lesson_ask_usage table if not exists."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lesson_ask_usage (
            session_id TEXT NOT NULL,
            lesson_path TEXT NOT NULL,
            count INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT,
            PRIMARY KEY (session_id, lesson_path)
        )
        """
    )
    conn.commit()


def _get_lesson_ask_session_id() -> str:
    """Stable session id for rate limiting (user_id or anonymous session)."""
    if session.get("user_id"):
        return f"user_{session['user_id']}"
    if not session.get("_lesson_ask_sid"):
        session["_lesson_ask_sid"] = str(uuid.uuid4())
    return session["_lesson_ask_sid"]


def _validate_lesson_path(lesson_path: str) -> Path:
    """Return resolved path if under ROOT and exists as directory; else raise ValidationError."""
    if not lesson_path or ".." in lesson_path or lesson_path.startswith("/"):
        raise ValidationError("Invalid lesson path")
    path = (ROOT / lesson_path.replace("\\", "/").lstrip("/")).resolve()
    try:
        root_resolved = ROOT.resolve()
        if not str(path).startswith(str(root_resolved)) or not path.is_dir():
            raise ValueError("Lesson path not under project")
    except Exception as e:
        raise ValidationError("Invalid lesson path") from e
    return path


@algorithm_index_bp.route("/api/lesson-ask/limit")
def lesson_ask_limit():
    """Return used count and limit for current user/session and lesson."""
    lesson_path = request.args.get("lesson_path")
    if not lesson_path:
        return jsonify({"error": "lesson_path required"}), 400
    try:
        _validate_lesson_path(lesson_path)
    except (ValueError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    sid = _get_lesson_ask_session_id()
    conn = get_db_connection()
    try:
        _ensure_lesson_ask_table(conn)
        row = conn.execute(
            "SELECT count FROM lesson_ask_usage WHERE session_id = ? AND lesson_path = ?",
            (sid, lesson_path),
        ).fetchone()
        used = int(row["count"]) if row else 0
    finally:
        conn.close()
    return jsonify({"used": used, "limit": LESSON_ASK_LIMIT_PER_LESSON})


@algorithm_index_bp.route("/api/lesson-ask", methods=["POST"])
def lesson_ask():
    """Ask AI a question about the current lesson. Rate limited to 25 per lesson per student."""
    data = request.get_json() or {}
    lesson_path = (data.get("lesson_path") or "").strip()
    question = (data.get("question") or "").strip()
    if not lesson_path:
        return jsonify({"error": "lesson_path required"}), 400
    if not question:
        return jsonify({"error": "question required"}), 400
    if len(question) > LESSON_ASK_QUESTION_MAX_LEN:
        return jsonify({"error": "question too long"}), 400
    if re.search(r"<script|javascript:|on\w+=|\.execute\s*\(|DROP\s+TABLE", question, re.I):
        return jsonify({"error": "Invalid question"}), 400
    try:
        lesson_dir = _validate_lesson_path(lesson_path)
    except (ValueError, ValidationError) as e:
        return jsonify({"error": str(e)}), 400
    sid = _get_lesson_ask_session_id()
    conn = get_db_connection()
    try:
        _ensure_lesson_ask_table(conn)
        row = conn.execute(
            "SELECT count FROM lesson_ask_usage WHERE session_id = ? AND lesson_path = ?",
            (sid, lesson_path),
        ).fetchone()
        used = int(row["count"]) if row else 0
        if used >= LESSON_ASK_LIMIT_PER_LESSON:
            return jsonify({"error": "Question limit reached for this lesson (25 max)."}), 429
        from datetime import datetime
        import openai
        api_key = None
        base_url = None
        try:
            from core.config import get_openai_api_key, get_openai_api_base
            api_key = get_openai_api_key()
            base_url = get_openai_api_base() or None
        except ImportError:
            pass
        if not api_key:
            return jsonify({"error": "AI not configured. Set OPENAI_API_KEY for this feature."}), 503
        lesson_text = ""
        for name in ("school.en.md", "univer.en.md", "README.md"):
            f = lesson_dir / name
            if f.exists():
                try:
                    lesson_text += f.read_text(encoding="utf-8")[:12000]
                    break
                except Exception:
                    pass
        if not lesson_text:
            lesson_text = f"Lesson folder: {lesson_path}"
        system = (
            "You are a tutor for an algorithms course. Answer ONLY questions about this lesson. "
            "Use the lesson content below. If the question is off-topic or not about this lesson, "
            "politely say you can only answer questions about this lesson. Keep answers concise and educational."
        )
        user_content = f"Lesson content:\n\n{lesson_text[:10000]}\n\n---\nStudent question: {question}"
        client = openai.OpenAI(api_key=api_key, base_url=base_url if base_url else None)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_content},
            ],
            max_tokens=800,
        )
        answer = (response.choices[0].message.content or "").strip()
        conn.execute(
            """
            INSERT INTO lesson_ask_usage (session_id, lesson_path, count, updated_at)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(session_id, lesson_path) DO UPDATE SET
                count = count + 1,
                updated_at = ?
            """,
            (sid, lesson_path, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()),
        )
        conn.commit()
    except Exception as e:
        if "429" in str(type(e).__name__) or "rate" in str(e).lower():
            return jsonify({"error": "Rate limit exceeded. Try again later."}), 429
        return jsonify({"error": "Failed to get answer. Try again."}), 500
    finally:
        conn.close()
    return jsonify({"answer": answer, "used": used + 1, "limit": LESSON_ASK_LIMIT_PER_LESSON})


@algorithm_index_bp.route("/api/preferences", methods=["GET", "POST"])
def user_preferences():
    """Get or set user preferences."""
    if "user_id" not in session:
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
        if level not in ["school", "university"]:
            level = "school"
        
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
        
        return jsonify({"success": True, "language": language, "level": level})

