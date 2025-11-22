#!/usr/bin/env python3
"""
Fix logger.info() calls without arguments in Python algorithm files.
"""

import os
import re
from pathlib import Path

def fix_logger_issues():
    """Fix logger.info() calls without arguments in all Python algorithm files."""

    # Get all Python algorithm files
    algorithm_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'target', '.vscode', '.idea', 'node_modules'}]
        for file in files:
            if file == 'algorithm.py':
                algorithm_files.append(Path(root) / file)

    fixed_count = 0

    for file_path in algorithm_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Fix logger.info() calls without arguments
            content = re.sub(r'logger\.info\(\)', 'logger.info("")', content)

            # Fix logger.info() calls with incorrect string formatting
            # Look for patterns like logger.info("message:", variable) which should be logger.info("message: %s", variable)
            content = re.sub(r'logger\.info\("([^"]*):",\s*([^)]+)\)', r'logger.info("\1: {}", \2)', content)

            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                print(f"Fixed logger issues in: {file_path}")
                fixed_count += 1

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"\nFixed logger issues in {fixed_count} Python algorithm files")

if __name__ == "__main__":
    fix_logger_issues()
