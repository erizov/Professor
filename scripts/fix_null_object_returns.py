#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Java methods that return null instead of empty objects.

This script finds all methods that return Object, Map, List, etc.
and replace 'return null;' with appropriate empty object returns.
"""

import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def fix_null_returns_in_file(java_file: Path) -> bool:
    """Fix null returns in a Java file."""
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        lines = content.split('\n')
        modified = False
        
        # Pattern to match method signatures
        # Match: public Object method_name(...) { ... return null; ... }
        # We need to track method context
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if this is a method that returns Object, Map, or List
            method_match = re.search(
                r'public\s+(Object|Map<[^>]+>|List<[^>]+>)\s+(\w+)\s*\(',
                line
            )
            
            if method_match:
                return_type = method_match.group(1)
                method_name = method_match.group(2)
                
                # Find the method body (until closing brace)
                brace_count = 0
                method_start = i
                method_end = i
                in_method = False
                
                for j in range(i, len(lines)):
                    line_j = lines[j]
                    if '{' in line_j:
                        brace_count += line_j.count('{')
                        in_method = True
                    if '}' in line_j:
                        brace_count -= line_j.count('}')
                    if in_method and brace_count == 0:
                        method_end = j
                        break
                
                # Search for 'return null;' in this method
                for j in range(method_start, method_end + 1):
                    if 'return null;' in lines[j]:
                        # Determine appropriate replacement based on return type
                        indent = len(lines[j]) - len(lines[j].lstrip())
                        
                        if return_type == 'Object':
                            # Return new Object() for Object type
                            replacement = ' ' * indent + 'return new Object();  // FIXME: Changed from null to empty object'
                        elif return_type.startswith('Map<'):
                            # Return new HashMap<>() for Map types
                            replacement = ' ' * indent + 'return new java.util.HashMap<>();  // FIXME: Changed from null to empty map'
                        elif return_type.startswith('List<'):
                            # Return new ArrayList<>() for List types
                            replacement = ' ' * indent + 'return new java.util.ArrayList<>();  // FIXME: Changed from null to empty list'
                        else:
                            # Keep null for other types (shouldn't happen, but safe)
                            replacement = lines[j]
                        
                        lines[j] = replacement
                        modified = True
                
                i = method_end + 1
            else:
                i += 1
        
        if modified:
            content = '\n'.join(lines)
            java_file.write_text(content, encoding='utf-8')
            return True
        
        return False
        
    except Exception as e:
        print(f"  ⚠ Error fixing {java_file}: {e}")
        return False


def get_all_java_files() -> List[Path]:
    """Get all Algorithm.java files."""
    java_files = []
    for java_file in ROOT.glob("**/Algorithm.java"):
        # Skip sandbox files
        if "sandboxes" in str(java_file):
            continue
        java_files.append(java_file)
    return sorted(java_files)


def main():
    """Main function."""
    print("=" * 70)
    print("FIXING NULL RETURNS IN JAVA FILES")
    print("=" * 70)
    print()
    
    java_files = get_all_java_files()
    print(f"Found {len(java_files)} Java files")
    print()
    
    fixed_count = 0
    for java_file in java_files:
        relative_path = java_file.relative_to(ROOT)
        print(f"Checking: {relative_path}")
        
        if fix_null_returns_in_file(java_file):
            print(f"  ✓ Fixed null returns")
            fixed_count += 1
        else:
            print(f"  - No changes needed")
    
    print()
    print("=" * 70)
    print(f"Fixed {fixed_count} files")
    print("=" * 70)


if __name__ == "__main__":
    main()

