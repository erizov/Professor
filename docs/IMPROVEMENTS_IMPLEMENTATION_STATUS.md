# Improvement plans — implementation status

This document cross-checks [IMPROVEMENTS_AND_FEATURES_PLAN.md](IMPROVEMENTS_AND_FEATURES_PLAN.md) and [IMPROVEMENTS_DRY_SOLID_MAINTAINABILITY.md](IMPROVEMENTS_DRY_SOLID_MAINTAINABILITY.md) against the current codebase. It is the single place to see what is done, partial, or not done across both plans.

**Status:** **Implemented** ✅ | **Partial** 🟡 | **Not implemented** ❌

---

## Part A — IMPROVEMENTS_AND_FEATURES_PLAN.md

### 1. Reach (teachers & institutions)

| Item | Status | Notes |
|------|--------|------|
| Public course index / “start here” | ✅ | README has “Start here” table (Student / Teacher / Citation) and course index under `course/`. |
| Clear licensing and citation | ✅ | LICENSE (MIT), [docs/CITATION.md](CITATION.md) with “How to cite” and “Use in your course”. |
| Static export / offline pack | ❌ | No script or pipeline for static HTML/ZIP export. |
| Docker / one-command run | ✅ | `Dockerfile` and `docker-compose.yml`; `docker-compose up` runs web UI on port 5000. |
| Showcase / testimonials | ❌ | Optional; not present. |
| Teacher quickstart | ✅ | [docs/TEACHER_QUICKSTART.md](TEACHER_QUICKSTART.md): clone, tests, workflow, web UI, where to edit. |
| Stable API for integrations | ✅ | [docs/API.md](API.md) documents course API (algorithms, categories, semesters, execution, preferences). |
| Bulk export for LMS | ❌ | No JSON/SCORM export for Moodle/Canvas. |
| Assignment templates | ❌ | No per-lecture/per-algorithm assignment templates. |
| Instructor dashboard | ❌ | No completion stats / most-viewed / placeholder coverage dashboard. |
| Content health report | ✅ | `scripts/content_health_report.py`; linked from Teacher Quickstart and README. |
| Consistent learning objectives | 🟡 | README claims “Learning Objectives” per algorithm; no CI lint for this. |
| Multilingual parity | ✅ | Tracked in content_health_report; [docs/MULTILINGUAL_PARITY.md](MULTILINGUAL_PARITY.md) states goals and how to track. |

### 2. Students learn better

| Item | Status | Notes |
|------|--------|------|
| Clear learning paths | ✅ | [docs/LEARNING_PATHS.md](LEARNING_PATHS.md): Interview prep, Semester 1 full, Design patterns + ML; in README. |
| Ask AI about lesson | ✅ | Algorithm Index: “Ask AI about this lesson” in modal; 25 questions/student/lesson; on-topic; [API](API.md#lesson-qa-ask-ai). |
| Progress and checkpoints | ❌ | No per-student “completed / in progress / not started” or checkpoints. |
| Spaced repetition | 🟡 | Mentioned in README; no dedicated UI or implementation. |
| Difficulty and time labels | ❌ | No tags (e.g. 1–3) or estimated time per algorithm. |
| Run and compare | 🟡 | Web “Algorithm Executor” runs algorithms; no explicit “compare with reference output” flow. |
| Exercises with model answers | 🟡 | README mentions “Practice Exercises”; no structured hidden model answers/hints. |
| Student sandbox | 🟡 | Plan in `docs/STUDENT_SANDBOX_PLAN.md`; sandbox UI exists; full isolated run env TBD. |
| Automated hints | ❌ | No “check edge case” / “review loop bounds” on wrong output. |
| TL;DR and “when to use” | 🟡 | README lists these as course features; not linted in CI. |
| Single worked example | 🟡 | Claimed in README; not enforced per algorithm. |
| Visualizations | 🟡 | ASCII/SVG mentioned; no mandatory expansion or step-through. |
| Common mistakes | 🟡 | Listed as feature; not enforced. |
| Glossary | ❌ | No central glossary linked from algorithm pages. |
| Self-check quizzes | 🟡 | “Self-Assessment Questions” mentioned; no “show answer” / scoring in UI. |
| Badges / gamification | 🟡 | GAMIFICATION_SYSTEM.md exists; no implemented badge UI. |
| Time and streak tracking | ❌ | Not implemented. |
| Certificates | ❌ | Not implemented. |

### 3. Implementation order (from plan)

| Phase | Status | Notes |
|-------|--------|------|
| 1. Reach quick wins (Teacher quickstart, course index, LICENSE, citation) | ✅ | All done. |
| 2. Learning quick wins (Learning paths, TL;DR/when to use, worked example) | 🟡 | Learning paths done; TL;DR/worked example not linted or enforced. |
| 3. Content health report | ✅ | Done. |
| 4. Stable course API, one-command run, assignment templates | 🟡 | API documented ([docs/API.md](API.md)), Docker done (`docker-compose up`); assignment templates not done. |
| 5. Progress/checkpoints, run and compare, exercises | 🟡 | Run exists; compare + progress + exercises not fully done. |
| 6. Later (sandbox, spaced repetition, badges, LMS export) | 🟡 | Sandbox plan and partial UI; rest not done. |

---

## Part B — IMPROVEMENTS_DRY_SOLID_MAINTAINABILITY.md

### 1. DRY

| Item | Status | Notes |
|------|--------|------|
| Single project-paths module | ✅ | `core/paths.py`: PROJECT_ROOT, COURSE_ROOT, get_database_path(), get_algos_db_path(). |
| Single content-metadata constants | ✅ | `core/content_metadata.py`: EXPECTED_MD_FILES, level_lang_from_md_name(), PLACEHOLDER_PATTERNS. |
| Shared placeholder detection | ✅ | count_placeholders(), needs_generation(); used by find_files_needing_generation.py. |
| Shared semester/lecture discovery | ✅ | `core/course_structure.py`: walk_algorithm_dirs(); used by find_files_needing_generation; executors use COURSE_ROOT. |

### 2. SOLID

| Item | Status | Notes |
|------|--------|------|
| One script = one responsibility | ✅ | Single find script (find_files_needing_generation.py); workflow composes steps. |
| Executors: split discovery / metadata / execution | 🟡 | Executors still combine discovery and execution; no separate discovery module. |
| Abstract AlgorithmExecutor (protocol) | ❌ | No common protocol; PythonExecutor and JavaExecutor are independent. |
| Placeholder rules as config list | ✅ | PLACEHOLDER_PATTERNS in content_metadata; extensible. |
| LSP: same result shape | 🟡 | Both return execution result; not formally standardized. |
| Config/database dependency inversion | ✅ | Framework and web_interface blueprints use core.paths (PROJECT_ROOT, get_database_path, get_algos_db_path). |

### 3. Data validation

| Item | Status | Notes |
|------|--------|------|
| Central config validation (env, API key) | ✅ | `core/config.py`: get_openai_api_key/base(), require_openai_config(), validate_project_layout(). |
| Validate PROJECT_ROOT / semester layout | ✅ | `core/config.py`: validate_project_layout() checks COURSE_ROOT; call on startup where needed. |
| Algorithm metadata validation | ❌ | No explicit validation of semester/lecture/algorithm names or DB writes. |
| Web/API input validation (400 on bad params) | 🟡 | lesson-ask validates input and returns 400 with message; core.exceptions.ValidationError used at boundary. |

### 4. Exceptions

| Item | Status | Notes |
|------|--------|------|
| Custom exception hierarchy | ✅ | `core/exceptions.py`: ProfessorError, ConfigurationError, ContentNotFoundError, ValidationError, ExecutionError. |
| Replace bare except / silent pass | 🟡 | Used in e2e/core tests; many scripts still use broad except. |
| ExecutionError with stdout/stderr | ✅ | ExecutionError carries message, stdout, stderr. |
| Catch at boundaries (CLI/Flask) | 🟡 | Exceptions exist; not consistently used in all executors or web routes. |

### 5. Modular design

| Item | Status | Notes |
|------|--------|------|
| Package layout (core, framework, database, web_interface) | ✅ | core/, framework/, database/, web_interface/ in place. |
| Single entry point for DB paths | ✅ | Web interface blueprints and app use core.paths (PROJECT_ROOT, get_database_path, get_algos_db_path). |
| scripts/README.md | ✅ | Lists find, content health, workflow, web; points to core. |
| One “find” + one “process batch” entry point | ✅ | find_files_needing_generation.py; batch scripts can consume its output. |
| Dry-run / skip existing | 🟡 | Some scripts support it; not universal. |
| Logging instead of print | 🟡 | Mixed; not all scripts use a logger. |

### 6. Quick wins (from DRY/SOLID doc)

| Item | Status | Notes |
|------|--------|------|
| core/paths.py with PROJECT_ROOT, get_db_path, get_algos_db_path | ✅ | Done. |
| core/content_metadata.py + refactor find scripts | ✅ | Done; single find script. |
| core/exceptions.py + replace one broad except | ✅ | Exceptions in place; partial adoption. |
| Validate config on first use | ✅ | `core/config.require_openai_config()` raises ConfigurationError if API key missing (for scripts that need it). |
| Document run_full_workflow and find vs generate | ✅ | scripts/README.md and Teacher Quickstart. |

### 7. E2E tests

| Item | Status | Notes |
|------|--------|------|
| tests/e2e/ (core, find script, workflow --help, web GET /) | ✅ | test_core_e2e.py, test_find_scripts_e2e.py, test_workflow_and_web_e2e.py. |
| CI runs e2e | ✅ | .github/workflows/ci.yml runs e2e. |

---

## Summary

- **Fully implemented:** Course index & start here, LICENSE & citation, Teacher quickstart, Content health report, Learning paths, core paths/content_metadata/exceptions/course_structure/config, single find script, scripts README, e2e tests and CI, **stable API doc** ([docs/API.md](API.md)), **Docker** (Dockerfile + docker-compose), **web_interface using core.paths**, **config validation** (require_openai_config, validate_project_layout), **content/link tracking** (check_content_and_links.py).
- **Partial:** Run algorithm (no “compare with reference”), TL;DR/worked example (content claim, not linted), executors (no shared AlgorithmExecutor protocol), exception/logging adoption in scripts, dry-run/skip existing not universal.
- **Not implemented:** Static export, LMS export, assignment templates, instructor dashboard, progress/checkpoints, difficulty/time labels, automated hints, glossary, time/streak tracking, certificates, abstract AlgorithmExecutor protocol, algorithm metadata validation, universal 400 on bad API params, universal dry-run/logging.

**Tracking missing content and links:**  
`python scripts/find_files_needing_generation.py` · `python scripts/content_health_report.py --only-problems` · `python scripts/check_content_and_links.py --json --links`

**Next steps (optional):** Add “compare with reference output” to the executor; LMS/SCORM export; assignment templates; AlgorithmExecutor protocol; CI lint for learning objectives.
