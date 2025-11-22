#!/usr/bin/env python3
"""
Analyze Java Algorithm files for consistency and correctness.
Checks: path, package, class, filename, packages/libraries, return types, main method.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
import subprocess

def find_java_algorithm_files(root_path: str = ".") -> List[Path]:
    """Find all Algorithm.java files in the project."""
    root = Path(root_path)
    java_files = []

    # Skip certain directories
    skip_dirs = {'.git', '__pycache__', 'target', '.vscode', '.idea', 'node_modules'}

    for path in root.rglob("Algorithm.java"):
        # Skip if any parent directory is in skip_dirs
        if any(part in skip_dirs for part in path.parts):
            continue
        java_files.append(path)

    return sorted(java_files)

def extract_package_info(content: str) -> str:
    """Extract package declaration from Java file content."""
    package_match = re.search(r'^\s*package\s+([^;]+);', content, re.MULTILINE)
    return package_match.group(1).strip() if package_match else ""

def extract_class_info(content: str) -> Tuple[str, str]:
    """Extract class name and extends/implements info."""
    # Look for public class declaration
    class_match = re.search(r'^\s*public\s+class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+[^}]+)?', content, re.MULTILINE)
    if class_match:
        class_name = class_match.group(1)
        extends = class_match.group(2) if class_match.group(2) else ""
        return class_name, extends
    return "", ""

def check_imports(content: str) -> List[str]:
    """Check for potentially problematic imports."""
    problematic_imports = []

    # Common problematic patterns
    patterns = [
        (r'import\s+java\.awt\.', 'AWT imports (GUI)'),
        (r'import\s+javax\.swing\.', 'Swing imports (GUI)'),
        (r'import\s+java\.net\.', 'Network imports'),
        (r'import\s+java\.nio\.', 'NIO imports'),
        (r'import\s+java\.security\.', 'Security imports'),
        (r'import\s+java\.sql\.', 'SQL imports'),
        (r'import\s+java\.rmi\.', 'RMI imports'),
        (r'import\s+javax\.xml\.', 'XML imports'),
    ]

    for pattern, description in patterns:
        if re.search(pattern, content):
            problematic_imports.append(description)

    return problematic_imports

def analyze_return_types(content: str) -> Dict[str, Set[str]]:
    """Analyze return types in methods."""
    return_types = {}

    # Find all method declarations (simplified pattern)
    method_pattern = r'^\s*(?:public|private|protected)?\s*\w+(?:<[^>]+>)?\s+(\w+)\s*\([^)]*\)\s*\{'
    methods = re.findall(method_pattern, content, re.MULTILINE)

    for return_type in methods:
        if return_type not in ['void', 'String', 'int', 'boolean', 'Object', 'List', 'Map', 'Set']:
            if return_type in return_types:
                return_types[return_type].add('method')
            else:
                return_types[return_type] = {'method'}

    # Find return statements
    return_pattern = r'^\s*return\s+([^;]+);'
    returns = re.findall(return_pattern, content, re.MULTILINE)

    for return_expr in returns:
        return_expr = return_expr.strip()
        if return_expr == 'null':
            return_types['null'] = return_types.get('null', set()) | {'return'}
        elif return_expr.startswith('new '):
            return_types['new_object'] = return_types.get('new_object', set()) | {'return'}
        elif '"' in return_expr:
            return_types['string_literal'] = return_types.get('string_literal', set()) | {'return'}
        elif return_expr.isdigit():
            return_types['int_literal'] = return_types.get('int_literal', set()) | {'return'}
        elif 'true' in return_expr or 'false' in return_expr:
            return_types['boolean_literal'] = return_types.get('boolean_literal', set()) | {'return'}

    return return_types

def check_main_method(content: str) -> bool:
    """Check if main method is present."""
    main_pattern = r'^\s*public\s+static\s+void\s+main\s*\(\s*String\s*\[\]\s+\w+\s*\)'
    return bool(re.search(main_pattern, content, re.MULTILINE))

def validate_package_path(java_file: Path, package: str) -> List[str]:
    """Validate that package matches directory structure."""
    issues = []

    if not package:
        issues.append("Missing package declaration")
        return issues

    # Convert package to path
    package_path = package.replace('.', '/')

    # Get the directory containing the file
    file_dir = java_file.parent

    # Check if the package path matches the directory structure
    # Look for the package path in the file's path
    file_path_str = str(java_file)

    if package_path not in file_path_str:
        issues.append(f"Package '{package}' doesn't match directory structure")

    # More specific check: the directory should contain the package path
    expected_package_parts = package.split('.')
    actual_path_parts = list(file_dir.parts)

    # Find where the package path should start
    for i, part in enumerate(actual_path_parts):
        if part == expected_package_parts[0]:
            # Check if the subsequent parts match
            if actual_path_parts[i:i+len(expected_package_parts)] == expected_package_parts:
                break
    else:
        issues.append(f"Package path '{package_path}' not found in directory structure")

    return issues

def compile_java_file(java_file: Path) -> Tuple[bool, str]:
    """Try to compile the Java file to check for syntax errors."""
    try:
        result = subprocess.run(
            ["javac", str(java_file)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(java_file.parent)
        )
        success = result.returncode == 0
        error_output = result.stderr.strip() if not success else ""
        return success, error_output
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out"
    except Exception as e:
        return False, f"Compilation error: {e}"

def analyze_java_file(java_file: Path) -> Dict:
    """Analyze a single Java file comprehensively."""
    try:
        content = java_file.read_text(encoding='utf-8')
    except Exception as e:
        return {
            'file_path': str(java_file),
            'error': f"Cannot read file: {e}",
            'valid': False
        }

    # Basic info
    file_path = str(java_file)
    filename = java_file.name
    relative_path = str(java_file.relative_to(Path('.')))

    # Extract info
    package = extract_package_info(content)
    class_name, extends = extract_class_info(content)

    # Validation
    package_issues = validate_package_path(java_file, package)
    has_main = check_main_method(content)
    problematic_imports = check_imports(content)
    return_types = analyze_return_types(content)

    # Compilation check
    compiles, compile_error = compile_java_file(java_file)

    # Check for inconsistent return types (methods returning null vs new Object)
    inconsistent_returns = []
    if 'null' in return_types and 'new_object' in return_types:
        inconsistent_returns.append("Mixed null and new Object() returns")

    result = {
        'file_path': file_path,
        'relative_path': relative_path,
        'filename': filename,
        'package': package,
        'class_name': class_name,
        'extends': extends,
        'has_main_method': has_main,
        'compiles': compiles,
        'compile_error': compile_error,
        'package_issues': package_issues,
        'problematic_imports': problematic_imports,
        'return_types': return_types,
        'inconsistent_returns': inconsistent_returns,
        'valid': len(package_issues) == 0 and compiles and has_main
    }

    return result

def generate_report(java_files: List[Path], output_file: str = "java_analysis_report.txt"):
    """Generate comprehensive analysis report."""
    print(f"Analyzing {len(java_files)} Java Algorithm files...")

    results = []
    summary = {
        'total_files': len(java_files),
        'valid_files': 0,
        'compilation_errors': 0,
        'missing_main': 0,
        'package_issues': 0,
        'problematic_imports': 0,
        'inconsistent_returns': 0
    }

    for java_file in java_files:
        print(f"Analyzing: {java_file}")
        result = analyze_java_file(java_file)
        results.append(result)

        if result.get('valid', False):
            summary['valid_files'] += 1
        if not result.get('compiles', False):
            summary['compilation_errors'] += 1
        if not result.get('has_main_method', False):
            summary['missing_main'] += 1
        if result.get('package_issues'):
            summary['package_issues'] += 1
        if result.get('problematic_imports'):
            summary['problematic_imports'] += 1
        if result.get('inconsistent_returns'):
            summary['inconsistent_returns'] += 1

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("JAVA ALGORITHM FILES ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")

        # Summary
        f.write("SUMMARY:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total files analyzed: {summary['total_files']}\n")
        f.write(f"Valid files: {summary['valid_files']} ({summary['valid_files']/summary['total_files']*100:.1f}%)\n")
        f.write(f"Compilation errors: {summary['compilation_errors']}\n")
        f.write(f"Missing main method: {summary['missing_main']}\n")
        f.write(f"Package issues: {summary['package_issues']}\n")
        f.write(f"Problematic imports: {summary['problematic_imports']}\n")
        f.write(f"Inconsistent returns: {summary['inconsistent_returns']}\n\n")

        # Detailed results
        f.write("DETAILED ANALYSIS:\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            f.write(f"File: {result['relative_path']}\n")
            f.write(f"  Filename: {result['filename']}\n")
            f.write(f"  Package: {result['package'] or 'MISSING'}\n")
            f.write(f"  Class: {result['class_name'] or 'MISSING'}\n")
            f.write(f"  Extends: {result['extends'] or 'None'}\n")
            f.write(f"  Has main method: {'YES' if result['has_main_method'] else 'NO'}\n")
            f.write(f"  Compiles: {'YES' if result['compiles'] else 'NO'}\n")

            if result.get('package_issues'):
                f.write(f"  Package issues: {', '.join(result['package_issues'])}\n")

            if result.get('problematic_imports'):
                f.write(f"  Problematic imports: {', '.join(result['problematic_imports'])}\n")

            if result.get('inconsistent_returns'):
                f.write(f"  Return inconsistencies: {', '.join(result['inconsistent_returns'])}\n")

            if not result['compiles'] and result.get('compile_error'):
                f.write(f"  Compile error: {result['compile_error'][:200]}...\n")

            f.write("\n")

    print(f"Report generated: {output_file}")
    print(f"Summary: {summary['valid_files']}/{summary['total_files']} files are valid")

def main():
    """Main function."""
    print("Java Algorithm Files Analyzer")
    print("=" * 40)

    # Find all Java Algorithm files
    java_files = find_java_algorithm_files()
    print(f"Found {len(java_files)} Algorithm.java files")

    if not java_files:
        print("No Java Algorithm files found!")
        return

    # Generate report
    output_file = "java_analysis_report.txt"
    generate_report(java_files, output_file)

if __name__ == "__main__":
    main()
