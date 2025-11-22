#!/usr/bin/env python3
"""
Quick check of Java Algorithm files.
"""

import os
import re
from pathlib import Path

def find_java_files():
    """Find all Algorithm.java files."""
    java_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'target', '.vscode', '.idea', 'node_modules'}]
        if 'Algorithm.java' in files:
            java_files.append(Path(root) / 'Algorithm.java')
    return sorted(java_files)

def analyze_file(java_file):
    """Quick analysis of a Java file."""
    try:
        content = java_file.read_text(encoding='utf-8')
    except:
        return f"ERROR: Cannot read {java_file}"

    # Extract basic info
    package_match = re.search(r'^\s*package\s+([^;]+);', content, re.MULTILINE)
    package = package_match.group(1).strip() if package_match else "MISSING"

    class_match = re.search(r'^\s*public\s+class\s+(\w+)', content, re.MULTILINE)
    class_name = class_match.group(1) if class_match else "MISSING"

    has_main = 'public static void main' in content

    return f"{java_file}|{package}|{class_name}|{has_main}"

def main():
    """Main function."""
    java_files = find_java_files()
    print(f"Found {len(java_files)} Java Algorithm files")

    with open('java_quick_analysis.txt', 'w') as f:
        f.write("File Path|Package|Class Name|Has Main Method\n")
        f.write("-" * 80 + "\n")

        for java_file in java_files:
            result = analyze_file(java_file)
            print(result)
            f.write(result + "\n")

    print("Results saved to java_quick_analysis.txt")

if __name__ == "__main__":
    main()
