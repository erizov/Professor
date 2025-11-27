# Algorithm Fetcher - Enhanced Version

## Overview

The enhanced `algo_fetcher.py` can now load algorithm information from:
1. **Local markdown files** (school.en.md, school.ru.md, univer.en.md, univer.ru.md)
2. **Web sources** (Wikipedia, e-maxx.ru)
3. **Curated summaries** (`load/curated_summaries.json`)

### Adapter Pipeline

Web enrichment now runs through a modular adapter pipeline:

| Adapter | Description | Notes |
|---------|-------------|-------|
| `CuratedSummaryAdapter` | Uses hand-written summaries stored in `load/curated_summaries.json` | Guaranteed clean content (fall back #1) |
| `WikipediaAdapter` | Fetches English/Russian Wikipedia content, extracts structured sections, and filters non-algorithm pages | Still respects placeholder / duplicate checks |
| `EMaxxAdapter` | (RU only) Scrapes e-maxx.ru if Wikipedia fails | Enabled only when `prefer_ru_emaxx` is True |

Each adapter returns structured sections (definition, application, examples, etc.). After a source succeeds the fetcher:

1. Sanitizes placeholders and generic defaults
2. Removes duplicate sections (Definition ≠ Technical Description ≠ Application ≠ Example)
3. Persists only meaningful, distinct text

## Database Schema Enhancements

The database schema (`createDbSql.txt`) has been enhanced to store all content from markdown files:

### New Columns Added

**School Level Fields:**
-`simple_explanation` - Simple explanation section
-`where_its_used` - Where It's Used section
-`example` - Example section

**University Level Fields:**
-`discipline` - Discipline field (from metadata)
- `algorithm_definition` - Algorithm Definition section
- `technical_description` - Technical Description section
- `application` - Application in Machine Learning / AI section
- `step_by_step` - Step-by-Step Scenario section
- `example_result` - Result from step-by-step scenario

**Common Fields (already existed):**
- `self_check_basic` - Basic level self-check questions
- `self_check_intermediate` - Intermediate level self-check questions
- `self_check_advanced` - Advanced level self-check questions
- `practical_tasks_basic` - Level 1 practical tasks
- `practical_tasks_applied` - Level 2 practical tasks
- `practical_tasks_research` - Level 3 practical tasks
- `ethical_reasoning` - Ethical reasoning/note section
- `extra_chapters` - JSONB field for additional content

## New Files

### `markdown_parser.py`

A comprehensive parser for algorithm markdown files that extracts:

- **School level files** (school.en.md, school.ru.md):
  - Simple Explanation
  - Where It's Used
  - Example
  - Self-Check Questions (Basic/Intermediate/Advanced)
  - Practical Tasks (Level 1/2/3)
  - Ethical Note

- **University level files** (univer.en.md, univer.ru.md):
  - Algorithm Definition
  - Technical Description
  - Application in Machine Learning / AI
  - Step-by-Step Scenario
  - Self-Check Questions (Basic/Intermediate/Advanced)
  - Practical Tasks (Level 1/2/3)
  - Ethical Reasoning

## Usage

### Load from Local Markdown Files

```bash
python algo_fetcher.py --mode local
```

This will:
1. Scan all `semester_*/lecture_*/algorithm_name/` folders
2. Look for markdown files (school.en.md, school.ru.md, univer.en.md, univer.ru.md)
3. Parse and store all structured content in the database

### Load from Web Sources

```bash
python algo_fetcher.py --mode web --algorithm "Dijkstra's algorithm" "QuickSort"
```

### Load from Both Sources

```bash
python algo_fetcher.py --mode both
```

### Specify Base Path

```bash
python algo_fetcher.py --mode local --base-path "E:/Python/GptEngineer/Professor"
```

## Algorithm Name Resolution

The fetcher uses the following priority to determine algorithm names:

1. `metadata.json` file in algorithm folder (`name` or `display_name` field)
2. Folder name (normalized)
3. User-provided name (for web fetching)

## Database Structure

### Primary Key
- `algorithm_name` (normalized, e.g., "blockchain-scalability-solutions")

### Unique Constraint
- `(algorithm_name, language, level)` - ensures one description per algorithm/language/level combination

### Language Support
- English (`en`)
- Russian (`ru`)

### Education Levels
- `school` - School-level content
- `university` - University-level content

## Example: Loading a Specific Algorithm

```python
from pathlib import Path
from algo_fetcher import Session, load_from_markdown_files, init_db

init_db()
session = Session()

# Load specific algorithm folder
algo_folder = Path("semester_13/lecture_87_blockchain_advanced/blockchain_scalability_solutions")
load_from_markdown_files(session, algo_folder)
```

## Integration with Existing Code

The enhanced fetcher maintains backward compatibility:
- All existing web fetching functionality remains unchanged
- New markdown loading is additive
- Database schema uses `ADD COLUMN IF NOT EXISTS` for safe migration

## Notes

- The parser handles both English and Russian markdown files
- Markdown parsing is robust and handles variations in formatting
- All content is stored with UTF-8 encoding
- Local files get a quality score of 1.0 (highest)
- Source URL for local files is stored as `file://` URI
