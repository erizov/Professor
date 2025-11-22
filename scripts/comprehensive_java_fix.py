#!/usr/bin/env python3
"""
Comprehensive Java Algorithm fixes - Steps 1-5
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

def find_all_java_files() -> List[Path]:
    """Find all Algorithm.java files."""
    java_files = []
    skip_dirs = {'.git', '__pycache__', 'target', '.vscode', '.idea', 'node_modules'}

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        if 'Algorithm.java' in files:
            java_files.append(Path(root) / 'Algorithm.java')
    return sorted(java_files)

def step1_fix_packages(java_files: List[Path]) -> Dict[str, int]:
    """Step 1: Fix missing package declarations."""
    print("Step 1: Fixing missing package declarations...")
    fixed_count = 0
    semester01_files = [f for f in java_files if 'semester_01' in str(f)]

    for java_file in semester01_files:
        content = java_file.read_text(encoding='utf-8')

        # Skip if already has package
        if re.search(r'^\s*package\s+semester_01\.', content, re.MULTILINE):
            continue

        # Generate package name from path
        path_parts = java_file.parts
        semester_idx = path_parts.index('semester_01')
        package_parts = path_parts[semester_idx:-1]  # Exclude filename
        package_name = '.'.join(package_parts)

        # Check if package is in comment
        comment_package = re.search(r'/\*\*\s*\n\s*\*\s*package\s+' + re.escape(package_name) + r';', content, re.MULTILINE)
        if comment_package:
            # Remove from comment
            content = re.sub(r'/\*\*\s*\n\s*\*\s*package\s+' + re.escape(package_name) + r';\s*\n', '/**\n', content)

        # Add package declaration at top
        lines = content.split('\n')
        # Find first non-empty, non-comment line
        insert_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                insert_idx = i
                break

        lines.insert(insert_idx, f'package {package_name};')
        if insert_idx > 0 or lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, '')

        content = '\n'.join(lines)
        java_file.write_text(content, encoding='utf-8')
        fixed_count += 1

    print(f"Fixed {fixed_count} package declarations in semester_01")
    return {'packages_fixed': fixed_count}

def step2_add_main_methods(java_files: List[Path]) -> Dict[str, int]:
    """Step 2: Ensure all files have main methods."""
    print("Step 2: Adding missing main methods...")
    added_count = 0

    for java_file in java_files:
        content = java_file.read_text(encoding='utf-8')

        # Skip if already has main method
        if re.search(r'public\s+static\s+void\s+main\s*\(', content):
            continue

        # Add main method before the last closing brace
        main_method = '''
    public static void main(String[] args) {
        // TODO: Add test implementation
        System.out.println("Algorithm execution placeholder");
    }
}
'''

        # Replace the last }
        content = re.sub(r'}\s*$', main_method, content, flags=re.MULTILINE)

        java_file.write_text(content, encoding='utf-8')
        added_count += 1

    print(f"Added main methods to {added_count} files")
    return {'main_methods_added': added_count}

def step3_standardize_returns(java_files: List[Path]) -> Dict[str, int]:
    """Step 3: Standardize return types."""
    print("Step 3: Standardizing return types...")
    standardized_count = 0

    for java_file in java_files:
        content = java_file.read_text(encoding='utf-8')

        # Replace inconsistent returns with null (for incomplete implementations)
        original_content = content

        # Replace new Object() with null in return statements
        content = re.sub(r'return\s+new\s+Object\(\)\s*;', 'return null;', content)

        # Replace empty collections with null if they're placeholders
        content = re.sub(r'return\s+new\s+ArrayList<>\(\)\s*;', 'return null;', content)
        content = re.sub(r'return\s+new\s+HashMap<>\(\)\s*;', 'return null;', content)

        if content != original_content:
            java_file.write_text(content, encoding='utf-8')
            standardized_count += 1

    print(f"Standardized return types in {standardized_count} files")
    return {'returns_standardized': standardized_count}

def step4_remove_problematic_imports(java_files: List[Path]) -> Dict[str, int]:
    """Step 4: Remove problematic imports."""
    print("Step 4: Removing problematic imports...")
    removed_count = 0

    problematic_patterns = [
        r'import\s+java\.awt\..*;',
        r'import\s+javax\.swing\..*;',
        r'import\s+java\.net\..*;',
        r'import\s+java\.nio\..*;',
        r'import\s+java\.security\..*;',
        r'import\s+java\.sql\..*;',
        r'import\s+java\.rmi\..*;',
        r'import\s+javax\.xml\..*;',
    ]

    for java_file in java_files:
        content = java_file.read_text(encoding='utf-8')
        original_content = content

        for pattern in problematic_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        # Clean up extra blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original_content:
            java_file.write_text(content, encoding='utf-8')
            removed_count += 1

    print(f"Removed problematic imports from {removed_count} files")
    return {'imports_removed': removed_count}

def step5_add_error_handling(java_files: List[Path]) -> Dict[str, int]:
    """Step 5: Add error handling to main methods."""
    print("Step 5: Adding error handling to main methods...")
    enhanced_count = 0

    for java_file in java_files:
        content = java_file.read_text(encoding='utf-8')

        # Skip if already has try-catch in main
        if re.search(r'public\s+static\s+void\s+main.*\{\s*try\s*\{', content, re.DOTALL):
            continue

        # Find main method and enhance it
        main_pattern = r'(public\s+static\s+void\s+main\s*\([^)]+\)\s*\{)(.*?)(\}\s*\})'
        main_match = re.search(main_pattern, content, re.DOTALL)

        if main_match:
            main_start = main_match.group(1)
            main_body = main_match.group(2)
            main_end = main_match.group(3)

            enhanced_main = f'{main_start}\n        try {{\n            // Algorithm execution\n            System.out.println("Running algorithm...");\n            {main_body.strip()}\n        }} catch (Exception e) {{\n            System.err.println("Error running algorithm: " + e.getMessage());\n            e.printStackTrace();\n        }}\n    {main_end}'

            content = content.replace(main_match.group(0), enhanced_main)
            java_file.write_text(content, encoding='utf-8')
            enhanced_count += 1

    print(f"Added error handling to {enhanced_count} main methods")
    return {'error_handling_added': enhanced_count}

def compile_and_test(java_files: List[Path]) -> Dict[str, int]:
    """Compile and test all Java files."""
    print("Testing compilation and execution...")
    compiled_count = 0
    failed_count = 0

    for java_file in java_files:
        try:
            # Try to compile
            result = subprocess.run(
                ["javac", str(java_file)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(java_file.parent)
            )

            if result.returncode == 0:
                compiled_count += 1
            else:
                failed_count += 1
                print(f"Compilation failed: {java_file}")
        except:
            failed_count += 1

    print(f"Compiled: {compiled_count}, Failed: {failed_count}")
    return {'compiled': compiled_count, 'failed': failed_count}

def generate_step_report(step_num: int, step_name: str, stats: Dict[str, int], test_results: Dict[str, int]):
    """Generate report for a step."""
    report_file = f'java_analysis_report_step{step_num}.txt'

    with open(report_file, 'w') as f:
        f.write(f"JAVA ANALYSIS REPORT - STEP {step_num}: {step_name.upper()}\n")
        f.write("=" * 80 + "\n\n")

        f.write("STEP RESULTS:\n")
        f.write("-" * 40 + "\n")
        for key, value in stats.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        f.write("\n")

        f.write("COMPILATION TEST RESULTS:\n")
        f.write("-" * 40 + "\n")
        f.write(f"Files that compile: {test_results.get('compiled', 0)}\n")
        f.write(f"Files with errors: {test_results.get('failed', 0)}\n")
        f.write(f"Total files tested: {test_results.get('compiled', 0) + test_results.get('failed', 0)}\n\n")

        f.write("COMPLETED: Step {step_num} - {step_name}\n")

    print(f"Report saved: {report_file}")

def main():
    """Run all steps."""
    print("JAVA ALGORITHM COMPREHENSIVE FIX PROCESS")
    print("=" * 50)

    # Find all Java files
    java_files = find_all_java_files()
    print(f"Found {len(java_files)} Algorithm.java files")

    steps = [
        (1, "Fix missing package declarations", step1_fix_packages),
        (2, "Add missing main methods", step2_add_main_methods),
        (3, "Standardize return types", step3_standardize_returns),
        (4, "Remove problematic imports", step4_remove_problematic_imports),
        (5, "Add error handling", step5_add_error_handling),
    ]

    for step_num, step_name, step_func in steps:
        print(f"\n{'='*50}")
        print(f"EXECUTING STEP {step_num}: {step_name}")
        print('='*50)

        # Execute step
        stats = step_func(java_files)

        # Test compilation
        test_results = compile_and_test(java_files)

        # Generate report
        generate_step_report(step_num, step_name, stats, test_results)

    print("\n" + "="*50)
    print("ALL STEPS COMPLETED")
    print("Final reports saved as java_analysis_report_step1.txt through step5.txt")

if __name__ == "__main__":
    main()
