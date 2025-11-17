#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improve algorithm implementations with complete, production-ready code.
Uses existing implementations as templates and enhances them.
"""

import re
from pathlib import Path
from typing import Dict, Optional
import json

ROOT = Path(__file__).resolve().parents[1]

# Algorithm-specific implementations
ALGORITHM_IMPLEMENTATIONS = {
    'selection_sort': {
        'python': '''def selection_sort(arr: List[T]) -> List[T]:
    """
    Sort array using selection sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list (modifies in-place and returns)
        
    Time Complexity: O(n²) - always
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Find minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap found minimum with first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr''',
        'java': '''public static int[] selectionSort(int[] arr) {
    int n = arr.length;
    
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        
        // Swap
        int temp = arr[minIdx];
        arr[minIdx] = arr[i];
        arr[i] = temp;
    }
    
    return arr;
}'''
    },
    'heap_sort': {
        'python': '''def heap_sort(arr: List[T]) -> List[T]:
    """
    Sort array using heap sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity: O(n log n) - always
    Space Complexity: O(1)
    """
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move root to end
        heapify(arr, i, 0)  # Heapify reduced heap
    
    return arr

def heapify(arr: List[T], n: int, i: int):
    """Heapify subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)''',
        'java': '''public static int[] heapSort(int[] arr) {
    int n = arr.length;
    
    // Build max heap
    for (int i = n / 2 - 1; i >= 0; i--) {
        heapify(arr, n, i);
    }
    
    // Extract elements from heap
    for (int i = n - 1; i > 0; i--) {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        
        heapify(arr, i, 0);
    }
    
    return arr;
}

private static void heapify(int[] arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest]) {
        largest = left;
    }
    
    if (right < n && arr[right] > arr[largest]) {
        largest = right;
    }
    
    if (largest != i) {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        
        heapify(arr, n, largest);
    }
}'''
    }
}

def improve_algorithm_file(file_path: Path, algorithm_name: str, lang: str) -> bool:
    """Improve algorithm implementation file."""
    if not file_path.exists():
        return False
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Check if it's a placeholder
        if 'TODO: Implement' in content or 'pass  # Placeholder' in content:
            # Get implementation if available
            if algorithm_name in ALGORITHM_IMPLEMENTATIONS:
                impl = ALGORITHM_IMPLEMENTATIONS[algorithm_name].get(lang)
                if impl:
                    # Replace placeholder function
                    if lang == 'python':
                        # Find function definition and replace
                        pattern = r'def\s+\w+.*?:\s*(?:"""[\s\S]*?""")?\s*(?:pass|\.\.\.|# TODO.*?\n)'
                        if re.search(pattern, content):
                            # Extract header and main, replace function
                            header_match = re.search(r'(.*?)(def\s+\w+)', content, re.DOTALL)
                            if header_match:
                                header = header_match.group(1)
                                func_name_match = re.search(r'def\s+(\w+)', content)
                                if func_name_match:
                                    func_name = func_name_match.group(1)
                                    new_func = impl.replace('selection_sort', func_name).replace('heap_sort', func_name)
                                    # Reconstruct file
                                    main_match = re.search(r'(def main\(\):.*)', content, re.DOTALL)
                                    main_part = main_match.group(1) if main_match else "\n\nif __name__ == \"__main__\":\n    main()\n"
                                    new_content = header + new_func + "\n\n" + main_part
                                    file_path.write_text(new_content, encoding='utf-8')
                                    return True
            
            return False
        
        return False
    except Exception as e:
        print(f"Error improving {file_path}: {e}")
        return False

def main():
    """Improve algorithm implementations."""
    improved = 0
    
    # Find algorithm files
    for py_file in ROOT.rglob("algorithm.py"):
        algo_dir = py_file.parent
        algorithm_name = algo_dir.name
        
        if improve_algorithm_file(py_file, algorithm_name, 'python'):
            improved += 1
            print(f"[OK] Improved: {py_file.relative_to(ROOT)}")
    
    for java_file in ROOT.rglob("Algorithm.java"):
        algo_dir = java_file.parent
        algorithm_name = algo_dir.name
        
        if improve_algorithm_file(java_file, algorithm_name, 'java'):
            improved += 1
            print(f"[OK] Improved: {java_file.relative_to(ROOT)}")
    
    print(f"\n[COMPLETE] Improved {improved} algorithm files")

if __name__ == "__main__":
    main()

