# Textbook Search and Filter Features

This document describes the search and filter functionality added to the comprehensive textbook.

## Quick Reference

### To regenerate TOC:
```bash
python scripts/generate_textbook_toc.py
```

### To regenerate interactive HTML:
```bash
python scripts/generate_interactive_textbook.py
```

### To use the interactive textbook:
1. Open `COMPREHENSIVE_COURSE_TEXTBOOK.html` in your web browser
2. Use the search box to find algorithms by name
3. Use the dropdown filters to narrow down by semester or category
4. Check/uncheck language or difficulty boxes to filter
5. The results counter shows how many algorithms match your criteria
6. Click "Clear All Filters" to reset

---

## Features Added

### 1. Table of Contents (TOC)

A comprehensive table of contents has been automatically generated and inserted into the `COMPREHENSIVE_COURSE_TEXTBOOK.md` file. The TOC includes:

- **Quick Navigation**: Links to major sections
- **Algorithms by Semester**: Organized by semester (1-16)
- **Algorithms by Category**: Grouped by algorithm type (Sorting, Searching, Data Structure, etc.)
- **Algorithms by Language**: Filtered by programming language (Python, Java, SQL)
- **Algorithms by Difficulty**: Separated into Undergraduate (Semesters 1-8) and Graduate (Semesters 9-16)
- **Full Algorithm List**: Complete table with all algorithms and their metadata

The TOC is automatically updated when you run the generation script.

### 2. Interactive HTML Textbook

An interactive HTML version of the textbook has been generated with advanced search and filter capabilities.

**File**: `COMPREHENSIVE_COURSE_TEXTBOOK.html`

**Features**:
- **Search by Name**: Real-time search as you type algorithm names
- **Filter by Semester**: Dropdown to select specific semesters
- **Filter by Category/Type**: Filter by algorithm category (Sorting, Searching, etc.)
- **Filter by Programming Language**: Checkboxes for Python, Java, SQL
- **Filter by Difficulty**: Checkboxes for Undergraduate/Graduate levels
- **Results Counter**: Shows how many algorithms match current filters
- **Clear Filters Button**: Reset all filters with one click

## Usage

### Generating/Updating Table of Contents

To regenerate the table of contents (useful after adding new algorithms):

```bash
python scripts/generate_textbook_toc.py
```

This will:
1. Extract metadata from all algorithm folders
2. Extract headings from the textbook
3. Generate a comprehensive TOC
4. Insert it into the textbook (between `<!-- TABLE_OF_CONTENTS -->` markers)
5. Save a standalone copy to `TABLE_OF_CONTENTS.md`

### Generating Interactive HTML Version

To generate or update the interactive HTML textbook:

```bash
python scripts/generate_interactive_textbook.py
```

This will:
1. Extract algorithm metadata (name, semester, category, languages, difficulty)
2. Convert the Markdown textbook to HTML
3. Add JavaScript for search and filtering
4. Generate a self-contained HTML file: `COMPREHENSIVE_COURSE_TEXTBOOK.html`

**Note**: The HTML file is large (several MB) due to the comprehensive content. Open it in a modern web browser for the best experience.

### Using the Interactive HTML Textbook

1. Open `COMPREHENSIVE_COURSE_TEXTBOOK.html` in your web browser
2. Use the search box to find algorithms by name
3. Use the dropdown filters to narrow down by semester or category
4. Check/uncheck language or difficulty boxes to filter
5. The results counter shows how many algorithms match your criteria
6. Click "Clear All Filters" to reset

## How It Works

### Algorithm Metadata Extraction

The scripts automatically extract metadata from:
- **Folder structure**: Semester and lecture information from paths
- **metadata.json files**: Category and complexity information
- **File presence**: Determines available languages (Python, Java, SQL)
- **Semester number**: Determines difficulty level (1-8 = Undergraduate, 9-16 = Graduate)

### Filtering Logic

The interactive HTML uses JavaScript to:
1. Match algorithm names in headings
2. Show/hide algorithm sections based on filter criteria
3. Update the results counter in real-time
4. Handle multiple filter combinations

## Integration with CI/CD

You can integrate these scripts into your CI/CD pipeline to ensure the TOC and HTML version stay up to date:

```yaml
- name: Generate Table of Contents
  run: python scripts/generate_textbook_toc.py

- name: Generate Interactive HTML
  run: python scripts/generate_interactive_textbook.py

- name: Check if files were updated
  run: |
    if [ -n "$(git status --porcelain COMPREHENSIVE_COURSE_TEXTBOOK.md COMPREHENSIVE_COURSE_TEXTBOOK.html)" ]; then
      echo "Textbook files need to be updated"
      git diff COMPREHENSIVE_COURSE_TEXTBOOK.md
      exit 1
    fi
```

## File Locations

- **Markdown Textbook**: `COMPREHENSIVE_COURSE_TEXTBOOK.md`
- **Interactive HTML**: `COMPREHENSIVE_COURSE_TEXTBOOK.html`
- **Standalone TOC**: `TABLE_OF_CONTENTS.md`
- **TOC Generator Script**: `scripts/generate_textbook_toc.py`
- **HTML Generator Script**: `scripts/generate_interactive_textbook.py`

## Dependencies

- **Python 3.8+**
- **markdown** library (install with `pip install markdown`)

## Notes

- The TOC is inserted between `<!-- TABLE_OF_CONTENTS -->` and `<!-- END_TABLE_OF_CONTENTS -->` markers
- The HTML version is self-contained (no external dependencies)
- Algorithm matching uses fuzzy matching to handle variations in naming
- The HTML file may take a few seconds to load due to its size

## Future Enhancements

Potential improvements:
- Export filtered results to PDF
- Bookmark/favorite algorithms
- Print-friendly view
- Dark mode toggle
- Algorithm comparison view
- Export search results

