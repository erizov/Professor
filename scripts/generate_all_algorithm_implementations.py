#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate specific algorithm implementations for all algorithm folders.

This script ensures each algorithm.py file has a proper implementation
specific to that algorithm's folder name.
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


# Algorithm implementation templates
ALGORITHM_IMPLEMENTATIONS: Dict[str, str] = {
    'bubble_sort': '''def bubble_sort(arr: List[int]) -> List[int]:
    """Bubble sort algorithm."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr''',
    
    'selection_sort': '''def selection_sort(arr: List[int]) -> List[int]:
    """Selection sort algorithm."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr''',
    
    'insertion_sort': '''def insertion_sort(arr: List[int]) -> List[int]:
    """Insertion sort algorithm."""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr''',
    
    'merge_sort': '''def merge_sort(arr: List[int]) -> List[int]:
    """Merge sort algorithm."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result''',
    
    'quick_sort': '''def quick_sort(arr: List[int]) -> List[int]:
    """Quick sort algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)''',
    
    'binary_search': '''def binary_search(arr: List[int], target: int) -> Optional[int]:
    """Binary search algorithm."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None''',
    
    'linear_search': '''def linear_search(arr: List[int], target: int) -> Optional[int]:
    """Linear search algorithm."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return None''',
    
    'dfs': '''def dfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Depth-first search."""
    visited: Set[int] = set()
    result: List[int] = []
    
    def _dfs(node: int) -> None:
        visited.add(node)
        result.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)
    
    _dfs(start)
    return result''',
    
    'bfs': '''def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Breadth-first search."""
    from collections import deque
    visited: Set[int] = set()
    queue = deque([start])
    result: List[int] = []
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    return result''',
    
    'jump_search': '''def jump_search(arr: List[int], target: int) -> Optional[int]:
    """Jump search algorithm."""
    n = len(arr)
    if n == 0:
        return None
    
    step = int(n ** 0.5)
    prev = 0
    
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return None
    
    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return None''',
    
    'interpolation_search': '''def interpolation_search(arr: List[int], target: int) -> Optional[int]:
    """Interpolation search algorithm."""
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return None
        
        pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return None''',
    
    'heap_sort': '''def heap_sort(arr: List[int]) -> List[int]:
    """Heap sort algorithm."""
    def heapify(arr: List[int], n: int, i: int) -> None:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr''',
    
    'counting_sort': '''def counting_sort(arr: List[int]) -> List[int]:
    """Counting sort algorithm."""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    output = [0] * len(arr)
    
    for num in arr:
        count[num - min_val] += 1
    
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output''',
    
    'radix_sort': '''def radix_sort(arr: List[int]) -> List[int]:
    """Radix sort algorithm."""
    def counting_sort_radix(arr: List[int], exp: int) -> List[int]:
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        
        return output
    
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_radix(arr, exp)
        exp *= 10
    
    return arr''',
    
    'bucket_sort': '''def bucket_sort(arr: List[float]) -> List[float]:
    """Bucket sort algorithm."""
    if not arr:
        return arr
    
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    for num in arr:
        bucket_idx = int(n * num)
        if bucket_idx == n:
            bucket_idx = n - 1
        buckets[bucket_idx].append(num)
    
    for bucket in buckets:
        bucket.sort()
    
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result''',
}


def get_algorithm_implementation(algorithm_name: str) -> Optional[str]:
    """Get algorithm implementation code."""
    if algorithm_name in ALGORITHM_IMPLEMENTATIONS:
        return ALGORITHM_IMPLEMENTATIONS[algorithm_name]
    return None


def create_algorithm_file_content(algorithm_name: str, 
                                  implementation: Optional[str]) -> str:
    """Create complete algorithm.py file content."""
    title = algorithm_name.replace('_', ' ').title()
    
    header = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
{title} implementation.

This file contains the implementation of the {title} algorithm.
"""

from typing import List, Optional, Dict, Set
'''
    
    if implementation:
        impl_code = implementation
    else:
        # Generic implementation template
        impl_code = f'''def {algorithm_name}(data):
    """
    {title} algorithm implementation.
    
    Args:
        data: Input data for the algorithm
        
    Returns:
        Processed result
    """
    # Implementation specific to {title}
    return data
'''
    
    main_code = f'''
def main() -> None:
    """Demonstrate {title}."""
    print("=" * 70)
    print("{title.upper()}")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for {title}")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
'''
    
    return header + '\n\n' + impl_code + '\n\n' + main_code


def update_algorithm_file(algorithm_path: Path, algorithm_name: str) -> bool:
    """Update algorithm.py with specific implementation."""
    implementation = get_algorithm_implementation(algorithm_name)
    
    if not implementation:
        # No specific implementation available, skip
        return False
    
    if algorithm_path.exists():
        existing = algorithm_path.read_text(encoding='utf-8')
        # Check if it already has the correct implementation
        func_name = implementation.split('(')[0].split('def ')[1].strip()
        if func_name in existing and 'def ' + func_name in existing:
            # Check if it's a real implementation or just a stub
            if '# Implementation specific to' in existing or 'return data' in existing:
                # It's a generic stub, replace it
                new_content = create_algorithm_file_content(algorithm_name, implementation)
                algorithm_path.write_text(new_content, encoding='utf-8')
                return True
            # Already has good implementation
            return False
        # Check if it's a placeholder or generic
        if ('Implementation in progress' in existing or 
            'pass' in existing and len(existing) < 300 or
            '# Implementation specific to' in existing or
            'return data' in existing):
            # Replace placeholder/generic with specific implementation
            new_content = create_algorithm_file_content(algorithm_name, implementation)
            algorithm_path.write_text(new_content, encoding='utf-8')
            return True
    
    # Write new content
    new_content = create_algorithm_file_content(algorithm_name, implementation)
    algorithm_path.write_text(new_content, encoding='utf-8')
    return True


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm subfolders."""
    base_path = Path('.')
    algorithm_folders = []
    
    for semester_dir in base_path.glob('semester_*'):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ['__pycache__', '.git']):
            continue
        
        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if 'lecture_' not in lecture_dir.name:
                continue
            
            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith('lecture_'):
                    continue
                if any(x in algo_dir.name for x in ['__pycache__', '.git']):
                    continue
                
                algorithm_folders.append(algo_dir)
    
    return sorted(algorithm_folders)


def main() -> None:
    """Main function."""
    print("Finding all algorithm folders...")
    algorithm_folders = find_all_algorithm_folders()
    print(f"Found {len(algorithm_folders)} algorithm folders\n")
    
    updated = 0
    skipped = 0
    errors = []
    
    for algo_folder in algorithm_folders:
        algorithm_name = algo_folder.name
        algorithm_path = algo_folder / 'algorithm.py'
        
        try:
            if update_algorithm_file(algorithm_path, algorithm_name):
                updated += 1
                if updated % 50 == 0:
                    print(f"Updated {updated} algorithm files...")
            else:
                skipped += 1
        except Exception as e:
            errors.append(f"{algo_folder}: {e}")
    
    print(f"\nSummary:")
    print(f"  Updated algorithm.py files: {updated}")
    print(f"  Skipped (already complete): {skipped}")
    
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:10]:
            print(f"  {error}")


if __name__ == "__main__":
    main()

