# Student Sandbox & Testing Framework Improvement Plan

## Executive Summary

This document outlines a comprehensive plan to create an interactive learning environment where students and professors can modify, test, and compare algorithm implementations in a secure sandbox environment, while maintaining the integrity of original algorithms.

---

## 1. User Authentication & Authorization System

### 1.1 User Roles

**Roles:**
- **Visitor/Reader** (default): Read-only access, can view algorithms and results
- **Student**: Can create sandbox copies, modify code, run tests, view comparisons
- **Professor**: Full access including student management, algorithm approval, analytics
- **Admin**: System administration

### 1.2 Authentication Implementation

**Phase 1: Basic Authentication**
- Implement session-based authentication using Flask-Login
- Store user credentials in `database/users.db`
- Password hashing using bcrypt
- Email-based registration with verification (optional)

**Phase 2: OAuth Integration (Optional)**
- Google OAuth for easy student access
- GitHub OAuth for developer students
- Institution SSO support

**Database Schema:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'visitor',  -- visitor, student, professor, admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 2. Sandbox Environment Architecture

### 2.1 Sandbox Concept

Each student gets an isolated workspace where they can:
- Create copies of original algorithms
- Modify code (Python/Java)
- Run tests independently
- Compare results with original implementation
- Save multiple versions of their work

### 2.2 Sandbox Storage Structure

```
sandboxes/
├── {user_id}/
│   ├── {algorithm_path}/
│   │   ├── version_1/          # Original copy
│   │   │   ├── algorithm.py
│   │   │   ├── Algorithm.java
│   │   │   └── metadata.json
│   │   ├── version_2/          # Student modification
│   │   │   ├── algorithm.py
│   │   │   ├── Algorithm.java
│   │   │   └── metadata.json
│   │   └── current/            # Symlink to active version
│   └── .sandbox_config.json
```

### 2.3 Sandbox Database Schema

```sql
CREATE TABLE sandboxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    algorithm_path TEXT NOT NULL,
    language TEXT NOT NULL,  -- 'python' or 'java'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, algorithm_path, language)
);

CREATE TABLE sandbox_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    code_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id),
    UNIQUE(sandbox_id, version_number)
);

CREATE TABLE sandbox_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    execution_time_ms REAL,
    memory_usage_kb REAL,
    cpu_usage_percent REAL,
    status TEXT NOT NULL,  -- 'success', 'failure', 'timeout', 'error'
    output TEXT,
    error_message TEXT,
    test_results JSON,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id)
);
```

---

## 3. Code Editor & Execution Interface

### 3.1 Web-Based Code Editor

**Technology Stack:**
- **Monaco Editor** (VS Code editor in browser) or **CodeMirror 6**
- Syntax highlighting for Python and Java
- Auto-completion and basic linting
- Line numbers, code folding, search/replace

**Features:**
- Split view: Original code (read-only) | Student code (editable)
- Real-time syntax validation
- Code diff visualization
- Save/load versions
- Undo/redo functionality

### 3.2 Execution Environment

**Isolated Execution:**
- **Docker containers** for each execution (recommended)
- **Process isolation** with resource limits (alternative)
- Timeout protection (max 30 seconds per execution)
- Memory limits (max 512MB per execution)
- CPU throttling

**Security Measures:**
- No network access from sandbox
- Restricted file system access (read-only original, write-only sandbox)
- Blocked system calls (file deletion, process spawning, etc.)
- Input sanitization
- Output size limits

---

## 4. Testing Framework Improvements

### 4.1 Enhanced Test Suite

**Test Categories:**

1. **Correctness Tests**
   - Unit tests for core functionality
   - Edge case testing
   - Boundary condition testing
   - Input validation tests

2. **Performance Tests**
   - Execution time benchmarks
   - Memory usage profiling
   - CPU utilization tracking
   - Scalability tests (various input sizes)

3. **Resource Tests**
   - Memory leak detection
   - File handle management
   - Thread safety (for concurrent algorithms)

4. **Regression Tests**
   - Ensure original functionality preserved
   - Output format validation
   - API contract compliance

### 4.2 Test Configuration

**Test Definition Format (YAML/JSON):**
```yaml
algorithm: bubble_sort
language: python
tests:
  correctness:
    - name: basic_sorting
      input: [64, 34, 25, 12, 22, 11, 90]
      expected_output: [11, 12, 22, 25, 34, 64, 90]
      timeout: 5s
    
    - name: empty_array
      input: []
      expected_output: []
      timeout: 1s
    
    - name: single_element
      input: [42]
      expected_output: [42]
      timeout: 1s

  performance:
    - name: small_dataset
      input_size: 100
      max_time_ms: 100
      max_memory_kb: 1024
    
    - name: medium_dataset
      input_size: 1000
      max_time_ms: 1000
      max_memory_kb: 2048

  regression:
    - name: output_format
      input: [3, 1, 4, 1, 5]
      validate: 
        type: list
        length: 5
        sorted: true
```

### 4.3 Test Execution Engine

**Components:**
- Test runner with timeout and resource monitoring
- Result collector and analyzer
- Comparison engine (original vs modified)
- Report generator

**Execution Flow:**
1. Load original algorithm
2. Load student's modified algorithm
3. Run both through same test suite
4. Collect metrics (time, memory, CPU, correctness)
5. Compare results
6. Generate comparison report

---

## 5. Comparison & Analysis System

### 5.1 Comparison Metrics

**Performance Metrics:**
- Execution time (wall clock, CPU time)
- Memory usage (peak, average, final)
- CPU utilization
- Time complexity analysis (if possible)

**Correctness Metrics:**
- Test pass rate
- Output accuracy (for numerical algorithms)
- Edge case handling
- Error handling

**Code Quality Metrics:**
- Code complexity (cyclomatic complexity)
- Code style compliance (PEP 8, Java conventions)
- Code size (lines of code, function count)

### 5.2 Comparison Report

**Visual Dashboard:**
- Side-by-side comparison charts
- Performance graphs (time, memory over input sizes)
- Test results matrix (pass/fail for each test)
- Code diff visualization
- Improvement/degradation indicators

**Report Sections:**
1. **Summary**: Overall comparison score
2. **Correctness**: Test results comparison
3. **Performance**: Speed and resource usage
4. **Code Quality**: Style and complexity
5. **Recommendations**: Suggestions for improvement

### 5.3 Algorithm Purpose Validation

**Purpose Preservation Checks:**
- Function signature must match (name, parameters, return type)
- Core algorithm logic category must remain (sorting, searching, etc.)
- Input/output contract must be preserved
- Algorithm class/type must not change

**Validation Rules:**
```python
def validate_algorithm_purpose(original, modified):
    """
    Ensure modified algorithm maintains original purpose.
    """
    checks = {
        'function_name': original.name == modified.name,
        'signature': original.signature == modified.signature,
        'return_type': original.return_type == modified.return_type,
        'algorithm_type': original.category == modified.category,
        'core_logic': detect_core_algorithm_type(original) == 
                      detect_core_algorithm_type(modified)
    }
    return all(checks.values()), checks
```

---

## 5A. DETAILED: Comparison with Original Implementation

### 5A.1 Performance Comparison System

**Architecture:**
```python
class PerformanceComparator:
    """
    Compare performance metrics between original and modified algorithms.
    """
    
    def __init__(self, original_code, modified_code, language):
        self.original_code = original_code
        self.modified_code = modified_code
        self.language = language
        self.test_suite = self.load_test_suite()
    
    def run_comparison(self, input_sizes=[10, 100, 1000, 10000]):
        """
        Run both algorithms on multiple input sizes and compare.
        """
        results = {
            'original': [],
            'modified': [],
            'comparison': {}
        }
        
        for size in input_sizes:
            test_data = self.generate_test_data(size)
            
            # Run original
            orig_metrics = self.execute_with_profiling(
                self.original_code, test_data
            )
            
            # Run modified
            mod_metrics = self.execute_with_profiling(
                self.modified_code, test_data
            )
            
            results['original'].append({
                'input_size': size,
                'execution_time_ms': orig_metrics['time'],
                'memory_peak_kb': orig_metrics['memory_peak'],
                'memory_avg_kb': orig_metrics['memory_avg'],
                'cpu_percent': orig_metrics['cpu']
            })
            
            results['modified'].append({
                'input_size': size,
                'execution_time_ms': mod_metrics['time'],
                'memory_peak_kb': mod_metrics['memory_peak'],
                'memory_avg_kb': mod_metrics['memory_avg'],
                'cpu_percent': mod_metrics['cpu']
            })
            
            # Calculate improvements/degradations
            results['comparison'][size] = {
                'time_improvement': self.calculate_improvement(
                    orig_metrics['time'], mod_metrics['time']
                ),
                'memory_improvement': self.calculate_improvement(
                    orig_metrics['memory_peak'], mod_metrics['memory_peak'],
                    lower_is_better=True
                ),
                'cpu_improvement': self.calculate_improvement(
                    orig_metrics['cpu'], mod_metrics['cpu'],
                    lower_is_better=True
                )
            }
        
        return results
```

**Profiling Implementation:**

**For Python:**
```python
import cProfile
import pstats
import tracemalloc
import time
import psutil
import os

def execute_with_profiling(code, test_data):
    """
    Execute code with comprehensive profiling.
    """
    # Start memory tracking
    tracemalloc.start()
    process = psutil.Process(os.getpid())
    
    # Start CPU monitoring
    cpu_before = process.cpu_percent()
    
    # Start time tracking
    start_time = time.perf_counter()
    
    # Execute code in isolated namespace
    namespace = {'input_data': test_data}
    exec(compile(code, '<string>', 'exec'), namespace)
    
    # Calculate metrics
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000  # Convert to ms
    
    # Memory metrics
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_peak = peak / 1024  # Convert to KB
    memory_avg = current / 1024
    
    # CPU metrics
    cpu_after = process.cpu_percent()
    cpu_usage = cpu_after - cpu_before
    
    return {
        'time': execution_time,
        'memory_peak': memory_peak,
        'memory_avg': memory_avg,
        'cpu': cpu_usage
    }
```

**For Java:**
```java
// Using JVM profiling tools
public class PerformanceProfiler {
    public static ExecutionMetrics profileExecution(
        String code, Object[] testData
    ) {
        // Start JVM profiling
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        
        long cpuBefore = threadBean.getCurrentThreadCpuTime();
        long memoryBefore = memoryBean.getHeapMemoryUsage().getUsed();
        long startTime = System.nanoTime();
        
        // Execute code
        Object result = executeCode(code, testData);
        
        long endTime = System.nanoTime();
        long cpuAfter = threadBean.getCurrentThreadCpuTime();
        long memoryAfter = memoryBean.getHeapMemoryUsage().getUsed();
        
        return new ExecutionMetrics(
            (endTime - startTime) / 1_000_000.0,  // ms
            (memoryAfter - memoryBefore) / 1024.0,  // KB
            (cpuAfter - cpuBefore) / 1_000_000.0  // ms
        );
    }
}
```

**Performance Comparison Metrics:**

```python
def calculate_improvement(original_value, modified_value, lower_is_better=False):
    """
    Calculate percentage improvement/degradation.
    
    Returns:
        {
            'percentage': float,  # Positive = improvement, Negative = degradation
            'status': str,  # 'improved', 'degraded', 'unchanged'
            'significance': str  # 'significant', 'moderate', 'negligible'
        }
    """
    if original_value == 0:
        return {'percentage': 0, 'status': 'unchanged', 'significance': 'negligible'}
    
    if lower_is_better:
        # For memory/CPU: lower is better
        change = ((original_value - modified_value) / original_value) * 100
    else:
        # For speed: higher is better
        change = ((modified_value - original_value) / original_value) * 100
    
    # Determine significance
    abs_change = abs(change)
    if abs_change < 1:
        significance = 'negligible'
    elif abs_change < 10:
        significance = 'moderate'
    else:
        significance = 'significant'
    
    status = 'improved' if change > 0 else 'degraded' if change < 0 else 'unchanged'
    
    return {
        'percentage': round(change, 2),
        'status': status,
        'significance': significance
    }
```

### 5A.2 Resource Usage Comparison

**Resource Monitoring:**

```python
class ResourceMonitor:
    """
    Monitor and compare resource usage between implementations.
    """
    
    def __init__(self):
        self.monitored_resources = {
            'memory': [],
            'cpu': [],
            'disk_io': [],
            'network_io': [],
            'file_handles': []
        }
    
    def monitor_execution(self, code, test_data):
        """
        Monitor resource usage during code execution.
        """
        import resource
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Memory tracking
        memory_samples = []
        memory_before = process.memory_info().rss / 1024  # KB
        
        # CPU tracking
        cpu_samples = []
        cpu_before = process.cpu_percent()
        
        # File handles
        handles_before = len(process.open_files())
        
        # Execute with periodic sampling
        start_time = time.time()
        sampling_interval = 0.01  # 10ms
        
        # Run in separate thread to allow sampling
        result = self.execute_with_sampling(
            code, test_data, sampling_interval,
            memory_samples, cpu_samples
        )
        
        # Final measurements
        memory_after = process.memory_info().rss / 1024
        cpu_after = process.cpu_percent()
        handles_after = len(process.open_files())
        
        return {
            'memory': {
                'peak': max(memory_samples) if memory_samples else memory_after,
                'average': sum(memory_samples) / len(memory_samples) if memory_samples else memory_after,
                'final': memory_after,
                'leak_detected': self.detect_memory_leak(memory_samples)
            },
            'cpu': {
                'peak': max(cpu_samples) if cpu_samples else cpu_after,
                'average': sum(cpu_samples) / len(cpu_samples) if cpu_samples else cpu_after,
                'final': cpu_after
            },
            'file_handles': {
                'before': handles_before,
                'after': handles_after,
                'leak_detected': handles_after > handles_before * 1.1
            }
        }
    
    def detect_memory_leak(self, memory_samples):
        """
        Detect potential memory leaks by analyzing memory trend.
        """
        if len(memory_samples) < 10:
            return False
        
        # Simple linear regression to detect upward trend
        from scipy import stats
        x = list(range(len(memory_samples)))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, memory_samples)
        
        # If slope is positive and significant, potential leak
        return slope > 0 and p_value < 0.05
```

### 5A.3 Correctness Comparison

**Correctness Testing Framework:**

```python
class CorrectnessComparator:
    """
    Compare correctness of original vs modified algorithm.
    """
    
    def __init__(self, original_code, modified_code, test_suite):
        self.original_code = original_code
        self.modified_code = modified_code
        self.test_suite = test_suite
    
    def run_correctness_tests(self):
        """
        Run all tests on both implementations and compare results.
        """
        results = {
            'original': {'passed': 0, 'failed': 0, 'tests': []},
            'modified': {'passed': 0, 'failed': 0, 'tests': []},
            'comparison': {
                'all_match': True,
                'regressions': [],
                'improvements': []
            }
        }
        
        for test_case in self.test_suite:
            # Run original
            orig_result = self.run_test(self.original_code, test_case)
            
            # Run modified
            mod_result = self.run_test(self.modified_code, test_case)
            
            # Compare results
            match = self.compare_results(orig_result, mod_result, test_case)
            
            # Record results
            results['original']['tests'].append({
                'name': test_case['name'],
                'status': orig_result['status'],
                'output': orig_result['output'],
                'error': orig_result.get('error')
            })
            
            results['modified']['tests'].append({
                'name': test_case['name'],
                'status': mod_result['status'],
                'output': mod_result['output'],
                'error': mod_result.get('error')
            })
            
            # Update statistics
            if orig_result['status'] == 'passed':
                results['original']['passed'] += 1
            else:
                results['original']['failed'] += 1
            
            if mod_result['status'] == 'passed':
                results['modified']['passed'] += 1
            else:
                results['modified']['failed'] += 1
            
            # Check for regressions
            if orig_result['status'] == 'passed' and mod_result['status'] == 'failed':
                results['comparison']['all_match'] = False
                results['comparison']['regressions'].append({
                    'test': test_case['name'],
                    'original_output': orig_result['output'],
                    'modified_output': mod_result.get('output'),
                    'error': mod_result.get('error')
                })
            
            # Check for improvements (fixed bugs)
            if orig_result['status'] == 'failed' and mod_result['status'] == 'passed':
                results['comparison']['improvements'].append({
                    'test': test_case['name'],
                    'original_error': orig_result.get('error'),
                    'modified_output': mod_result['output']
                })
        
        return results
    
    def compare_results(self, orig_result, mod_result, test_case):
        """
        Compare outputs with appropriate comparison method.
        """
        if test_case.get('comparison_method') == 'exact':
            return orig_result['output'] == mod_result['output']
        elif test_case.get('comparison_method') == 'numerical':
            # For numerical algorithms, allow small floating point differences
            tolerance = test_case.get('tolerance', 1e-6)
            return abs(orig_result['output'] - mod_result['output']) < tolerance
        elif test_case.get('comparison_method') == 'sorted':
            # For sorting algorithms, check if both are sorted and contain same elements
            return (self.is_sorted(mod_result['output']) and
                    set(orig_result['output']) == set(mod_result['output']))
        else:
            # Default: structural equality
            return orig_result['output'] == mod_result['output']
```

**Output Accuracy Analysis:**

```python
def analyze_output_accuracy(original_output, modified_output, expected_output):
    """
    Analyze accuracy of outputs for numerical algorithms.
    """
    if isinstance(expected_output, (int, float)):
        orig_error = abs(original_output - expected_output)
        mod_error = abs(modified_output - expected_output)
        
        return {
            'original_accuracy': 100 * (1 - orig_error / abs(expected_output)) if expected_output != 0 else 100,
            'modified_accuracy': 100 * (1 - mod_error / abs(expected_output)) if expected_output != 0 else 100,
            'improvement': mod_error < orig_error
        }
    elif isinstance(expected_output, list):
        # For list outputs, calculate element-wise accuracy
        if len(original_output) != len(modified_output) != len(expected_output):
            return {'error': 'Length mismatch'}
        
        orig_accuracies = [
            abs(o - e) / abs(e) if e != 0 else abs(o - e)
            for o, e in zip(original_output, expected_output)
        ]
        mod_accuracies = [
            abs(m - e) / abs(e) if e != 0 else abs(m - e)
            for m, e in zip(modified_output, expected_output)
        ]
        
        return {
            'original_avg_error': sum(orig_accuracies) / len(orig_accuracies),
            'modified_avg_error': sum(mod_accuracies) / len(mod_accuracies),
            'improvement': sum(mod_accuracies) < sum(orig_accuracies)
        }
```

---

## 5B. DETAILED: Version History & Rollback System

### 5B.1 Version Management Architecture

**Database Schema for Versions:**

```sql
CREATE TABLE sandbox_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id INTEGER NOT NULL,
    version_number INTEGER NOT NULL,
    parent_version_id INTEGER,  -- For branching
    code_content TEXT NOT NULL,
    language TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL,  -- user_id
    description TEXT,
    tags TEXT,  -- JSON array of tags
    is_current BOOLEAN DEFAULT 0,
    execution_count INTEGER DEFAULT 0,
    last_executed_at TIMESTAMP,
    FOREIGN KEY (sandbox_id) REFERENCES sandboxes(id),
    FOREIGN KEY (parent_version_id) REFERENCES sandbox_versions(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    UNIQUE(sandbox_id, version_number)
);

CREATE TABLE version_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    FOREIGN KEY (version_id) REFERENCES sandbox_versions(id),
    UNIQUE(version_id, key)
);

CREATE TABLE version_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER NOT NULL,
    execution_time_ms REAL,
    memory_usage_kb REAL,
    status TEXT NOT NULL,
    test_results JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (version_id) REFERENCES sandbox_versions(id)
);
```

**Version Management Class:**

```python
class VersionManager:
    """
    Manage versions of student code with full history and rollback.
    """
    
    def __init__(self, sandbox_id, db_connection):
        self.sandbox_id = sandbox_id
        self.db = db_connection
    
    def create_version(self, code_content, language, user_id, 
                      description=None, parent_version_id=None, tags=None):
        """
        Create a new version of the code.
        """
        cursor = self.db.cursor()
        
        # Get next version number
        cursor.execute("""
            SELECT MAX(version_number) 
            FROM sandbox_versions 
            WHERE sandbox_id = ?
        """, (self.sandbox_id,))
        max_version = cursor.fetchone()[0]
        next_version = (max_version or 0) + 1
        
        # Mark previous version as not current
        cursor.execute("""
            UPDATE sandbox_versions 
            SET is_current = 0 
            WHERE sandbox_id = ? AND is_current = 1
        """, (self.sandbox_id,))
        
        # Insert new version
        cursor.execute("""
            INSERT INTO sandbox_versions 
            (sandbox_id, version_number, parent_version_id, code_content, 
             language, created_by, description, tags, is_current)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            self.sandbox_id, next_version, parent_version_id,
            code_content, language, user_id, description,
            json.dumps(tags) if tags else None
        ))
        
        version_id = cursor.lastrowid
        self.db.commit()
        
        # Store code in file system
        self._store_version_file(version_id, code_content, language)
        
        return version_id, next_version
    
    def get_version(self, version_number):
        """
        Retrieve a specific version.
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, version_number, code_content, language, 
                   created_at, description, tags, is_current,
                   execution_count, last_executed_at
            FROM sandbox_versions
            WHERE sandbox_id = ? AND version_number = ?
        """, (self.sandbox_id, version_number))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'id': row[0],
            'version_number': row[1],
            'code_content': row[2],
            'language': row[3],
            'created_at': row[4],
            'description': row[5],
            'tags': json.loads(row[6]) if row[6] else [],
            'is_current': bool(row[7]),
            'execution_count': row[8],
            'last_executed_at': row[9]
        }
    
    def list_versions(self, limit=50, offset=0):
        """
        List all versions with pagination.
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, version_number, created_at, description, 
                   is_current, execution_count, last_executed_at
            FROM sandbox_versions
            WHERE sandbox_id = ?
            ORDER BY version_number DESC
            LIMIT ? OFFSET ?
        """, (self.sandbox_id, limit, offset))
        
        return [
            {
                'id': row[0],
                'version_number': row[1],
                'created_at': row[2],
                'description': row[3],
                'is_current': bool(row[4]),
                'execution_count': row[5],
                'last_executed_at': row[6]
            }
            for row in cursor.fetchall()
        ]
    
    def rollback_to_version(self, version_number, user_id, 
                           create_new_version=True):
        """
        Rollback to a specific version.
        
        If create_new_version=True, creates a new version with the old code.
        If False, just marks the old version as current.
        """
        target_version = self.get_version(version_number)
        if not target_version:
            raise ValueError(f"Version {version_number} not found")
        
        if create_new_version:
            # Create a new version with the old code (preserves history)
            return self.create_version(
                code_content=target_version['code_content'],
                language=target_version['language'],
                user_id=user_id,
                description=f"Rollback to version {version_number}",
                parent_version_id=target_version['id']
            )
        else:
            # Just mark the old version as current
            cursor = self.db.cursor()
            cursor.execute("""
                UPDATE sandbox_versions 
                SET is_current = 0 
                WHERE sandbox_id = ? AND is_current = 1
            """, (self.sandbox_id,))
            
            cursor.execute("""
                UPDATE sandbox_versions 
                SET is_current = 1 
                WHERE sandbox_id = ? AND version_number = ?
            """, (self.sandbox_id, version_number))
            
            self.db.commit()
            return None, version_number
    
    def compare_versions(self, version1, version2):
        """
        Compare two versions and return diff.
        """
        v1 = self.get_version(version1)
        v2 = self.get_version(version2)
        
        if not v1 or not v2:
            return None
        
        # Use difflib for text comparison
        import difflib
        
        diff = list(difflib.unified_diff(
            v1['code_content'].splitlines(keepends=True),
            v2['code_content'].splitlines(keepends=True),
            fromfile=f"Version {version1}",
            tofile=f"Version {version2}",
            lineterm=''
        ))
        
        # Calculate statistics
        added_lines = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
        removed_lines = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
        
        return {
            'diff': ''.join(diff),
            'statistics': {
                'lines_added': added_lines,
                'lines_removed': removed_lines,
                'net_change': added_lines - removed_lines
            },
            'version1': v1,
            'version2': v2
        }
    
    def get_version_tree(self):
        """
        Get version tree showing branching and relationships.
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id, version_number, parent_version_id, created_at, 
                   description, is_current
            FROM sandbox_versions
            WHERE sandbox_id = ?
            ORDER BY version_number
        """, (self.sandbox_id,))
        
        versions = {}
        root_versions = []
        
        for row in cursor.fetchall():
            version = {
                'id': row[0],
                'version_number': row[1],
                'parent_version_id': row[2],
                'created_at': row[3],
                'description': row[4],
                'is_current': bool(row[5]),
                'children': []
            }
            versions[row[1]] = version
            
            if row[2] is None:
                root_versions.append(version)
            else:
                # Find parent and add as child
                parent_version = next(
                    (v for v in versions.values() if v['id'] == row[2]),
                    None
                )
                if parent_version:
                    parent_version['children'].append(version)
        
        return {
            'root_versions': root_versions,
            'all_versions': versions
        }
    
    def _store_version_file(self, version_id, code_content, language):
        """
        Store version code in file system for quick access.
        """
        sandbox_path = Path(f"sandboxes/{self.sandbox_id}")
        version_path = sandbox_path / f"version_{version_id}"
        version_path.mkdir(parents=True, exist_ok=True)
        
        file_extension = '.py' if language == 'python' else '.java'
        file_name = f"algorithm{file_extension}"
        
        (version_path / file_name).write_text(code_content, encoding='utf-8')
```

### 5B.2 Version History UI

**Timeline View:**

```html
<!-- Version History Timeline -->
<div class="version-timeline">
    <div class="timeline-header">
        <h3>Version History</h3>
        <button onclick="createNewVersion()">Save Current as New Version</button>
    </div>
    
    <div class="timeline-container">
        <!-- Version items -->
        <div class="version-item current" data-version="5">
            <div class="version-number">v5</div>
            <div class="version-info">
                <div class="version-date">2025-11-21 18:30:00</div>
                <div class="version-description">Optimized bubble sort</div>
                <div class="version-stats">
                    <span>✓ 12 tests passed</span>
                    <span>⚡ 15% faster</span>
                    <span>💾 8% less memory</span>
                </div>
            </div>
            <div class="version-actions">
                <button onclick="viewVersion(5)">View</button>
                <button onclick="rollbackToVersion(5)">Rollback</button>
                <button onclick="compareVersions(4, 5)">Compare</button>
            </div>
        </div>
        
        <div class="version-item" data-version="4">
            <!-- Similar structure -->
        </div>
        
        <!-- More versions... -->
    </div>
</div>
```

**Version Comparison View:**

```javascript
function compareVersions(version1, version2) {
    fetch(`/api/sandboxes/${sandboxId}/versions/${version1}/compare/${version2}`)
        .then(response => response.json())
        .then(data => {
            // Display side-by-side diff
            displayDiff(data.diff);
            
            // Show statistics
            displayStatistics(data.statistics);
            
            // Show performance comparison if available
            if (data.performance_comparison) {
                displayPerformanceComparison(data.performance_comparison);
            }
        });
}

function displayDiff(diff) {
    const diffViewer = document.getElementById('diff-viewer');
    diffViewer.innerHTML = '';
    
    // Use a diff library like diff2html or CodeMirror merge
    const diff2htmlUi = new Diff2HtmlUI(diffViewer, diff, {
        drawFileList: false,
        matching: 'lines',
        outputFormat: 'side-by-side'
    });
    diff2htmlUi.draw();
}
```

---

## 5C. DETAILED: Results Visualization System

### 5C.1 Performance Visualization

**Interactive Charts:**

```javascript
// Using Chart.js for performance visualization
class PerformanceVisualizer {
    constructor(containerId, comparisonData) {
        this.container = document.getElementById(containerId);
        this.data = comparisonData;
        this.charts = {};
    }
    
    renderExecutionTimeChart() {
        const ctx = document.createElement('canvas');
        this.container.appendChild(ctx);
        
        const chartData = {
            labels: this.data.input_sizes,
            datasets: [
                {
                    label: 'Original',
                    data: this.data.original.execution_times,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                },
                {
                    label: 'Your Version',
                    data: this.data.modified.execution_times,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.1
                }
            ]
        };
        
        this.charts.executionTime = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Execution Time Comparison'
                    },
                    legend: {
                        display: true
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const improvement = calculateImprovement(
                                    context.datasetIndex === 0 ? 
                                    context.raw : 
                                    getOriginalValue(context.dataIndex),
                                    context.raw
                                );
                                return `${context.dataset.label}: ${context.raw}ms ${improvement}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time (ms)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Input Size'
                        }
                    }
                }
            }
        });
    }
    
    renderMemoryUsageChart() {
        // Similar implementation for memory usage
    }
    
    renderImprovementHeatmap() {
        // Heatmap showing improvements/degradations across different metrics
        const heatmapData = {
            labels: ['Execution Time', 'Memory Peak', 'Memory Avg', 'CPU Usage'],
            datasets: [{
                label: 'Improvement %',
                data: [
                    this.data.comparison.time_improvement,
                    this.data.comparison.memory_peak_improvement,
                    this.data.comparison.memory_avg_improvement,
                    this.data.comparison.cpu_improvement
                ],
                backgroundColor: function(context) {
                    const value = context.parsed.y;
                    if (value > 10) return 'rgba(0, 255, 0, 0.6)';  // Green - significant improvement
                    if (value > 0) return 'rgba(144, 238, 144, 0.6)';  // Light green - improvement
                    if (value > -10) return 'rgba(255, 255, 0, 0.6)';  // Yellow - minor degradation
                    return 'rgba(255, 0, 0, 0.6)';  // Red - significant degradation
                }
            }]
        };
        
        // Render bar chart with color coding
    }
}
```

### 5C.2 Test Results Visualization

**Test Results Matrix:**

```html
<div class="test-results-matrix">
    <table class="comparison-table">
        <thead>
            <tr>
                <th>Test Case</th>
                <th>Original</th>
                <th>Your Version</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
            <tr class="test-pass">
                <td>Basic Sorting</td>
                <td>
                    <span class="status-badge success">✓ Passed</span>
                    <span class="time">2.3ms</span>
                </td>
                <td>
                    <span class="status-badge success">✓ Passed</span>
                    <span class="time">1.8ms</span>
                    <span class="improvement">⚡ 22% faster</span>
                </td>
                <td><span class="status-icon improved">↗</span></td>
                <td><button onclick="showTestDetails('basic_sort')">View</button></td>
            </tr>
            <tr class="test-fail">
                <td>Large Array (10k)</td>
                <td>
                    <span class="status-badge success">✓ Passed</span>
                    <span class="time">45.2ms</span>
                </td>
                <td>
                    <span class="status-badge error">✗ Timeout</span>
                    <span class="time">>30s</span>
                </td>
                <td><span class="status-icon regression">↘</span></td>
                <td><button onclick="showTestDetails('large_array')">View</button></td>
            </tr>
            <!-- More test rows... -->
        </tbody>
    </table>
</div>
```

**Progress Indicators:**

```javascript
function renderOverallScore(comparisonData) {
    // Calculate overall score
    const score = calculateOverallScore(comparisonData);
    
    // Render circular progress indicator
    const canvas = document.getElementById('score-chart');
    const ctx = canvas.getContext('2d');
    
    // Draw circular progress
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    
    // Background circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 20;
    ctx.stroke();
    
    // Progress circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, -Math.PI / 2, 
            (-Math.PI / 2) + (2 * Math.PI * score / 100));
    ctx.strokeStyle = score >= 70 ? '#4caf50' : score >= 50 ? '#ff9800' : '#f44336';
    ctx.lineWidth = 20;
    ctx.lineCap = 'round';
    ctx.stroke();
    
    // Score text
    ctx.fillStyle = '#333';
    ctx.font = 'bold 36px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${score}%`, centerX, centerY);
}
```

### 5C.3 Code Diff Visualization

**Side-by-Side Code Comparison:**

```html
<div class="code-comparison-view">
    <div class="comparison-header">
        <div class="original-header">
            <h4>Original (v1)</h4>
            <span class="file-info">bubble_sort.py • 45 lines</span>
        </div>
        <div class="modified-header">
            <h4>Your Version (v5)</h4>
            <span class="file-info">bubble_sort.py • 52 lines</span>
        </div>
    </div>
    
    <div class="code-diff-container">
        <div class="original-code">
            <div class="code-line unchanged">
                <span class="line-number">1</span>
                <span class="code-content">def bubble_sort(arr):</span>
            </div>
            <div class="code-line unchanged">
                <span class="line-number">2</span>
                <span class="code-content">    n = len(arr)</span>
            </div>
            <div class="code-line removed">
                <span class="line-number">3</span>
                <span class="code-content">    for i in range(n):</span>
            </div>
            <!-- More lines... -->
        </div>
        
        <div class="modified-code">
            <div class="code-line unchanged">
                <span class="line-number">1</span>
                <span class="code-content">def bubble_sort(arr):</span>
            </div>
            <div class="code-line unchanged">
                <span class="line-number">2</span>
                <span class="code-content">    n = len(arr)</span>
            </div>
            <div class="code-line added">
                <span class="line-number">3</span>
                <span class="code-content">    # Optimized with early termination</span>
            </div>
            <div class="code-line added">
                <span class="line-number">4</span>
                <span class="code-content">    for i in range(n):</span>
            </div>
            <!-- More lines... -->
        </div>
    </div>
</div>
```

**Diff Statistics:**

```javascript
function renderDiffStatistics(diffData) {
    const stats = {
        'Lines Added': diffData.statistics.lines_added,
        'Lines Removed': diffData.statistics.lines_removed,
        'Net Change': diffData.statistics.net_change,
        'Files Changed': 1,
        'Complexity Change': calculateComplexityChange(diffData)
    };
    
    // Render as cards or bar chart
    Object.entries(stats).forEach(([label, value]) => {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
            <div class="stat-label">${label}</div>
            <div class="stat-value ${value >= 0 ? 'positive' : 'negative'}">
                ${value >= 0 ? '+' : ''}${value}
            </div>
        `;
        document.getElementById('diff-stats').appendChild(card);
    });
}
```

### 5C.4 Real-time Execution Visualization

**Live Execution Monitor:**

```javascript
class ExecutionMonitor {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.metrics = {
            time: [],
            memory: [],
            cpu: []
        };
    }
    
    startMonitoring(executionId) {
        // Connect to WebSocket for real-time updates
        this.ws = new WebSocket(`ws://localhost:5000/ws/execution/${executionId}`);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateMetrics(data);
            this.renderMetrics();
        };
    }
    
    updateMetrics(data) {
        this.metrics.time.push({
            timestamp: data.timestamp,
            value: data.execution_time
        });
        this.metrics.memory.push({
            timestamp: data.timestamp,
            value: data.memory_usage
        });
        this.metrics.cpu.push({
            timestamp: data.timestamp,
            value: data.cpu_usage
        });
    }
    
    renderMetrics() {
        // Update real-time charts
        this.updateTimeChart();
        this.updateMemoryChart();
        this.updateCPUChart();
    }
}
```

---

## Summary

These detailed implementations provide:

1. **Comprehensive Comparison**: Performance, resources, and correctness metrics with statistical analysis
2. **Full Version History**: Complete versioning system with rollback, branching, and diff capabilities
3. **Rich Visualizations**: Interactive charts, test matrices, code diffs, and real-time monitoring

All components are designed to be modular, extensible, and user-friendly.

---

## 6. User Interface Design

### 6.1 Sandbox Dashboard

**Main Page:**
- List of algorithms available for sandboxing
- Student's active sandboxes
- Recent executions and results
- Quick stats (total sandboxes, success rate, etc.)

### 6.2 Algorithm Sandbox Page

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Algorithm: Bubble Sort                    [Save] [Run]  │
├──────────────────┬──────────────────────────────────────┤
│ ORIGINAL (RO)    │ YOUR VERSION (Editable)              │
│                  │                                       │
│ [Code Editor]    │ [Code Editor]                        │
│                  │                                       │
│                  │                                       │
├──────────────────┴──────────────────────────────────────┤
│ Test Results & Comparison                               │
│ ┌──────────────┬──────────────┬─────────────────────┐  │
│ │ Test         │ Original     │ Your Version        │  │
│ ├──────────────┼──────────────┼─────────────────────┤  │
│ │ Basic Sort   │ ✓ 2.3ms      │ ✓ 1.8ms (faster!)  │  │
│ │ Empty Array  │ ✓ 0.1ms      │ ✓ 0.1ms            │  │
│ │ Large Array  │ ✓ 45.2ms     │ ✗ Timeout          │  │
│ └──────────────┴──────────────┴─────────────────────┘  │
│                                                          │
│ Performance Comparison:                                  │
│ [Chart: Execution Time vs Input Size]                   │
│ [Chart: Memory Usage Comparison]                        │
└─────────────────────────────────────────────────────────┘
```

### 6.3 Version History

- Timeline view of all versions
- Diff between versions
- Restore previous versions
- Branch/merge capabilities (advanced)

---

## 7. Security & Isolation

### 7.1 Code Execution Security

**Docker-Based Isolation (Recommended):**
```dockerfile
# Python sandbox
FROM python:3.11-slim
RUN useradd -m sandbox
USER sandbox
WORKDIR /sandbox
# Restricted environment, no network, limited resources
```

**Resource Limits:**
- CPU: 1 core, 50% throttle
- Memory: 512MB hard limit
- Disk: 100MB temporary space
- Network: Blocked (except for test data)
- Time: 30 second timeout

**Process Isolation (Alternative):**
- Use `subprocess` with resource limits
- `ulimit` for memory/CPU
- `chroot` or `nsjail` for filesystem isolation
- `seccomp` for system call filtering

### 7.2 Code Analysis & Validation

**Pre-Execution Checks:**
- Block dangerous imports (`os`, `subprocess`, `sys` with modifications)
- Block file system operations (except read-only test data)
- Block network operations
- Block process spawning
- Validate code structure (AST analysis)

**Static Analysis:**
- AST parsing to detect dangerous patterns
- Import whitelist/blacklist
- Function call restrictions
- Resource usage estimation

### 7.3 Data Protection

- Student code is private (only student and professor can view)
- Original algorithms remain read-only
- No access to other students' sandboxes
- Audit log for all executions

---

## 8. Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- [ ] User authentication system
- [ ] Role-based access control
- [ ] Basic sandbox database schema
- [ ] Sandbox file system structure

### Phase 2: Code Editor (Weeks 3-4)
- [ ] Web-based code editor integration
- [ ] Code save/load functionality
- [ ] Version management
- [ ] Basic UI for sandbox page

### Phase 3: Execution Engine (Weeks 5-6)
- [ ] Docker container setup
- [ ] Isolated execution environment
- [ ] Resource monitoring
- [ ] Timeout and error handling

### Phase 4: Testing Framework (Weeks 7-8)
- [ ] Enhanced test suite format
- [ ] Test execution engine
- [ ] Test result collection
- [ ] Basic comparison system

### Phase 5: Comparison & Analysis (Weeks 9-10)
- [ ] Performance metrics collection
- [ ] Comparison algorithms
- [ ] Visualization components
- [ ] Report generation

### Phase 6: UI/UX Polish (Weeks 11-12)
- [ ] Dashboard design
- [ ] Interactive charts
- [ ] Version history UI
- [ ] Mobile responsiveness

### Phase 7: Security Hardening (Week 13)
- [ ] Security audit
- [ ] Penetration testing
- [ ] Code analysis improvements
- [ ] Documentation

### Phase 8: Testing & Deployment (Week 14)
- [ ] Integration testing
- [ ] Performance testing
- [ ] User acceptance testing
- [ ] Production deployment

---

## 9. Technical Stack Recommendations

### Backend
- **Framework**: Flask (current) or FastAPI (for async execution)
- **Database**: SQLite (current) or PostgreSQL (for production)
- **Containerization**: Docker + Docker Compose
- **Task Queue**: Celery + Redis (for async test execution)
- **Caching**: Redis (for test results, user sessions)

### Frontend
- **Code Editor**: Monaco Editor or CodeMirror 6
- **Charts**: Chart.js or D3.js
- **UI Framework**: Bootstrap 5 or Tailwind CSS
- **JavaScript**: Vanilla JS or Vue.js/React (if needed)

### Infrastructure
- **Container Runtime**: Docker
- **Orchestration**: Docker Compose (dev) or Kubernetes (prod)
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with rotation

---

## 10. Database Schema Summary

```sql
-- Users and Authentication
users
user_sessions
user_permissions

-- Sandbox Management
sandboxes
sandbox_versions
sandbox_executions
sandbox_test_results

-- Algorithm Metadata
algorithms (existing)
test_suites
test_cases

-- Comparison & Analytics
comparison_results
performance_metrics
code_quality_metrics

-- Audit & Logging
execution_logs
user_activity_logs
security_events
```

---

## 11. API Endpoints Design

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Sandbox Management
- `GET /api/sandboxes` - List user's sandboxes
- `POST /api/sandboxes` - Create new sandbox
- `GET /api/sandboxes/{id}` - Get sandbox details
- `PUT /api/sandboxes/{id}/code` - Update sandbox code
- `POST /api/sandboxes/{id}/execute` - Execute sandbox code
- `GET /api/sandboxes/{id}/versions` - List versions
- `POST /api/sandboxes/{id}/versions` - Create new version

### Testing & Comparison
- `POST /api/sandboxes/{id}/test` - Run test suite
- `GET /api/sandboxes/{id}/comparison` - Get comparison results
- `GET /api/sandboxes/{id}/metrics` - Get performance metrics

### Algorithms
- `GET /api/algorithms` - List available algorithms
- `GET /api/algorithms/{path}` - Get algorithm details
- `GET /api/algorithms/{path}/original` - Get original code (read-only)

---

## 12. Example User Flow

### Student Workflow:
1. **Browse**: Student visits algorithm page
2. **Create Sandbox**: Clicks "Create Sandbox" button
3. **Edit Code**: Modifies algorithm in code editor
4. **Save Version**: Saves current version
5. **Run Tests**: Executes test suite
6. **View Results**: Sees comparison with original
7. **Iterate**: Makes improvements based on feedback
8. **Submit**: Submits final version to professor (optional)

### Professor Workflow:
1. **Monitor**: Views all student sandboxes
2. **Review**: Examines student modifications
3. **Compare**: Reviews comparison reports
4. **Provide Feedback**: Comments on student work
5. **Approve**: Marks successful implementations

---

## 13. Success Metrics

**Technical Metrics:**
- Execution isolation success rate: >99.9%
- Average test execution time: <5 seconds
- System uptime: >99.5%
- Security incidents: 0

**User Metrics:**
- Student engagement: % of students using sandbox
- Average sandboxes per student
- Test execution frequency
- Code improvement rate (performance gains)

**Educational Metrics:**
- Learning outcomes improvement
- Student satisfaction scores
- Algorithm understanding assessment
- Code quality improvement over time

---

## 14. Risks & Mitigations

**Security Risks:**
- **Risk**: Code injection attacks
- **Mitigation**: Strict code analysis, container isolation, no network access

- **Risk**: Resource exhaustion
- **Mitigation**: Hard limits, timeouts, rate limiting

**Performance Risks:**
- **Risk**: Slow execution with many concurrent users
- **Mitigation**: Task queue, horizontal scaling, caching

**Data Risks:**
- **Risk**: Data loss or corruption
- **Mitigation**: Regular backups, version control, audit logs

---

## 15. Future Enhancements

- **Collaborative Editing**: Multiple students working together
- **Code Review System**: Peer review functionality
- **AI-Powered Suggestions**: Automated code improvement hints
- **Gamification**: Points, badges, leaderboards
- **Integration**: LMS integration (Moodle, Canvas, etc.)
- **Mobile App**: Native mobile application
- **Offline Mode**: Work offline, sync when online

---

## Conclusion

This plan provides a comprehensive roadmap for creating a secure, interactive learning environment where students can experiment with algorithms while maintaining the integrity of original implementations. The phased approach allows for iterative development and testing, ensuring a robust and user-friendly system.

**Next Steps:**
1. Review and approve this plan
2. Prioritize features for MVP (Minimum Viable Product)
3. Set up development environment
4. Begin Phase 1 implementation

