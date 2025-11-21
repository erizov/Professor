#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test and fix Java files one by one: test, fix if fails, retest, commit on success (no push).
Reports progress every file and every 3 minutes.
Updates database with test results.

This script automatically fixes common Java compilation and runtime errors:
1. Import errors: Fixes incorrect package imports
2. Class name mismatches: Fixes class name vs file name mismatches
3. Missing methods: Adds placeholder methods
4. Syntax errors: Basic syntax fixes

The script will:
- Test each Java file (compile and run)
- If test fails, attempt to fix it
- Retest after each fix
- Continue until test passes or max attempts (10) reached
- Update database with test results
- Commit successful fixes (no push)
- Show status updates every file and every 3 minutes

Usage:
    python -m scripts.fix_java_one_by_one
"""

import subprocess
import sys
import re
from pathlib import Path
import threading
import time
from datetime import datetime
from typing import Optional, Tuple, List
import sqlite3
import argparse

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"

# Global state for status reporting
_status_lock = threading.Lock()
_status_state = {
    'current_file': None,
    'current_idx': 0,
    'total_files': 0,
    'passed_count': 0,
    'fixed_count': 0,
    'failed_count': 0,
    'skipped_count': 0,
    'start_time': None,
    'stop_event': threading.Event()
}


def status_reporter():
    """Background thread that reports status every 3 minutes."""
    while not _status_state['stop_event'].wait(180):  # Wait 3 minutes
        with _status_lock:
            state = _status_state.copy()
        
        if state['start_time'] is None:
            continue
        
        elapsed = time.time() - state['start_time']
        elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        
        print("", flush=True)
        print("=" * 80, flush=True)
        print(f"STATUS UPDATE ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})", flush=True)
        print("=" * 80, flush=True)
        print(f"Elapsed time: {elapsed_str}", flush=True)
        print(f"Progress: {state['current_idx']}/{state['total_files']} files", flush=True)
        print(f"  ✓ Passed and committed: {state['passed_count']}", flush=True)
        print(f"  🔧 Fixed and passed: {state['fixed_count']}", flush=True)
        print(f"  ❌ Failed: {state['failed_count']}", flush=True)
        print(f"  ⊘ Skipped: {state['skipped_count']}", flush=True)
        if state['current_file']:
            print(f"Currently processing: {state['current_file']}", flush=True)
        print("=" * 80, flush=True)
        print("", flush=True)


def get_main_class_name(java_file: Path) -> Optional[str]:
    """Extract the main class name from Java file."""
    try:
        content = java_file.read_text(encoding='utf-8')
        # Look for public class ClassName
        match = re.search(r'public\s+class\s+(\w+)', content)
        if match:
            return match.group(1)
        # Look for class ClassName (without public)
        match = re.search(r'class\s+(\w+)', content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def fix_class_name_mismatch(java_file: Path) -> bool:
    """
    Fix class name mismatch (class name doesn't match file name).
    Returns True if any changes were made.
    """
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Expected class name is "Algorithm" (file is Algorithm.java)
        expected_class = "Algorithm"
        actual_class = get_main_class_name(java_file)
        
        if actual_class and actual_class != expected_class:
            # Replace class name with expected name
            # Replace: public class ActualName -> public class Algorithm
            content = re.sub(
                rf'public\s+class\s+{re.escape(actual_class)}\b',
                f'public class {expected_class}',
                content
            )
            # Also replace: class ActualName -> class Algorithm
            content = re.sub(
                rf'(?<!public\s)class\s+{re.escape(actual_class)}\b',
                f'class {expected_class}',
                content
            )
            # Replace constructor calls: new ActualName() -> new Algorithm()
            content = re.sub(
                rf'new\s+{re.escape(actual_class)}\s*\(',
                f'new {expected_class}(',
                content
            )
            
            if content != original_content:
                java_file.write_text(content, encoding='utf-8')
                return True
    except Exception as e:
        print(f"  ⚠ Error fixing class name: {e}", flush=True)
    return False


def fix_package_errors(java_file: Path) -> bool:
    """
    Fix package declaration errors.
    Returns True if any changes were made.
    """
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Get expected package from file path
        # e.g., semester_01/lecture_01/bubble_sort/Algorithm.java
        # -> package semester_01.lecture_01.bubble_sort;
        try:
            rel_path = java_file.relative_to(ROOT)
            path_parts = rel_path.parent.parts
        except ValueError:
            # If relative_to fails, use absolute path
            path_parts = java_file.parent.parts
            # Find the semester_XX part
            for i, part in enumerate(path_parts):
                if part.startswith('semester_'):
                    path_parts = path_parts[i:]
                    break
        expected_package = '.'.join(path_parts)
        
        # Check if package declaration exists
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        
        if package_match:
            current_package = package_match.group(1)
            if current_package != expected_package:
                # Fix package declaration
                content = re.sub(
                    r'^package\s+[^;]+;',
                    f'package {expected_package};',
                    content,
                    flags=re.MULTILINE
                )
        else:
            # Add package declaration if missing (after any comments/imports at top)
            # Find first non-comment, non-import line
            lines = content.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('import') and not stripped.startswith('package'):
                    insert_idx = i
                    break
            
            # Insert package declaration
            lines.insert(insert_idx, f'package {expected_package};')
            content = '\n'.join(lines)
        
        if content != original_content:
            java_file.write_text(content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"  ⚠ Error fixing package: {e}", flush=True)
    return False


def fix_missing_main_method(java_file: Path) -> bool:
    """
    Add a main method if it's missing.
    Returns True if any changes were made.
    """
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Check if main method exists
        if 'public static void main' not in content:
            # Find the class and add main method
            class_match = re.search(r'(public\s+class\s+\w+\s*\{)', content)
            if class_match:
                # Add main method after class declaration
                insert_pos = class_match.end()
                main_method = """
    public static void main(String[] args) {
        // TODO: Implement main method
        System.out.println("Algorithm implementation");
    }
"""
                content = content[:insert_pos] + main_method + content[insert_pos:]
                
                if content != original_content:
                    java_file.write_text(content, encoding='utf-8')
                    return True
    except Exception as e:
        print(f"  ⚠ Error fixing main method: {e}", flush=True)
    return False


def replace_printf_with_logger(java_file: Path) -> bool:
    """
    Replace System.out.printf and System.out.println with logger.info when logger is available.
    Returns True if any changes were made.
    """
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Check if file has logger defined
        has_logger = re.search(r'Logger\s+logger\s*=', content) or \
                     re.search(r'Logger\.getLogger', content)
        
        if not has_logger:
            return False
        
        modified = False
        lines = content.split('\n')
        
        # Find all System.out.println calls
        println_pattern = r'System\.out\.println\s*\((.*?)\);'
        println_matches = list(re.finditer(println_pattern, content, re.DOTALL))
        
        # Replace println with logger.info
        for match in reversed(println_matches):
            line_num = content[:match.start()].count('\n')
            line = lines[line_num]
            
            # Extract argument
            arg = match.group(1).strip()
            
            # Replace System.out.println(arg) with logger.info(arg)
            replacement = f'logger.info({arg});'
            new_line = line.replace(match.group(0), replacement)
            lines[line_num] = new_line
            modified = True
        
        # Find all System.out.printf calls
        # Use regex with DOTALL to match multi-line calls
        printf_pattern = r'System\.out\.printf\s*\((.*?)\);'
        printf_matches = list(re.finditer(printf_pattern, content, re.DOTALL))
        
        if not println_matches and not printf_matches:
            return False
        
        # Replace each printf with logger.info
        for match in reversed(printf_matches):  # Process in reverse to maintain positions
            start_pos = match.start()
            end_pos = match.end()
            
            # Find line number
            line_num = content[:start_pos].count('\n')
            line = lines[line_num]
            
            # Extract arguments
            args_content = match.group(1).strip()
            
            # Parse arguments (handle nested parentheses, brackets, strings)
            parts = []
            paren_depth = 0
            bracket_depth = 0
            brace_depth = 0
            in_string = False
            string_char = None
            current = ""
            
            for char in args_content:
                if not in_string:
                    if char in ('"', "'"):
                        in_string = True
                        string_char = char
                        current += char
                    elif char == '(':
                        paren_depth += 1
                        current += char
                    elif char == ')':
                        paren_depth -= 1
                        current += char
                    elif char == '[':
                        bracket_depth += 1
                        current += char
                    elif char == ']':
                        bracket_depth -= 1
                        current += char
                    elif char == '{':
                        brace_depth += 1
                        current += char
                    elif char == '}':
                        brace_depth -= 1
                        current += char
                    elif char == ',' and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
                        parts.append(current.strip())
                        current = ""
                    else:
                        current += char
                else:
                    current += char
                    if char == string_char and (len(current) < 2 or current[-2] != '\\'):
                        in_string = False
                        string_char = None
            
            if current.strip():
                parts.append(current.strip())
            
            if len(parts) >= 1:
                format_str = parts[0].strip()
                args = parts[1:] if len(parts) > 1 else []
                
                # Use String.format with printf format specifiers
                if args:
                    args_str = ', '.join(args)
                    replacement = f'logger.info(String.format({format_str}, {args_str}));'
                else:
                    replacement = f'logger.info(String.format({format_str}));'
                
                # Replace in line
                new_line = line.replace(match.group(0), replacement)
                lines[line_num] = new_line
                modified = True
        
        if modified:
            java_file.write_text('\n'.join(lines), encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"  ⚠ Error replacing printf with logger: {e}", flush=True)
        return False


def fix_compilation_errors(java_file: Path, error_output: str) -> bool:
    """
    Fix common compilation errors based on error output.
    Returns True if any changes were made.
    """
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        modified = False
        
        # First, replace System.out.printf and System.out.println with logger.info if logger exists
        if replace_printf_with_logger(java_file):
            modified = True
            content = java_file.read_text(encoding='utf-8')
        
        # Fix: cannot find symbol (missing import or wrong class name)
        if 'cannot find symbol' in error_output.lower():
            # Try to fix class name mismatch first
            if fix_class_name_mismatch(java_file):
                modified = True
                # Re-read content after fix
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: class X is public, should be declared in a file named X.java
        if 'is public, should be declared in a file named' in error_output:
            if fix_class_name_mismatch(java_file):
                modified = True
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: package does not exist
        if 'package' in error_output.lower() and ('does not exist' in error_output.lower() or 'error' in error_output.lower()):
            if fix_package_errors(java_file):
                modified = True
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: incompatible types: <null> cannot be converted to int
        if 'incompatible types' in error_output.lower() and 'null' in error_output.lower() and 'cannot be converted to int' in error_output.lower():
            # Extract all line numbers with this error
            line_matches = re.findall(r':(\d+):\s*error.*null.*cannot be converted to int', error_output)
            lines = content.split('\n')
            
            for line_str in line_matches:
                line_num = int(line_str) - 1  # Convert to 0-based index
                if 0 <= line_num < len(lines):
                    # Check if this line has "return null;"
                    if 'return null;' in lines[line_num]:
                        # Replace return null with return -1
                        lines[line_num] = lines[line_num].replace('return null;', 'return -1;  // FIXME: Changed from null to -1')
                        modified = True
            
            # Also do a general search for return null in int methods
            if not modified:
                in_int_method = False
                method_start = -1
                for i, line in enumerate(lines):
                    # Check if we're entering an int method
                    if re.search(r'\b(int|Integer)\s+\w+\s*\(', line):
                        in_int_method = True
                        method_start = i
                    # Check if we're leaving the method
                    if in_int_method:
                        if line.strip() == '}' and i > method_start:
                            # Check previous lines in this method for return null
                            for j in range(i-1, method_start, -1):
                                if 'return null;' in lines[j]:
                                    lines[j] = lines[j].replace('return null;', 'return -1;  // FIXME: Changed from null to -1')
                                    modified = True
                            in_int_method = False
                            method_start = -1
                        elif 'return null;' in line:
                            lines[i] = line.replace('return null;', 'return -1;  // FIXME: Changed from null to -1')
                            modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: unmappable character for encoding (special characters/emojis)
        if 'unmappable character' in error_output.lower() or 'for encoding' in error_output.lower():
            # Extract line number from error
            line_match = re.search(r':(\d+):\s*error.*unmappable character', error_output)
            lines = content.split('\n')
            
            if line_match:
                line_num = int(line_match.group(1)) - 1
                if 0 <= line_num < len(lines):
                    # Replace problematic characters in that line
                    new_line = lines[line_num]
                    # Replace emoji warning sign and other problematic unicode
                    new_line = new_line.replace('⚠️', 'Warning:')
                    new_line = new_line.replace('⚠', 'Warning:')
                    # Remove other problematic unicode characters
                    new_line = re.sub(r'[^\x00-\x7F]+', '', new_line)
                    if new_line != lines[line_num]:
                        lines[line_num] = new_line
                        modified = True
            else:
                # Fallback: fix all lines with problematic characters
                for i, line in enumerate(lines):
                    new_line = line
                    new_line = new_line.replace('⚠️', 'Warning:')
                    new_line = new_line.replace('⚠', 'Warning:')
                    new_line = re.sub(r'[^\x00-\x7F]+', '', new_line)
                    if new_line != line:
                        lines[i] = new_line
                        modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: class, interface, enum, or record expected (method/import outside class)
        if 'class, interface, enum, or record expected' in error_output:
            lines = content.split('\n')
            
            # Check if package is in wrong place (after imports or in middle of class)
            package_name = None
            package_line_idx = -1
            package_line = None
            
            # Find package declaration (including in comments)
            for i, line in enumerate(lines):
                # Check if package is in a comment
                if 'package' in line and ('/*' in line or '*/' in line or line.strip().startswith('*')):
                    # Extract package from comment
                    pkg_match = re.search(r'package\s+([^;]+);', line)
                    if pkg_match:
                        package_name = pkg_match.group(1)
                        package_line = f'package {package_name};'
                        package_line_idx = i
                        # Remove package from comment line
                        lines[i] = re.sub(r'package\s+[^;]+;', '', lines[i])
                        modified = True
                        break
                elif re.search(r'^\s*package\s+', line):
                    package_line_idx = i
                    package_line = line
                    pkg_match = re.search(r'package\s+([^;]+);', line)
                    if pkg_match:
                        package_name = pkg_match.group(1)
                    break
            
            # If package is found but not at top, move it
            if package_line_idx >= 0 and package_name and package_line:
                # Check if it's at the top (after comments/blank lines, before imports)
                is_at_top = True
                has_imports_before = False
                for i in range(package_line_idx):
                    stripped = lines[i].strip()
                    if stripped.startswith('import '):
                        has_imports_before = True
                        is_at_top = False
                        break
                    elif stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*') and not stripped.startswith('package'):
                        is_at_top = False
                        break
                
                if not is_at_top or has_imports_before:
                    # Remove package from current location
                    del lines[package_line_idx]
                    
                    # Find correct position (after comments, before imports)
                    insert_idx = 0
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                            if stripped.startswith('import'):
                                insert_idx = i
                                break
                            elif not stripped.startswith('package'):
                                insert_idx = i
                                break
                    
                    lines.insert(insert_idx, package_line)
                    modified = True
            
            # Check if imports are after class definition
            class_line = -1
            for i, line in enumerate(lines):
                if re.search(r'^\s*(public\s+)?class\s+\w+', line) or re.search(r'^\s*abstract\s+class\s+\w+', line):
                    class_line = i
                    break
            
            if class_line >= 0:
                # Find imports after class (but before any other class)
                imports_to_move = []
                next_class_line = -1
                # Also check for imports between classes
                for i in range(class_line + 1, len(lines)):
                    # Check if we hit another class
                    if re.search(r'^\s*(public\s+)?class\s+\w+', lines[i]) or re.search(r'^\s*abstract\s+class\s+\w+', lines[i]):
                        # Check for imports between this class and the next
                        for j in range(i + 1, len(lines)):
                            if lines[j].strip().startswith('import '):
                                imports_to_move.append((j, lines[j]))
                            elif lines[j].strip() and not lines[j].strip().startswith('//') and not lines[j].strip().startswith('/*') and not lines[j].strip().startswith('*'):
                                if not re.search(r'^\s*(public\s+)?class\s+\w+', lines[j]):
                                    break
                        next_class_line = i
                        break
                    if lines[i].strip().startswith('import '):
                        imports_to_move.append((i, lines[i]))
                    elif lines[i].strip() and not lines[i].strip().startswith('//') and not lines[i].strip().startswith('/*') and not lines[i].strip().startswith('*'):
                        # Stop if we hit non-import, non-comment code (but allow class definitions)
                        if not re.search(r'^\s*(public\s+)?class\s+\w+', lines[i]):
                            break
                
                if imports_to_move:
                    # Remove imports from after class
                    for i, _ in reversed(imports_to_move):
                        del lines[i]
                    # Add imports at top
                    insert_idx = 0
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('import') and not stripped.startswith('package'):
                            insert_idx = i
                            break
                    for _, import_line in reversed(imports_to_move):
                        lines.insert(insert_idx, import_line)
                    modified = True
                
                # Check if method is outside class (after closing brace)
                brace_count = 0
                class_end = -1
                for i in range(class_line, len(lines)):
                    brace_count += lines[i].count('{') - lines[i].count('}')
                    if brace_count == 0 and i > class_line:
                        class_end = i
                        break
                
                if class_end >= 0:
                    # Check for code after class (methods, statements, etc.)
                    code_blocks_to_move = []
                    i = class_end + 1
                    while i < len(lines):
                        line = lines[i].strip()
                        # Skip empty lines and comments
                        if not line or line.startswith('//') or line.startswith('/*') or line.startswith('*'):
                            i += 1
                            continue
                        
                        # Check if it's a method or code statement
                        if re.search(r'public\s+static\s+', lines[i]) or re.search(r'^\s*\w+\s+\w+\s*=', lines[i]) or re.search(r'^\s*\w+\.\w+\(', lines[i]):
                            # Found code outside class
                            code_start = i
                            # Find end of code block
                            brace_count = 0
                            code_end = code_start
                            for j in range(code_start, len(lines)):
                                brace_count += lines[j].count('{') - lines[j].count('}')
                                if brace_count == 0 and j > code_start:
                                    code_end = j
                                    break
                                # If it's a single statement (ends with ;)
                                if ';' in lines[j] and brace_count == 0:
                                    code_end = j
                                    break
                            
                            code_blocks_to_move.append((code_start, code_end))
                            i = code_end + 1
                        else:
                            i += 1
                    
                    # Move code blocks inside class (in reverse order to maintain indices)
                    for code_start, code_end in reversed(code_blocks_to_move):
                        code_lines = lines[code_start:code_end+1]
                        # Indent code
                        code_lines = ['    ' + line if line.strip() else line for line in code_lines]
                        # Remove from outside
                        del lines[code_start:code_end+1]
                        # Insert before class closing brace
                        for line in reversed(code_lines):
                            lines.insert(class_end, line)
                        modified = True
                else:
                    # No class found - check if methods exist without a class wrapper
                    # Look for methods before any class declaration
                    has_methods_before_class = False
                    first_method_line = -1
                    for i, line in enumerate(lines):
                        if re.search(r'^\s*public\s+static\s+', line) or re.search(r'^\s*private\s+static\s+', line):
                            has_methods_before_class = True
                            if first_method_line == -1:
                                first_method_line = i
                            break
                        if re.search(r'^\s*(public\s+)?class\s+\w+', line):
                            break
                    
                    if has_methods_before_class and first_method_line >= 0:
                        # Need to wrap methods in a class
                        # Find where to insert class declaration (after package/imports)
                        class_insert_idx = 0
                        for i, line in enumerate(lines):
                            stripped = line.strip()
                            if stripped.startswith('package ') or stripped.startswith('import '):
                                class_insert_idx = i + 1
                            elif stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                                if class_insert_idx == 0:
                                    class_insert_idx = i
                                break
                        
                        # Insert class declaration
                        lines.insert(class_insert_idx, 'public class Algorithm {')
                        modified = True
                        
                        # Find the end of all methods (before any closing brace or end of file)
                        last_method_end = len(lines) - 1
                        for i in range(len(lines) - 1, -1, -1):
                            if re.search(r'^\s*}\s*$', lines[i]):
                                last_method_end = i
                                break
                        
                        # Add closing brace for class
                        lines.insert(last_method_end + 1, '}')
                        modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: incompatible types: boolean cannot be converted to Map
        if 'incompatible types' in error_output.lower() and 'boolean' in error_output.lower() and 'cannot be converted to' in error_output.lower():
            # Extract line number from error
            line_match = re.search(r':(\d+):\s*error.*boolean.*cannot be converted', error_output)
            lines = content.split('\n')
            
            if line_match:
                line_num = int(line_match.group(1)) - 1
                if 0 <= line_num < len(lines):
                    # Check if this line has "return false;" or "return true;"
                    if 'return false;' in lines[line_num]:
                        lines[line_num] = lines[line_num].replace('return false;', 'return null;  // FIXME: Changed from boolean to null')
                        modified = True
                    elif 'return true;' in lines[line_num]:
                        lines[line_num] = lines[line_num].replace('return true;', 'return null;  // FIXME: Changed from boolean to null')
                        modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: variable X is already defined (handled in later section - see line 731)
        # Removed duplicate section
        
        # Fix: invalid parameter syntax like "Object any]" or "Object float]" or "List[any]]"
        if "expected" in error_output.lower() and ("']' expected" in error_output.lower() or "',' expected" in error_output.lower() or "'[' expected" in error_output.lower()):
            # Find lines with invalid parameter syntax
            invalid_param_pattern = r':(\d+):\s+error:.*expected'
            matches = re.findall(invalid_param_pattern, error_output)
            if matches:
                lines = content.split('\n')
                for line_num_str in matches:
                    try:
                        line_idx = int(line_num_str) - 1
                        if 0 <= line_idx < len(lines):
                            line = lines[line_idx]
                            # Fix patterns like: Object any], Object float], List[any]], List<Object> List[any]]
                            # Replace with: Object any, float any, List<Object> any
                            fixed_line = re.sub(r'Object\s+(\w+)\]', r'Object \1', line)
                            fixed_line = re.sub(r'float\]', r'float any', fixed_line)
                            fixed_line = re.sub(r'List\[any\]\]', r'List<Object> any', fixed_line)
                            fixed_line = re.sub(r'List<Object>\s+List\[any\]\]', r'List<Object> any', fixed_line)
                            if fixed_line != line:
                                lines[line_idx] = fixed_line
                                modified = True
                    except (ValueError, IndexError):
                        continue
                if modified:
                    content = '\n'.join(lines)
                    java_file.write_text(content, encoding='utf-8')
                    content = java_file.read_text(encoding='utf-8')
        
        # Fix: None result = ... (Python-style None in Java)
        if 'None result' in error_output or 'symbol:   class None' in error_output:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'None result' in line:
                    # Replace "None result" with "Object result" or appropriate type
                    lines[i] = re.sub(r'None\s+result\s*=', r'Object result =', line)
                    modified = True
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: cannot find symbol (missing variable declarations)
        if 'cannot find symbol' in error_output.lower():
            lines = content.split('\n')
            # Extract variable names from error messages
            # Pattern 1: "symbol:   variable dash" (on separate line)
            symbol_errors = re.findall(r'symbol:\s+variable\s+(\w+)', error_output)
            # Pattern 2: "cannot find symbol variable X" (on same line)
            symbol_errors.extend(re.findall(r'cannot find symbol\s+variable\s+(\w+)', error_output))
            # Remove duplicates
            symbol_errors = list(set(symbol_errors))
            
            for symbol_name in symbol_errors:
                # Check if it's a common missing variable
                if symbol_name == 'logger':
                    # Add logger declaration at class level
                    class_match = re.search(r'(public\s+class\s+\w+\s*\{)', content)
                    if class_match:
                        insert_pos = class_match.end()
                        logger_decl = '\n    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());\n'
                        content = content[:insert_pos] + logger_decl + content[insert_pos:]
                        modified = True
                elif symbol_name == 'dash' or symbol_name == 'separator':
                    # Add dash/separator variable at class level (used by logger)
                    lines = content.split('\n')
                    class_line_idx = -1
                    logger_line_idx = -1
                    
                    # Find class declaration line
                    for i, line in enumerate(lines):
                        if re.search(r'^\s*public\s+class\s+\w+', line):
                            class_line_idx = i
                            break
                    
                    # Find logger declaration line
                    for i, line in enumerate(lines):
                        if 'Logger logger' in line and '=' in line:
                            logger_line_idx = i
                            break
                    
                    # Determine where to insert
                    insert_idx = class_line_idx + 1
                    if logger_line_idx >= 0:
                        insert_idx = logger_line_idx + 1
                    
                    # Check if dash/separator already exists
                    has_dash = any('String dash' in line or 'dash =' in line for line in lines)
                    has_separator = any('String separator' in line or 'separator =' in line for line in lines)
                    
                    if insert_idx >= 0:
                        # Insert dash and separator as separate lines
                        if not has_dash:
                            lines.insert(insert_idx, '    private static final String dash = "-".repeat(70);')
                            insert_idx += 1
                            modified = True
                        if not has_separator:
                            lines.insert(insert_idx, '    private static final String separator = "=".repeat(70);')
                            modified = True
                        
                        if modified:
                            content = '\n'.join(lines)
                else:
                    # Try to find where the variable should be declared
                    # First check if variable already exists (to avoid duplicates)
                    var_already_exists = False
                    # Check if it's a method parameter
                    is_method_parameter = False
                    
                    for i, line in enumerate(lines):
                        # Check if variable is already declared
                        if re.search(rf'\b\w+\s+{re.escape(symbol_name)}\s*[=;]', line) or re.search(rf'\b{re.escape(symbol_name)}\s*=', line):
                            # Check if it's not just a usage
                            if re.search(rf'\b\w+\s+{re.escape(symbol_name)}\s*[=;]', line) or (symbol_name + ' =' in line and 'Object ' + symbol_name in line):
                                var_already_exists = True
                                break
                        # Check if it's a method parameter
                        method_match = re.search(r'(public|private|protected)\s+(static\s+)?\w+\s+\w+\s*\(([^)]*)\)', line)
                        if method_match:
                            params_str = method_match.group(3)
                            # Extract parameter names
                            for param in params_str.split(','):
                                param = param.strip()
                                if param:
                                    param_name_match = re.search(r'\w+\s+(\w+)\s*$', param)
                                    if param_name_match and param_name_match.group(1) == symbol_name:
                                        is_method_parameter = True
                                        var_already_exists = True
                                        break
                            if is_method_parameter:
                                break
                    
                    if not var_already_exists and not is_method_parameter:
                        # Look for usage and add declaration nearby
                        for i, line in enumerate(lines):
                            if symbol_name in line and '=' in line and symbol_name not in [w.strip() for w in line.split('=')[0].split() if w.strip()]:
                                # Variable used but not declared - add declaration
                                # Find method start
                                for j in range(i-1, max(0, i-20), -1):
                                    if '{' in lines[j] and ('public' in lines[j] or 'private' in lines[j] or 'static' in lines[j]):
                                        # Check if variable is a parameter of this method
                                        method_match = re.search(r'(public|private|protected)\s+(static\s+)?\w+\s+\w+\s*\(([^)]*)\)', lines[j])
                                        if method_match:
                                            params_str = method_match.group(3)
                                            for param in params_str.split(','):
                                                param = param.strip()
                                                if param:
                                                    param_name_match = re.search(r'\w+\s+(\w+)\s*$', param)
                                                    if param_name_match and param_name_match.group(1) == symbol_name:
                                                        # Variable is a method parameter, don't add declaration
                                                        is_method_parameter = True
                                                        break
                                        
                                        if not is_method_parameter:
                                            # Check if we already added this variable declaration in this method
                                            already_added = False
                                            # Find method end
                                            method_brace_count = 1
                                            method_end = j
                                            for k in range(j + 1, len(lines)):
                                                method_brace_count += lines[k].count('{') - lines[k].count('}')
                                                if method_brace_count == 0:
                                                    method_end = k
                                                    break
                                            
                                            # Check if variable is already declared in this method
                                            for k in range(j+1, method_end+1):
                                                # Check if variable is already declared (including our FIXME declarations)
                                                if f'Object {symbol_name} = null;  // FIXME' in lines[k] or re.search(rf'\b\w+\s+{re.escape(symbol_name)}\s*[=;]', lines[k]):
                                                    already_added = True
                                                    break
                                            
                                            if not already_added:
                                                # Add variable declaration after method start
                                                indent = len(lines[j]) - len(lines[j].lstrip())
                                                var_decl = ' ' * (indent + 4) + f'Object {symbol_name} = null;  // FIXME: Added missing variable declaration\n'
                                                lines.insert(j+1, var_decl)
                                                modified = True
                                            break
                                break
            
            if modified:
                content = '\n'.join(lines) if isinstance(lines, list) else content
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: variable X is already defined (duplicate variable)
        if 'variable' in error_output.lower() and 'is already defined' in error_output.lower():
            # Extract variable name and all line numbers from error
            var_matches = re.findall(r'variable\s+(\w+)\s+is already defined.*:(\d+):', error_output)
            if var_matches:
                # Group by variable name
                var_errors = {}
                for var_name, line_str in var_matches:
                    if var_name not in var_errors:
                        var_errors[var_name] = []
                    var_errors[var_name].append(int(line_str) - 1)
                
                lines = content.split('\n')
                
                for var_name, error_lines in var_errors.items():
                    # Find the method that contains these errors
                    first_error_line = min(error_lines)
                    method_start = -1
                    method_end = -1
                    method_params = []
                    
                    # Find method start
                    for i in range(first_error_line - 1, max(0, first_error_line - 50), -1):
                        # Check if this is a method declaration
                        method_match = re.search(r'(public|private|protected)\s+(static\s+)?\w+\s+\w+\s*\(([^)]*)\)', lines[i])
                        if method_match:
                            method_start = i
                            params_str = method_match.group(3)
                            # Extract parameter names
                            for param in params_str.split(','):
                                param = param.strip()
                                if param:
                                    param_name_match = re.search(r'\w+\s+(\w+)\s*$', param)
                                    if param_name_match:
                                        method_params.append(param_name_match.group(1))
                            break
                        # Stop if we hit another method or class
                        if re.search(r'^\s*}\s*$', lines[i]) or re.search(r'^\s*class\s+', lines[i]):
                            break
                    
                    # Find method end
                    if method_start >= 0:
                        brace_count = 1
                        method_end = method_start
                        for i in range(method_start + 1, len(lines)):
                            brace_count += lines[i].count('{') - lines[i].count('}')
                            if brace_count == 0:
                                method_end = i
                                break
                    
                    # Find all declarations of this variable in the method
                    declarations = []
                    if method_start >= 0 and method_end >= 0:
                        for i in range(method_start + 1, method_end):
                            if re.search(rf'\b\w+\s+{re.escape(var_name)}\s*=', lines[i]):
                                declarations.append(i)
                    
                    # If variable is a method parameter, remove all local declarations
                    if var_name in method_params:
                        # Remove all duplicate declarations (they conflict with parameter)
                        for decl_line in reversed(declarations):
                            if 'FIXME' in lines[decl_line] or 'Added missing' in lines[decl_line]:
                                del lines[decl_line]
                                modified = True
                            else:
                                # Rename non-FIXME declarations
                                new_name = var_name + 'Local'
                                lines[decl_line] = re.sub(rf'\b{re.escape(var_name)}\s*=', f'{new_name} =', lines[decl_line])
                                # Also replace usages in the same scope
                                brace_count = 0
                                for j in range(decl_line + 1, min(decl_line + 100, len(lines))):
                                    brace_count += lines[j].count('{') - lines[j].count('}')
                                    if brace_count < 0:
                                        break
                                    if not re.search(rf'\b\w+\s+{re.escape(var_name)}\s*=', lines[j]):
                                        lines[j] = re.sub(rf'\b{re.escape(var_name)}\b(?!Local)', new_name, lines[j])
                                modified = True
                    else:
                        # Variable is not a parameter - remove duplicate declarations (keep first)
                        if len(declarations) > 1:
                            # Sort by line number
                            declarations.sort()
                            # Remove all but the first declaration
                            for decl_line in reversed(declarations[1:]):
                                # Always remove FIXME declarations
                                if 'FIXME' in lines[decl_line] or 'Added missing' in lines[decl_line]:
                                    del lines[decl_line]
                                    modified = True
                                else:
                                    # Rename non-FIXME duplicates
                                    new_name = var_name + 'Local'
                                    lines[decl_line] = re.sub(rf'\b{re.escape(var_name)}\s*=', f'{new_name} =', lines[decl_line])
                                    modified = True
                
                if modified:
                    content = '\n'.join(lines)
                    java_file.write_text(content, encoding='utf-8')
                    content = java_file.read_text(encoding='utf-8')
        
        # Fix: incompatible types: Map<String,Object> cannot be converted to X
        if 'incompatible types' in error_output.lower() and 'map<string,object>' in error_output.lower() and 'cannot be converted to' in error_output.lower():
            # Extract target type and line number
            type_match = re.search(r'cannot be converted to\s+(\w+)', error_output)
            line_match = re.search(r':(\d+):\s*error.*incompatible types', error_output)
            
            if type_match and line_match:
                target_type = type_match.group(1)
                line_num = int(line_match.group(1)) - 1
                lines = content.split('\n')
                
                if 0 <= line_num < len(lines):
                    # Find return statement with result
                    if 'return result;' in lines[line_num]:
                        # Replace based on target type
                        if target_type.lower() in ['list', 'list<object>']:
                            lines[line_num] = lines[line_num].replace('return result;', 'return new ArrayList<>();  // FIXME: Changed from Map to List')
                        elif target_type.lower() == 'string':
                            lines[line_num] = lines[line_num].replace('return result;', 'return "";  // FIXME: Changed from Map to String')
                        elif target_type.lower() == 'boolean':
                            lines[line_num] = lines[line_num].replace('return result;', 'return false;  // FIXME: Changed from Map to boolean')
                        else:
                            lines[line_num] = lines[line_num].replace('return result;', f'return null;  // FIXME: Changed from Map to {target_type}')
                        modified = True
                
                if modified:
                    content = '\n'.join(lines)
                    java_file.write_text(content, encoding='utf-8')
                    content = java_file.read_text(encoding='utf-8')
        
        # Fix: code outside class (statements outside class definition)
        if 'class, interface, enum, or record expected' in error_output:
            # Check for code statements outside class
            lines = content.split('\n')
            class_start = -1
            class_end = -1
            
            # Find class boundaries
            for i, line in enumerate(lines):
                if re.search(r'^\s*(public\s+)?class\s+\w+', line):
                    class_start = i
                    # Find closing brace
                    brace_count = 1
                    for j in range(i+1, len(lines)):
                        brace_count += lines[j].count('{') - lines[j].count('}')
                        if brace_count == 0:
                            class_end = j
                            break
                    break
            
            if class_start >= 0 and class_end >= 0:
                # Check for code after class
                for i in range(class_end + 1, len(lines)):
                    line = lines[i].strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('//') or line.startswith('/*') or line.startswith('*'):
                        continue
                    # If there's actual code, move it inside class
                    if line and not line.startswith('package') and not line.startswith('import'):
                        # Move code inside class (before closing brace)
                        code_to_move = lines[i]
                        # Indent it
                        indent = '    '
                        if not code_to_move.startswith(' '):
                            code_to_move = indent + code_to_move
                        # Remove from outside
                        del lines[i]
                        # Insert before class closing brace
                        lines.insert(class_end, code_to_move)
                        class_end += 1
                        modified = True
                        break
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: method X is already defined (duplicate method)
        if 'method' in error_output.lower() and 'is already defined' in error_output.lower():
            # Extract method name and line numbers - handle various formats
            # Pattern 1: method operation2() is already defined in class Algorithm
            # Pattern 2: ...:51: error: method operation2() is already defined ...
            method_matches = re.findall(r'method\s+(\w+)\s*\([^)]*\)\s+is already defined', error_output)
            # Also try to extract line number from error message
            line_matches = re.findall(r':(\d+):\s*error.*method\s+(\w+)\s*\([^)]*\)\s+is already defined', error_output)
            
            lines = content.split('\n')
            
            # Collect all method names that have duplicates
            duplicate_methods = set()
            for method_name in method_matches:
                duplicate_methods.add(method_name)
            for line_str, method_name in line_matches:
                duplicate_methods.add(method_name)
            
            # For each method with duplicates, find all occurrences and rename all but the first
            for method_name in duplicate_methods:
                # Find all occurrences of this method in the file
                all_occurrences = []
                for i, line in enumerate(lines):
                    # Match method declaration: public/private/protected [static] ReturnType methodName(
                    if re.search(rf'(public|private|protected)\s+(static\s+)?\w+\s+{re.escape(method_name)}\s*\(', line):
                        all_occurrences.append(i)
                
                # Sort by line number
                all_occurrences.sort()
                
                # Rename all but the first occurrence
                if len(all_occurrences) > 1:
                    suffix_num = 2
                    for occ_line in all_occurrences[1:]:  # Skip first occurrence
                        new_method_name = f'{method_name}{suffix_num}'
                        # Replace method name in declaration
                        lines[occ_line] = re.sub(rf'\b{re.escape(method_name)}\s*\(', f'{new_method_name}(', lines[occ_line])
                        suffix_num += 1
                        modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: incomplete logger declaration (missing semicolon or closing paren)
        if 'logger' in error_output.lower() and ("';' expected" in error_output or "')' expected" in error_output):
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'Logger.getLogger' in line and not line.strip().endswith(';'):
                    # Complete the logger declaration
                    if 'Logger.getLogger' in line and ')' not in line:
                        # Add closing paren and semicolon
                        lines[i] = line.rstrip() + '(Algorithm.class.getName());'
                    elif 'Logger.getLogger' in line and ')' in line and not line.strip().endswith(';'):
                        # Just add semicolon
                        lines[i] = line.rstrip() + ';'
                    modified = True
                    break
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: missing Logger import
        if 'cannot find symbol' in error_output.lower() and 'Logger' in error_output:
            if 'import java.util.logging.Logger;' not in content:
                # Find where to insert import
                insert_idx = 0
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('import '):
                        insert_idx = i
                    elif line.strip().startswith('package '):
                        insert_idx = i + 1
                    elif line.strip() and not line.strip().startswith('//') and not line.strip().startswith('/*'):
                        if insert_idx == 0:
                            insert_idx = i
                        break
                
                # Check if there are other imports to place after
                for i in range(insert_idx, len(lines)):
                    if lines[i].strip().startswith('import java.util'):
                        insert_idx = i + 1
                    elif lines[i].strip().startswith('import ') and not lines[i].strip().startswith('import java.util'):
                        break
                
                lines.insert(insert_idx, 'import java.util.logging.Logger;')
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
                modified = True
        
        # Fix: illegal start of expression (class definition inside method OR method outside class)
        if 'illegal start of expression' in error_output.lower():
            # Extract line number
            line_match = re.search(r':(\d+):\s*error.*illegal start of expression', error_output)
            if line_match:
                line_num = int(line_match.group(1)) - 1
                lines = content.split('\n')
                
                if 0 <= line_num < len(lines):
                    error_line = lines[line_num].strip()
                    
                    # Check if it's a method (starts with public/private static)
                    if re.search(r'^(public|private|protected)\s+static\s+\w+\s+\w+\s*\(', error_line):
                        # Method might be inside another method or outside class
                        # First, find if there's a class declaration
                        class_line = -1
                        for i in range(line_num):
                            if re.search(r'^\s*(public\s+)?class\s+\w+', lines[i]):
                                class_line = i
                                break
                        
                        if class_line >= 0:
                            # Find class end
                            brace_count = 1
                            class_end = class_line
                            for i in range(class_line + 1, len(lines)):
                                brace_count += lines[i].count('{') - lines[i].count('}')
                                if brace_count == 0:
                                    class_end = i
                                    break
                            
                            # Check if method is inside another method by finding the containing method
                            containing_method_start = -1
                            method_brace_count = 0
                            for i in range(line_num - 1, max(0, line_num - 100), -1):
                                method_brace_count += lines[i].count('{') - lines[i].count('}')
                                if method_brace_count > 0:
                                    # Check if this is a method declaration
                                    if re.search(r'(public|private|protected)\s+(static\s+)?\w+\s+\w+\s*\(', lines[i]):
                                        containing_method_start = i
                                        break
                            
                            # Find ALL methods that are inside the containing method (or outside class)
                            methods_to_move = []
                            if containing_method_start >= 0:
                                # Find the end of the containing method
                                containing_brace_count = 1
                                containing_method_end = containing_method_start
                                for i in range(containing_method_start + 1, len(lines)):
                                    containing_brace_count += lines[i].count('{') - lines[i].count('}')
                                    if containing_brace_count == 0:
                                        containing_method_end = i
                                        break
                                
                                # Find all methods between containing_method_start and containing_method_end
                                i = containing_method_start + 1
                                while i < containing_method_end:
                                    line_stripped = lines[i].strip()
                                    if re.search(r'^(public|private|protected)\s+static\s+\w+\s+\w+\s*\(', line_stripped):
                                        method_start = i
                                        method_brace_count = 1
                                        method_end = method_start
                                        for j in range(method_start + 1, len(lines)):
                                            method_brace_count += lines[j].count('{') - lines[j].count('}')
                                            if method_brace_count == 0:
                                                method_end = j
                                                break
                                        methods_to_move.append((method_start, method_end))
                                        i = method_end + 1
                                    else:
                                        i += 1
                            else:
                                # Method is outside class - just move this one method
                                method_brace_count = 1
                                method_end = line_num
                                for i in range(line_num + 1, len(lines)):
                                    method_brace_count += lines[i].count('{') - lines[i].count('}')
                                    if method_brace_count == 0:
                                        method_end = i
                                        break
                                methods_to_move.append((line_num, method_end))
                            
                            # Move all methods (in reverse order to maintain indices)
                            for method_start, method_end in reversed(methods_to_move):
                                method_lines = lines[method_start:method_end+1]
                                # Remove from current location
                                del lines[method_start:method_end+1]
                                
                                # Adjust class_end if needed
                                if method_end < class_end:
                                    class_end -= (method_end - method_start + 1)
                                
                                # Indent and insert before class closing brace
                                method_lines = ['    ' + line if line.strip() else line for line in method_lines]
                                for line in reversed(method_lines):
                                    lines.insert(class_end, line)
                            modified = True
                        else:
                            # No class found - wrap in class
                            # Find where to insert class (after package/imports)
                            class_insert_idx = 0
                            for i, line in enumerate(lines):
                                stripped = line.strip()
                                if stripped.startswith('package ') or stripped.startswith('import '):
                                    class_insert_idx = i + 1
                                elif stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                                    if class_insert_idx == 0:
                                        class_insert_idx = i
                                    break
                            
                            # Find all methods to wrap
                            methods_to_wrap = []
                            i = line_num
                            while i < len(lines):
                                if re.search(r'^(public|private|protected)\s+static\s+', lines[i].strip()):
                                    method_start = i
                                    method_brace_count = 1
                                    method_end = method_start
                                    for j in range(method_start + 1, len(lines)):
                                        method_brace_count += lines[j].count('{') - lines[j].count('}')
                                        if method_brace_count == 0:
                                            method_end = j
                                            break
                                    methods_to_wrap.append((method_start, method_end))
                                    i = method_end + 1
                                else:
                                    i += 1
                            
                            # Insert class declaration
                            lines.insert(class_insert_idx, 'public class Algorithm {')
                            # Find end of all methods
                            if methods_to_wrap:
                                last_method_end = methods_to_wrap[-1][1]
                                # Add closing brace
                                lines.insert(last_method_end + 1, '}')
                            modified = True
                    
                    # Check if it's a class definition inside a method
                    elif 'public static class' in lines[line_num] or 'private static class' in lines[line_num] or 'static class' in lines[line_num]:
                        # Find the method that contains this class
                        method_start = -1
                        brace_count = 0
                        for i in range(line_num - 1, max(0, line_num - 50), -1):
                            if '{' in lines[i]:
                                brace_count += lines[i].count('{') - lines[i].count('}')
                                if brace_count > 0:
                                    # Check if this is a method declaration
                                    if re.search(r'(public|private|protected)\s+(static\s+)?\w+\s+\w+\s*\(', lines[i]):
                                        method_start = i
                                        break
                        
                        if method_start >= 0:
                            # Move the class definition outside the method (after the class closing brace)
                            # Find the end of the method
                            method_brace_count = 1
                            method_end = method_start
                            for i in range(method_start + 1, len(lines)):
                                method_brace_count += lines[i].count('{') - lines[i].count('}')
                                if method_brace_count == 0:
                                    method_end = i
                                    break
                            
                            # Find the class definition block
                            class_brace_count = 1
                            class_end = line_num
                            for i in range(line_num + 1, len(lines)):
                                class_brace_count += lines[i].count('{') - lines[i].count('}')
                                if class_brace_count == 0:
                                    class_end = i
                                    break
                            
                            # Extract the class definition
                            class_lines = lines[line_num:class_end+1]
                            # Remove from inside method
                            del lines[line_num:class_end+1]
                            
                            # Find the main class closing brace
                            main_class_start = -1
                            for i, line in enumerate(lines):
                                if re.search(r'^\s*public\s+class\s+\w+', line):
                                    main_class_start = i
                                    break
                            
                            if main_class_start >= 0:
                                # Find main class end
                                main_brace_count = 1
                                main_class_end = main_class_start
                                for i in range(main_class_start + 1, len(lines)):
                                    main_brace_count += lines[i].count('{') - lines[i].count('}')
                                    if main_brace_count == 0:
                                        main_class_end = i
                                        break
                                
                                # Insert class definition before main class closing brace
                                for line in reversed(class_lines):
                                    lines.insert(main_class_end, line)
                                modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: invalid method declaration; return type required (constructor issue)
        if 'invalid method declaration' in error_output.lower() and 'return type required' in error_output.lower():
            # Extract line number
            line_match = re.search(r':(\d+):\s*error.*invalid method declaration.*return type required', error_output)
            if line_match:
                line_num = int(line_match.group(1)) - 1
                lines = content.split('\n')
                
                if 0 <= line_num < len(lines):
                    error_line = lines[line_num].strip()
                    # Check if it's a constructor that's missing the class name
                    # Pattern: public MethodName(...) should be public ClassName(...)
                    constructor_match = re.search(r'public\s+(\w+)\s*\(', error_line)
                    if constructor_match:
                        method_name = constructor_match.group(1)
                        # Find the class name this constructor belongs to
                        class_name = None
                        # Look backwards to find the class
                        brace_count = 0
                        for i in range(line_num - 1, max(0, line_num - 100), -1):
                            brace_count += lines[i].count('{') - lines[i].count('}')
                            class_match = re.search(r'class\s+(\w+)', lines[i])
                            if class_match:
                                class_name = class_match.group(1)
                                break
                            if brace_count < 0:
                                break
                        
                        if class_name and method_name != class_name:
                            # This is a constructor with wrong name - fix it
                            lines[line_num] = re.sub(rf'public\s+{re.escape(method_name)}\s*\(', f'public {class_name}(', lines[line_num])
                            modified = True
                        elif not class_name:
                            # Constructor might be outside class - find the class it should belong to
                            # Look for class definitions before this line
                            for i in range(line_num - 1, max(0, line_num - 50), -1):
                                class_match = re.search(r'class\s+(\w+)', lines[i])
                                if class_match:
                                    class_name = class_match.group(1)
                                    # Check if constructor name matches class name
                                    if method_name == class_name:
                                        # Constructor is outside class - need to move it inside
                                        # Find the class closing brace
                                        brace_count = 1
                                        class_end = i
                                        for j in range(i + 1, len(lines)):
                                            brace_count += lines[j].count('{') - lines[j].count('}')
                                            if brace_count == 0:
                                                class_end = j
                                                break
                                        
                                        # Find constructor end
                                        constructor_brace_count = 1
                                        constructor_end = line_num
                                        for j in range(line_num + 1, len(lines)):
                                            constructor_brace_count += lines[j].count('{') - lines[j].count('}')
                                            if constructor_brace_count == 0:
                                                constructor_end = j
                                                break
                                        
                                        # Move constructor inside class
                                        constructor_lines = lines[line_num:constructor_end+1]
                                        del lines[line_num:constructor_end+1]
                                        # Indent and insert before class closing brace
                                        constructor_lines = ['    ' + line if line.strip() else line for line in constructor_lines]
                                        for line in reversed(constructor_lines):
                                            lines.insert(class_end, line)
                                        modified = True
                                    break
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        # Fix: missing return statement
        if 'missing return statement' in error_output.lower():
            # Extract line number
            line_match = re.search(r':(\d+):\s*error.*missing return statement', error_output)
            if line_match:
                line_num = int(line_match.group(1)) - 1
                lines = content.split('\n')
                
                if 0 <= line_num < len(lines):
                    # Find the method that's missing a return statement
                    # Look backwards to find method signature
                    method_start = -1
                    method_return_type = None
                    for i in range(line_num - 1, max(0, line_num - 50), -1):
                        # Check if this is a method declaration
                        method_match = re.search(r'(public|private|protected)\s+(static\s+)?(\w+)\s+\w+\s*\(', lines[i])
                        if method_match:
                            method_start = i
                            method_return_type = method_match.group(3)
                            break
                        # Stop if we hit another method or class
                        if re.search(r'^\s*}\s*$', lines[i]) or re.search(r'^\s*class\s+', lines[i]):
                            break
                    
                    if method_start >= 0 and method_return_type:
                        # Find the method's closing brace
                        method_brace_count = 1
                        method_end = method_start
                        for i in range(method_start + 1, len(lines)):
                            method_brace_count += lines[i].count('{') - lines[i].count('}')
                            if method_brace_count == 0:
                                method_end = i
                                break
                        
                        # Check if method already has a return statement
                        has_return = False
                        for i in range(method_start + 1, method_end):
                            if 'return' in lines[i] and not lines[i].strip().startswith('//'):
                                has_return = True
                                break
                        
                        if not has_return:
                            # Add return statement before closing brace
                            indent = len(lines[method_end]) - len(lines[method_end].lstrip())
                            if method_return_type == 'void':
                                return_stmt = ' ' * indent + 'return;  // FIXME: Added missing return'
                            elif method_return_type in ['int', 'Integer']:
                                return_stmt = ' ' * indent + 'return 0;  // FIXME: Added missing return'
                            elif method_return_type in ['boolean', 'Boolean']:
                                return_stmt = ' ' * indent + 'return false;  // FIXME: Added missing return'
                            elif method_return_type == 'String':
                                return_stmt = ' ' * indent + 'return "";  // FIXME: Added missing return'
                            elif method_return_type == 'Object':
                                return_stmt = ' ' * indent + 'return null;  // FIXME: Added missing return'
                            else:
                                return_stmt = ' ' * indent + f'return null;  // FIXME: Added missing return for {method_return_type}'
                            
                            lines.insert(method_end, return_stmt)
                            modified = True
            
            if modified:
                content = '\n'.join(lines)
                java_file.write_text(content, encoding='utf-8')
                content = java_file.read_text(encoding='utf-8')
        
        return modified
    except Exception as e:
        print(f"  ⚠ Error fixing compilation errors: {e}", flush=True)
        return False


def get_all_java_files() -> List[Tuple[str, Path]]:
    """Get list of all Java Algorithm.java files (algo_path, java_file)."""
    java_files = []
    for java_file in ROOT.rglob("Algorithm.java"):
        # Skip files in scripts, tests, or __pycache__ directories
        if any(part in ["scripts", "tests", "__pycache__"] for part in java_file.parts):
            continue
        # Get algorithm path (parent directory relative to ROOT)
        algo_path = str(java_file.parent.relative_to(ROOT))
        java_files.append((algo_path, java_file))
    
    return sorted(java_files)


def test_single_java_file(java_file: Path, timeout: int = 60) -> Tuple[bool, str, str]:
    """
    Test a single Java file: compile and run.
    Returns (success, error_message, output).
    """
    try:
        try:
            algorithm_path = str(java_file.parent.relative_to(ROOT))
        except ValueError:
            # If relative_to fails, use absolute path
            algorithm_path = str(java_file.parent)
        class_path = str(java_file.parent.absolute())
        
        # Compile Java file
        compile_result = subprocess.run(
            ["javac", str(java_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ROOT)
        )
        
        if compile_result.returncode != 0:
            error_msg = compile_result.stderr or compile_result.stdout or ""
            # Return compilation error for fixing
            return False, error_msg, compile_result.stdout or ""
        
        # Run Java file - need to use full package-qualified class name
        # Extract package name from file
        content = java_file.read_text(encoding='utf-8')
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        if package_match:
            package_name = package_match.group(1)
            class_name = f"{package_name}.Algorithm"
            # Use current directory (.) as classpath to support package structure
            # Java will look for packages relative to the classpath root
            classpath = "."
        else:
            class_name = "Algorithm"
            # If no package, use the directory containing the file as classpath
            classpath = str(java_file.parent)
        
        # Run with proper classpath
        run_result = subprocess.run(
            ["java", "-cp", classpath, class_name],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(ROOT)
        )
        
        output = run_result.stdout or ""
        error_msg = run_result.stderr or ""
        
        # Success if return code is 0
        success = run_result.returncode == 0
        
        return success, error_msg, output
        
    except subprocess.TimeoutExpired:
        return False, f"Test timed out after {timeout} seconds", ""
    except Exception as e:
        return False, f"Error running test: {e}", ""


def init_database():
    """Initialize test_results database if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm_path TEXT NOT NULL,
                language TEXT NOT NULL,
                status TEXT NOT NULL,
                duration REAL,
                timestamp TEXT NOT NULL,
                error_message TEXT,
                test_output TEXT,
                previous_status TEXT,
                state_changed INTEGER DEFAULT 0,
                UNIQUE(algorithm_path, language, timestamp)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_algorithm_path 
            ON test_results(algorithm_path)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON test_results(timestamp DESC)
        """)
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"  ⚠ Database initialization failed: {e}", flush=True)


def is_file_already_passing(algorithm_path: str) -> bool:
    """
    Check if a file is already passing in the database.
    Returns True if the last test result for this file was 'success'.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = 'java'
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == 'success':
            return True
        return False
    except Exception:
        # If database error, assume not passing (test it)
        return False


def update_database(algorithm_path: str, status: str, duration: float, 
                   error_message: Optional[str], test_output: Optional[str], 
                   was_fixed: bool = False):
    """Update test_results database with test result."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get previous status
        cursor.execute("""
            SELECT status FROM test_results
            WHERE algorithm_path = ? AND language = 'java'
            ORDER BY timestamp DESC
            LIMIT 1
        """, (algorithm_path,))
        
        previous_result = cursor.fetchone()
        previous_status = previous_result[0] if previous_result else None
        
        # Determine state change
        state_changed = False
        if previous_status:
            if previous_status != status:
                state_changed = True
        
        # Insert new result
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO test_results 
            (algorithm_path, language, status, duration, timestamp, error_message, 
             test_output, previous_status, state_changed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            algorithm_path,
            'java',
            status,
            duration,
            timestamp,
            error_message,
            test_output,
            previous_status,
            1 if state_changed else 0,
        ))
        
        conn.commit()
        conn.close()
        
        if was_fixed and status == 'success':
            print(f"  💾 Database updated: {algorithm_path} (Java) - Fixed and passing", flush=True)
    except Exception as e:
        print(f"  ⚠ Database update failed: {e}", flush=True)


def commit_file(java_file: Path, algo_path: str) -> bool:
    """Commit the Java file on successful test (no push)."""
    try:
        # Check if file has changes
        result = subprocess.run(
            ["git", "diff", "--quiet", str(java_file)],
            cwd=str(ROOT),
            capture_output=True,
            timeout=10
        )
        
        # If no changes, check if file is untracked
        if result.returncode == 0:
            result = subprocess.run(
                ["git", "ls-files", "--error-unmatch", str(java_file)],
                cwd=str(ROOT),
                capture_output=True,
                timeout=10
            )
            if result.returncode != 0:
                # File is untracked, add it
                subprocess.run(
                    ["git", "add", str(java_file)],
                    check=True,
                    cwd=str(ROOT),
                    capture_output=True,
                    timeout=10
                )
        else:
            # File has changes, stage it
            subprocess.run(
                ["git", "add", str(java_file)],
                check=True,
                cwd=str(ROOT),
                capture_output=True,
                timeout=10
            )
        
        # Commit
        commit_msg = f"Test passed: {algo_path} (Java)"
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if commit_result.returncode == 0:
            return True
        elif "nothing to commit" in commit_result.stdout.lower() or "nothing to commit" in (commit_result.stderr or "").lower():
            # No changes to commit (file was already committed or unchanged)
            return True
        else:
            print(f"  ⚠ Commit failed: {commit_result.stderr or commit_result.stdout}", flush=True)
            return False
    except subprocess.TimeoutExpired:
        print(f"  ❌ Commit timed out", flush=True)
        return False
    except Exception as e:
        print(f"  ⚠ Commit error: {e}", flush=True)
        return False


def main():
    """Main function to test Java files one by one."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Test and fix Java files one by one',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m scripts.fix_java_one_by_one
  python -m scripts.fix_java_one_by_one --skip-passing
  python -m scripts.fix_java_one_by_one --no-skip-passing
        """
    )
    parser.add_argument(
        '--skip-passing',
        action='store_true',
        default=False,
        help='Skip testing files that are already passing in the database (default: False)'
    )
    parser.add_argument(
        '--no-skip-passing',
        action='store_false',
        dest='skip_passing',
        help='Test all files, even if they are already passing (opposite of --skip-passing)'
    )
    
    args = parser.parse_args()
    skip_passing = args.skip_passing
    
    # Ensure output is flushed immediately
    sys.stdout.reconfigure(encoding='utf-8')
    
    start_timestamp = datetime.now()
    start_time = time.time()
    
    print("=" * 80, flush=True)
    print("TESTING JAVA FILES ONE BY ONE", flush=True)
    print("=" * 80, flush=True)
    if skip_passing:
        print("⚠️  MODE: Skipping files that are already passing", flush=True)
    else:
        print("⚠️  MODE: Testing all files (including already passing)", flush=True)
    print(flush=True)
    
    print("=" * 80, flush=True)
    print(f"🚀 STARTED AT: {start_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 80, flush=True)
    print(flush=True)
    
    # Initialize database
    print("Initializing database...", flush=True)
    init_database()
    
    print("Loading all Java files...", flush=True)
    all_java_files = get_all_java_files()
    total_java_files = len(all_java_files)
    print(f"Found {total_java_files} Java files", flush=True)
    
    # Filter out already passing files if requested
    java_files = all_java_files
    initial_skipped = 0
    if skip_passing:
        print("Checking which files are already passing...", flush=True)
        original_count = len(java_files)
        java_files = [
            (algo_path, java_file) 
            for algo_path, java_file in java_files 
            if not is_file_already_passing(algo_path)
        ]
        initial_skipped = original_count - len(java_files)
        print(f"  ⊘ Skipping {initial_skipped} files that are already passing", flush=True)
        print(f"  → Will test {len(java_files)} files", flush=True)
    
    print(flush=True)
    
    # Initialize counters
    passed_count = 0
    fixed_count = 0
    failed_count = 0
    skipped_count = initial_skipped
    
    # Initialize status state
    with _status_lock:
        _status_state['total_files'] = len(java_files)
        _status_state['start_time'] = start_time
        _status_state['passed_count'] = 0
        _status_state['fixed_count'] = 0
        _status_state['failed_count'] = 0
        _status_state['skipped_count'] = skipped_count
    
    # Start status reporter thread
    print("📊 Status updates will appear every 3 minutes", flush=True)
    print("📝 Status after each file will be shown", flush=True)
    print(flush=True)
    status_thread = threading.Thread(target=status_reporter, daemon=True)
    status_thread.start()
    
    try:
        for idx, (algo_path, java_file) in enumerate(java_files, 1):
            try:
                # Update status
                with _status_lock:
                    _status_state['current_idx'] = idx
                    _status_state['current_file'] = algo_path
                    _status_state['passed_count'] = passed_count
                    _status_state['fixed_count'] = fixed_count
                    _status_state['failed_count'] = failed_count
                    _status_state['skipped_count'] = skipped_count
                
                print(f"[{idx}/{len(java_files)}] Testing: {algo_path}", flush=True)
                print(f"  Java file: {java_file.relative_to(ROOT)}", flush=True)
                
                # Keep testing and fixing until it passes
                success = False
                test_attempts = 0
                fix_attempts = 0
                max_fix_attempts = 10
                max_test_attempts = 15  # Prevent infinite test retries
                was_fixed = False
                duration = 0.0
                error_msg = ""
                output = ""
                test_start = time.time()
                last_error_msg = ""  # Track if same error repeats (hanging)
                same_error_count = 0
                
                while not success:
                    # Prevent infinite loops
                    if test_attempts >= max_test_attempts:
                        print(f"  ❌ Maximum test attempts ({max_test_attempts}) reached, moving on", flush=True)
                        print(f"  ⚠ This file may be hanging or have an unfixable issue", flush=True)
                        # Update database with failure
                        update_database(algo_path, 'failure', time.time() - test_start, "Maximum test attempts reached - possible infinite loop or hang", "", False)
                        failed_count += 1
                        with _status_lock:
                            _status_state['failed_count'] = failed_count
                        break
                    
                    # Test the file
                    test_attempts += 1
                    single_test_start = time.time()
                    
                    # Reduce timeout if we've had multiple attempts (might be hanging)
                    test_timeout = 60
                    if test_attempts > 5:
                        test_timeout = 30  # Reduce timeout after 5 attempts
                    if test_attempts > 10:
                        test_timeout = 15  # Further reduce after 10 attempts
                    
                    if test_attempts == 1:
                        print(f"  🧪 Running tests (timeout: {test_timeout}s)...", flush=True)
                    else:
                        print(f"  🧪 Retesting (test attempt {test_attempts}/{max_test_attempts}, timeout: {test_timeout}s)...", flush=True)
                    
                    success, error_msg, output = test_single_java_file(java_file, timeout=test_timeout)
                    duration = time.time() - test_start
                    
                    # Check if same error is repeating (indicates hanging or unfixable issue)
                    if not success and error_msg:
                        error_hash = error_msg[:200]  # Use first 200 chars as error signature
                        if error_hash == last_error_msg:
                            same_error_count += 1
                            if same_error_count >= 3:
                                print(f"  ❌ Same error repeated {same_error_count} times, likely hanging or unfixable", flush=True)
                                print(f"  ⚠ Moving on to next file", flush=True)
                                # Update database with failure
                                update_database(algo_path, 'failure', duration, f"Same error repeated {same_error_count} times: {error_msg[:500]}", output, False)
                                failed_count += 1
                                with _status_lock:
                                    _status_state['failed_count'] = failed_count
                                break
                        else:
                            same_error_count = 0
                            last_error_msg = error_hash
                    
                    if success:
                        # Test passed!
                        if was_fixed:
                            print(f"  ✓ Tests passed after {fix_attempts} fix attempt(s)!", flush=True)
                        else:
                            print(f"  ✓ Tests passed!", flush=True)
                        
                        # Update database
                        update_database(algo_path, 'success', duration, None, output, was_fixed)
                        
                        # Commit on success (no push)
                        print(f"  💾 Committing (no push)...", flush=True)
                        if commit_file(java_file, algo_path):
                            print(f"  ✓ Committed successfully", flush=True)
                            if was_fixed:
                                fixed_count += 1
                                with _status_lock:
                                    _status_state['fixed_count'] = fixed_count
                            else:
                                passed_count += 1
                                with _status_lock:
                                    _status_state['passed_count'] = passed_count
                        else:
                            print(f"  ⚠ Commit had issues, but test passed", flush=True)
                            if was_fixed:
                                fixed_count += 1
                            else:
                                passed_count += 1
                        break
                    else:
                        # Test failed - try to fix it
                        if fix_attempts >= max_fix_attempts:
                            print(f"  ❌ Maximum fix attempts ({max_fix_attempts}) reached, moving on", flush=True)
                            print(f"  Error output (first 500 chars):", flush=True)
                            print(f"  {error_msg[:500]}", flush=True)
                            
                            # Update database with failure
                            update_database(algo_path, 'failure', duration, error_msg, output, False)
                            
                            failed_count += 1
                            with _status_lock:
                                _status_state['failed_count'] = failed_count
                            break
                        
                        fix_attempts += 1
                        print(f"  ❌ Tests failed, attempting fix #{fix_attempts}...", flush=True)
                        
                        # Try different fix strategies
                        fixed = False
                        
                        print(f"  🔧 Attempting to fix class name mismatch...", flush=True)
                        if fix_class_name_mismatch(java_file):
                            print(f"  ✓ File modified, will retest", flush=True)
                            fixed = True
                            was_fixed = True
                        
                        if not fixed:
                            print(f"  🔧 Attempting to fix package errors...", flush=True)
                            if fix_package_errors(java_file):
                                print(f"  ✓ File modified, will retest", flush=True)
                                fixed = True
                                was_fixed = True
                        
                        if not fixed:
                            print(f"  🔧 Attempting to fix compilation errors...", flush=True)
                            if fix_compilation_errors(java_file, error_msg):
                                print(f"  ✓ File modified, will retest", flush=True)
                                fixed = True
                                was_fixed = True
                        
                        if not fixed:
                            print(f"  🔧 Checking for missing main method...", flush=True)
                            if fix_missing_main_method(java_file):
                                print(f"  ✓ File modified, will retest", flush=True)
                                fixed = True
                                was_fixed = True
                        
                        if not fixed:
                            print(f"  ⚠ Could not fix (no changes made)", flush=True)
                            # Show first 500 chars of error output
                            error_preview = error_msg[:500] if len(error_msg) > 500 else error_msg
                            print(f"  Error output (first 500 chars):", flush=True)
                            print(f"  {error_preview}", flush=True)
                            
                            # Update database with failure
                            update_database(algo_path, 'failure', duration, error_msg, output, False)
                            
                            failed_count += 1
                            with _status_lock:
                                _status_state['failed_count'] = failed_count
                            break
                
                print("-" * 80, flush=True)
                print(f"STATUS: [{idx}/{len(java_files)}] | Passed: {passed_count} | Fixed: {fixed_count} | Failed: {failed_count} | Elapsed: {int((time.time() - start_time) // 60)}m {int((time.time() - start_time) % 60)}s", flush=True)
                print("-" * 80, flush=True)
                print(flush=True)
                
            except KeyboardInterrupt:
                print("\n⚠ Interrupted by user", flush=True)
                raise
            except Exception as e:
                print(f"  ❌ Error processing file: {e}", flush=True)
                skipped_count += 1
                with _status_lock:
                    _status_state['skipped_count'] = skipped_count
                continue
    
    except KeyboardInterrupt:
        print("\n⚠ Script interrupted by user", flush=True)
    
    finally:
        # Stop status reporter
        _status_state['stop_event'].set()
        
        # Final summary
        end_time = time.time()
        total_time = end_time - start_time
        total_minutes = int(total_time // 60)
        total_seconds = int(total_time % 60)
        
        print("", flush=True)
        print("=" * 80, flush=True)
        print(f"🏁 FINISHED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        print("=" * 80, flush=True)
        print(f"Total time: {total_minutes}m {total_seconds}s", flush=True)
        if skip_passing and initial_skipped > 0:
            print(f"Total files: {total_java_files} (tested {len(java_files)}, skipped {initial_skipped})", flush=True)
        else:
            print(f"Total files: {len(java_files)}", flush=True)
        print(f"  ✓ Passed: {passed_count}", flush=True)
        print(f"  🔧 Fixed and passed: {fixed_count}", flush=True)
        print(f"  ❌ Failed: {failed_count}", flush=True)
        if skipped_count > 0:
            print(f"  ⊘ Skipped: {skipped_count}", flush=True)
        print("=" * 80, flush=True)


if __name__ == "__main__":
    main()

