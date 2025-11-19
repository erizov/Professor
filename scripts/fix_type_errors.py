#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix TypeError failures - tests importing __init__ instead of classes/functions."""

import ast
import re
from pathlib import Path
from typing import List, Optional
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

def get_type_errors():
    """Get algorithms with TypeError."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
        SELECT algorithm_path, error_message, test_output
        FROM recent
        WHERE rn = 1 AND status IN ('failure', 'error')
        ORDER BY algorithm_path
    """)
    
    failures = []
    for algo_path, error_msg, test_output in cursor.fetchall():
        text = (error_msg or "") + "\n" + (test_output or "")
        if 'typeerror' in text.lower() and ('module()' in text.lower() or 'module.__new__' in text.lower()):
            failures.append(algo_path)
    
    conn.close()
    return failures

def get_exported_names(algorithm_file: Path) -> List[str]:
    """Get names exported from algorithm file."""
    try:
        with open(algorithm_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        names = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                names.append(node.name)
        
        return names
    except Exception:
        return []

def get_main_export(algorithm_file: Path) -> Optional[str]:
    """Get the main class or function to import."""
    names = get_exported_names(algorithm_file)
    
    if not names:
        return None
    
    # Get directory name
    path_parts = algorithm_file.parts
    algo_name = path_parts[-2]  # Directory name
    
    # Try to find matching name
    algo_name_camel = ''.join(word.capitalize() for word in algo_name.split('_'))
    
    # Priority: exact match, then camel case, then first class, then first function
    for name in names:
        if name.lower() == algo_name.lower():
            return name
        if name == algo_name_camel:
            return name
        if name.lower() == algo_name.lower() + '_sort':
            return name
        if name.lower() == algo_name.lower() + '_search':
            return name
    
    # Return first class, or first function
    classes = [n for n in names if n[0].isupper()]
    if classes:
        return classes[0]
    
    functions = [n for n in names if n[0].islower() and not n.startswith('_')]
    if functions:
        return functions[0]
    
    return names[0] if names else None

def fix_test_file(test_file: Path, algorithm_file: Path) -> bool:
    """Fix test file to import correct class/function."""
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Get algorithm module path
        algo_rel_path = algorithm_file.relative_to(ROOT)
        algo_module = str(algo_rel_path.with_suffix('')).replace('\\', '.').replace('/', '.')
        
        # Get what should be imported
        main_export = get_main_export(algorithm_file)
        if not main_export:
            return False
        
        # Fix import of __init__
        pattern1 = rf'from\s+{re.escape(algo_module)}\s+import\s+__init__'
        replacement1 = f'from {algo_module} import {main_export}'
        content = re.sub(pattern1, replacement1, content)
        
        # Fix import (__init__,)
        pattern2 = rf'from\s+{re.escape(algo_module)}\s+import\s+\(\s*__init__\s*,?\s*\)'
        replacement2 = f'from {algo_module} import {main_export}'
        content = re.sub(pattern2, replacement2, content)
        
        # Fix self.algorithm = __init__
        pattern3 = r'self\.algorithm\s*=\s*__init__\b'
        replacement3 = f'self.algorithm = {main_export}'
        content = re.sub(pattern3, replacement3, content)
        
        if content != original_content:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {test_file}: {e}")
        return False

def main():
    """Main function."""
    type_errors = get_type_errors()
    print(f"Found {len(type_errors)} algorithms with TypeError")
    
    fixed_count = 0
    for algo_path in type_errors:
        algorithm_file = ROOT / Path(*algo_path.replace('\\', '/').split('/')) / "algorithm.py"
        test_file = ROOT / Path(*algo_path.replace('\\', '/').split('/')) / "test_algorithm.py"
        
        if not algorithm_file.exists() or not test_file.exists():
            print(f"Skipping {algo_path}: files not found")
            continue
        
        if fix_test_file(test_file, algorithm_file):
            print(f"Fixed: {algo_path}")
            fixed_count += 1
        else:
            print(f"Could not fix: {algo_path}")
    
    print(f"\nFixed: {fixed_count}/{len(type_errors)}")

if __name__ == "__main__":
    main()

