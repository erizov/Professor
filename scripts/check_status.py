#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check status of replace_printf_logger_all script."""

import sqlite3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

# Check database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Count recent Java test results
cursor.execute("""
    SELECT COUNT(*) FROM test_results 
    WHERE language = 'java' AND status = 'success'
""")
success_count = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM test_results 
    WHERE language = 'java'
""")
total_count = cursor.fetchone()[0]

# Count files with System.out
java_files = list(ROOT.rglob("Algorithm.java"))
files_with_system_out = 0
files_with_logger_and_system_out = 0

for java_file in java_files[:100]:  # Sample first 100
    try:
        content = java_file.read_text(encoding='utf-8')
        has_system_out = 'System.out.println' in content or 'System.out.printf' in content
        has_logger = re.search(r'Logger\s+logger\s*=', content) or \
                    re.search(r'Logger\.getLogger', content)
        
        if has_system_out:
            files_with_system_out += 1
            if has_logger:
                files_with_logger_and_system_out += 1
    except:
        pass

conn.close()

print(f"Database Status:")
print(f"  Total Java test records: {total_count}")
print(f"  Successful Java tests: {success_count}")
print(f"\nFile Status (sample of 100 files):")
print(f"  Files with System.out: {files_with_system_out}")
print(f"  Files with logger AND System.out: {files_with_logger_and_system_out}")

