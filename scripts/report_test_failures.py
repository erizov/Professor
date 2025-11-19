#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a comprehensive report on test failures and their fixability.
"""

import sqlite3
from pathlib import Path
from collections import defaultdict
import re

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_all_failures():
    """Get all Python test failures with details."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get latest status for ALL tests first, then filter failures
    # This matches the web interface logic
    cursor.execute("""
        WITH recent AS (
            SELECT 
                algorithm_path,
                language,
                status,
                error_message,
                test_output,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
            WHERE language = 'python'
        )
        SELECT algorithm_path, status, error_message, test_output
        FROM recent
        WHERE rn = 1 AND status IN ('failure', 'error')
        ORDER BY algorithm_path
    """)
    
    failures = cursor.fetchall()
    conn.close()
    
    return failures

def extract_error_type(error_msg, test_output):
    """Extract the actual error type from error message or test output."""
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Look for common error patterns
    patterns = [
        (r'ImportError: (.+)', 'ImportError'),
        (r'ModuleNotFoundError: (.+)', 'ModuleNotFoundError'),
        (r'TypeError: (.+)', 'TypeError'),
        (r'AttributeError: (.+)', 'AttributeError'),
        (r'NameError: (.+)', 'NameError'),
        (r'SyntaxError: (.+)', 'SyntaxError'),
        (r'IndentationError: (.+)', 'IndentationError'),
        (r'FileNotFoundError: (.+)', 'FileNotFoundError'),
        (r'AssertionError: (.+)', 'AssertionError'),
        (r'cannot import name (\w+)', 'ImportError'),
        (r'has no attribute (\w+)', 'AttributeError'),
    ]
    
    for pattern, error_type in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return error_type
    
    # Check for specific error messages
    if 'import' in text.lower() and 'error' in text.lower():
        return 'ImportError'
    if 'cannot import' in text.lower():
        return 'ImportError'
    if 'no module named' in text.lower():
        return 'ModuleNotFoundError'
    
    return 'Unknown'

def is_fixable(error_type, error_msg, test_output):
    """Determine if the error is fixable."""
    text = (error_msg or "") + "\n" + (test_output or "")
    
    # Check for actual timeout errors (not just pytest timeout plugin output)
    # Look for timeout errors in the actual error message, not in pytest headers
    timeout_patterns = [
        'test exceeded timeout',
        'timed out',
        'timeout expired',
        'timeout of',
        'status.*timeout',  # Status is timeout
    ]
    
    # Only check for timeout if it's in an error context, not in pytest config
    error_section = text.lower()
    # Remove pytest header info that always contains "timeout: X.Xs"
    if 'test session starts' in error_section:
        # Find where the actual error starts
        error_start = error_section.find('failures') or error_section.find('errors') or error_section.find('error:')
        if error_start > 0:
            error_section = error_section[error_start:]
    
    for pattern in timeout_patterns:
        if pattern in error_section:
            return False
    
    # Check if status is actually "timeout"
    # This is more reliable than parsing text
    # (We'll check this in the calling code if needed)
    
    # All other errors are generally fixable:
    # - Import errors: fix imports
    # - Type errors: fix type mismatches
    # - Attribute errors: fix attribute access
    # - Assertion errors: fix algorithm logic or test expectations
    # - Syntax errors: fix syntax
    # - Name errors: fix variable/function names
    return True

def generate_report():
    """Generate comprehensive failure report."""
    failures = get_all_failures()
    
    print("=" * 80)
    print("PYTHON TEST FAILURE ANALYSIS REPORT")
    print("=" * 80)
    print(f"\nTotal Failures: {len(failures)}")
    print()
    
    # Categorize failures
    categories = defaultdict(list)
    fixable_count = 0
    unfixable_count = 0
    
    for algo_path, status, error_msg, test_output in failures:
        error_type = extract_error_type(error_msg, test_output)
        fixable = is_fixable(error_type, error_msg, test_output)
        
        categories[error_type].append({
            'path': algo_path,
            'error_type': error_type,
            'fixable': fixable,
            'error_msg': error_msg,
            'test_output': test_output
        })
        
        if fixable:
            fixable_count += 1
        else:
            unfixable_count += 1
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Fixable: {fixable_count} ({fixable_count/len(failures)*100:.1f}%)")
    print(f"Unfixable: {unfixable_count} ({unfixable_count/len(failures)*100:.1f}%)")
    print()
    
    # Error categories
    print("=" * 80)
    print("ERROR CATEGORIES")
    print("=" * 80)
    for error_type in sorted(categories.keys(), key=lambda x: len(categories[x]), reverse=True):
        items = categories[error_type]
        fixable_items = [i for i in items if i['fixable']]
        print(f"\n{error_type}: {len(items)} failures")
        print(f"  Fixable: {len(fixable_items)}")
        print(f"  Unfixable: {len(items) - len(fixable_items)}")
        
        # Show examples
        print("  Examples:")
        for item in items[:3]:
            print(f"    - {item['path']}")
            # Extract specific error detail
            text = (item['error_msg'] or "") + "\n" + (item['test_output'] or "")
            error_detail = re.search(r'(ImportError|TypeError|AttributeError|NameError|SyntaxError|IndentationError|FileNotFoundError|AssertionError|ModuleNotFoundError):\s*(.+)', text, re.IGNORECASE)
            if error_detail:
                print(f"      {error_detail.group(1)}: {error_detail.group(2)[:100]}")
    
    # Detailed fixable failures
    print("\n" + "=" * 80)
    print("FIXABLE FAILURES (Sample)")
    print("=" * 80)
    
    fixable_items = [item for category in categories.values() for item in category if item['fixable']]
    
    for i, item in enumerate(fixable_items[:20], 1):
        print(f"\n{i}. {item['path']}")
        print(f"   Error Type: {item['error_type']}")
        
        # Extract specific error
        text = (item['error_msg'] or "") + "\n" + (item['test_output'] or "")
        error_detail = re.search(r'(ImportError|TypeError|AttributeError|NameError|SyntaxError|IndentationError|FileNotFoundError|AssertionError|ModuleNotFoundError):\s*(.+)', text, re.IGNORECASE)
        if error_detail:
            print(f"   Error: {error_detail.group(1)}: {error_detail.group(2)[:150]}")
        elif 'cannot import' in text.lower():
            import_match = re.search(r'cannot import (?:name )?[\'"]?(\w+)[\'"]?', text, re.IGNORECASE)
            if import_match:
                print(f"   Error: Cannot import {import_match.group(1)}")
    
    if len(fixable_items) > 20:
        print(f"\n... and {len(fixable_items) - 20} more fixable failures")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print(f"\n[FIXABLE] {fixable_count} failures can be fixed")
    print(f"  - Most common issues: Import errors, type errors, attribute errors")
    print(f"  - These are typically caused by:")
    print(f"    * Incorrect imports in test files")
    print(f"    * Missing or incorrect class/function names")
    print(f"    * Type mismatches in function calls")
    print(f"    * Missing attributes or methods")
    print(f"\n[UNFIXABLE] {unfixable_count} failures may require algorithm changes or are timeouts")
    
    return {
        'total': len(failures),
        'fixable': fixable_count,
        'unfixable': unfixable_count,
        'categories': dict(categories)
    }

if __name__ == "__main__":
    generate_report()

