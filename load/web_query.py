"""
Web interface for querying algorithm_descriptions database.
Run with: python web_query.py
Then open: http://localhost:5000
"""
from flask import Flask, render_template_string, request, jsonify
import sqlite3
from pathlib import Path
from urllib.parse import unquote
from typing import Optional
import re

app = Flask(__name__)

# Database path
def get_db_path():
    # Prioritize main database in parent directory (has more data)
    db_path = Path("../algos.db")
    if not db_path.exists():
        db_path = Path("algos.db")
    if not db_path.exists():
        db_path = Path("load/algos.db")
    return str(db_path)


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def get_column_names():
    """Get all column names from algorithm_descriptions table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(algorithm_descriptions)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns


PLACEHOLDER_PATTERNS = [
    r"\[specific purpose\]", r"\[specific mechanism\]", r"\[конкретная цель\]",
    r"\[конкретный механизм\]", r"\[.*?\]", r"placeholder", r"заполнитель",
    r"конкретный алгоритм/техника", r"конкретных задач в области",
    r"используемая для \[", r"работает путем \[",
]


def has_placeholder(text: str) -> bool:
    if not text:
        return False
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def clean_field(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    cleaned = text.strip()
    if not cleaned or has_placeholder(cleaned):
        return None
    return cleaned


HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Algorithm Descriptions Database Query</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .search-form {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: inline-block;
            width: 120px;
            font-weight: bold;
            color: #555;
        }
        input, select {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        input[type="text"] {
            width: 300px;
        }
        input[type="number"] {
            width: 100px;
        }
        select {
            width: 200px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .stats {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .stats strong {
            color: #2e7d32;
        }
        .table-wrapper {
            margin-top: 20px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 1400px;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            cursor: pointer;
            position: relative;
        }
        th:hover {
            background-color: #45a049;
        }
        th.sortable::after {
            content: ' ↕';
            opacity: 0.5;
        }
        th.sorted-asc::after {
            content: ' ↑';
            opacity: 1;
        }
        th.sorted-desc::after {
            content: ' ↓';
            opacity: 1;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }
        .multi-line {
            white-space: pre-wrap;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .pagination {
            margin-top: 20px;
            text-align: center;
        }
        .pagination a {
            display: inline-block;
            padding: 8px 16px;
            margin: 0 4px;
            text-decoration: none;
            border: 1px solid #ddd;
            border-radius: 4px;
            color: #333;
        }
        .pagination a:hover {
            background-color: #4CAF50;
            color: white;
        }
        .pagination .current {
            background-color: #4CAF50;
            color: white;
            border: 1px solid #4CAF50;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="margin-bottom: 20px;">
            <a href="/" style="padding: 8px 16px; background: #999; color: white; text-decoration: none; border-radius: 4px; margin-right: 10px;">Home</a>
            <a href="/load" style="padding: 8px 16px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px; margin-right: 10px;">Search</a>
            <a href="/stats" style="padding: 8px 16px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px;">Statistics</a>
        </div>
        <h1>Algorithm Descriptions Database Query</h1>
        
        <div class="search-form">
            <form method="GET" action="/">
                <div class="form-group">
                    <label for="search">Search:</label>
                    <input type="text" id="search" name="search" 
                           value="{{ request.args.get('search', '') }}" 
                           placeholder="Search in algorithm name, title, description...">
                </div>
                
                <div class="form-group">
                    <label for="language">Language:</label>
                    <select id="language" name="language">
                        <option value="">All</option>
                        <option value="en" {{ 'selected' if request.args.get('language') == 'en' }}>English</option>
                        <option value="ru" {{ 'selected' if request.args.get('language') == 'ru' }}>Russian</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="level">Level:</label>
                    <select id="level" name="level">
                        <option value="">All</option>
                        <option value="school" {{ 'selected' if request.args.get('level') == 'school' }}>School</option>
                        <option value="university" {{ 'selected' if request.args.get('level') == 'university' }}>University</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="source">Source:</label>
                    <select id="source" name="source">
                        <option value="">All</option>
                        <option value="local_markdown" {{ 'selected' if request.args.get('source') == 'local_markdown' }}>Local Markdown</option>
                        <option value="wikipedia.en" {{ 'selected' if request.args.get('source') == 'wikipedia.en' }}>Wikipedia EN</option>
                        <option value="wikipedia.ru" {{ 'selected' if request.args.get('source') == 'wikipedia.ru' }}>Wikipedia RU</option>
                        <option value="e-maxx.ru" {{ 'selected' if request.args.get('source') == 'e-maxx.ru' }}>e-maxx.ru</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="order_by">Order By:</label>
                    <select id="order_by" name="order_by">
                        <option value="fetched_at" {{ 'selected' if request.args.get('order_by', 'fetched_at') == 'fetched_at' }}>Fetched At</option>
                        <option value="algorithm_name" {{ 'selected' if request.args.get('order_by') == 'algorithm_name' }}>Algorithm Name</option>
                        <option value="title" {{ 'selected' if request.args.get('order_by') == 'title' }}>Title</option>
                        <option value="language" {{ 'selected' if request.args.get('order_by') == 'language' }}>Language</option>
                        <option value="level" {{ 'selected' if request.args.get('order_by') == 'level' }}>Level</option>
                        <option value="source_site" {{ 'selected' if request.args.get('order_by') == 'source_site' }}>Source</option>
                        <option value="quality_score" {{ 'selected' if request.args.get('order_by') == 'quality_score' }}>Quality Score</option>
                    </select>
                    
                    <select id="order_dir" name="order_dir">
                        <option value="DESC" {{ 'selected' if request.args.get('order_dir', 'DESC') == 'DESC' }}>Descending</option>
                        <option value="ASC" {{ 'selected' if request.args.get('order_dir') == 'ASC' }}>Ascending</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="limit">Limit:</label>
                    <input type="number" id="limit" name="limit" 
                           value="{{ request.args.get('limit', '200') }}" 
                           min="1" max="1000" step="1">
                </div>
                
                <div class="form-group">
                    <button type="submit">Search</button>
                    <a href="/" style="margin-left: 10px; padding: 10px 20px; background: #999; color: white; text-decoration: none; border-radius: 4px;">Reset</a>
                </div>
            </form>
        </div>
        
        <div class="stats">
            <strong>Total Results:</strong> {{ total_count }} | 
            <strong>Showing:</strong> {{ showing_count }} | 
            <strong>Database:</strong> {{ db_path }}
            <a href="/stats" style="margin-left: 20px; color: #2e7d32; text-decoration: underline;">View Statistics</a>
        </div>
        
        {% if results %}
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th class="sortable" onclick="sortBy('algorithm_name')">Algorithm</th>
                        <th class="sortable" onclick="sortBy('language')">Lang</th>
                        <th class="sortable" onclick="sortBy('level')">Level</th>
                        <th class="sortable" onclick="sortBy('title')">Title</th>
                        <th class="sortable" onclick="sortBy('source_site')">Source</th>
                        <th class="sortable" onclick="sortBy('quality_score')">Quality</th>
                        <th class="sortable" onclick="sortBy('fetched_at')">Fetched At</th>
                        <th>Short Description</th>
                        <th>Long Description</th>
                        <th>Simple Explanation</th>
                        <th>Where It's Used</th>
                        <th>Example</th>
                        <th>Algorithm Definition</th>
                        <th>Technical Description</th>
                        <th>Application</th>
                        <th>Step-by-Step</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in results %}
                    <tr>
                        <td>{{ row.algorithm_name }}</td>
                        <td>{{ row.language }}</td>
                        <td>{{ row.level }}</td>
                        <td>{{ row.title or '—' }}</td>
                        <td>{{ row.source_site or '—' }}</td>
                        <td>{{ '%.2f'|format(row.quality_score) if row.quality_score else '—' }}</td>
                        <td>{{ row.fetched_at[:19] if row.fetched_at else '—' }}</td>
                        <td class="multi-line">{{ row.short_description or '—' }}</td>
                        <td class="multi-line">{{ row.long_description or '—' }}</td>
                        <td class="multi-line">{{ row.simple_explanation or '—' }}</td>
                        <td class="multi-line">{{ row.where_its_used or '—' }}</td>
                        <td class="multi-line">{{ row.example or '—' }}</td>
                        <td class="multi-line">{{ row.algorithm_definition or '—' }}</td>
                        <td class="multi-line">{{ row.technical_description or '—' }}</td>
                        <td class="multi-line">{{ row.application or '—' }}</td>
                        <td class="multi-line">{{ row.step_by_step or '—' }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="no-results">
            <p>No results found.</p>
        </div>
        {% endif %}
    </div>
    
    <script>
        function sortBy(column) {
            const url = new URL(window.location);
            const currentOrder = url.searchParams.get('order_by');
            const currentDir = url.searchParams.get('order_dir') || 'DESC';
            
            if (currentOrder === column) {
                // Toggle direction
                url.searchParams.set('order_dir', currentDir === 'ASC' ? 'DESC' : 'ASC');
            } else {
                url.searchParams.set('order_by', column);
                url.searchParams.set('order_dir', 'DESC');
            }
            
            window.location = url;
        }
        
        // Highlight current sort column
        document.addEventListener('DOMContentLoaded', function() {
            const orderBy = '{{ request.args.get("order_by", "fetched_at") }}';
            const orderDir = '{{ request.args.get("order_dir", "DESC") }}';
            const headers = document.querySelectorAll('th.sortable');
            headers.forEach(header => {
                if (header.textContent.trim().toLowerCase().replace(/\s+/g, '_') === orderBy || 
                    header.getAttribute('onclick').includes(orderBy)) {
                    header.classList.add(orderDir.toLowerCase() === 'asc' ? 'sorted-asc' : 'sorted-desc');
                }
            });
        });
    </script>
</body>
</html>
"""


HOME_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Algorithm Descriptions Database</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            background: white;
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 600px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        .nav-buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .nav-button {
            display: inline-block;
            padding: 20px 40px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        .nav-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        .nav-button.stats {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
        }
        .nav-button.stats:hover {
            box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
        }
        .info {
            margin-top: 40px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Algorithm Descriptions Database</h1>
        <p class="subtitle">Search and explore algorithm information</p>
        
        <div class="nav-buttons">
            <a href="/" class="nav-button">🔍 Search Database</a>
            <a href="/stats" class="nav-button stats">📊 View Statistics</a>
        </div>
        
        <div class="info">
            <p><strong>Database:</strong> {{ db_path }}</p>
            <p><strong>Total Algorithms:</strong> {{ total_algorithms }} | 
               <strong>Total Descriptions:</strong> {{ total_descriptions }}</p>
        </div>
    </div>
</body>
</html>
"""


@app.route('/load')
def index():
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
    conn = get_connection()
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
    results = [dict(row) for row in rows]
    
    conn.close()
    
    # Get database path for display
    db_path = Path(get_db_path()).absolute()
    
    return render_template_string(
        HTML_TEMPLATE,
        results=results,
        total_count=total_count,
        showing_count=len(results),
        db_path=str(db_path)
    )


@app.route('/')
def home():
    """Home page - serves the main web interface index.html."""
    # Read the index.html file from web_interface/templates
    index_path = Path(__file__).parent.parent / "web_interface" / "templates" / "index.html"
    
    if not index_path.exists():
        return f"Error: index.html not found at {index_path}", 404
    
    # Read and return the HTML file
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content


STATS_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Database Statistics</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .nav-link {
            display: inline-block;
            margin: 10px 0;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .nav-link:hover {
            background-color: #45a049;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }
        .stat-card h3 {
            margin-top: 0;
            color: #2e7d32;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
            margin: 10px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .progress-bar {
            background: #e0e0e0;
            border-radius: 10px;
            height: 20px;
            margin: 5px 0;
            overflow: hidden;
        }
        .progress-fill {
            background: #4CAF50;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="margin-bottom: 20px;">
            <a href="/" style="padding: 8px 16px; background: #999; color: white; text-decoration: none; border-radius: 4px; margin-right: 10px;">Home</a>
            <a href="/load" style="padding: 8px 16px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px; margin-right: 10px;">Search</a>
            <a href="/stats" style="padding: 8px 16px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px;">Statistics</a>
        </div>
        <h1>Database Statistics</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Algorithms</h3>
                <div class="stat-value">{{ total_algorithms }}</div>
            </div>
            <div class="stat-card">
                <h3>Total Descriptions</h3>
                <div class="stat-value">{{ total_descriptions }}</div>
            </div>
            <div class="stat-card">
                <h3>Web Descriptions</h3>
                <div class="stat-value">{{ web_descriptions }}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (web_descriptions / total_descriptions * 100) if total_descriptions > 0 else 0 }}%">
                        {{ "%.1f"|format((web_descriptions / total_descriptions * 100) if total_descriptions > 0 else 0) }}%
                    </div>
                </div>
            </div>
            <div class="stat-card">
                <h3>Local Descriptions</h3>
                <div class="stat-value">{{ local_descriptions }}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{ (local_descriptions / total_descriptions * 100) if total_descriptions > 0 else 0 }}%">
                        {{ "%.1f"|format((local_descriptions / total_descriptions * 100) if total_descriptions > 0 else 0) }}%
                    </div>
                </div>
            </div>
        </div>
        
        <h2>Breakdown by Source</h2>
        <table>
            <thead>
                <tr>
                    <th>Source</th>
                    <th>Count</th>
                    <th>Percentage</th>
                    <th>Progress</th>
                </tr>
            </thead>
            <tbody>
                {% for source, count in sources %}
                <tr>
                    <td>{{ source or 'Unknown' }}</td>
                    <td>{{ count }}</td>
                    <td>{{ "%.2f"|format((count / total_descriptions * 100) if total_descriptions > 0 else 0) }}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ (count / total_descriptions * 100) if total_descriptions > 0 else 0 }}%"></div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>Breakdown by Language</h2>
        <table>
            <thead>
                <tr>
                    <th>Language</th>
                    <th>Count</th>
                    <th>Percentage</th>
                    <th>Progress</th>
                </tr>
            </thead>
            <tbody>
                {% for lang, count in languages %}
                <tr>
                    <td>{{ lang or 'Unknown' }}</td>
                    <td>{{ count }}</td>
                    <td>{{ "%.2f"|format((count / total_descriptions * 100) if total_descriptions > 0 else 0) }}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ (count / total_descriptions * 100) if total_descriptions > 0 else 0 }}%"></div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>Breakdown by Level</h2>
        <table>
            <thead>
                <tr>
                    <th>Level</th>
                    <th>Count</th>
                    <th>Percentage</th>
                    <th>Progress</th>
                </tr>
            </thead>
            <tbody>
                {% for level, count in levels %}
                <tr>
                    <td>{{ level or 'Unknown' }}</td>
                    <td>{{ count }}</td>
                    <td>{{ "%.2f"|format((count / total_descriptions * 100) if total_descriptions > 0 else 0) }}%</td>
                    <td>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {{ (count / total_descriptions * 100) if total_descriptions > 0 else 0 }}%"></div>
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>Database Information</h2>
        <div class="stat-card">
            <p><strong>Database Path:</strong> {{ db_path }}</p>
            <p><strong>Last Updated:</strong> {{ last_updated }}</p>
        </div>
    </div>
</body>
</html>
"""


@app.route('/api/algorithm-details/<int:desc_id>')
def get_algorithm_details(desc_id):
    """API endpoint to get full algorithm description details."""
    conn = get_connection()
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
    
    keys = [
        'title', 'short_description', 'long_description', 'simple_explanation',
        'algorithm_definition', 'technical_description', 'where_its_used',
        'application', 'step_by_step', 'example', 'discipline',
        'self_check_basic', 'self_check_intermediate', 'self_check_advanced',
        'practical_tasks_basic', 'practical_tasks_applied', 'practical_tasks_research',
        'ethical_reasoning', 'example_result'
    ]
    
    raw_details = dict(zip(keys, row))
    sanitized = {}
    for key, value in raw_details.items():
        cleaned = clean_field(value) if key != 'title' else (clean_field(value) or value)
        if cleaned:
            sanitized[key] = cleaned
    
    return jsonify(sanitized)


@app.route('/stats')
def stats():
    """Display database statistics page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get total algorithms
    cursor.execute("SELECT COUNT(DISTINCT algorithm_name) FROM algorithms")
    total_algorithms = cursor.fetchone()[0]
    
    # Get total descriptions
    cursor.execute("SELECT COUNT(*) FROM algorithm_descriptions")
    total_descriptions = cursor.fetchone()[0]
    
    # Get web vs local counts (SQLite-compatible)
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN source_site != 'local_markdown' THEN 1 ELSE 0 END) as web_count,
            SUM(CASE WHEN source_site = 'local_markdown' THEN 1 ELSE 0 END) as local_count
        FROM algorithm_descriptions
    """)
    row = cursor.fetchone()
    web_descriptions = row[0] if row and row[0] else 0
    local_descriptions = row[1] if row and row[1] else 0
    
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
    
    db_path = Path(get_db_path()).absolute()
    
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


if __name__ == '__main__':
    print(f"Starting web server...")
    print(f"Database: {Path(get_db_path()).absolute()}")
    print(f"Open your browser at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

