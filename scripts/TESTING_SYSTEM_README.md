# Comprehensive Testing System

This document describes the comprehensive testing system that keeps all algorithms in workable condition with configurable timeouts, separate Python/Java test execution, and detailed reporting.

## Features

### 1. Configurable Timeouts
- **Short-running algorithms**: Default 30s (Python), 60s (Java)
- **Long-running algorithms**: Default 300s (Python), 600s (Java)
- Automatically detects long-running algorithms based on keywords
- Configurable via `test_config.json`

### 2. Separate Test Execution
- **Python tests**: Run via pytest with timeout support
- **Java tests**: Compile and run Java files with timeout support
- Can run independently or together

### 3. Test Result Tracking
- SQLite database stores all test results
- Tracks up to 5 most recent results per algorithm
- Detects state changes (success → failure, failure → success)
- Stores error messages and test output

### 4. Web Reporting Interface
- Real-time test results dashboard
- Search and filter by algorithm path, status, language
- Sort by timestamp, algorithm path, status, duration
- Highlights state changes (bold + colored background)
- Shows test history (up to 5 most recent results)
- Statistics dashboard

## Usage

### Running Tests

**Run all tests (Python and Java):**
```bash
python scripts/test_runner.py
```

**Run Python tests only:**
```bash
python scripts/test_runner.py --python
```

**Run Java tests only:**
```bash
python scripts/test_runner.py --java
```

**Run with custom config:**
```bash
python scripts/test_runner.py --config test_config.json
```

**Filter tests by path:**
```bash
python scripts/test_runner.py --filter "semester_01"
```

### Configuration

Edit `test_config.json` to customize timeouts and long-running keywords:

```json
{
  "python": {
    "short_timeout": 30,
    "long_timeout": 300
  },
  "java": {
    "short_timeout": 60,
    "long_timeout": 600
  },
  "long_running_keywords": [
    "quantum",
    "distributed",
    "training",
    "inference",
    "optimization",
    "simulation",
    "benchmark",
    "performance",
    "mlops",
    "pipeline"
  ]
}
```

### Web Reporting Interface

**Start the web interface:**
```bash
cd web_interface
python app.py
```

**Access test reports:**
Navigate to `http://localhost:5000/test-reports`

**Features:**
- **Search**: Type algorithm path to filter
- **Filter**: Filter by status (success, failure, timeout, error) or language (Python, Java)
- **Sort**: Click column headers to sort
- **State Changes**: Rows with state changes are highlighted:
  - Yellow background: State changed
  - Green background: Changed to success
  - Red background: Changed to failure
- **History**: Click "Show History" to see up to 5 most recent test results

## CI/CD Integration

The testing system is integrated into GitHub Actions CI:

1. **Python Tests Job**: Runs Python tests with timeouts
2. **Java Tests Job**: Runs Java tests with timeouts
3. Both jobs use `continue-on-error: true` to allow other tests to continue

### CI Workflow

```yaml
- name: Run Python tests with timeouts
  run: |
    python scripts/test_runner.py --python --config test_config.json
  continue-on-error: true

- name: Run Java tests with timeouts
  run: |
    python scripts/test_runner.py --java --config test_config.json
  continue-on-error: true
```

## Database Schema

Test results are stored in `test_results.db`:

```sql
CREATE TABLE test_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    algorithm_path TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL,
    duration REAL,
    timestamp TEXT NOT NULL,
    error_message TEXT,
    test_output TEXT,
    previous_status TEXT,
    state_changed INTEGER DEFAULT 0
);
```

## Long-Running Algorithm Detection

Algorithms are automatically classified as long-running if their path contains any of these keywords:
- quantum
- distributed
- training
- inference
- optimization
- simulation
- benchmark
- performance
- mlops
- pipeline
- parallel
- concurrent
- federated
- reinforcement

## Test Status Values

- **success**: Test passed
- **failure**: Test failed
- **timeout**: Test exceeded timeout
- **error**: Test encountered an error (compilation, import, etc.)
- **skipped**: Test was skipped
- **running**: Test is currently running (not stored in database)

## State Change Detection

The system automatically detects when an algorithm's test status changes:
- **Success → Failure**: Highlighted in red
- **Failure → Success**: Highlighted in green
- **Any change**: Highlighted in yellow

State changes are tracked in the database and displayed prominently in the web interface.

## Best Practices

1. **Regular Testing**: Run tests regularly to catch regressions early
2. **Monitor State Changes**: Pay attention to state changes in the web interface
3. **Adjust Timeouts**: If tests consistently timeout, adjust timeouts in `test_config.json`
4. **Review Failures**: Check error messages in the web interface to understand failures
5. **CI Integration**: Ensure CI runs tests on every push/PR

## Troubleshooting

### Tests Timing Out

1. Check if algorithm is correctly classified as long-running
2. Increase timeout in `test_config.json`
3. Check for infinite loops or blocking operations

### Java Tests Failing

1. Ensure Java is installed and in PATH
2. Check for compilation errors
3. Verify Java files have main methods (if required)

### Python Tests Failing

1. Ensure pytest and pytest-timeout are installed
2. Check for import errors
3. Verify test files are in correct locations

### Database Issues

1. Delete `test_results.db` to reset
2. Check file permissions
3. Ensure SQLite is available

## API Endpoints

### GET /api/test-results
Get test results with filtering and sorting.

**Query Parameters:**
- `search`: Search algorithm path
- `status`: Filter by status
- `language`: Filter by language
- `sort`: Sort column (timestamp, algorithm_path, status, duration)
- `order`: Sort order (asc, desc)

### GET /api/test-statistics
Get test statistics.

**Response:**
```json
{
  "status_counts": {
    "success": 100,
    "failure": 5,
    "timeout": 2
  },
  "language_stats": {
    "python": {
      "success": 80,
      "failure": 3
    },
    "java": {
      "success": 20,
      "failure": 2
    }
  },
  "recent_changes": 3
}
```

## Future Enhancements

- Email notifications on state changes
- Slack/Teams integration
- Performance regression detection
- Test coverage tracking
- Parallel test execution
- Test result export (CSV, JSON)


