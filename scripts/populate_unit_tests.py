#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Populate unit tests with specific test cases based on algorithm type.
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Test cases by algorithm category
TEST_CASES = {
    "sorting": {
        "test_basic": '''def test_basic_functionality(self):
        """Test basic sorting functionality."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = self.algorithm(arr.copy())
        self.assert_sorted(result, arr)''',
        "test_empty": '''def test_empty_input(self):
        """Test with empty input."""
        result = self.algorithm([])
        self.assertEqual(result, [])''',
        "test_single": '''def test_single_element(self):
        """Test with single element."""
        result = self.algorithm([1])
        self.assertEqual(result, [1])''',
        "test_sorted": '''def test_already_sorted(self):
        """Test with already sorted input."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr.copy())
        self.assertEqual(result, arr)''',
        "test_reverse": '''def test_reverse_sorted(self):
        """Test with reverse sorted input."""
        arr = [5, 4, 3, 2, 1]
        result = self.algorithm(arr.copy())
        self.assertEqual(result, [1, 2, 3, 4, 5])''',
        "test_duplicates": '''def test_duplicates(self):
        """Test with duplicate elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = self.algorithm(arr.copy())
        self.assert_sorted(result, arr)''',
        "test_negative": '''def test_negative_numbers(self):
        """Test with negative numbers."""
        arr = [-5, -2, -8, -1, -9]
        result = self.algorithm(arr.copy())
        self.assertEqual(result, [-9, -8, -5, -2, -1])''',
        "test_performance": '''def test_performance(self):
        """Test algorithm performance."""
        import random
        arr = [random.randint(0, 1000) for _ in range(1000)]
        self.assert_performance(lambda: self.algorithm(arr.copy()), max_time_seconds=1.0)''',
    },
    "searching": {
        "test_basic": '''def test_basic_functionality(self):
        """Test basic search functionality."""
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = self.algorithm(arr, 5)
        self.assert_search_result(result, 5, arr, found=True)''',
        "test_not_found": '''def test_not_found(self):
        """Test when target not found."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 6)
        self.assert_search_result(result, 6, arr, found=False)''',
        "test_first": '''def test_first_element(self):
        """Test searching for first element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 1)
        self.assert_search_result(result, 1, arr, found=True)''',
        "test_last": '''def test_last_element(self):
        """Test searching for last element."""
        arr = [1, 2, 3, 4, 5]
        result = self.algorithm(arr, 5)
        self.assert_search_result(result, 5, arr, found=True)''',
        "test_empty": '''def test_empty_array(self):
        """Test with empty array."""
        result = self.algorithm([], 5)
        self.assert_search_result(result, 5, [], found=False)''',
        "test_single": '''def test_single_element(self):
        """Test with single element."""
        arr = [5]
        result = self.algorithm(arr, 5)
        self.assert_search_result(result, 5, arr, found=True)''',
        "test_duplicates": '''def test_duplicates(self):
        """Test with duplicate elements."""
        arr = [1, 2, 2, 3, 3, 3, 4, 5]
        result = self.algorithm(arr, 3)
        self.assert_search_result(result, 3, arr, found=True)''',
    },
    "graph": {
        "test_basic": '''def test_basic_functionality(self):
        """Test basic graph traversal."""
        graph = {
            0: [1, 2],
            1: [3, 4],
            2: [5],
            3: [],
            4: [],
            5: []
        }
        result = self.algorithm(graph, 0)
        self.assertIsInstance(result, list)
        self.assertIn(0, result)''',
        "test_empty": '''def test_empty_graph(self):
        """Test with empty graph."""
        result = self.algorithm({}, 0)
        self.assertEqual(result, [0] if hasattr(self.algorithm, '__name__') and 'dfs' in self.algorithm.__name__.lower() else [])''',
        "test_single": '''def test_single_node(self):
        """Test with single node."""
        graph = {0: []}
        result = self.algorithm(graph, 0)
        self.assertIn(0, result)''',
        "test_disconnected": '''def test_disconnected_graph(self):
        """Test with disconnected components."""
        graph = {
            0: [1],
            1: [0],
            2: [3],
            3: [2]
        }
        result = self.algorithm(graph, 0)
        self.assertIn(0, result)''',
    },
    "pattern": {
        "test_basic": '''def test_basic_functionality(self):
        """Test basic pattern functionality."""
        # Pattern-specific test
        instance1 = self.algorithm()
        instance2 = self.algorithm()
        # For singleton: should be same instance
        # For factory: should create objects
        self.assertIsNotNone(instance1)''',
        "test_multiple_instances": '''def test_multiple_instances(self):
        """Test multiple instance creation."""
        instance1 = self.algorithm()
        instance2 = self.algorithm()
        # Pattern-specific assertion
        self.assertIsNotNone(instance1)
        self.assertIsNotNone(instance2)''',
    },
}


def get_algorithm_category(algorithm_path: Path, algorithm_name: str) -> str:
    """Determine algorithm category."""
    path_str = str(algorithm_path).lower()
    algo_name_lower = algorithm_name.lower()

    if "sort" in path_str or "sort" in algo_name_lower:
        return "sorting"
    elif "search" in path_str or "search" in algo_name_lower:
        return "searching"
    elif "graph" in path_str or "bfs" in algo_name_lower or "dfs" in algo_name_lower:
        return "graph"
    elif "pattern" in path_str or "design" in path_str:
        return "pattern"
    elif "tree" in path_str:
        return "tree"
    elif "dp" in path_str or "dynamic" in path_str or "knapsack" in algo_name_lower:
        return "dp"
    else:
        return "general"


def populate_test_file(
    test_path: Path, algorithm_path: Path, algorithm_name: str
) -> bool:
    """Populate test file with specific test cases."""
    if not test_path.exists():
        return False

    try:
        content = test_path.read_text(encoding="utf-8")

        # Check if already populated
        if "def test_basic_functionality(self):" in content and "arr = [" in content:
            return False

        category = get_algorithm_category(algorithm_path, algorithm_name)
        test_cases = TEST_CASES.get(category, {})

        if not test_cases:
            return False

        # Find the test class
        class_match = re.search(
            r"(class\s+Test\w+.*?:.*?)(def\s+test_\w+.*?:.*?pass)", content, re.DOTALL
        )
        if not class_match:
            return False

        class_start = class_match.group(1)
        # Replace placeholder tests with real tests
        new_tests = []
        for test_name, test_code in test_cases.items():
            # Check if test already exists
            if f"def {test_name}" not in content:
                new_tests.append("    " + test_code)

        if not new_tests:
            return False

        # Replace placeholder tests
        placeholder_pattern = r"(def\s+test_\w+.*?:.*?pass\n)"
        new_content = re.sub(placeholder_pattern, "", content)

        # Insert new tests before the last method or before if __name__
        insert_pos = new_content.rfind("if __name__")
        if insert_pos == -1:
            insert_pos = len(new_content)

        tests_text = "\n\n".join(new_tests) + "\n\n    "
        new_content = new_content[:insert_pos] + tests_text + new_content[insert_pos:]

        test_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error populating {test_path}: {e}")
        return False


def main():
    """Populate unit tests with specific test cases."""
    populated = 0

    for test_file in ROOT.rglob("test_algorithm.py"):
        algo_dir = test_file.parent
        algo_name = algo_dir.name

        if populate_test_file(test_file, algo_dir, algo_name):
            populated += 1
            if populated % 10 == 0:
                print(f"[PROGRESS] Populated {populated} test files...")

    print(f"\n[COMPLETE] Populated {populated} unit test files")


if __name__ == "__main__":
    main()
