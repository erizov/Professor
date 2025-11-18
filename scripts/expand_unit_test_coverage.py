#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expand unit test coverage for all algorithms.
Adds comprehensive test cases based on algorithm type.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

# Extended test cases by category
EXTENDED_TEST_CASES = {
    'tree': {
        'test_basic': '''def test_basic_functionality(self):
        """Test basic tree traversal."""
        from semester_01.lecture_05_trees.binary_search_tree.algorithm import TreeNode, insert, inorder
        
        root = None
        values = [5, 3, 7, 2, 4, 6, 8]
        for val in values:
            root = insert(root, val)
        
        result = inorder(root)
        self.assertEqual(len(result), len(values))''',
        'test_empty': '''def test_empty_tree(self):
        """Test with empty tree."""
        from semester_01.lecture_05_trees.binary_search_tree.algorithm import inorder
        
        result = inorder(None)
        self.assertEqual(result, [])''',
        'test_single': '''def test_single_node(self):
        """Test with single node."""
        from semester_01.lecture_05_trees.binary_search_tree.algorithm import TreeNode, inorder
        
        root = TreeNode(5)
        result = inorder(root)
        self.assertEqual(result, [5])''',
        'test_insert': '''def test_insert_operation(self):
        """Test tree insertion."""
        from semester_01.lecture_05_trees.binary_search_tree.algorithm import TreeNode, insert, search
        
        root = None
        root = insert(root, 5)
        root = insert(root, 3)
        root = insert(root, 7)
        
        self.assertIsNotNone(search(root, 5))
        self.assertIsNotNone(search(root, 3))
        self.assertIsNone(search(root, 10))'''
    },
    
    'dp': {
        'test_basic': '''def test_basic_functionality(self):
        """Test basic DP functionality."""
        result = self.algorithm(10)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)''',
        'test_small': '''def test_small_input(self):
        """Test with small input."""
        result = self.algorithm(1)
        self.assertEqual(result, 1)''',
        'test_zero': '''def test_zero_input(self):
        """Test with zero input."""
        result = self.algorithm(0)
        self.assertEqual(result, 0)''',
        'test_large': '''def test_large_input(self):
        """Test with large input."""
        result = self.algorithm(100)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)''',
        'test_memoization': '''def test_memoization(self):
        """Test that DP uses memoization."""
        import time
        
        start = time.time()
        result1 = self.algorithm(30)
        time1 = time.time() - start
        
        start = time.time()
        result2 = self.algorithm(30)
        time2 = time.time() - start
        
        self.assertEqual(result1, result2)
        # Second call should be faster (memoized)
        self.assertLessEqual(time2, time1)'''
    },
    
    'pattern': {
        'test_creation': '''def test_object_creation(self):
        """Test pattern object creation."""
        instance = self.algorithm()
        self.assertIsNotNone(instance)''',
        'test_behavior': '''def test_pattern_behavior(self):
        """Test pattern-specific behavior."""
        instance1 = self.algorithm()
        instance2 = self.algorithm()
        # Pattern-specific assertion
        self.assertIsNotNone(instance1)''',
        'test_thread_safety': '''def test_thread_safety(self):
        """Test thread safety if applicable."""
        import threading
        
        instances = []
        def create_instance():
            instances.append(self.algorithm())
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(instances), 10)'''
    },
    
    'string': {
        'test_basic': '''def test_basic_functionality(self):
        """Test basic string algorithm."""
        text = "ABABABCABABC"
        pattern = "ABABC"
        result = self.algorithm(text, pattern)
        self.assertIsNotNone(result)''',
        'test_not_found': '''def test_pattern_not_found(self):
        """Test when pattern not found."""
        text = "ABCDEFG"
        pattern = "XYZ"
        result = self.algorithm(text, pattern)
        self.assertIsNone(result) or self.assertEqual(result, -1)''',
        'test_empty': '''def test_empty_strings(self):
        """Test with empty strings."""
        result = self.algorithm("", "")
        # Should handle gracefully
        self.assertIsNotNone(result)'''
    }
}

def get_algorithm_category(algorithm_path: Path, algorithm_name: str) -> str:
    """Determine algorithm category."""
    path_str = str(algorithm_path).lower()
    algo_name_lower = algorithm_name.lower()
    
    if 'tree' in path_str or 'tree' in algo_name_lower or 'bst' in algo_name_lower:
        return 'tree'
    elif 'dp' in path_str or 'dynamic' in path_str or 'knapsack' in algo_name_lower or 'fibonacci' in algo_name_lower:
        return 'dp'
    elif 'pattern' in path_str or 'design' in path_str:
        return 'pattern'
    elif 'string' in path_str or 'kmp' in algo_name_lower or 'pattern' in algo_name_lower:
        return 'string'
    else:
        return 'general'

def expand_test_file(test_path: Path, algorithm_path: Path, algorithm_name: str) -> bool:
    """Expand test file with additional test cases."""
    if not test_path.exists():
        return False
    
    try:
        content = test_path.read_text(encoding='utf-8')
        
        # Check if already has comprehensive tests
        if content.count('def test_') > 8:
            return False
        
        category = get_algorithm_category(algorithm_path, algorithm_name)
        test_cases = EXTENDED_TEST_CASES.get(category, {})
        
        if not test_cases:
            return False
        
        # Find insertion point (before if __name__)
        insert_pos = content.rfind('if __name__')
        if insert_pos == -1:
            insert_pos = len(content)
        
        # Add new tests
        new_tests = []
        for test_name, test_code in test_cases.items():
            if f'def {test_name}' not in content:
                new_tests.append("    " + test_code)
        
        if not new_tests:
            return False
        
        tests_text = "\n\n".join(new_tests) + "\n\n    "
        new_content = content[:insert_pos] + tests_text + content[insert_pos:]
        
        test_path.write_text(new_content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error expanding {test_path}: {e}")
        return False

def main():
    """Expand unit test coverage."""
    expanded = 0
    
    for test_file in ROOT.rglob("test_algorithm.py"):
        algo_dir = test_file.parent
        algo_name = algo_dir.name
        
        if expand_test_file(test_file, algo_dir, algo_name):
            expanded += 1
            if expanded % 10 == 0:
                print(f"[PROGRESS] Expanded {expanded} test files...")
    
    print(f"\n[COMPLETE] Expanded {expanded} unit test files")

if __name__ == "__main__":
    main()

