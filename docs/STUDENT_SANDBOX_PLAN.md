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

