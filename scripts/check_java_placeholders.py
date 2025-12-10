#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Java files for placeholder implementations.
Identifies Java files that are just shells without actual algorithm logic.
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def is_java_placeholder(java_file: Path) -> Tuple[bool, str]:
    """
    Check if a Java file is a placeholder.
    Returns (is_placeholder, reason)
    """
    if not java_file.exists():
        return True, "File does not exist"
    
    try:
        content = java_file.read_text(encoding='utf-8')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Too short = likely placeholder
        if len(lines) < 30:
            return True, f"Too short ({len(lines)} lines)"
        
        # Check for placeholder patterns
        placeholder_indicators = [
            (r'logger\.info\("Executing \w+"\);', "Only logging, no implementation"),
            (r'return null;', "Returns null without logic"),
            (r'return -1;', "Returns -1 without logic"),
            (r'return;', "Empty return"),
            (r'// Initialize\s*$', "Only comment, no initialization"),
            (r'// Placeholder', "Explicit placeholder comment"),
            (r'TODO.*Implement', "TODO comment"),
        ]
        
        # Count meaningful code (not just comments, logging, or returns)
        meaningful_lines = 0
        has_algorithm_logic = False
        
        for line in lines:
            # Skip comments
            if line.startswith('//') or line.startswith('/*') or line.startswith('*'):
                continue
            
            # Skip package/import
            if line.startswith('package ') or line.startswith('import '):
                continue
            
            # Skip class declaration
            if 'public class' in line or 'private static' in line:
                continue
            
            # Skip getters/setters
            if 'getLogger' in line or 'Logger.getLogger' in line:
                continue
            
            # Check for actual algorithm logic
            if any(keyword in line for keyword in [
                'if (', 'for (', 'while (', 'switch (',
                '=', '+=', '-=', '*=', '/=',
                'List<', 'Map<', 'Set<', 'Queue<',
                'new ', 'add(', 'put(', 'get(',
                'return ', 'throw '
            ]):
                meaningful_lines += 1
                # Check if it's not just logging
                if 'logger.' not in line and 'System.out.println' not in line:
                    has_algorithm_logic = True
        
        # If very few meaningful lines, it's a placeholder
        if meaningful_lines < 5:
            return True, f"Too few meaningful lines ({meaningful_lines})"
        
        # Check for specific placeholder patterns
        for pattern, reason in placeholder_indicators:
            if re.search(pattern, content):
                # But check if there's also real logic
                if not has_algorithm_logic:
                    return True, reason
        
        # Check if methods only log and return null/-1
        method_pattern = r'public\s+\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\}'
        methods = re.findall(method_pattern, content, re.DOTALL)
        
        placeholder_methods = 0
        for method in methods:
            # Check if method only has logging and return null/-1
            if 'logger.info' in method or 'logger.' in method:
                if 'return null' in method or 'return -1' in method or 'return;' in method:
                    if len(method.split('\n')) < 5:  # Very short method
                        placeholder_methods += 1
        
        # If all methods are placeholders
        if len(methods) > 0 and placeholder_methods == len(methods):
            return True, "All methods are placeholders (only logging and return null/-1)"
        
        # Check if there's a corresponding Python file with real implementation
        python_file = java_file.parent / "algorithm.py"
        if python_file.exists():
            python_content = python_file.read_text(encoding='utf-8')
            python_lines = len([l for l in python_content.split('\n') if l.strip()])
            
            # If Python file is much longer and has real logic, Java might be placeholder
            if python_lines > 50 and meaningful_lines < 10:
                return True, f"Python file has {python_lines} lines, Java only {meaningful_lines} meaningful lines"
        
        return False, "Has algorithm implementation"
    
    except Exception as e:
        return True, f"Error reading file: {e}"


def check_algorithm_folder(algorithm_folder: Path) -> Dict:
    """Check Java file in an algorithm folder."""
    java_file = algorithm_folder / "Algorithm.java"
    
    if not java_file.exists():
        return {
            'algorithm': algorithm_folder.name,
            'path': str(algorithm_folder.relative_to(ROOT)),
            'is_placeholder': True,
            'reason': "Algorithm.java does not exist"
        }
    
    is_placeholder, reason = is_java_placeholder(java_file)
    
    return {
        'algorithm': algorithm_folder.name,
        'path': str(algorithm_folder.relative_to(ROOT)),
        'is_placeholder': is_placeholder,
        'reason': reason,
        'file': str(java_file.relative_to(ROOT))
    }


def find_all_algorithm_folders() -> list:
    """Find all algorithm folders."""
    folders = []
    
    for folder in ROOT.glob("semester_*/lecture_*/*/"):
        if folder.is_dir() and not folder.name.startswith('.'):
            # Check if it looks like an algorithm folder
            if (folder / "metadata.json").exists() or (folder / "algorithm.py").exists():
                folders.append(folder)
    
    return sorted(folders)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("CHECKING JAVA PLACEHOLDERS")
    print("="*70)
    
    algorithm_folders = find_all_algorithm_folders()
    print(f"\nFound {len(algorithm_folders)} algorithm folders")
    print("\nChecking Java files...")
    
    placeholders = []
    checked = 0
    
    for i, folder in enumerate(algorithm_folders, 1):
        result = check_algorithm_folder(folder)
        if result['is_placeholder']:
            placeholders.append(result)
        checked += 1
        
        if i % 100 == 0:
            print(f"Progress: {i}/{len(algorithm_folders)} ({i/len(algorithm_folders)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"Checked: {checked} algorithm folders")
    print(f"Placeholders found: {len(placeholders)}")
    print(f"{'='*70}")
    
    if placeholders:
        print("\nJava Placeholder Files:")
        print("-" * 70)
        for item in placeholders[:50]:  # Show first 50
            print(f"Algorithm: {item['algorithm']}")
            print(f"  Path: {item['path']}")
            if 'file' in item:
                print(f"  File: {item['file']}")
            print(f"  Reason: {item['reason']}")
            print()
        
        if len(placeholders) > 50:
            print(f"... and {len(placeholders) - 50} more placeholders")
        
        # Save to file
        report_path = ROOT / "java_placeholders_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Java Placeholder Files Report\n")
            f.write("=" * 70 + "\n\n")
            for item in placeholders:
                f.write(f"Algorithm: {item['algorithm']}\n")
                f.write(f"  Path: {item['path']}\n")
                if 'file' in item:
                    f.write(f"  File: {item['file']}\n")
                f.write(f"  Reason: {item['reason']}\n\n")
        
        print(f"\nFull report saved to: {report_path}")
        return 1
    
    print("\n✓ No Java placeholder files found!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

