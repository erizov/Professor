# Code Synchronization System

## Overview

This system provides **one-directional code synchronization** from individual algorithm files to the comprehensive textbook. This ensures:

- ✅ **Source files are the source of truth** - Individual Python, Java, and SQL files remain testable and working
- ✅ **Textbook stays updated** - Code in the textbook automatically reflects changes in source files
- ✅ **Manual textbook edits are preserved** - Changes to textbook text/narrative don't affect source files
- ✅ **CI/CD integration** - Can be run automatically in CI pipelines

## How It Works

### Code Markers

The textbook uses HTML comment markers to identify where code should be inserted:

```markdown
<!-- CODE:semester_01/lecture_01_sorting_fundamentals/bubble_sort/algorithm.py:python -->
```python
# Code from algorithm.py will be inserted here
```
<!-- END_CODE -->
```

### One-Directional Flow

```
Source Files (algorithm.py, Algorithm.java, algorithm.sql)
    ↓
    [sync_code_to_textbook.py]
    ↓
Comprehensive Textbook (COMPREHENSIVE_COURSE_TEXTBOOK.md)
```

**Important**: Changes flow ONLY from source files → textbook, never the reverse.

## Usage

### Initial Setup (One-Time)

Insert code markers in the textbook:

```bash
python scripts/sync_code_to_textbook.py --insert-markers --no-update
```

This will scan all algorithm folders and insert markers where code should be synced.

### Update Code in Textbook

Update the textbook with latest code from source files:

```bash
python scripts/sync_code_to_textbook.py
```

Or explicitly:

```bash
python scripts/sync_code_to_textbook.py --update-code
```

### Both Operations

Run both marker insertion and code update:

```bash
python scripts/sync_code_to_textbook.py --insert-markers
```

## Workflow

### For Developers

1. **Modify source files** (algorithm.py, Algorithm.java, algorithm.sql)
2. **Test your changes** using unit tests
3. **Run sync script** to update textbook:
   ```bash
   python scripts/sync_code_to_textbook.py
   ```
4. **Commit both** source files and updated textbook

### For CI/CD

Add to your CI workflow:

```yaml
- name: Sync code to textbook
  run: python scripts/sync_code_to_textbook.py
```

This ensures the textbook is always up-to-date with source code.

## File Structure

```
project/
├── semester_01/
│   └── lecture_01_sorting_fundamentals/
│       └── bubble_sort/
│           ├── algorithm.py          ← Source of truth
│           ├── Algorithm.java        ← Source of truth
│           ├── algorithm.sql         ← Source of truth (if applicable)
│           └── test_algorithm.py     ← Tests ensure code works
├── COMPREHENSIVE_COURSE_TEXTBOOK.md  ← Auto-generated code blocks
└── scripts/
    └── sync_code_to_textbook.py      ← Sync script
```

## Marker Format

Code markers use this format:

```html
<!-- CODE:relative/path/to/file.py:python -->
```

Where:
- `relative/path/to/file.py` is the path relative to project root
- `python`, `java`, or `sql` indicates the code type

## Benefits

1. **Single Source of Truth**: Source files are always the authoritative version
2. **Testability**: Individual files can be unit tested independently
3. **Consistency**: Textbook code always matches working source code
4. **Maintainability**: Fix bugs once in source, textbook updates automatically
5. **Documentation Safety**: Manual edits to textbook narrative are preserved

## Troubleshooting

### Markers Not Found

If you see "No code markers found", run:

```bash
python scripts/sync_code_to_textbook.py --insert-markers
```

### Code Not Updating

Check that:
1. Source file exists at the path specified in marker
2. Source file is readable
3. Marker format is correct: `<!-- CODE:path:type -->`

### Encoding Issues

The script uses UTF-8 encoding. If you encounter encoding errors:
- Ensure source files are UTF-8 encoded
- Check that textbook file is UTF-8

## Integration with CI

Add this step to your CI workflow after tests pass:

```yaml
- name: Sync code to textbook
  run: |
    python scripts/sync_code_to_textbook.py
    git diff --exit-code COMPREHENSIVE_COURSE_TEXTBOOK.md || \
      (echo "Textbook needs update" && exit 1)
```

This ensures the textbook is always in sync with source files.

