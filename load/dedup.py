#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup.py

Local cleanup script that scans algorithm_descriptions and removes duplicate
and subset content within each record.

For each record, the script:
- Checks if Short Description is a subset of Long Description (or vice versa)
- Removes shorter versions when they are contained in longer versions
- Removes exact duplicates, keeping the longer version
- Applies this logic to all description fields:
  * algorithm_definition, technical_description, application, step_by_step
  * simple_explanation, where_its_used, example
  * long_description, short_description

- No web requests are made; everything is done against the existing database.
- For every modified record, the script logs before/after values into
  load/dedup_log.txt so individual records can be reverted later if needed.
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from text_utils import normalize_text, is_content_duplicate

# Target fields - all description fields that might contain overlapping content
TARGET_FIELDS = [
    "algorithm_definition",
    "technical_description",
    "application",
    "step_by_step",
    "simple_explanation",
    "where_its_used",
    "example",
    "long_description",
    "short_description",
]

LOG_PATH = Path(__file__).with_name("dedup_log.txt")


def get_db_path() -> Path:
    """
    Resolve the database path.
    Priority: ../algos.db (project root), fallback to algos.db in current dir,
    then load/algos.db.
    """
    load_dir = Path(__file__).resolve().parent
    candidates = [
        load_dir.parent / "algos.db",
        load_dir / "algos.db",
        load_dir / "load" / "algos.db",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not find algos.db in known locations.")


def is_subset(text1: Optional[str], text2: Optional[str], min_length: int = 20) -> bool:
    """
    Check if text1 is a subset of text2 (i.e., text1 is contained in text2).
    Both texts are normalized for comparison.
    Returns True if text1 is substantially contained within text2.
    """
    if not text1 or not text2:
        return False
    
    # Skip very short texts to avoid false positives
    if len(text1) < min_length or len(text2) < min_length:
        return False
    
    # Normalize both texts
    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)
    
    if not norm1 or not norm2:
        return False
    
    # If text1 is shorter and is contained in text2, it's a subset
    if len(norm1) < len(norm2):
        # Check if norm1 is contained in norm2
        if norm1 in norm2:
            # Additional check: ensure at least 80% of text1's content is in text2
            words1 = set(norm1.split())
            words2 = set(norm2.split())
            if words1:
                overlap = len(words1 & words2)
                coverage = overlap / len(words1) if len(words1) > 0 else 0
                return coverage >= 0.8
    elif len(norm2) < len(norm1):
        # Check if norm2 is contained in norm1
        if norm2 in norm1:
            words1 = set(norm1.split())
            words2 = set(norm2.split())
            if words2:
                overlap = len(words1 & words2)
                coverage = overlap / len(words2) if len(words2) > 0 else 0
                return coverage >= 0.8
    
    return False


def deduplicate_fields(record: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """
    Remove duplicate and subset content between all description fields.
    If a shorter field is contained in a longer field, remove the shorter one.
    Also removes exact duplicates, keeping the longer version.
    Returns a new dictionary with potentially cleaned values.
    """
    values = {field: record.get(field) for field in TARGET_FIELDS}
    to_clear = set()
    
    # Get all fields that have content
    fields_with_content = [
        field for field in TARGET_FIELDS 
        if values.get(field) and values[field].strip()
    ]
    
    # Compare each pair of fields
    for i, field_i in enumerate(fields_with_content):
        if field_i in to_clear:
            continue
        
        text_i = values[field_i]
        len_i = len(text_i)
        
        for field_j in fields_with_content[i + 1:]:
            if field_j in to_clear:
                continue
            
            text_j = values[field_j]
            len_j = len(text_j)
            
            # Skip if both are too short
            if len_i < 20 and len_j < 20:
                continue
            
            # Check if one is a subset of the other
            if is_subset(text_i, text_j):
                # text_i is subset of text_j, clear text_i
                to_clear.add(field_i)
                break
            elif is_subset(text_j, text_i):
                # text_j is subset of text_i, clear text_j
                to_clear.add(field_j)
                continue
            
            # Check for exact duplicates (using existing function)
            if is_content_duplicate(text_i, text_j):
                # Keep the longer one
                if len_i >= len_j:
                    to_clear.add(field_j)
                else:
                    to_clear.add(field_i)
                    break
    
    cleaned = values.copy()
    for field in to_clear:
        cleaned[field] = None
    
    return cleaned


def log_changes(row: sqlite3.Row, before: Dict[str, Optional[str]], after: Dict[str, Optional[str]]):
    """Append before/after changes for a record to the log file."""
    timestamp = datetime.now(timezone.utc).isoformat()
    entry = {
        "timestamp": timestamp,
        "id": row["id"],
        "algorithm_name": row["algorithm_name"],
        "language": row["language"],
        "level": row["level"],
        "before": before,
        "after": after,
    }
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    db_path = get_db_path()
    print(f"Using database: {db_path}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id, algorithm_name, language, level,
            long_description, short_description,
            algorithm_definition, technical_description,
            application, step_by_step,
            simple_explanation, where_its_used, example
        FROM algorithm_descriptions
        """
    )
    rows = cursor.fetchall()

    total_rows = len(rows)
    cleaned_rows = 0

    print(f"Total records scanned: {total_rows}")

    for row in rows:
        before = {
            "long_description": row["long_description"],
            "short_description": row["short_description"],
            "algorithm_definition": row["algorithm_definition"],
            "technical_description": row["technical_description"],
            "application": row["application"],
            "step_by_step": row["step_by_step"],
            "simple_explanation": row["simple_explanation"],
            "where_its_used": row["where_its_used"],
            "example": row["example"],
        }

        after = deduplicate_fields(before)

        if after != before:
            cursor.execute(
                """
                UPDATE algorithm_descriptions
                SET long_description = ?, short_description = ?,
                    algorithm_definition = ?, technical_description = ?,
                    application = ?, step_by_step = ?,
                    simple_explanation = ?, where_its_used = ?, example = ?
                WHERE id = ?
                """,
                (
                    after["long_description"],
                    after["short_description"],
                    after["algorithm_definition"],
                    after["technical_description"],
                    after["application"],
                    after["step_by_step"],
                    after["simple_explanation"],
                    after["where_its_used"],
                    after["example"],
                    row["id"],
                ),
            )
            log_changes(row, before, after)
            cleaned_rows += 1

    conn.commit()
    conn.close()

    print(f"Records cleaned: {cleaned_rows}")
    if cleaned_rows > 0:
        print(f"Detailed logs written to {LOG_PATH}")
    else:
        print("No duplicate sections detected.")


if __name__ == "__main__":
    main()

