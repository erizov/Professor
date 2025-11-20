#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test import fixing on a specific file."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.fix_test_imports import find_test_file, find_algorithm_file, fix_test_imports

algo_path = 'semester_01\\lecture_05_trees\\avl_tree'
test_file = find_test_file(algo_path)
algo_file = find_algorithm_file(algo_path)

print(f'Test file: {test_file}')
print(f'Algo file: {algo_file}')

if test_file and algo_file:
    # Check current import
    content = open(test_file, 'r', encoding='utf-8').read()
    algo_rel_path = algo_file.relative_to(ROOT)
    algo_module = str(algo_rel_path.with_suffix('')).replace('\\', '.').replace('/', '.')
    print(f'Module: {algo_module}')
    
    pattern = rf'from\s+{re.escape(algo_module)}\s+import\s+([^\n]+)'
    match = re.search(pattern, content)
    print(f'Match found: {match is not None}')
    if match:
        print(f'Matched: {match.group(0)}')
        print(f'Imported: {match.group(1)}')
    
    result = fix_test_imports(test_file, algo_file)
    print(f'Fixed: {result}')
    
    # Check after fix
    if result:
        content_after = open(test_file, 'r', encoding='utf-8').read()
        match_after = re.search(pattern, content_after)
        if match_after:
            print(f'After fix - Imported: {match_after.group(1)}')

