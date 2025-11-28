# Sandbox System Implementation Steps

**Status**: Planning Complete - Ready for Implementation  
**Last Updated**: 2025-01-XX  
**Priority**: High

## Overview

This document outlines the step-by-step implementation plan for the algorithm sandbox system where users can modify algorithms, run them safely, and compare performance with original implementations while ensuring correctness.

---

## Implementation Phases

### Phase 1: Access & Isolation Setup

**Goal**: Create secure, isolated execution environment for user-modified algorithms

#### Step 1.1: User Role System
- [ ] Extend existing user authentication to support roles:
  - `visitor` (read-only)
  - `sandbox_user` (can create/modify sandboxes)
  - `reviewer`/`professor` (can approve changes)
  - `admin` (full access)
- [ ] Update `database/setup_user_tables.py` to add role-based permissions
- [ ] Create middleware/decorators for role-based route protection

#### Step 1.2: Sandbox Directory Structure
- [ ] Create `sandboxes/` directory structure:
  ```
  sandboxes/
  ├── <user_id>/
  │   ├── <algorithm_path>/
  │   │   ├── algorithm.py (or Algorithm.java)
  │   │   ├── metadata.json
  │   │   ├── version_history.json
  │   │   └── run_results/
  ```
- [ ] Implement `scripts/create_sandbox.py` to clone canonical algorithm to user workspace
- [ ] Add cleanup job for old/inactive sandboxes

#### Step 1.3: Container Isolation
- [ ] Set up Docker containerization for safe execution:
  - [ ] Create `Dockerfile` for Python execution environment
  - [ ] Create `Dockerfile.java` for Java execution environment
  - [ ] Configure resource limits (CPU, memory, timeout)
  - [ ] Set up `docker-compose.yml` for orchestration
- [ ] Implement container management utilities:
  - [ ] Start/stop containers
  - [ ] Resource monitoring
  - [ ] Cleanup after execution

**Files to Create/Modify**:
- `sandboxes/` (directory)
- `scripts/create_sandbox.py`
- `scripts/container_manager.py`
- `docker/Dockerfile.python`
- `docker/Dockerfile.java`
- `docker/docker-compose.yml`
- `web_interface/auth.py` (extend with roles)

---

### Phase 2: Instrumentation & Resource Measurement

**Goal**: Capture detailed performance metrics for comparison

#### Step 2.1: Enhanced Runner Scripts
- [ ] Extend `framework/python_executor.py`:
  - [ ] Add `psutil` for memory/CPU monitoring
  - [ ] Capture peak memory usage
  - [ ] Measure CPU time vs wall-clock time
  - [ ] Log stdout/stderr separately
  - [ ] Add timeout handling
- [ ] Extend `framework/java_executor.py`:
  - [ ] Use `jcmd` or `ps` for Java process monitoring
  - [ ] Capture JVM memory metrics
  - [ ] Measure execution time accurately
  - [ ] Handle Java-specific errors

#### Step 2.2: Standardized Input Profiles
- [ ] Create `test_profiles/` directory with JSON test cases:
  ```json
  {
    "small": {"n": 100, "inputs": [...]},
    "medium": {"n": 10000, "inputs": [...]},
    "large": {"n": 100000, "inputs": [...]},
    "edge_cases": [...]
  }
  ```
- [ ] Implement profile loader that works for both Python and Java
- [ ] Ensure same inputs are used for canonical vs sandbox comparison

#### Step 2.3: Metrics Collection Framework
- [ ] Create `framework/metrics_collector.py`:
  - [ ] Runtime (ms)
  - [ ] Peak memory (MB)
  - [ ] CPU usage (%)
  - [ ] I/O operations (if applicable)
  - [ ] Execution status (success/failure/error)
- [ ] Store metrics in structured format (JSON/DB)

**Files to Create/Modify**:
- `framework/python_executor.py` (enhance)
- `framework/java_executor.py` (enhance)
- `framework/metrics_collector.py` (new)
- `test_profiles/` (directory)
- `test_profiles/<algorithm_name>.json` (per algorithm)

---

### Phase 3: Comparison Pipeline

**Goal**: Run canonical and sandbox versions side-by-side and compare results

#### Step 3.1: Comparison Runner
- [ ] Create `scripts/compare_algorithms.py`:
  - [ ] Accept canonical and sandbox algorithm paths
  - [ ] Run both on same input profiles
  - [ ] Collect metrics for each
  - [ ] Compare outputs (exact match or tolerance-based)
  - [ ] Generate comparison report
- [ ] Handle edge cases:
  - [ ] Timeout handling
  - [ ] Memory limit exceeded
  - [ ] Compilation/runtime errors

#### Step 3.2: Database Schema for Comparisons
- [ ] Extend `database/schema.sql` or create `database/sandbox_schema.sql`:
  ```sql
  CREATE TABLE sandbox_runs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      algorithm_id INTEGER NOT NULL,
      sandbox_path TEXT NOT NULL,
      canonical_path TEXT NOT NULL,
      run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      status TEXT,  -- 'pending', 'running', 'completed', 'failed'
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (algorithm_id) REFERENCES algorithms(id)
  );
  
  CREATE TABLE run_metrics (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sandbox_run_id INTEGER NOT NULL,
      version TEXT NOT NULL,  -- 'canonical' or 'sandbox'
      dataset_size TEXT,  -- 'small', 'medium', 'large'
      runtime_ms REAL,
      peak_memory_mb REAL,
      cpu_percent REAL,
      success BOOLEAN,
      FOREIGN KEY (sandbox_run_id) REFERENCES sandbox_runs(id)
  );
  
  CREATE TABLE run_outputs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sandbox_run_id INTEGER NOT NULL,
      test_name TEXT,
      version TEXT,  -- 'canonical' or 'sandbox'
      output_text TEXT,
      error_log TEXT,
      status TEXT,  -- 'pass', 'fail', 'error'
      FOREIGN KEY (sandbox_run_id) REFERENCES sandbox_runs(id)
  );
  
  CREATE TABLE comparison_reports (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sandbox_run_id INTEGER NOT NULL,
      output_match BOOLEAN,
      performance_delta REAL,  -- percentage change
      memory_delta REAL,
      correctness_score REAL,  -- 0.0 to 1.0
      report_json TEXT,  -- detailed comparison data
      FOREIGN KEY (sandbox_run_id) REFERENCES sandbox_runs(id)
  );
  ```

#### Step 3.3: Comparison Logic
- [ ] Implement output comparison:
  - [ ] Exact match for deterministic algorithms
  - [ ] Tolerance-based for floating-point results
  - [ ] Structural comparison for complex outputs (trees, graphs)
- [ ] Calculate performance deltas:
  - [ ] Runtime difference (%)
  - [ ] Memory difference (%)
  - [ ] CPU usage difference (%)

**Files to Create/Modify**:
- `scripts/compare_algorithms.py` (new)
- `database/sandbox_schema.sql` (new)
- `database/populate_sandbox_tables.py` (new)

---

### Phase 4: Correctness & Purpose Verification

**Goal**: Ensure modified algorithms still solve the original problem correctly

#### Step 4.1: Test Suite Integration
- [ ] Extend existing test runners to work with sandbox code:
  - [ ] `framework/test_runner.py` - run tests on sandbox code
  - [ ] Ensure test isolation (sandbox tests don't affect canonical)
- [ ] Create test result aggregator:
  - [ ] Parse test output
  - [ ] Count pass/fail
  - [ ] Extract error messages

#### Step 4.2: Purpose Validation
- [ ] Create `framework/purpose_validator.py`:
  - [ ] Load algorithm purpose from `metadata.json` or README
  - [ ] Define validation rules per algorithm type:
    - Sorting: output is sorted, contains all input elements
    - Searching: returns correct index or None
    - Graph algorithms: shortest path is optimal, etc.
  - [ ] Run property-based checks where applicable
- [ ] Implement invariant checking:
  - [ ] Pre/post conditions
  - [ ] Loop invariants (where applicable)
  - [ ] Data structure integrity

#### Step 4.3: Semantic Comparison
- [ ] For algorithms with structured outputs:
  - [ ] Tree algorithms: verify tree properties (balance, ordering)
  - [ ] Graph algorithms: verify path optimality, connectivity
  - [ ] ML algorithms: verify prediction accuracy within tolerance
- [ ] Create algorithm-specific validators in `framework/validators/`

**Files to Create/Modify**:
- `framework/test_runner.py` (extend)
- `framework/purpose_validator.py` (new)
- `framework/validators/` (directory)
- `framework/validators/sorting_validator.py` (example)
- `framework/validators/graph_validator.py` (example)

---

### Phase 5: Web UI Enhancements

**Goal**: User-friendly interface for sandbox management and comparison

#### Step 5.1: Sandbox Management UI
- [ ] Extend `/sandbox` route in `web_interface/sandbox_bp.py`:
  - [ ] List user's sandboxes
  - [ ] Create new sandbox from algorithm
  - [ ] Delete sandbox
  - [ ] View sandbox history
- [ ] Create templates:
  - [ ] `templates/sandbox/list.html` - sandbox browser
  - [ ] `templates/sandbox/create.html` - create sandbox form
  - [ ] `templates/sandbox/edit.html` - code editor view

#### Step 5.2: Code Editor Integration
- [ ] Integrate Monaco Editor or CodeMirror:
  - [ ] Syntax highlighting (Python/Java)
  - [ ] Code completion
  - [ ] Diff view (sandbox vs canonical)
  - [ ] Save functionality
- [ ] Add code validation:
  - [ ] Syntax checking
  - [ ] Basic linting
  - [ ] Compilation check (for Java)

#### Step 5.3: Comparison Dashboard
- [ ] Create comparison view:
  - [ ] Side-by-side metrics table
  - [ ] Performance charts (runtime, memory over dataset sizes)
  - [ ] Correctness status indicators
  - [ ] Code diff viewer
  - [ ] Test results table
- [ ] Add export functionality:
  - [ ] Download comparison report (PDF/JSON)
  - [ ] Share comparison link

#### Step 5.4: Real-time Execution Status
- [ ] Implement WebSocket or polling for:
  - [ ] Run status updates
  - [ ] Live metrics during execution
  - [ ] Progress indicators
- [ ] Add notification system:
  - [ ] Email/Slack when run completes
  - [ ] In-app notifications

**Files to Create/Modify**:
- `web_interface/sandbox_bp.py` (extend)
- `templates/sandbox/` (new directory)
- `templates/sandbox/list.html` (new)
- `templates/sandbox/edit.html` (new)
- `templates/sandbox/compare.html` (new)
- `static/js/sandbox_editor.js` (new)
- `static/js/comparison_charts.js` (new)

---

### Phase 6: Approval Workflow

**Goal**: Allow reviewers to approve sandbox changes

#### Step 6.1: Review Request System
- [ ] Add "Request Review" button in sandbox UI
- [ ] Create review request table:
  ```sql
  CREATE TABLE review_requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sandbox_run_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      reviewer_id INTEGER,
      status TEXT,  -- 'pending', 'approved', 'rejected', 'needs_changes'
      comments TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reviewed_at TIMESTAMP,
      FOREIGN KEY (sandbox_run_id) REFERENCES sandbox_runs(id),
      FOREIGN KEY (user_id) REFERENCES users(id),
      FOREIGN KEY (reviewer_id) REFERENCES users(id)
  );
  ```
- [ ] Implement review assignment logic (auto-assign or manual)

#### Step 6.2: Review Interface
- [ ] Create reviewer dashboard:
  - [ ] List pending reviews
  - [ ] View comparison reports
  - [ ] Approve/reject with comments
  - [ ] Request changes
- [ ] Add merge functionality:
  - [ ] Option to merge sandbox into canonical (creates new version)
  - [ ] Or create "variant" entry in database

#### Step 6.3: Notification System
- [ ] Email notifications:
  - [ ] User: review requested, review completed
  - [ ] Reviewer: new review request
- [ ] In-app notifications

**Files to Create/Modify**:
- `database/sandbox_schema.sql` (extend)
- `web_interface/review_bp.py` (new)
- `templates/review/` (new directory)
- `templates/review/dashboard.html` (new)
- `templates/review/detail.html` (new)

---

### Phase 7: Automation & Monitoring

**Goal**: Efficient execution and monitoring of sandbox operations

#### Step 7.1: Task Queue System
- [ ] Set up Celery or RQ for async task execution:
  - [ ] Queue comparison runs
  - [ ] Queue test executions
  - [ ] Handle long-running operations
- [ ] Configure workers:
  - [ ] Resource limits per worker
  - [ ] Priority queues
  - [ ] Retry logic

#### Step 7.2: Monitoring & Logging
- [ ] Implement comprehensive logging:
  - [ ] Execution logs
  - [ ] Error logs
  - [ ] Performance logs
- [ ] Create monitoring dashboard:
  - [ ] Active sandboxes
  - [ ] Queue status
  - [ ] Resource usage
  - [ ] Error rates

#### Step 7.3: Cleanup & Maintenance
- [ ] Automated cleanup jobs:
  - [ ] Remove old sandbox runs (configurable retention)
  - [ ] Archive inactive sandboxes
  - [ ] Clean up Docker containers
- [ ] Health checks:
  - [ ] Container health
  - [ ] Database connectivity
  - [ ] Queue worker status

**Files to Create/Modify**:
- `scripts/sandbox_worker.py` (new)
- `scripts/cleanup_sandboxes.py` (new)
- `config/celery_config.py` (new, if using Celery)
- `web_interface/monitoring_bp.py` (new)

---

### Phase 8: Documentation & Testing

**Goal**: Complete documentation and system testing

#### Step 8.1: User Documentation
- [ ] Create `docs/SANDBOX_USER_GUIDE.md`:
  - [ ] How to create a sandbox
  - [ ] How to modify code
  - [ ] How to run comparisons
  - [ ] How to interpret results
  - [ ] How to request reviews
- [ ] Create `docs/SANDBOX_REVIEWER_GUIDE.md`:
  - [ ] Review process
  - [ ] Approval criteria
  - [ ] Merge process

#### Step 8.2: Developer Documentation
- [ ] API documentation for sandbox endpoints
- [ ] Architecture diagrams
- [ ] Database schema documentation
- [ ] Deployment guide

#### Step 8.3: System Testing
- [ ] Unit tests for:
  - [ ] Sandbox creation
  - [ ] Comparison logic
  - [ ] Metrics collection
  - [ ] Purpose validation
- [ ] Integration tests:
  - [ ] End-to-end sandbox workflow
  - [ ] Review and approval flow
- [ ] Performance tests:
  - [ ] Concurrent sandbox execution
  - [ ] Resource limits enforcement

**Files to Create/Modify**:
- `docs/SANDBOX_USER_GUIDE.md` (new)
- `docs/SANDBOX_REVIEWER_GUIDE.md` (new)
- `docs/SANDBOX_ARCHITECTURE.md` (new)
- `tests/test_sandbox.py` (new)
- `tests/test_comparison.py` (new)

---

## Implementation Order

**Recommended sequence**:

1. **Phase 1** (Access & Isolation) - Foundation
2. **Phase 2** (Instrumentation) - Core functionality
3. **Phase 3** (Comparison Pipeline) - Main feature
4. **Phase 4** (Correctness) - Quality assurance
5. **Phase 5** (Web UI) - User experience
6. **Phase 6** (Approval) - Workflow completion
7. **Phase 7** (Automation) - Scalability
8. **Phase 8** (Documentation) - Polish

---

## Dependencies

- **Python packages**:
  - `psutil` - system resource monitoring
  - `docker` - container management
  - `celery` or `rq` - task queue (optional)
  - `flask-socketio` - WebSocket support (optional)

- **System requirements**:
  - Docker installed and running
  - Sufficient disk space for sandboxes
  - Database with appropriate schema

---

## Success Criteria

- [ ] Users can create sandboxes from any algorithm
- [ ] Sandbox code executes safely in isolated containers
- [ ] Comparisons show accurate performance metrics
- [ ] Correctness validation catches purpose changes
- [ ] Review workflow is functional
- [ ] System handles concurrent users
- [ ] Documentation is complete

---

## Notes

- Start with Python algorithms, then extend to Java
- Consider starting with a subset of algorithms for testing
- Monitor resource usage during development
- Keep security as top priority (container isolation is critical)

---

**Next Steps**: Begin with Phase 1, Step 1.1 (User Role System)

