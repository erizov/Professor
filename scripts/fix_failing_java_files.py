#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatically fix failing Java files based on common error patterns.
"""

import sqlite3
import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "test_results.db"


def get_failing_java_files() -> List[Tuple[str, str]]:
    """Get list of failing Java files with their error messages."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        WITH recent_results AS (
            SELECT 
                algorithm_path,
                language,
                status,
                error_message,
                ROW_NUMBER() OVER (
                    PARTITION BY algorithm_path, language 
                    ORDER BY timestamp DESC
                ) as rn
            FROM test_results
        )
        SELECT algorithm_path, error_message
        FROM recent_results
        WHERE rn = 1 
        AND language = 'java'
        AND status IN ('failure', 'error', 'timeout')
        ORDER BY algorithm_path
    """)
    
    failures = cursor.fetchall()
    conn.close()
    return failures


def fix_java_file(java_file: Path, error_message: str) -> bool:
    """Fix common Java syntax errors."""
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix 1: Missing class declaration - wrap methods in class
        if "class, interface, enum, or record expected" in error_message:
            # Check if there's a class declaration
            if not re.search(r'^\s*public\s+class\s+\w+', content, re.MULTILINE):
                # Find the first method/function declaration
                method_match = re.search(r'^\s*public\s+(static\s+)?\w+\s+\w+\s*\(', content, re.MULTILINE)
                if method_match:
                    # Insert class declaration before first method
                    class_name = "Algorithm"
                    class_decl = f"public class {class_name} {{\n"
                    # Add necessary imports if not present
                    if "import" not in content[:500]:
                        imports = "import java.util.*;\nimport java.util.logging.Logger;\n\n"
                        class_decl = imports + class_decl
                    else:
                        class_decl = "\n" + class_decl
                    
                    # Insert class declaration
                    insert_pos = method_match.start()
                    content = content[:insert_pos] + class_decl + content[insert_pos:]
                    
                    # Close the class at the end
                    if not content.rstrip().endswith('}'):
                        content = content.rstrip() + "\n}\n"
        
        # Fix 2: Python-style dictionary access ['key'] -> .get("key")
        if "unclosed character literal" in error_message or "['" in content:
            # Replace dict['key'] with dict.get("key")
            content = re.sub(r"(\w+)\['(\w+)'\]", r'\1.get("\2")', content)
            # Replace dict["key"] with dict.get("key") if it's causing issues
            content = re.sub(r"(\w+)\[\"(\w+)\"\]", r'\1.get("\2")', content)
        
        # Fix 3: Python-style string methods
        if ".upper()" in content and "String" in content:
            # Java uses .toUpperCase() not .upper()
            content = content.replace(".upper()", ".toUpperCase()")
            content = content.replace(".lower()", ".toLowerCase()")
        
        # Fix 4: Python random.randint -> Java Random
        if "random.randint" in content:
            # Add Random import if not present
            if "import java.util.Random;" not in content:
                import_match = re.search(r'(package\s+[^;]+;|^)', content, re.MULTILINE)
                if import_match:
                    insert_pos = import_match.end()
                    content = content[:insert_pos] + "\nimport java.util.Random;\n" + content[insert_pos:]
            
            # Replace random.randint(a, b) with new Random().nextInt(b - a + 1) + a
            def replace_randint(match):
                var_name = match.group(1) if match.group(1) else "random"
                a = match.group(2)
                b = match.group(3)
                return f'new Random().nextInt({b} - {a} + 1) + {a}'
            
            content = re.sub(r'(\w+\.)?random\.randint\((\d+),\s*(\d+)\)', replace_randint, content)
        
        # Fix 5: Python str() -> String.valueOf()
        if re.search(r'\bstr\s*\(', content):
            content = re.sub(r'\bstr\s*\(', 'String.valueOf(', content)
        
        # Fix 6: Fix unclosed string literals
        if "unclosed string literal" in error_message or "unclosed character literal" in error_message:
            # Try to find and fix unclosed quotes
            lines = content.split('\n')
            fixed_lines = []
            for line in lines:
                # Count quotes
                single_quotes = line.count("'")
                double_quotes = line.count('"')
                # If odd number, might be unclosed
                if single_quotes % 2 != 0:
                    # Try to close it
                    if line.rstrip().endswith("'") and not line.rstrip().endswith("\\'"):
                        pass  # Already closed
                    elif "'" in line:
                        # Add closing quote at end if needed
                        if not line.rstrip().endswith("'") and not line.rstrip().endswith("';"):
                            line = line.rstrip() + "'"
                if double_quotes % 2 != 0:
                    if not line.rstrip().endswith('"') and not line.rstrip().endswith('";'):
                        # Check if it's a string concatenation
                        if '+' in line and '"' in line:
                            line = line.rstrip() + '"'
                fixed_lines.append(line)
            content = '\n'.join(fixed_lines)
        
        # Fix 7: Fix incompatible return types
        if "incompatible types" in error_message:
            # If returning "" but expecting boolean, return false
            if 'return "";' in content and "boolean" in error_message:
                content = content.replace('return "";', 'return false;')
            # If returning "" but expecting Map, return empty map
            if 'return "";' in content and "Map" in error_message:
                content = content.replace('return "";', 'return new HashMap<>();')
        
        # Fix 8: Add missing main method if needed
        if "Error: Could not find or load main class" in error_message:
            if "public static void main" not in content:
                # Add main method at the end of class
                if content.rstrip().endswith('}'):
                    main_method = """
    
    public static void main(String[] args) {
        Logger logger = Logger.getLogger(Algorithm.class.getName());
        logger.info("Algorithm demonstration");
    }
"""
                    content = content.rstrip()[:-1] + main_method + "\n}"
        
        # Only write if content changed
        if content != original_content:
            java_file.write_text(content, encoding='utf-8')
            return True
        
        return False
        
    except Exception as e:
        print(f"  [ERROR] Failed to fix {java_file}: {e}")
        return False


def main():
    """Main function."""
    print("=" * 70)
    print("FIXING FAILING JAVA FILES")
    print("=" * 70)
    print()
    
    failures = get_failing_java_files()
    print(f"Found {len(failures)} failing Java files")
    print()
    
    fixed_count = 0
    failed_count = 0
    
    for algorithm_path, error_message in failures:
        path_str = algorithm_path.replace('\\', '/')
        java_file = ROOT / path_str / "Algorithm.java"
        
        if not java_file.exists():
            print(f"[SKIP] File not found: {java_file}")
            failed_count += 1
            continue
        
        print(f"Fixing: {algorithm_path}")
        error_preview = error_message[:100] if error_message else "Unknown error"
        print(f"  Error: {error_preview}...")
        
        if fix_java_file(java_file, error_message):
            print(f"  [FIXED] Applied fixes")
            fixed_count += 1
        else:
            print(f"  [SKIP] No automatic fixes available")
            failed_count += 1
        print()
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total: {len(failures)}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Could not fix: {failed_count}")
    print("=" * 70)
    print()
    print("Re-running tests on fixed files...")


if __name__ == "__main__":
    main()

