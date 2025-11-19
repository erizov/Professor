#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade Java algorithm files to use java.util.logging instead of System.out.println.
- Targets files named Algorithm.java under semester_*/**
- Adds import java.util.logging.Logger; if missing
- Adds private static final Logger logger = Logger.getLogger(Algorithm.class.getName()); inside class if missing
- Replaces System.out.println(...) -> logger.info(...)
- Replaces System.err.println(...) -> logger.severe(...)
- Simplifies banner prints ("==", "--") by converting to concise logger.info messages
- Idempotent: running multiple times should not duplicate imports/fields

Usage:
    python scripts/upgrade_java_logging.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IMPORT_LOGGER = "import java.util.logging.Logger;"
LOGGER_FIELD = (
    "private static final Logger logger = Logger.getLogger(Algorithm.class.getName());"
)


def add_imports(content: str) -> str:
    if IMPORT_LOGGER in content:
        return content
    # Insert after package/imports block if present, else at top
    lines = content.splitlines()
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("import "):
            insert_idx = i + 1
        elif line.strip().startswith("public class") or line.strip().startswith(
            "class "
        ):
            insert_idx = i
            break
    lines.insert(insert_idx, IMPORT_LOGGER)
    return "\n".join(lines)


def add_logger_field(content: str) -> str:
    if LOGGER_FIELD in content:
        return content
    # Insert just after class declaration
    class_decl = re.search(r"(public\s+class\s+Algorithm\s*\{)", content)
    if not class_decl:
        class_decl = re.search(r"(class\s+Algorithm\s*\{)", content)
    if not class_decl:
        return content
    start = class_decl.end()
    return content[:start] + "\n    " + LOGGER_FIELD + "\n" + content[start:]


def replace_prints(content: str) -> str:
    # Simplify banner prints to concise messages
    banner_patterns = [
        re.compile(r'System\.out\.println\("=+"\);'),
        re.compile(r'System\.out\.println\("-+"\);'),
    ]
    for pat in banner_patterns:
        content = pat.sub('logger.info("-")', content)

    # Replace System.err.println first
    content = re.sub(r"System\.err\.println\(", "logger.severe(", content)
    # Replace System.out.println
    content = re.sub(r"System\.out\.println\(", "logger.info(", content)
    return content


def process_java_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    orig = src
    src = add_imports(src)
    src = add_logger_field(src)
    src = replace_prints(src)
    if src != orig:
        path.write_text(src, encoding="utf-8")
        print(f"updated {path}")
        return True
    return False


def main() -> None:
    updated = 0
    processed = 0
    for p in ROOT.rglob("Algorithm.java"):
        if "semester_" in str(p):
            processed += 1
            if process_java_file(p):
                updated += 1
    print(f"Processed {processed} Java files; updated {updated}.")


if __name__ == "__main__":
    main()
