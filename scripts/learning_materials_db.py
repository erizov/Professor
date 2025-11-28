#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared helpers for learning-material generators.

Provides:
- Stable lookup of algorithm identifiers based on README or folder name.
- SQLite accessors for the `algorithm_descriptions` table in algos.db.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Dict, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

LOCAL_SOURCE_SITE = "local_markdown"
ALGO_DB_CANDIDATES = [
    ROOT / "algos.db",
    ROOT / "load" / "algos.db",
    ROOT / "database" / "algos.db",
]
ALGOS_DB_PATH = next(
    (path for path in ALGO_DB_CANDIDATES if path.exists()),
    ALGO_DB_CANDIDATES[0],
)
_ALGO_DESC_COLUMNS_CACHE: set[str] = set()


def _slugify(value: str) -> str:
    """Convert display name to normalized key."""
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "algorithm"


def read_algorithm_identifiers(readme_path: Path) -> Tuple[str, str]:
    """Return (algorithm_key, display_name) using README first heading."""
    display_name = ""
    if readme_path.exists():
        try:
            for line in readme_path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped.startswith("#"):
                    display_name = stripped.lstrip("#").strip()
                    break
        except Exception:
            display_name = ""
    
    if not display_name:
        display_name = readme_path.parent.name.replace("_", " ").title()
    
    slug = _slugify(display_name)
    if not slug:
        slug = _slugify(readme_path.parent.name)
    
    return slug, display_name


def read_algorithm_identifiers_from_folder(folder_path: Path) -> Tuple[str, str]:
    """Return (algorithm_key, display_name) for a folder."""
    readme_path = folder_path / "README.md"
    if readme_path.exists():
        return read_algorithm_identifiers(readme_path)
    
    display_name = folder_path.name.replace("_", " ").title()
    slug = _slugify(display_name)
    if not slug:
        slug = _slugify(folder_path.name)
    return slug, display_name


def get_algos_db_connection() -> Optional[sqlite3.Connection]:
    """Get connection to the algorithm descriptions database."""
    try:
        ALGOS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(ALGOS_DB_PATH))
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
    except Exception:
        return None


def ensure_algorithm_descriptions_schema(conn: sqlite3.Connection) -> None:
    """Ensure algorithm_descriptions table exists with required columns."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS algorithm_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm_name TEXT NOT NULL,
            language TEXT NOT NULL,
            level TEXT NOT NULL,
            title TEXT,
            short_description TEXT,
            long_description TEXT,
            simple_explanation TEXT,
            where_its_used TEXT,
            example TEXT,
            example_snippet TEXT,
            source_url TEXT,
            source_site TEXT,
            quality_score REAL DEFAULT 0.0,
            fetched_at TEXT DEFAULT CURRENT_TIMESTAMP,
            discipline TEXT,
            algorithm_definition TEXT,
            technical_description TEXT,
            application TEXT,
            step_by_step TEXT,
            self_check_basic TEXT,
            self_check_intermediate TEXT,
            self_check_advanced TEXT,
            practical_tasks_basic TEXT,
            practical_tasks_applied TEXT,
            practical_tasks_research TEXT,
            ethical_reasoning TEXT,
            extra_chapters TEXT,
            UNIQUE(algorithm_name, language, level)
        )
        """
    )
    conn.commit()


def get_algorithm_description_columns(conn: sqlite3.Connection) -> set[str]:
    """Return column names for algorithm_descriptions table."""
    global _ALGO_DESC_COLUMNS_CACHE
    if _ALGO_DESC_COLUMNS_CACHE:
        return _ALGO_DESC_COLUMNS_CACHE
    ensure_algorithm_descriptions_schema(conn)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(algorithm_descriptions)")
    _ALGO_DESC_COLUMNS_CACHE = {row[1] for row in cursor.fetchall()}
    return _ALGO_DESC_COLUMNS_CACHE


def fetch_learning_record(
    algorithm_key: str,
    language: str,
    level: str,
) -> Optional[Dict[str, Optional[str]]]:
    """Fetch a single learning record from the database."""
    conn = get_algos_db_connection()
    if not conn:
        return None
    
    try:
        ensure_algorithm_descriptions_schema(conn)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM algorithm_descriptions
            WHERE algorithm_name = ?
              AND language = ?
              AND level = ?
            LIMIT 1
            """,
            (algorithm_key, language, level),
        )
        row = cursor.fetchone()
        if not row:
            return None
        columns = [description[0] for description in cursor.description]
        return {columns[i]: row[i] for i in range(len(columns))}
    finally:
        conn.close()


def fetch_learning_record_for_folder(
    folder_path: Path,
    language: str,
    level: str,
) -> Optional[Dict[str, Optional[str]]]:
    """Convenience wrapper to fetch record for a folder path."""
    algorithm_key, _ = read_algorithm_identifiers_from_folder(folder_path)
    return fetch_learning_record(algorithm_key, language, level)

