# Multilingual parity (EN / RU, school / univer)

**Goal:** Treat English and Russian, and school and university levels, as first-class. Track gaps and reduce them over time.

## How we track

- **Content health:** `python scripts/content_health_report.py` reports counts by semester and by level/language (school.en, school.ru, univer.en, univer.ru). Use `--only-problems` to list missing or placeholder-heavy files.
- **Find files needing generation:** `python scripts/find_files_needing_generation.py` lists MD files that are missing or full of placeholders.
- **Broken links:** `python scripts/check_content_and_links.py --links` checks internal MD links.

## Targets (optional)

- Prefer generating EN first, then RU for the same algorithm/level so both languages stay in sync.
- Use the same placeholder and “needs generation” rules for all four level×language combinations (see `core/content_metadata.py`).

## See also

- [TEACHER_QUICKSTART.md](TEACHER_QUICKSTART.md) — workflow to generate EN and RU content.
- [IMPROVEMENTS_AND_FEATURES_PLAN.md](IMPROVEMENTS_AND_FEATURES_PLAN.md) — content and quality section.
