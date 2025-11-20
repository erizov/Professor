#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix import errors in test files.
"""

import ast
import re
from pathlib import Path
from typing import List, Tuple, Optional
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_import_errors() -> List[Tuple[str, str]]:
    """Get list of algorithms with import errors."""
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
        if 'import' in text.lower() and ('error' in text.lower() or 'cannot import' in text.lower()):
            failures.append((algo_path, text))
    
    conn.close()
    return failures

def find_all_test_files_with_import_issues() -> List[Tuple[Path, Path]]:
    """Find all test files that might have import issues by scanning files."""
    test_files = []
    
    # Find all test_algorithm.py files
    for test_file in ROOT.rglob("test_algorithm.py"):
        algo_dir = test_file.parent
        algo_file = algo_dir / "algorithm.py"
        
        if algo_file.exists():
            # Check if test file imports __init__
            try:
                content = test_file.read_text(encoding='utf-8')
                algo_rel_path = algo_file.relative_to(ROOT)
                algo_module = str(algo_rel_path.with_suffix('')).replace('\\', '.').replace('/', '.')
                
                # Check for __init__ import
                if f'import __init__' in content and algo_module in content:
                    test_files.append((test_file, algo_file))
            except Exception:
                pass
    
    return test_files


def find_algorithm_file(algo_path: str) -> Optional[Path]:
    """Find the algorithm.py file for a given path."""
    path_parts = algo_path.replace('\\', '/').split('/')
    algo_file = ROOT / Path(*path_parts) / "algorithm.py"
    if algo_file.exists():
        return algo_file
    return None


def find_test_file(algo_path: str) -> Optional[Path]:
    """Find the test_algorithm.py file for a given path."""
    path_parts = algo_path.replace('\\', '/').split('/')
    test_file = ROOT / Path(*path_parts) / "test_algorithm.py"
    if test_file.exists():
        return test_file
    return None


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
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.append(target.id)
        
        return names
    except Exception:
        return []


def get_main_class_or_function(algorithm_file: Path) -> Optional[str]:
    """Get the main class or function name from algorithm file."""
    names = get_exported_names(algorithm_file)
    
    # Common patterns for main exports
    path_parts = algorithm_file.parts
    algo_name = path_parts[-2]  # Directory name
    
    # Try to find class or function matching algorithm name
    algo_name_camel = ''.join(word.capitalize() for word in algo_name.split('_'))
    algo_name_pascal = algo_name_camel
    
    # Check for common patterns
    for name in names:
        if name.lower() == algo_name.lower():
            return name
        if name.lower() == algo_name.lower() + '_sort':
            return name
        if name.lower() == algo_name.lower() + '_search':
            return name
        if name == algo_name_camel or name == algo_name_pascal:
            return name
        if name.lower().replace('_', '') == algo_name.lower().replace('_', ''):
            return name
    
    # Return first class or function (excluding __init__, main, etc.)
    for name in names:
        if not name.startswith('_') and name not in ['main']:
            if any(name == n for n in names if isinstance(n, str)):
                return name
    
    return names[0] if names else None


def fix_test_imports(test_file: Path, algorithm_file: Path) -> bool:
    """Fix import statements in test file."""
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find the algorithm module path
        algo_rel_path = algorithm_file.relative_to(ROOT)
        algo_module = str(algo_rel_path.with_suffix('')).replace('\\', '.').replace('/', '.')
        
        # Get what should be imported
        main_export = get_main_class_or_function(algorithm_file)
        all_exports = get_exported_names(algorithm_file)
        
        if not main_export:
            return False
        
        # Find what's currently being imported
        import_pattern = rf'from\s+{re.escape(algo_module)}\s+import\s+([^\n]+)'
        match = re.search(import_pattern, content)
        
        if not match:
            return False
        
        imported_names_str = match.group(1).strip()
        # Handle parentheses
        if imported_names_str.startswith('('):
            imported_names_str = imported_names_str[1:-1].strip()
        
        imported_names = [name.strip() for name in imported_names_str.split(',')]
        imported_names = [name for name in imported_names if name]
        
        # Check if any imported name doesn't exist in exports
        needs_fix = False
        for imp_name in imported_names:
            if imp_name == '__init__' or imp_name not in all_exports:
                needs_fix = True
                break
        
        if not needs_fix:
            return False
        
        # Replace with correct import
        # If importing __init__, replace with main_export
        # If importing non-existent name, try to find similar name or use main_export
        fixed_imports = []
        for imp_name in imported_names:
            if imp_name == '__init__':
                fixed_imports.append(main_export)
            elif imp_name not in all_exports:
                # Try to find similar name
                found = False
                imp_lower = imp_name.lower()
                for exp_name in all_exports:
                    if exp_name.lower() == imp_lower or exp_name.lower().replace('_', '') == imp_lower.replace('_', ''):
                        fixed_imports.append(exp_name)
                        found = True
                        break
                if not found:
                    fixed_imports.append(main_export)
            else:
                fixed_imports.append(imp_name)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_imports = []
        for imp in fixed_imports:
            if imp not in seen:
                seen.add(imp)
                unique_imports.append(imp)
        
        # Format the import statement
        if len(unique_imports) == 1:
            new_import = f'from {algo_module} import {unique_imports[0]}'
        else:
            imports_str = ',\n            '.join(unique_imports)
            new_import = f'from {algo_module} import (\n            {imports_str},\n        )'
        
        # Replace the import
        content = re.sub(import_pattern, new_import, content)
        
        # Also fix self.algorithm assignments
        for old_name in imported_names:
            if old_name == '__init__' or old_name not in all_exports:
                # Find which name to use
                if old_name == '__init__':
                    new_name = main_export
                else:
                    new_name = unique_imports[0] if unique_imports else main_export
                
                # Fix self.algorithm = old_name
                pattern = rf'self\.algorithm\s*=\s*{re.escape(old_name)}\b'
                replacement = f'self.algorithm = {new_name}'
                content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {test_file}: {e}")
        return False


def main():
    """Main function to fix import errors."""
    # First, try to find files by scanning
    print("Scanning for test files with import issues...")
    test_files = find_all_test_files_with_import_issues()
    print(f"Found {len(test_files)} test files with potential __init__ imports")
    
    fixed_count = 0
    skipped_count = 0
    
    for test_file, algorithm_file in test_files:
        if fix_test_imports(test_file, algorithm_file):
            fixed_count += 1
            print(f"Fixed: {test_file.relative_to(ROOT)}")
        else:
            skipped_count += 1
    
    # Also try from database
    print("\nChecking database for import errors...")
    import_errors = get_import_errors()
    print(f"Found {len(import_errors)} algorithms with import errors in database")
    
    db_fixed = 0
    for algo_path, error_text in import_errors:
        algorithm_file = find_algorithm_file(algo_path)
        test_file = find_test_file(algo_path)
        
        if not algorithm_file or not test_file:
            continue
        
        if fix_test_imports(test_file, algorithm_file):
            db_fixed += 1
            print(f"Fixed (from DB): {algo_path}")
    
    print(f"\nTotal Fixed: {fixed_count + db_fixed}")
    print(f"Skipped/Could not fix: {skipped_count}")


if __name__ == "__main__":
    main()

