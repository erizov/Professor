# Course API (stable surface)

The web interface exposes these HTTP endpoints for listing and querying course content. Use them for integrations, LMS, or external tools. Base URL: `http://localhost:5000` when running `python scripts/run_web_interface.py`.

## Algorithms and structure

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/algorithms` | List algorithms with optional filters: `search`, `level` (school/univer), `language` (en/ru), `category`, `semester`, `sort`, `order`, `page`, `per_page`, `limit`. Returns list (or dict with `algorithms` key) of algorithm records. |
| GET | `/api/algorithm/<int:algorithm_id>` | Get one algorithm by ID (from DB). |
| GET | `/api/categories` | List distinct categories. |
| GET | `/api/semesters` | List distinct semester numbers. |
| GET | `/api/statistics` | Aggregate counts: total_algorithms, total_tests, total_framework_examples, total_semesters. |

## Algorithm index (level/language-aware)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/algorithm-index/api/algorithms` | List algorithms with level/language filters; returns algorithms that have the corresponding MD file. |
| GET | `/algorithm-index/api/md-file?path=...&level=...&language=...` | Get content of a specific MD file (school/univer, en/ru). |
| GET/POST | `/algorithm-index/api/preferences` | Get or set user preferences (language, level). |

## Execution

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/algorithm/algorithms` | List runnable algorithms (Python/Java). Query: `language`, `semester`, `lecture`. |
| GET | `/api/algorithm/source` | Get source code for an algorithm. Query: `path`, `language` (python/java). |
| POST | `/api/algorithm/run` | Run an algorithm (body: path, language, optional input). Returns success, stdout, stderr, time. |
| GET | `/api/java/algorithms` | List Java algorithms. Query: `semester`, `lecture`. |
| POST | `/api/java/run` | Run a Java algorithm. |

## User and dashboard

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/user/preferences` | Get or set current user preferences (language, level). |
| GET | `/dashboard/api/progress` | Student progress (requires auth). |
| GET | `/dashboard/api/statistics` | Dashboard statistics. |
| GET | `/api/test-results` | Test results (test_reports). |
| GET | `/api/test-statistics` | Test statistics. |

## Recommendations (constraint-based)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/recommend` | Request a resource recommendation. Body: constraints (e.g. memory, cpu_power, dataset_size). Returns recommended algorithm/resource and reasoning. |

## Lesson Q&A (Ask AI)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/algorithm-index/api/lesson-ask/limit?lesson_path=...` | Return `{ used, limit }` (max 25 questions per student per lesson). |
| POST | `/algorithm-index/api/lesson-ask` | Body: `{ lesson_path, question }`. Rate limited; answers only about the lesson; requires OPENAI_API_KEY. Returns `{ answer, used, limit }` or 429 when limit reached. |

## Content and links

- Algorithm **folder paths** in the DB are relative to the project root (e.g. `course/semester_01/lecture_01_.../algorithm_name`).
- To get file paths for a given algorithm: use `folder_path` from `/api/algorithms`; MD files are `{folder_path}/{level}.{language}.md` (e.g. `school.en.md`, `univer.ru.md`).
- For a **content health** report (missing/placeholder files), run `python scripts/content_health_report.py` or `python scripts/find_files_needing_generation.py`; they do not expose HTTP endpoints.

## Errors

- 400: Bad request (e.g. invalid parameters).
- 401: Not authenticated.
- 403: Insufficient permissions.
- 404: Algorithm or resource not found.
- 500: Server error (check logs).

Responses are JSON. List endpoints return arrays or objects with a list key (e.g. `algorithms`).
