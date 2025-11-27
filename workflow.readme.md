## Markdown Generation Workflow

### Quick Start (All Steps)

Run the complete workflow with a single command:

```bash
python scripts/run_full_workflow.py
```

This orchestrates all four steps automatically with progress reporting and error handling.

### Manual Step-by-Step

1. `python scripts/enhance_readmes_improved.py`  
   Scan every algorithm folder, extract identifiers from `README.md`, gather multilingual data, and upsert the four `(language, level)` combinations into `algos.db` (`en/ru` × `school/university`).

2. `python scripts/generate_english_md_files.py`  
   Read the English school and university records from the database and render `school.en.md` plus `univer.en.md` for each algorithm.

3. `python scripts/generate_school_ru_md_improved.py`  
   Read the Russian school records (fallback to legacy logic if the DB row is missing) and generate every `school.ru.md`.

4. `python scripts/generate_univer_ru_md.py`  
   Read the Russian university records (with the same fallback) and produce every `univer.ru.md`.

### Workflow Details

This pipeline keeps the database as the single source of truth: update READMEs → run step 1 to refresh DB → run steps 2‑4 to mirror the latest content into all four Markdown files per algorithm folder.

Each script includes detailed logging:
- **enhance_readmes_improved.py**: Shows every SQL INSERT/UPDATE statement with full parameter values
- **Generator scripts**: Display which DB records are being extracted and which files are being written

