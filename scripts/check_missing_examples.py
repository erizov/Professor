#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for missing example implementations in algorithm files.
Finds functions that are called but not defined.
"""

import ast
import re
from pathlib import Path
from typing import Set, List, Dict

ROOT = Path(__file__).resolve().parents[1]


def find_called_functions(content: str) -> Set[str]:
    """Find all function calls in Python code."""
    try:
        tree = ast.parse(content)
        called = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    called.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    called.add(node.func.attr)
        
        return called
    except SyntaxError:
        return set()


def find_defined_functions(content: str) -> Set[str]:
    """Find all defined functions in Python code."""
    try:
        tree = ast.parse(content)
        defined = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined.add(node.name)
        
        return defined
    except SyntaxError:
        return set()


def find_java_called_methods(content: str) -> Set[str]:
    """Find all method calls in Java code."""
    called = set()
    # Pattern for method calls: methodName(...)
    pattern = r'(\w+)\s*\('
    matches = re.findall(pattern, content)
    
    # Filter out keywords and common methods
    keywords = {'if', 'for', 'while', 'switch', 'catch', 'new', 'return', 
                'System', 'Arrays', 'String', 'Integer', 'List', 'Map'}
    
    for match in matches:
        if match not in keywords and match[0].islower():
            called.add(match)
    
    return called


def find_java_defined_methods(content: str) -> Set[str]:
    """Find all defined methods in Java code."""
    defined = set()
    # Pattern for method definitions: public/private/protected ... methodName(...)
    pattern = r'(?:public|private|protected|static)\s+(?:static\s+)?(?:[\w<>\[\]]+\s+)?(\w+)\s*\('
    matches = re.findall(pattern, content)
    
    for match in matches:
        if match not in {'main', 'class', 'interface', 'enum'}:
            defined.add(match)
    
    return defined


def check_python_file(py_file: Path) -> List[str]:
    """Check a Python file for missing function implementations."""
    try:
        content = py_file.read_text(encoding='utf-8')
        called = find_called_functions(content)
        defined = find_defined_functions(content)
        
        missing = []
        for func in called:
            # Skip built-ins and imports
            if func not in defined and func not in {
                'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
                'set', 'tuple', 'sorted', 'max', 'min', 'sum', 'abs', 'round',
                'isinstance', 'type', 'hasattr', 'getattr', 'setattr', 'delattr',
                'logger', 'info', 'debug', 'warning', 'error', 'critical',
                'measure', 'copy', 'clone', 'toString', 'format', 'join', 'split'
            }:
                # Check if it's a method call (obj.method)
                if f'.{func}(' in content or f'{func}(' in content:
                    # Only report if it's called in main or example sections
                    if 'main' in content.lower() or 'example' in content.lower():
                        if func not in defined:
                            missing.append(func)
        
        return missing
    except Exception as e:
        return [f"Error: {e}"]


def check_java_file(java_file: Path) -> List[str]:
    """Check a Java file for missing method implementations."""
    try:
        content = java_file.read_text(encoding='utf-8')
        called = find_java_called_methods(content)
        defined = find_java_defined_methods(content)
        
        missing = []
        for method in called:
            # Skip common methods
            if method not in defined and method not in {
                'println', 'print', 'toString', 'length', 'size', 'get', 'set',
                'add', 'remove', 'contains', 'equals', 'hashCode', 'clone',
                'format', 'valueOf', 'parseInt', 'parseDouble', 'substring',
                'indexOf', 'lastIndexOf', 'split', 'trim', 'toLowerCase',
                'toUpperCase', 'charAt', 'startsWith', 'endsWith', 'replace',
                'repeat', 'nextInt', 'nextDouble', 'next', 'hasNext',
                'info', 'debug', 'warning', 'error', 'severe', 'log'
            }:
                # Only report if it's called in main
                if 'main' in content and method not in defined:
                    missing.append(method)
        
        return missing
    except Exception as e:
        return [f"Error: {e}"]


def main():
    """Check all algorithm files for missing examples."""
    python_missing = {}
    java_missing = {}
    
    # Check Python files
    for py_file in ROOT.rglob("algorithm.py"):
        missing = check_python_file(py_file)
        if missing:
            rel_path = py_file.relative_to(ROOT)
            python_missing[str(rel_path)] = missing
    
    # Check Java files
    for java_file in ROOT.rglob("Algorithm.java"):
        missing = check_java_file(java_file)
        if missing:
            rel_path = java_file.relative_to(ROOT)
            java_missing[str(rel_path)] = missing
    
    # Report results
    print("=" * 70)
    print("Missing Example Implementations Report")
    print("=" * 70)
    
    if python_missing:
        print(f"\nPython files with missing functions ({len(python_missing)}):")
        for file_path, missing_funcs in sorted(python_missing.items()):
            print(f"  {file_path}:")
            for func in missing_funcs:
                print(f"    - {func}")
    else:
        print("\n✓ No missing Python function implementations found")
    
    if java_missing:
        print(f"\nJava files with missing methods ({len(java_missing)}):")
        for file_path, missing_methods in sorted(java_missing.items()):
            print(f"  {file_path}:")
            for method in missing_methods:
                print(f"    - {method}")
    else:
        print("\n✓ No missing Java method implementations found")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

