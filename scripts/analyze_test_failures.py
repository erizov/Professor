#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze test failures and determine if they can be fixed.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_failure_summary() -> Dict:
    """Get summary of test failures."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all Python failures
    cursor.execute("""
        SELECT DISTINCT algorithm_path, language, status, error_message
        FROM test_results
        WHERE language = 'python' 
        AND status IN ('failure', 'error')
        ORDER BY algorithm_path
    """)
    
    failures = cursor.fetchall()
    
    # Get latest result for each algorithm
    cursor.execute("""
        WITH recent AS (
            SELECT 
                algorithm_path,
                language,
                status,
                error_message,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
            WHERE language = 'python'
        )
        SELECT algorithm_path, status, error_message
        FROM recent
        WHERE rn = 1 AND status IN ('failure', 'error')
        ORDER BY algorithm_path
    """)
    
    latest_failures = cursor.fetchall()
    
    conn.close()
    
    return {
        'all_failures': failures,
        'latest_failures': latest_failures,
        'total_failures': len(latest_failures)
    }

def categorize_error(error_msg: str) -> Tuple[str, bool]:
    """Categorize error and determine if fixable."""
    if not error_msg:
        return "Unknown error", False
    
    error_lower = error_msg.lower()
    
    # Import errors - usually fixable
    if 'import' in error_lower or 'modulenotfounderror' in error_lower:
        return "Import error", True
    
    # Syntax errors - fixable
    if 'syntaxerror' in error_lower or 'syntax error' in error_lower:
        return "Syntax error", True
    
    # Name errors - fixable
    if 'nameerror' in error_lower or 'name error' in error_lower:
        return "Name error", True
    
    # Attribute errors - fixable
    if 'attributeerror' in error_lower or 'attribute error' in error_lower:
        return "Attribute error", True
    
    # Type errors - fixable
    if 'typeerror' in error_lower or 'type error' in error_lower:
        return "Type error", True
    
    # Indentation errors - fixable
    if 'indentationerror' in error_lower or 'indentation error' in error_lower:
        return "Indentation error", True
    
    # File not found - might be fixable
    if 'filenotfounderror' in error_lower or 'file not found' in error_lower:
        return "File not found", True
    
    # Assertion errors - might be fixable (algorithm logic issue)
    if 'assertionerror' in error_lower or 'assertion error' in error_lower:
        return "Assertion error", True
    
    # Test file missing - fixable
    if 'no such file' in error_lower or 'cannot find' in error_lower:
        return "Test file missing", True
    
    # Timeout - might not be fixable (algorithm too slow)
    if 'timeout' in error_lower or 'timed out' in error_lower:
        return "Timeout", False
    
    # Test collection errors - fixable
    if 'collection' in error_lower and 'error' in error_lower:
        return "Test collection error", True
    
    return "Other error", True

def get_detailed_error(algo_path: str) -> str:
    """Get detailed error message for an algorithm."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT error_message, output
        FROM test_results
        WHERE algorithm_path = ? AND language = 'python'
        ORDER BY timestamp DESC
        LIMIT 1
    """, (algo_path,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        error_msg = row[0] or ""
        output = row[1] or ""
        # Extract actual error from pytest output
        if "ERROR" in output or "FAILED" in output:
            lines = output.split('\n')
            for i, line in enumerate(lines):
                if "ERROR" in line or "FAILED" in line or "ImportError" in line or "ModuleNotFoundError" in line:
                    # Get next few lines for context
                    return '\n'.join(lines[max(0, i-2):min(len(lines), i+10)])
        return error_msg[:500]
    return ""

def analyze_failures():
    """Analyze all failures and generate report."""
    summary = get_failure_summary()
    
    print(f"Total Python test failures: {summary['total_failures']}")
    print("=" * 80)
    
    categories = defaultdict(list)
    fixable_count = 0
    unfixable_count = 0
    
    for algo_path, status, error_msg in summary['latest_failures']:
        # Get more detailed error
        detailed_error = get_detailed_error(algo_path)
        category, fixable = categorize_error(detailed_error or error_msg or "")
        categories[category].append((algo_path, detailed_error or error_msg))
        
        if fixable:
            fixable_count += 1
        else:
            unfixable_count += 1
    
    print(f"\nFixable failures: {fixable_count}")
    print(f"Unfixable failures: {unfixable_count}")
    print("\n" + "=" * 80)
    print("Error Categories:")
    print("=" * 80)
    
    for category, items in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        fixable = categorize_error(items[0][1] or "")[1]
        status = "✓ Fixable" if fixable else "✗ Unfixable"
        print(f"\n{category} ({len(items)} failures) - {status}")
        print("-" * 80)
        
        # Show first 5 examples
        for algo_path, error_msg in items[:5]:
            print(f"  {algo_path}")
            if error_msg:
                error_preview = error_msg[:200].replace('\n', ' ')
                print(f"    {error_preview}...")
        
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")
    
    # Generate detailed report
    print("\n" + "=" * 80)
    print("Detailed Fixable Failures (first 20):")
    print("=" * 80)
    
    fixable_items = []
    for algo_path, status, error_msg in summary['latest_failures']:
        category, fixable = categorize_error(error_msg or "")
        if fixable:
            fixable_items.append((algo_path, error_msg, category))
    
    for i, (algo_path, error_msg, category) in enumerate(fixable_items[:20], 1):
        print(f"\n{i}. {algo_path}")
        print(f"   Category: {category}")
        if error_msg:
            error_preview = error_msg[:300].replace('\n', ' ')
            print(f"   Error: {error_preview}...")
    
    if len(fixable_items) > 20:
        print(f"\n... and {len(fixable_items) - 20} more fixable failures")
    
    return {
        'total': summary['total_failures'],
        'fixable': fixable_count,
        'unfixable': unfixable_count,
        'categories': dict(categories),
        'fixable_items': fixable_items
    }

if __name__ == "__main__":
    analyze_failures()

