# Bidirectional Amendment Files Sync

This document describes the bidirectional synchronization system between amendment files and the comprehensive textbook.

## Overview

The bidirectional sync system maintains synchronized content between 10 amendment files and the `COMPREHENSIVE_COURSE_TEXTBOOK.md`. Changes made to either the amendment files or the textbook are automatically reflected in both locations.

## Amendment Files

The following files are synchronized with the textbook:

1. **ASSESSMENT_FRAMEWORK.md** - Comprehensive evaluation system
2. **CLIENT_READY_TEMPLATES.md** - Professional service templates
3. **CODE_OF_CONDUCT.md** - Community guidelines
4. **COLLABORATION_TOOLS.md** - Collaboration and communication tools
5. **GAMIFICATION_SYSTEM.md** - Gamification and engagement system
6. **LEARNING_PATHS.md** - Learning path guides
7. **METACOGNITIVE_STRATEGIES.md** - Learning strategies
8. **MLOPS_INTEGRATION_GUIDE.md** - MLOps integration guide
9. **STRATEGIC_DOCUMENTATION.md** - Documentation strategies
10. **TEACHING_RESOURCES.md** - Teaching resources and materials

## How It Works

### Sync Markers

The sync system uses HTML comment markers to identify synchronized sections:

- **Start Marker**: `<!-- SYNC_START:FILENAME.md -->`
- **End Marker**: `<!-- SYNC_END:FILENAME.md -->`

Content between these markers is synchronized bidirectionally.

### Sync Directions

1. **Sync to Textbook** (`--sync-to-textbook`):
   - Reads content from amendment files
   - Updates corresponding sections in the textbook
   - Preserves header information in amendment files

2. **Sync from Textbook** (`--sync-from-textbook`):
   - Reads content from textbook sync sections
   - Updates corresponding amendment files
   - Preserves header information in amendment files

3. **Sync Both** (`--sync-both`):
   - Syncs in both directions
   - Useful for ensuring complete synchronization

## Usage

### Sync Amendment Files to Textbook

To update the textbook with changes from amendment files:

```bash
python scripts/sync_amendments_bidirectional.py --sync-to-textbook
```

This is the default behavior if no option is specified.

### Sync Textbook to Amendment Files

To update amendment files with changes from the textbook:

```bash
python scripts/sync_amendments_bidirectional.py --sync-from-textbook
```

### Sync in Both Directions

To sync in both directions:

```bash
python scripts/sync_amendments_bidirectional.py --sync-both
```

## Integration with PDF Generation

The `generate_comprehensive_pdf.py` script has been updated to:

1. **Extract synced content** from the textbook's sync sections
2. **Use synced content** when generating the PDF
3. **Fallback to files** if sync sections are not found

This ensures the PDF always contains the most up-to-date synchronized content.

## Workflow

### Recommended Workflow

1. **Make changes** to either:
   - Individual amendment files (e.g., `ASSESSMENT_FRAMEWORK.md`)
   - Or the textbook's sync sections

2. **Run sync script**:
   ```bash
   python scripts/sync_amendments_bidirectional.py
   ```

3. **Verify changes** in both locations

4. **Generate PDF** (if needed):
   ```bash
   python scripts/generate_comprehensive_pdf.py
   ```

### Before Committing

Always run the sync script before committing to ensure both files are synchronized:

```bash
# Sync to ensure everything is up to date
python scripts/sync_amendments_bidirectional.py --sync-both

# Check for changes
git status

# Commit if needed
git add COMPREHENSIVE_COURSE_TEXTBOOK.md *.md
git commit -m "Update amendment files and sync with textbook"
```

## File Structure

### Amendment File Structure

Each amendment file should have:

```markdown
# Title

> **📚 This document is part of the comprehensive course materials.**  
> For the complete textbook, see: [COMPREHENSIVE_COURSE_TEXTBOOK.md](COMPREHENSIVE_COURSE_TEXTBOOK.md)  
> This content is also included in the textbook as Appendix: [Title].

---

[Content here - this is what gets synced]
```

### Textbook Sync Section Structure

In the textbook, each amendment has a section like:

```markdown
## [Title]

<!-- SYNC_START:FILENAME.md -->
*This section is synchronized with [Title](FILENAME.md). Changes to either file will be reflected in both.*

[Synced content here]

<!-- SYNC_END:FILENAME.md -->
```

## CI/CD Integration

You can integrate the sync script into your CI/CD pipeline:

```yaml
- name: Sync Amendment Files
  run: |
    python scripts/sync_amendments_bidirectional.py --sync-both
    
- name: Check if sync updated files
  run: |
    if [ -n "$(git status --porcelain COMPREHENSIVE_COURSE_TEXTBOOK.md)" ]; then
      echo "Textbook was updated by sync. Please commit changes."
      git diff COMPREHENSIVE_COURSE_TEXTBOOK.md
      exit 1
    fi
```

## Troubleshooting

### Sync Section Not Found

If you see "Warning: No sync section found in textbook for FILENAME.md":

1. Run `--sync-to-textbook` to create the sync section
2. The section will be added to the Appendices area

### Content Not Syncing

If content is not syncing properly:

1. Check that markers are correct: `<!-- SYNC_START:FILENAME.md -->` and `<!-- SYNC_END:FILENAME.md -->`
2. Verify file names match exactly (case-sensitive)
3. Check for encoding issues (files should be UTF-8)

### Header Information Lost

The sync script preserves header information (title, links) in amendment files. If headers are being modified:

1. Check the file structure matches the expected format
2. The script preserves everything before the first `---` separator

## Benefits

1. **Single Source of Truth**: Content can be edited in either location
2. **Consistency**: Ensures textbook and amendment files stay in sync
3. **Flexibility**: Edit in the most convenient location
4. **Automation**: Reduces manual copy-paste errors
5. **Version Control**: Both files are tracked in git

## Notes

- The sync is **bidirectional** - changes to either side are reflected in both
- Header information (title, links) in amendment files is preserved
- The sync script is idempotent - running it multiple times is safe
- Always run sync before generating PDFs to ensure latest content

