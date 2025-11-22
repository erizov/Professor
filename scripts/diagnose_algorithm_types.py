#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnose algorithm type matching issues.
"""

import sqlite3
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
TEST_DB = ROOT / "test_results.db"
ALGO_DB = ROOT / "database" / "algorithms.db"


def normalize_path(path):
    """Normalize path for comparison."""
    if not path:
        return ""
    return str(path).replace("\\", "/").rstrip("/")


def main():
    """Diagnose issues."""
    print("=" * 70)
    print("ALGORITHM TYPE DIAGNOSIS")
    print("=" * 70)
    print()
    
    # Load algorithm types
    algo_conn = sqlite3.connect(ALGO_DB)
    algo_cursor = algo_conn.cursor()
    algo_cursor.execute("SELECT folder_path, algorithm_type FROM algorithms")
    algo_types = {}
    for row in algo_cursor.fetchall():
        folder_path, algo_type = row
        normalized = normalize_path(folder_path)
        algo_types[normalized] = algo_type
        algo_types[folder_path] = algo_type  # Also store original
    algo_conn.close()
    
    print(f"Loaded {len(algo_types)} algorithm type mappings")
    print()
    
    # Check test results
    test_conn = sqlite3.connect(TEST_DB)
    test_cursor = test_conn.cursor()
    
    # Get latest test results
    test_cursor.execute("""
        WITH recent_results AS (
            SELECT 
                algorithm_path,
                language,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
        )
        SELECT DISTINCT algorithm_path, language
        FROM recent_results
        WHERE rn = 1
    """)
    
    test_results = test_cursor.fetchall()
    test_conn.close()
    
    print(f"Found {len(test_results)} test results")
    print()
    
    # Check matching
    matched = defaultdict(int)
    unmatched = []
    type_counts = defaultdict(int)
    
    for test_path, language in test_results:
        normalized_test = normalize_path(test_path)
        algo_type = algo_types.get(normalized_test) or algo_types.get(test_path) or "unknown"
        
        if algo_type == "unknown":
            unmatched.append((test_path, language))
        else:
            matched[algo_type] += 1
            type_counts[algo_type] += 1
    
    print("Algorithm types found in test results:")
    for algo_type in sorted(type_counts.keys()):
        print(f"  {algo_type}: {type_counts[algo_type]}")
    print()
    
    print(f"Unmatched test results: {len(unmatched)}")
    if unmatched:
        print("Sample unmatched paths:")
        for path, lang in unmatched[:10]:
            print(f"  {path} ({lang})")
    print()
    
    # Check specific types
    target_types = ["sorting", "searching", "dynamic_programming", "string_algorithms", "greedy"]
    print("Checking target types:")
    for target_type in target_types:
        count = type_counts.get(target_type, 0)
        print(f"  {target_type}: {count} test results")
        
        # Find sample paths
        if count == 0:
            # Find algorithms with this type
            algo_conn = sqlite3.connect(ALGO_DB)
            algo_cursor = algo_conn.cursor()
            algo_cursor.execute(
                "SELECT folder_path FROM algorithms WHERE algorithm_type = ? LIMIT 3",
                (target_type,)
            )
            algo_paths = [row[0] for row in algo_cursor.fetchall()]
            algo_conn.close()
            
            print(f"    Sample algorithm paths with this type:")
            for path in algo_paths:
                print(f"      {path}")
                
                # Check if there are test results for similar paths
                test_conn = sqlite3.connect(TEST_DB)
                test_cursor = test_conn.cursor()
                normalized_algo = normalize_path(path)
                test_cursor.execute(
                    "SELECT DISTINCT algorithm_path FROM test_results WHERE algorithm_path LIKE ? LIMIT 3",
                    (f"%{normalized_algo.split('/')[-1]}%",)
                )
                similar_paths = [row[0] for row in test_cursor.fetchall()]
                test_conn.close()
                
                if similar_paths:
                    print(f"      Similar test result paths:")
                    for similar in similar_paths:
                        print(f"        {similar}")
    print()
    
    # Check Java vs Python
    java_count = sum(1 for _, lang in test_results if lang.lower() == "java")
    python_count = sum(1 for _, lang in test_results if lang.lower() == "python")
    
    print(f"Test results by language:")
    print(f"  Java: {java_count}")
    print(f"  Python: {python_count}")
    print()
    
    # Count actual files
    java_files = list(ROOT.rglob("**/Algorithm.java"))
    python_files = list(ROOT.rglob("**/algorithm.py"))
    
    print(f"Actual files on disk:")
    print(f"  Java files: {len(java_files)}")
    print(f"  Python files: {len(python_files)}")
    print()
    
    # Find Java files without test results
    java_paths = {normalize_path(f.parent.relative_to(ROOT)) for f in java_files}
    python_paths = {normalize_path(f.parent.relative_to(ROOT)) for f in python_files}
    
    test_paths = {normalize_path(path) for path, _ in test_results}
    
    java_untested = java_paths - test_paths
    python_untested = python_paths - test_paths
    
    print(f"Untested algorithms:")
    print(f"  Java: {len(java_untested)}")
    print(f"  Python: {len(python_untested)}")
    
    if java_untested:
        print(f"  Sample untested Java algorithms:")
        for path in list(java_untested)[:5]:
            print(f"    {path}")
    
    if python_untested:
        print(f"  Sample untested Python algorithms:")
        for path in list(python_untested)[:5]:
            print(f"    {path}")


if __name__ == "__main__":
    main()

