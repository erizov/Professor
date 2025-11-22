#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix for failing Java files.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_java_file_comprehensive(java_file: Path) -> bool:
    """Comprehensively fix Java file issues."""
    try:
        content = java_file.read_text(encoding='utf-8')
        original_content = content
        
        # Fix 1: Move methods that are outside class into class
        # Check if there are methods before "public class"
        class_match = re.search(r'public\s+class\s+\w+', content)
        if class_match:
            class_start = class_match.start()
            before_class = content[:class_start]
            after_class = content[class_start:]
            
            # Find methods before class
            method_pattern = r'^\s*public\s+(static\s+)?\w+\s+\w+\s*\([^)]*\)\s*\{'
            methods_before = []
            lines_before = before_class.split('\n')
            method_start_idx = None
            
            for i, line in enumerate(lines_before):
                if re.match(method_pattern, line.strip()):
                    method_start_idx = i
                    break
            
            if method_start_idx is not None:
                # Extract method(s) before class
                method_lines = []
                brace_count = 0
                for i in range(method_start_idx, len(lines_before)):
                    line = lines_before[i]
                    method_lines.append(line)
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0 and i > method_start_idx:
                        break
                
                # Remove methods from before_class
                before_class = '\n'.join(lines_before[:method_start_idx])
                
                # Insert methods after class opening brace
                class_brace_match = re.search(r'\{', after_class)
                if class_brace_match:
                    insert_pos = class_brace_match.end()
                    methods_text = '\n'.join(method_lines)
                    after_class = after_class[:insert_pos] + '\n' + methods_text + after_class[insert_pos:]
                
                content = before_class + after_class
        
        # Fix 2: Fix string concatenation issues
        # Fix unclosed string literals
        lines = content.split('\n')
        fixed_lines = []
        for line in lines:
            # Fix lines with unclosed strings
            if '"' in line and not line.strip().endswith('";') and not line.strip().endswith('"') and '+' in line:
                # Count quotes
                quote_count = line.count('"')
                if quote_count % 2 != 0:
                    # Try to close it
                    if not line.rstrip().endswith('"'):
                        line = line.rstrip() + '"'
            fixed_lines.append(line)
        content = '\n'.join(fixed_lines)
        
        # Fix 3: Replace Python-style syntax
        # Replace str() with String.valueOf()
        content = re.sub(r'\bstr\s*\(', 'String.valueOf(', content)
        # Replace dict with Map
        content = re.sub(r'\bdict\s+(\w+)', r'Map<String, Object> \1', content)
        # Replace tuple with appropriate Java type
        content = re.sub(r'\btuple\s+(\w+)', r'String \1', content)
        
        # Fix 4: Fix .repeat() - Java doesn't have this, use loop or manual repeat
        def replace_repeat(match):
            count = match.group(1)
            char = match.group(2) if match.group(2) else '"'
            if char == '"':
                return f'String.join("", Collections.nCopies({count}, "="))'
            else:
                return f'String.join("", Collections.nCopies({count}, "{char}"))'
        
        content = re.sub(r'"([^"]+)"\.repeat\((\d+)\)', replace_repeat, content)
        content = re.sub(r"'([^']+)'\.repeat\((\d+)\)", replace_repeat, content)
        
        # Add Collections import if using nCopies
        if 'Collections.nCopies' in content and 'import java.util.Collections;' not in content:
            if 'import java.util.*;' not in content:
                import_match = re.search(r'(package\s+[^;]+;|^)', content, re.MULTILINE)
                if import_match:
                    insert_pos = import_match.end()
                    content = content[:insert_pos] + '\nimport java.util.Collections;\n' + content[insert_pos:]
        
        # Fix 5: Fix method name mismatches in main
        # Find method definitions
        method_defs = re.findall(r'public\s+(static\s+)?\w+\s+(\w+)\s*\(', content)
        method_names = {name for _, name in method_defs}
        
        # Fix calls in main that don't match
        main_match = re.search(r'public\s+static\s+void\s+main[^{]*\{([^}]+)\}', content, re.DOTALL)
        if main_match:
            main_body = main_match.group(1)
            for method_name in method_names:
                # Fix snake_case to camelCase mismatches
                camel_case = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), method_name)
                if camel_case != method_name and camel_case in method_names:
                    main_body = main_body.replace(f'{method_name}()', f'{camel_case}()')
            
            # Replace main body
            content = content[:main_match.start(1)] + main_body + content[main_match.end(1):]
        
        # Fix 6: Fix .get() on non-Map objects
        # If using .get() on something that's not a Map, it might be a method call issue
        # This is complex, so we'll handle common cases
        
        # Fix 7: Ensure proper class structure
        if 'public class Algorithm' not in content:
            # Wrap everything in a class
            if not re.search(r'^\s*public\s+class\s+\w+', content, re.MULTILINE):
                # Find first method
                first_method = re.search(r'^\s*public\s+(static\s+)?\w+\s+\w+\s*\(', content, re.MULTILINE)
                if first_method:
                    class_decl = "public class Algorithm {\n"
                    if "import" not in content[:500]:
                        imports = "import java.util.*;\nimport java.util.logging.Logger;\n\n"
                        class_decl = imports + class_decl
                    content = content[:first_method.start()] + class_decl + content[first_method.start():]
                    if not content.rstrip().endswith('}'):
                        content = content.rstrip() + "\n}\n"
        
        # Only write if changed
        if content != original_content:
            java_file.write_text(content, encoding='utf-8')
            return True
        
        return False
        
    except Exception as e:
        print(f"  [ERROR] Failed to fix {java_file}: {e}")
        return False


# Get list of failing files and fix them
def main():
    """Main function."""
    failing_files = [
        "semester_12/lecture_79_quantum_algorithms_advanced/quantum_cryptography",
        "semester_12/lecture_79_quantum_algorithms_advanced/quantum_teleportation",
        "semester_12/lecture_86_quantum_security/post_quantum_cryptography",
        "semester_12/lecture_86_quantum_security/quantum_defense",
        "semester_13/lecture_88_consensus_advanced/dpos_advanced",
        "semester_13/lecture_91_blockchain_privacy/privacy_coins",
        "semester_14/lecture_100_documentation_ai/ai_doc_generation",
        "semester_14/lecture_100_documentation_ai/code_to_docs",
        "semester_14/lecture_101_developer_experience/tutorial_systems",
        "semester_14/lecture_95_support_advanced/knowledge_graph",
        "semester_14/lecture_97_knowledge_management/knowledge_graph_construction",
        "semester_14/lecture_98_documentation_advanced/automated_documentation",
        "semester_14/lecture_99_technical_writing_advanced/accessibility_docs",
        "semester_15/lecture_104_database_performance/index_strategies",
        "semester_15/lecture_104_database_performance/statistics_management",
        "semester_15/lecture_108_graph_databases_advanced/graph_algorithms_db",
        "semester_15/lecture_108_graph_databases_advanced/graph_analytics",
        "semester_15/lecture_108_graph_databases_advanced/graph_ml",
        "semester_15/lecture_108_graph_databases_advanced/graph_pattern_matching",
        "semester_15/lecture_108_graph_databases_advanced/graph_traversal",
        "semester_15/lecture_108_graph_databases_advanced/graph_visualization",
        "semester_16/lecture_113_data_lakes_advanced/data_quality",
        "semester_16/lecture_115_data_governance_advanced/gdpr_compliance",
    ]
    
    print("=" * 70)
    print("COMPREHENSIVE JAVA FILE FIXES")
    print("=" * 70)
    print()
    
    fixed_count = 0
    
    for algorithm_path in failing_files:
        java_file = ROOT / algorithm_path.replace('/', '\\') / "Algorithm.java"
        
        if not java_file.exists():
            print(f"[SKIP] {algorithm_path} - File not found")
            continue
        
        print(f"Fixing: {algorithm_path}")
        if fix_java_file_comprehensive(java_file):
            print(f"  [FIXED]")
            fixed_count += 1
        else:
            print(f"  [SKIP] No changes needed or error occurred")
        print()
    
    print(f"Fixed {fixed_count} files")


if __name__ == "__main__":
    main()

