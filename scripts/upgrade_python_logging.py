#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade Python algorithm files to use logging instead of print.
- Targets Python files under semester_*/** that look like algorithm modules
  (algorithm.py or a .py whose name equals its parent directory)
- Inserts:
    from framework.logging_utils import get_logger
    logger = get_logger(__name__)
  if missing
- Replaces print(...) with logger.info(...)
- Heuristics to use debug for noisy visualization lines and info for banners
- Idempotent: multiple runs won't duplicate imports/definitions

Usage:
    python scripts/upgrade_python_logging.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IMPORT_LINE = "from framework.logging_utils import get_logger"
LOGGER_LINE = "logger = get_logger(__name__)"

PRINT_PATTERN = re.compile(r"(^|\s)print\((.*?)\)")
BANNER_PATTERN = re.compile(r"[=\-]{10,}")
VISUAL_CUES = re.compile(r"(Comparing|Swapped|Pass\\s+\d+|Iteration|Step)\b", re.IGNORECASE)


def is_candidate(py_path: Path) -> bool:
    if "tests" in py_path.parts or "framework" in py_path.parts or "web_interface" in py_path.parts or "scripts" in py_path.parts:
        return False
    if not any(p.name.startswith("semester_") for p in py_path.parents):
        return False
    if py_path.name == "algorithm.py":
        return True
    # folder-named module
    if py_path.stem == py_path.parent.name:
        return True
    return False


def ensure_imports(src: str) -> str:
    if IMPORT_LINE in src and LOGGER_LINE in src:
        return src
    lines = src.splitlines()
    insert_idx = 0
    # After shebang/encoding and imports
    for i, line in enumerate(lines[:50]):
        if line.startswith("from ") or line.startswith("import "):
            insert_idx = i + 1
        if line.strip().startswith("T = TypeVar("):
            # keep logger before type vars typically
            break
    if IMPORT_LINE not in src:
        lines.insert(insert_idx, IMPORT_LINE)
        insert_idx += 1
    if LOGGER_LINE not in src:
        lines.insert(insert_idx, LOGGER_LINE)
    return "\n".join(lines)


def replace_prints(src: str) -> str:
    result_lines = []
    for line in src.splitlines():
        if "print(" not in line:
            result_lines.append(line)
            continue
        # Determine logging level based on content
        level = "info"
        if BANNER_PATTERN.search(line):
            level = "info"
        elif VISUAL_CUES.search(line):
            level = "debug"
        # stderr prints
        if "file=sys.stderr" in line or "sys.stderr" in line:
            level = "error"
        # naive transform: print(f"...") -> logger.level(f"...")
        transformed = line.replace("print(", f"logger.{level}(")
        # remove trailing end="" args for prints
        transformed = transformed.replace(", end=\"\")", ")")
        transformed = transformed.replace(", end=\'\')", ")")
        result_lines.append(transformed)
    return "\n".join(result_lines)


def process_file(py_path: Path) -> bool:
    src = py_path.read_text(encoding="utf-8")
    orig = src
    src2 = ensure_imports(src)
    src3 = replace_prints(src2)
    if src3 != orig:
        py_path.write_text(src3, encoding="utf-8")
        print(f"updated {py_path}")
        return True
    return False


def main() -> None:
    updated = 0
    processed = 0
    for py in ROOT.rglob("*.py"):
        if is_candidate(py):
            processed += 1
            try:
                if process_file(py):
                    updated += 1
            except Exception as e:
                print(f"skip {py}: {e}")
    print(f"Processed {processed} Python algorithm files; updated {updated}.")


if __name__ == "__main__":
    main()
