#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace System.out.println and System.out.printf with logger.info in all Java files.
Then test and commit each file.
"""

import subprocess
import sys
from pathlib import Path
import re
from scripts.fix_java_one_by_one import replace_printf_with_logger, test_single_java_file, commit_file, update_database, init_database

ROOT = Path(__file__).resolve().parents[1]


def get_all_java_files():
    """Get all Algorithm.java files."""
    java_files = []
    for java_file in ROOT.rglob("Algorithm.java"):
        java_files.append(java_file)
    return sorted(java_files)


def main():
    """Main function."""
    print("=" * 80)
    print("REPLACING System.out.println/printf WITH logger.info IN ALL JAVA FILES")
    print("=" * 80)
    print()
    
    init_database()
    
    java_files = get_all_java_files()
    print(f"Found {len(java_files)} Java files")
    print()
    
    modified_count = 0
    tested_count = 0
    passed_count = 0
    committed_count = 0
    
    for i, java_file in enumerate(java_files, 1):
        algo_path = str(java_file.relative_to(ROOT))
        print(f"[{i}/{len(java_files)}] Processing: {algo_path}")
        
        # Try to replace printf/println with logger
        if replace_printf_with_logger(java_file):
            modified_count += 1
            print(f"  [OK] Modified: Replaced System.out.println/printf with logger.info")
            
            # Test the file
            print(f"  Testing...")
            success, output, duration = test_single_java_file(java_file)
            tested_count += 1
            
            if success:
                passed_count += 1
                print(f"  [OK] Tests passed!")
                
                # Update database
                update_database(algo_path, 'success', duration, None, output, True)
                
                # Commit
                if commit_file(java_file):
                    committed_count += 1
                    print(f"  [OK] Committed")
                else:
                    print(f"  [WARN] Commit failed")
            else:
                print(f"  [FAIL] Tests failed")
                error_msg = output[:500] if output else "Unknown error"
                update_database(algo_path, 'failure', duration, error_msg, output, False)
        else:
            # Check if file has System.out.println/printf but no logger
            content = java_file.read_text(encoding='utf-8')
            has_system_out = 'System.out.println' in content or 'System.out.printf' in content
            has_logger = re.search(r'Logger\s+logger\s*=', content) or \
                        re.search(r'Logger\.getLogger', content)
            
            if has_system_out and not has_logger:
                print(f"  [SKIP] Skipped: Has System.out but no logger defined")
            else:
                print(f"  [SKIP] Skipped: No System.out.println/printf found or already using logger")
        
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files: {len(java_files)}")
    print(f"Modified: {modified_count}")
    print(f"Tested: {tested_count}")
    print(f"Passed: {passed_count}")
    print(f"Committed: {committed_count}")
    print("=" * 80)


if __name__ == "__main__":
    main()

