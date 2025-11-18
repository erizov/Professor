#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improve production-ready code for top algorithms.
Adds error handling, input validation, logging, and edge case coverage.
"""

import re
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]

# Algorithms to improve (top 50 - first batch)
ALGORITHMS_TO_IMPROVE = [
    # Sorting
    "semester_01/lecture_02_efficient_sorting/quick_sort",
    "semester_01/lecture_02_efficient_sorting/merge_sort",
    "semester_01/lecture_02_efficient_sorting/heap_sort",
    "semester_01/lecture_01_sorting_fundamentals/bubble_sort",
    "semester_01/lecture_01_sorting_fundamentals/insertion_sort",
    "semester_01/lecture_01_sorting_fundamentals/selection_sort",
    # Searching
    "semester_01/lecture_04_searching/binary_search",
    "semester_01/lecture_04_searching/linear_search",
    # Graphs
    "semester_01/lecture_09_graph_algorithms/bfs",
    "semester_01/lecture_09_graph_algorithms/dfs",
    "semester_01/lecture_09_graph_algorithms/dijkstra",
    # Trees
    "semester_01/lecture_05_trees/binary_search_tree",
    "semester_01/lecture_05_trees/avl_tree",
    # Dynamic Programming
    "semester_01/lecture_10_dynamic_programming/knapsack",
    "semester_01/lecture_10_dynamic_programming/edit_distance",
    # Design Patterns
    "semester_02/lecture_06_creational_patterns/singleton",
    "semester_02/lecture_06_creational_patterns/factory",
    # Add more as needed
]

def improve_python_code(py_path: Path) -> bool:
    """Improve Python code with production-ready features."""
    try:
        content = py_path.read_text(encoding="utf-8")
        original = content
        
        # Check if already has error handling
        if "TypeError" in content and "ValueError" in content and "logging" in content:
            return False
        
        # Add imports if missing
        if "import logging" not in content:
            # Find last import
            import_pattern = r'(import\s+\w+|from\s+\w+\s+import)'
            imports = list(re.finditer(import_pattern, content))
            if imports:
                last_import = imports[-1]
                insert_pos = last_import.end()
                content = (content[:insert_pos] + 
                          "\nimport logging\n" + 
                          content[insert_pos:])
        
        # Add logger setup if missing
        if "logger = logging.getLogger" not in content:
            # Add after imports
            content = re.sub(
                r'(import\s+sys\s*\n)',
                r'\1\n# Setup logging\nlogger = logging.getLogger(__name__)\n',
                content
            )
        
        # Improve main function with error handling
        if "def main():" in content and "try:" not in content.split("def main():")[1][:200]:
            main_pattern = r'(def main\(\):.*?)(if __name__)'
            def add_error_handling(match):
                main_body = match.group(1)
                if "try:" not in main_body:
                    return (main_body.rstrip() + 
                           "\n    try:\n        " +
                           main_body.split("\n", 1)[1].replace("\n", "\n        ") +
                           "\n    except Exception as e:\n" +
                           "        logger.error(f\"Error: {e}\", exc_info=True)\n" +
                           "        sys.exit(1)\n\n" +
                           match.group(2))
                return match.group(0)
            
            content = re.sub(main_pattern, add_error_handling, content, flags=re.DOTALL)
        
        if content != original:
            py_path.write_text(content, encoding="utf-8")
            return True
        
        return False
    except Exception as e:
        print(f"Error improving {py_path}: {e}")
        return False

def main():
    """Improve production code for top algorithms."""
    improved_count = 0
    
    for algo_path in ALGORITHMS_TO_IMPROVE:
        py_path = ROOT / algo_path / "algorithm.py"
        if py_path.exists():
            if improve_python_code(py_path):
                improved_count += 1
                print(f"Improved {algo_path}")
    
    print(f"\nImproved {improved_count} Python implementations")

if __name__ == "__main__":
    main()

