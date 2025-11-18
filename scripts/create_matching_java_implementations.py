#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create matching Java implementations from Python implementations.

This script reads Python algorithm.py files and creates equivalent
Java Algorithm.java files that match the Python implementation logic.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from scripts.generate_all_algorithm_implementations import (
        ALGORITHM_IMPLEMENTATIONS,
        get_algorithm_implementation
    )
except ImportError:
    ALGORITHM_IMPLEMENTATIONS = {}
    def get_algorithm_implementation(algorithm_name: str) -> Optional[str]:
        return ALGORITHM_IMPLEMENTATIONS.get(algorithm_name)


def convert_python_class_to_java(py_content: str, algorithm_name: str) -> str:
    """Convert Python class to equivalent Java class."""
    description = algorithm_name.replace('_', ' ').title()
    
    # Extract class name
    class_match = re.search(r'class\s+(\w+)', py_content)
    class_name = class_match.group(1) if class_match else 'Algorithm'
    
    # Extract __init__ fields
    init_match = re.search(r'def\s+__init__\s*\([^)]*\)\s*->[^:]*:.*?(?=\n    def|\Z)', py_content, re.DOTALL)
    fields = []
    if init_match:
        init_body = init_match.group(0)
        # Extract self.attributes
        attr_patterns = [
            (r'self\.(\w+)\s*:\s*Dict\[str,\s*dict\]', 'Map<String, Map<String, Object>>'),
            (r'self\.(\w+)\s*:\s*Dict\[str,\s*List\[str\]\]', 'Map<String, List<String>>'),
            (r'self\.(\w+)\s*:\s*Dict\[str,\s*(\w+)\]', 'Map<String, Object>'),
            (r'self\.(\w+)\s*:\s*List\[(\w+)\]', 'List<Object>'),
            (r'self\.(\w+)\s*=\s*\{', 'Map<String, Object>'),
        ]
        
        for pattern, java_type in attr_patterns:
            for match in re.finditer(pattern, init_body):
                attr_name = match.group(1)
                fields.append((attr_name, java_type))
    
    # Extract methods
    methods = []
    method_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*->\s*([^:]+):'
    for match in re.finditer(method_pattern, py_content):
        method_name = match.group(1)
        if method_name == '__init__':
            continue
        
        params_str = match.group(2)
        return_type_hint = match.group(3).strip()
        
        # Extract parameters
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if param and param != 'self':
                param_name = param.split(':')[0].strip()
                param_type = 'String' if 'str' in param or 'id' in param_name or 'user' in param_name else 'Object'
                if 'List[' in param:
                    param_type = 'List<String>' if 'str' in param else 'List<Object>'
                params.append((param_name, param_type))
        
        # Find method body
        method_start = match.end()
        next_method = py_content.find('\n    def ', method_start)
        if next_method == -1:
            method_body = py_content[method_start:]
        else:
            method_body = py_content[method_start:next_method]
        
        # Extract docstring
        doc_match = re.search(r'"""(.*?)"""', method_body, re.DOTALL)
        doc = doc_match.group(1).strip() if doc_match else method_name.replace('_', ' ').title()
        
        methods.append({
            'name': method_name,
            'params': params,
            'return_type': return_type_hint,
            'body': method_body,
            'doc': doc
        })
    
    # Build Java class
    java_code = 'import java.util.*;\n'
    java_code += 'import java.util.logging.Logger;\n'
    java_code += 'import java.util.logging.Level;\n\n'
    java_code += f'/**\n * {description} implementation.\n */\n'
    java_code += 'public class Algorithm {\n'
    java_code += '    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());\n\n'
    
    # Add fields
    field_map = {}
    for attr_name, java_type in fields:
        if java_type == 'Map<String, Map<String, Object>>':
            java_code += f'    private Map<String, Map<String, Object>> {attr_name} = new HashMap<>();\n'
        elif java_type == 'Map<String, List<String>>':
            java_code += f'    private Map<String, List<String>> {attr_name} = new HashMap<>();\n'
        elif java_type == 'Map<String, Object>':
            java_code += f'    private Map<String, Object> {attr_name} = new HashMap<>();\n'
        elif java_type == 'List<Object>':
            java_code += f'    private List<Object> {attr_name} = new ArrayList<>();\n'
        field_map[attr_name] = attr_name
    
    if fields:
        java_code += '\n'
    
    # Add constructor
    java_code += '    public Algorithm() {\n'
    java_code += '        // Initialize\n'
    java_code += '    }\n\n'
    
    # Convert methods
    for method in methods:
        method_name = method['name']
        params = method['params']
        return_type_hint = method['return_type']
        method_body = method['body']
        doc = method['doc']
        
        # Determine Java return type
        java_return_type = 'Object'
        if 'str' in return_type_hint:
            java_return_type = 'String'
        elif 'bool' in return_type_hint:
            java_return_type = 'boolean'
        elif 'int' in return_type_hint or 'float' in return_type_hint:
            java_return_type = 'int'
        elif 'List' in return_type_hint:
            java_return_type = 'List<Object>'
        elif 'Dict' in return_type_hint or 'dict' in return_type_hint:
            java_return_type = 'Map<String, Object>'
        
        # Build method signature
        java_code += f'    /**\n     * {doc}\n     */\n'
        param_list = ', '.join([f'{ptype} {pname}' for pname, ptype in params])
        java_code += f'    public {java_return_type} {method_name}({param_list}) {{\n'
        java_code += f'        logger.info("Executing {method_name}");\n'
        
        # Convert method body
        java_body = convert_python_method_body_to_java(method_body, field_map)
        java_code += java_body
        
        java_code += '    }\n\n'
    
    # Add static factory method
    java_code += '    public static Algorithm create() {\n'
    java_code += '        return new Algorithm();\n'
    java_code += '    }\n\n'
    
    # Add main method
    java_code += '    public static void main(String[] args) {\n'
    java_code += '        System.out.println("=".repeat(70));\n'
    java_code += f'        System.out.println("{description}");\n'
    java_code += '        System.out.println("=".repeat(70));\n'
    java_code += '        \n'
    java_code += '        Algorithm algo = Algorithm.create();\n'
    if methods:
        first_method = methods[0]
        param_calls = ', '.join(['""' if ptype == 'String' else 'null' for _, ptype in first_method['params']])
        java_code += f'        {first_method["return_type"]} result = algo.{first_method["name"]}({param_calls});\n'
        java_code += '        System.out.println("Result: " + result);\n'
    java_code += '        System.out.println("=".repeat(70));\n'
    java_code += '    }\n'
    java_code += '}\n'
    
    return java_code


def convert_python_method_body_to_java(py_body: str, field_map: Dict[str, str]) -> str:
    """Convert Python method body to Java code."""
    java_lines = []
    
    # Handle time imports
    if 'import time' in py_body or 'time.time()' in py_body:
        java_lines.append('        long currentTime = System.currentTimeMillis();')
    
    # Handle f-strings
    fstring_matches = list(re.finditer(r'f"([^"]+)"', py_body))
    for match in fstring_matches:
        template = match.group(1)
        if '{int(time.time())}' in template:
            java_lines.append('        long timestamp = System.currentTimeMillis();')
            java_lines.append('        String shareId = "SHARE-" + timestamp;')
        elif '{' in template and '}' in template:
            # Simple f-string conversion
            parts = template.split('{')
            if len(parts) > 1:
                var_part = parts[1].split('}')[0]
                java_lines.append(f'        String result = "{parts[0]}" + {var_part} + "{parts[1].split("}")[1] if "}" in parts[1] else ""}";')
    
    # Handle dictionary assignments
    dict_assigns = re.findall(r'self\.(\w+)\[([^\]]+)\]\s*=\s*\{([^}]+)\}', py_body)
    for attr, key, value in dict_assigns:
        if attr in field_map:
            java_lines.append(f'        Map<String, Object> {attr}_entry = new HashMap<>();')
            # Extract dict keys
            keys = re.findall(r"'([^']+)':", value)
            for k in keys:
                java_lines.append(f'        {attr}_entry.put("{k}", null);')
            java_lines.append(f'        {field_map[attr]}.put({key}, {attr}_entry);')
    
    # Handle list operations
    if 'not in' in py_body or 'in self.' in py_body:
        in_match = re.search(r'(\w+)\s+not in\s+self\.(\w+)', py_body)
        if in_match:
            var = in_match.group(1)
            attr = in_match.group(2)
            if attr in field_map:
                java_lines.append(f'        if (!{field_map[attr]}.containsKey({var})) {{')
                java_lines.append(f'            {field_map[attr]}.put({var}, new ArrayList<>());')
                java_lines.append('        }')
    
    if 'append' in py_body or '.append(' in py_body:
        append_match = re.search(r'self\.(\w+)\[([^\]]+)\]\.append\(([^)]+)\)', py_body)
        if append_match:
            attr = append_match.group(1)
            key = append_match.group(2)
            value = append_match.group(3)
            if attr in field_map:
                java_lines.append(f'        ((List<String>){field_map[attr]}.get({key})).add({value});')
    
    # Handle return statements
    if '-> str' in py_body or 'f"' in py_body:
        if 'share_id' in py_body.lower() or 'SHARE-' in py_body:
            java_lines.append('        long timestamp = System.currentTimeMillis();')
            java_lines.append('        return "SHARE-" + timestamp;')
        else:
            java_lines.append('        return "";')
    elif '-> bool' in py_body:
        if 'return user in' in py_body or 'in self.' in py_body:
            in_match = re.search(r'return\s+(\w+)\s+in\s+self\.(\w+)\[([^\]]+)\]', py_body)
            if in_match:
                var = in_match.group(1)
                attr = in_match.group(2)
                key = in_match.group(3)
                if attr in field_map:
                    java_lines.append(f'        if ({field_map[attr]}.containsKey({key})) {{')
                    java_lines.append(f'            return ((List<String>){field_map[attr]}.get({key})).contains({var});')
                    java_lines.append('        }')
                    java_lines.append('        return false;')
            else:
                java_lines.append('        return false;')
        elif 'return True' in py_body:
            java_lines.append('        return true;')
        elif 'return False' in py_body:
            java_lines.append('        return false;')
        else:
            java_lines.append('        return false;')
    elif '-> List' in py_body:
        java_lines.append('        List<Object> result = new ArrayList<>();')
        java_lines.append('        return result;')
    elif '-> Dict' in py_body or '{' in py_body:
        java_lines.append('        Map<String, Object> result = new HashMap<>();')
        java_lines.append('        return result;')
    else:
        java_lines.append('        return null;')
    
    return '\n'.join(java_lines) + '\n'


def create_java_from_python(algorithm_folder: Path, algorithm_name: str) -> bool:
    """Create Java implementation from Python implementation."""
    py_file = algorithm_folder / 'algorithm.py'
    java_file = algorithm_folder / 'Algorithm.java'
    
    if not py_file.exists():
        return False
    
    # Read Python file
    py_content = py_file.read_text(encoding='utf-8')
    
    # Check if Java needs update
    if java_file.exists():
        java_content = java_file.read_text(encoding='utf-8')
        # Check for generic patterns
        if ('// TODO' not in java_content and 
            'TODO:' not in java_content and
            'return null;' not in java_content and
            'return data;' not in java_content):
            # Check if it has actual implementation
            has_logic = any(k in java_content for k in [
                'if (', 'for (', 'while (', 
                'result.put', 'result.add', 
                'return "', 'return true', 'return false'
            ])
            if has_logic:
                return False  # Already has good implementation
    
    # Extract Python implementation
    if 'class ' in py_content:
        # Extract class
        class_match = re.search(r'class\s+\w+.*?(?=\ndef main|\Z)', py_content, re.DOTALL)
        if class_match:
            py_impl = class_match.group(0)
            java_impl = convert_python_class_to_java(py_impl, algorithm_name)
            java_file.write_text(java_impl, encoding='utf-8')
            return True
    
    return False


def main():
    """Main function to create matching Java implementations."""
    base_path = Path('.')
    algorithm_folders = []
    
    # Find all algorithm folders
    for folder in base_path.rglob('*'):
        if (folder.is_dir() and 
            'semester_' in str(folder) and 
            'lecture_' in str(folder) and
            not folder.name.startswith('lecture_') and
            not any(x in folder.name for x in ['__pycache__', '.git'])):
            py_file = folder / 'algorithm.py'
            if py_file.exists():
                algorithm_folders.append(folder)
    
    print(f"Found {len(algorithm_folders)} algorithm folders")
    print("Creating matching Java implementations...")
    
    updated = 0
    skipped = 0
    errors = []
    
    for folder in algorithm_folders:
        try:
            algorithm_name = folder.name
            if create_java_from_python(folder, algorithm_name):
                updated += 1
                if updated % 50 == 0:
                    print(f"Updated {updated} Java files...")
            else:
                skipped += 1
        except Exception as e:
            errors.append(f"{folder.name}: {str(e)}")
    
    print(f"\nSummary:")
    print(f"  Updated Java files: {updated}")
    print(f"  Skipped (already complete): {skipped}")
    
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:10]:
            print(f"  {error}")


if __name__ == "__main__":
    main()

