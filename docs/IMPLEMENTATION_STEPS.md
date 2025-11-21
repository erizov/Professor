# First Easy Steps to Implement Student Sandbox

## Overview

This document outlines the **simplest and quickest** steps to start implementing the Student Sandbox system. These steps build incrementally and can be completed in order.

---

## Step 1: Create Sandbox Database Schema (30 minutes)

**Difficulty**: ⭐ Easy  
**Time**: 30 minutes  
**Dependencies**: None

### What to do:
1. Create `database/setup_sandbox_tables.py` script
2. Add tables: `sandboxes`, `sandbox_versions`
3. Run script to initialize database

### Why this first:
- No UI needed
- Foundation for everything else
- Can test with SQL queries

### Implementation:

```python
# database/setup_sandbox_tables.py
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "users.db"  # Or create sandboxes.db

def create_sandbox_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Sandboxes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sandboxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            algorithm_path TEXT NOT NULL,
            language TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_modified TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            UNIQUE(user_id, algorithm_path, language)
        )
    """)
    
    # Sandbox versions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sandbox_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sandbox_id INTEGER NOT NULL,
            version_number INTEGER NOT NULL,
            code_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id),
            UNIQUE(sandbox_id, version_number)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Sandbox tables created successfully")

if __name__ == "__main__":
    create_sandbox_schema()
```

---

## Step 2: Create Sandbox File Structure (15 minutes)

**Difficulty**: ⭐ Easy  
**Time**: 15 minutes  
**Dependencies**: Step 1

### What to do:
1. Create `sandboxes/` directory
2. Create helper function to create user sandbox directories
3. Test directory creation

### Implementation:

```python
# framework/sandbox_manager.py
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SANDBOXES_DIR = ROOT / "sandboxes"

def create_user_sandbox_dir(user_id: int) -> Path:
    """Create sandbox directory for user if it doesn't exist."""
    user_dir = SANDBOXES_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def get_sandbox_path(user_id: int, algorithm_path: str, language: str) -> Path:
    """Get path to sandbox for specific algorithm."""
    user_dir = create_user_sandbox_dir(user_id)
    # Normalize algorithm path (replace slashes with underscores)
    safe_path = algorithm_path.replace('/', '_').replace('\\', '_')
    sandbox_dir = user_dir / f"{safe_path}_{language}"
    sandbox_dir.mkdir(parents=True, exist_ok=True)
    return sandbox_dir
```

---

## Step 3: Create Simple Sandbox API Endpoints (1 hour)

**Difficulty**: ⭐⭐ Easy-Medium  
**Time**: 1 hour  
**Dependencies**: Step 1, Step 2

### What to do:
1. Create `web_interface/sandbox_bp.py` blueprint
2. Add endpoints:
   - `POST /api/sandbox/create` - Create new sandbox
   - `GET /api/sandbox/list` - List user's sandboxes
   - `GET /api/sandbox/<id>` - Get sandbox details
   - `PUT /api/sandbox/<id>/code` - Save code

### Implementation:

```python
# web_interface/sandbox_bp.py
from flask import Blueprint, request, jsonify, session
from pathlib import Path
import sqlite3
import json
from datetime import datetime

from framework.sandbox_manager import get_sandbox_path, create_user_sandbox_dir

sandbox_bp = Blueprint('sandbox', __name__, url_prefix='/api/sandbox')

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "users.db"

@sandbox_bp.route('/create', methods=['POST'])
def create_sandbox():
    """Create a new sandbox for an algorithm."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if session.get('role') not in ['student', 'professor', 'admin']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    algorithm_path = data.get('algorithm_path')
    language = data.get('language', 'python')
    
    if not algorithm_path:
        return jsonify({'error': 'algorithm_path required'}), 400
    
    user_id = session['user_id']
    
    # Read original code
    original_file = ROOT / algorithm_path
    if not original_file.exists():
        return jsonify({'error': 'Algorithm not found'}), 404
    
    original_code = original_file.read_text(encoding='utf-8')
    
    # Create sandbox in database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO sandboxes (user_id, algorithm_path, language)
            VALUES (?, ?, ?)
        """, (user_id, algorithm_path, language))
        
        sandbox_id = cursor.lastrowid
        
        # Create first version with original code
        cursor.execute("""
            INSERT INTO sandbox_versions (sandbox_id, version_number, code_content, description)
            VALUES (?, 1, ?, 'Original copy')
        """, (sandbox_id, original_code))
        
        conn.commit()
        
        # Create file system structure
        sandbox_dir = get_sandbox_path(user_id, algorithm_path, language)
        version_dir = sandbox_dir / "version_1"
        version_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = "algorithm.py" if language == "python" else "Algorithm.java"
        (version_dir / file_name).write_text(original_code, encoding='utf-8')
        
        return jsonify({
            'success': True,
            'sandbox_id': sandbox_id,
            'message': 'Sandbox created successfully'
        })
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Sandbox already exists'}), 409
    finally:
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
    
    cursor.execute("""
        SELECT id, algorithm_path, language, created_at, last_modified
        FROM sandboxes
        WHERE user_id = ? AND is_active = 1
        ORDER BY last_modified DESC
    """, (user_id,))
    
    sandboxes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'sandboxes': sandboxes})

@sandbox_bp.route('/<int:sandbox_id>', methods=['GET'])
def get_sandbox(sandbox_id):
    """Get sandbox details and current code."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get sandbox info
    cursor.execute("""
        SELECT id, algorithm_path, language, created_at, last_modified
        FROM sandboxes
        WHERE id = ? AND user_id = ?
    """, (sandbox_id, user_id))
    
    sandbox = cursor.fetchone()
    if not sandbox:
        conn.close()
        return jsonify({'error': 'Sandbox not found'}), 404
    
    # Get current version (latest)
    cursor.execute("""
        SELECT version_number, code_content, created_at, description
        FROM sandbox_versions
        WHERE sandbox_id = ?
        ORDER BY version_number DESC
        LIMIT 1
    """, (sandbox_id,))
    
    version = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'sandbox': dict(sandbox),
        'current_version': dict(version) if version else None
    })

@sandbox_bp.route('/<int:sandbox_id>/code', methods=['PUT'])
def save_code(sandbox_id):
    """Save code to sandbox (creates new version)."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    data = request.get_json()
    code = data.get('code')
    description = data.get('description', 'Updated code')
    
    if not code:
        return jsonify({'error': 'code required'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verify ownership
    cursor.execute("""
        SELECT id, algorithm_path, language
        FROM sandboxes
        WHERE id = ? AND user_id = ?
    """, (sandbox_id, user_id))
    
    sandbox = cursor.fetchone()
    if not sandbox:
        conn.close()
        return jsonify({'error': 'Sandbox not found'}), 404
    
    # Get next version number
    cursor.execute("""
        SELECT MAX(version_number) FROM sandbox_versions
        WHERE sandbox_id = ?
    """, (sandbox_id,))
    
    max_version = cursor.fetchone()[0] or 0
    next_version = max_version + 1
    
    # Create new version
    cursor.execute("""
        INSERT INTO sandbox_versions (sandbox_id, version_number, code_content, description)
        VALUES (?, ?, ?, ?)
    """, (sandbox_id, next_version, code, description))
    
    # Update sandbox last_modified
    cursor.execute("""
        UPDATE sandboxes
        SET last_modified = datetime('now')
        WHERE id = ?
    """, (sandbox_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'version_number': next_version,
        'message': 'Code saved successfully'
    })
```

**Register blueprint in `web_interface/app.py`:**
```python
from web_interface.sandbox_bp import sandbox_bp
app.register_blueprint(sandbox_bp)
```

---

## Step 4: Create Simple Sandbox UI Page (1.5 hours)

**Difficulty**: ⭐⭐ Easy-Medium  
**Time**: 1.5 hours  
**Dependencies**: Step 3

### What to do:
1. Create `web_interface/templates/sandbox.html`
2. Simple page with:
   - Algorithm selector dropdown
   - Language selector (Python/Java)
   - "Create Sandbox" button
   - Simple textarea for code editing
   - "Save" button
   - "Run" button (basic execution)

### Implementation:

```html
<!-- web_interface/templates/sandbox.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Sandbox</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .controls {
            margin-bottom: 20px;
        }
        .controls select, .controls button {
            padding: 10px;
            margin: 5px;
        }
        .code-editor {
            width: 100%;
            height: 500px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .output {
            margin-top: 20px;
            padding: 10px;
            background: #f5f5f5;
            border: 1px solid #ddd;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>Algorithm Sandbox</h1>
    
    <div class="controls">
        <select id="algorithm-select">
            <option value="">Select Algorithm...</option>
        </select>
        <select id="language-select">
            <option value="python">Python</option>
            <option value="java">Java</option>
        </select>
        <button onclick="createSandbox()">Create Sandbox</button>
        <button onclick="saveCode()" id="save-btn" disabled>Save</button>
        <button onclick="runCode()" id="run-btn" disabled>Run</button>
    </div>
    
    <div>
        <textarea id="code-editor" class="code-editor" placeholder="Select an algorithm and create a sandbox to start editing..."></textarea>
    </div>
    
    <div class="output" id="output">Output will appear here...</div>
    
    <script>
        let currentSandboxId = null;
        
        // Load algorithms on page load
        async function loadAlgorithms() {
            const response = await fetch('/api/algorithms');
            const data = await response.json();
            const select = document.getElementById('algorithm-select');
            
            data.algorithms.forEach(algo => {
                const option = document.createElement('option');
                option.value = algo.folder_path || algo.path;
                option.textContent = `${algo.display_name} (${algo.folder_path})`;
                select.appendChild(option);
            });
        }
        
        async function createSandbox() {
            const algorithmPath = document.getElementById('algorithm-select').value;
            const language = document.getElementById('language-select').value;
            
            if (!algorithmPath) {
                alert('Please select an algorithm');
                return;
            }
            
            const response = await fetch('/api/sandbox/create', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    algorithm_path: algorithmPath,
                    language: language
                })
            });
            
            const data = await response.json();
            if (data.success) {
                currentSandboxId = data.sandbox_id;
                document.getElementById('save-btn').disabled = false;
                document.getElementById('run-btn').disabled = false;
                loadSandboxCode();
            } else {
                alert('Error: ' + data.error);
            }
        }
        
        async function loadSandboxCode() {
            if (!currentSandboxId) return;
            
            const response = await fetch(`/api/sandbox/${currentSandboxId}`);
            const data = await response.json();
            
            if (data.current_version) {
                document.getElementById('code-editor').value = data.current_version.code_content;
            }
        }
        
        async function saveCode() {
            if (!currentSandboxId) return;
            
            const code = document.getElementById('code-editor').value;
            
            const response = await fetch(`/api/sandbox/${currentSandboxId}/code`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    code: code,
                    description: 'Manual save'
                })
            });
            
            const data = await response.json();
            if (data.success) {
                alert('Code saved! Version ' + data.version_number);
            }
        }
        
        async function runCode() {
            // Basic execution - will be enhanced later
            document.getElementById('output').textContent = 'Running...';
            // TODO: Implement execution
        }
        
        loadAlgorithms();
    </script>
</body>
</html>
```

**Add route in `web_interface/app.py`:**
```python
@app.route("/sandbox")
def sandbox_page():
    """Sandbox page for students."""
    return render_template("sandbox.html")
```

---

## Step 5: Add Role-Based Access Control (30 minutes)

**Difficulty**: ⭐ Easy  
**Time**: 30 minutes  
**Dependencies**: Step 3, Step 4

### What to do:
1. Add decorator to check user role
2. Protect sandbox routes
3. Show/hide UI elements based on role

### Implementation:

```python
# In web_interface/app.py or sandbox_bp.py
from functools import wraps

def require_role(*allowed_roles):
    """Decorator to require specific role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'error': 'Not authenticated'}), 401
            if session.get('role') not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Use it:
@sandbox_bp.route('/create', methods=['POST'])
@require_role('student', 'professor', 'admin')
def create_sandbox():
    # ... existing code
```

---

## Step 6: Basic Code Execution (1 hour)

**Difficulty**: ⭐⭐ Easy-Medium  
**Time**: 1 hour  
**Dependencies**: Step 4

### What to do:
1. Use existing `framework/python_executor.py` and `framework/java_executor.py`
2. Add execution endpoint
3. Display results in UI

### Implementation:

```python
# In web_interface/sandbox_bp.py
@sandbox_bp.route('/<int:sandbox_id>/execute', methods=['POST'])
@require_role('student', 'professor', 'admin')
def execute_sandbox(sandbox_id):
    """Execute sandbox code."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    # Get sandbox and code
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.algorithm_path, s.language, sv.code_content
        FROM sandboxes s
        JOIN sandbox_versions sv ON s.id = sv.sandbox_id
        WHERE s.id = ? AND s.user_id = ?
        ORDER BY sv.version_number DESC
        LIMIT 1
    """, (sandbox_id, user_id))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return jsonify({'error': 'Sandbox not found'}), 404
    
    algorithm_path, language, code = result
    
    # Execute using existing executors
    if language == 'python':
        from framework.python_executor import PythonExecutor
        executor = PythonExecutor()
        # Create temporary file and execute
        # (Simplified - in production, use proper isolation)
        success, stdout, stderr, exec_time = executor.execute_code(code)
    else:
        from framework.java_executor import JavaExecutor
        executor = JavaExecutor()
        success, stdout, stderr, exec_time = executor.execute_code(code)
    
    return jsonify({
        'success': success,
        'stdout': stdout,
        'stderr': stderr,
        'execution_time': exec_time
    })
```

---

## Step 7: List User's Sandboxes (30 minutes)

**Difficulty**: ⭐ Easy  
**Time**: 30 minutes  
**Dependencies**: Step 3

### What to do:
1. Create sandbox list page
2. Show all user's sandboxes
3. Allow opening sandbox for editing

### Implementation:

```html
<!-- web_interface/templates/sandbox_list.html -->
<!-- Simple list of sandboxes with links to edit -->
```

---

## Summary: Quick Start Path

**Total Time**: ~5 hours for basic working system

### Phase 1 (2 hours): Foundation
1. ✅ Create database schema (30 min)
2. ✅ Create file structure (15 min)
3. ✅ Create API endpoints (1 hour)
4. ✅ Add role-based access (30 min)

### Phase 2 (2 hours): Basic UI
5. ✅ Create sandbox page (1.5 hours)
6. ✅ Basic code execution (30 min)

### Phase 3 (1 hour): Polish
7. ✅ Sandbox list page (30 min)
8. ✅ Testing and bug fixes (30 min)

---

## Next Steps After Quick Start

Once basic system works:

1. **Add Monaco Editor** (2 hours) - Replace textarea with proper code editor
2. **Add Version History UI** (2 hours) - Show version list, allow rollback
3. **Add Basic Comparison** (3 hours) - Compare execution time with original
4. **Add Test Execution** (2 hours) - Run test suite on sandbox code
5. **Add Docker Isolation** (4 hours) - Secure code execution

---

## Testing Checklist

After each step:
- [ ] Test with student account
- [ ] Test with visitor account (should be blocked)
- [ ] Test with professor account
- [ ] Verify database entries
- [ ] Check file system structure
- [ ] Test error handling

---

## Quick Commands

```bash
# Step 1: Create database
python database/setup_sandbox_tables.py

# Step 2: Test file structure
python -c "from framework.sandbox_manager import create_user_sandbox_dir; create_user_sandbox_dir(1)"

# Step 3-7: Start server and test
python scripts/run_web_interface.py
# Visit http://localhost:5000/sandbox
```

---

## Tips

1. **Start Simple**: Use textarea first, upgrade to Monaco later
2. **Test Incrementally**: Test each step before moving to next
3. **Use Existing Code**: Leverage `python_executor.py` and `java_executor.py`
4. **Don't Over-Engineer**: Basic version first, enhance later
5. **Focus on Student Role**: Get student workflow working first

