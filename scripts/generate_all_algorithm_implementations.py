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
    
    'dijkstra': '''def dijkstra(graph: Dict[int, List[tuple]], start: int) -> Dict[int, int]:
    """Dijkstra's shortest path algorithm."""
    from heapq import heappush, heappop
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heappush(pq, (distance, neighbor))
    
    return distances''',
    
    'bellman_ford': '''def bellman_ford(graph: Dict[int, List[tuple]], start: int, n: int) -> Dict[int, int]:
    """Bellman-Ford shortest path algorithm."""
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    
    for _ in range(n - 1):
        for u in graph:
            for v, w in graph[u]:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
    
    return distances''',
    
    'floyd_warshall': '''def floyd_warshall(graph: List[List[int]], n: int) -> List[List[int]]:
    """Floyd-Warshall all-pairs shortest path algorithm."""
    dist = [row[:] for row in graph]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist''',
    
    'kmp': '''def kmp_search(text: str, pattern: str) -> List[int]:
    """KMP string search algorithm."""
    def build_lps(pattern: str) -> List[int]:
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = build_lps(pattern)
    i = j = 0
    result = []
    
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result''',
    
    'knapsack': '''def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """0/1 Knapsack problem using dynamic programming."""
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]''',
    
    'longest_common_subsequence': '''def longest_common_subsequence(s1: str, s2: str) -> int:
    """Longest Common Subsequence using dynamic programming."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]''',
    
    'edit_distance': '''def edit_distance(s1: str, s2: str) -> int:
    """Edit distance (Levenshtein distance) using dynamic programming."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1]   # substitution
                )
    
    return dp[m][n]''',
    
    'fibonacci': '''def fibonacci(n: int) -> int:
    """Fibonacci using dynamic programming."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]''',
    
    'binary_tree': '''class TreeNode:
    """Binary tree node."""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Inorder traversal of binary tree."""
    result = []
    if root:
        result.extend(inorder_traversal(root.left))
        result.append(root.val)
        result.extend(inorder_traversal(root.right))
    return result

def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Preorder traversal of binary tree."""
    result = []
    if root:
        result.append(root.val)
        result.extend(preorder_traversal(root.left))
        result.extend(preorder_traversal(root.right))
    return result

def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Postorder traversal of binary tree."""
    result = []
    if root:
        result.extend(postorder_traversal(root.left))
        result.extend(postorder_traversal(root.right))
        result.append(root.val)
    return result''',
    
    'binary_search_tree': '''class BSTNode:
    """Binary Search Tree node."""
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BinarySearchTree:
    """Binary Search Tree implementation."""
    def __init__(self):
        self.root: Optional[BSTNode] = None
    
    def insert(self, val: int) -> None:
        """Insert value into BST."""
        self.root = self._insert(self.root, val)
    
    def _insert(self, root: Optional[BSTNode], val: int) -> BSTNode:
        if root is None:
            return BSTNode(val)
        if val < root.val:
            root.left = self._insert(root.left, val)
        elif val > root.val:
            root.right = self._insert(root.right, val)
        return root
    
    def search(self, val: int) -> bool:
        """Search for value in BST."""
        return self._search(self.root, val)
    
    def _search(self, root: Optional[BSTNode], val: int) -> bool:
        if root is None:
            return False
        if root.val == val:
            return True
        elif val < root.val:
            return self._search(root.left, val)
        else:
            return self._search(root.right, val)''',
    
    'hash_table': '''class HashTable:
    """Hash table implementation with chaining."""
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[List[tuple]] = [[] for _ in range(size)]
    
    def _hash(self, key: int) -> int:
        """Hash function."""
        return key % self.size
    
    def insert(self, key: int, value: any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
    
    def get(self, key: int) -> Optional[any]:
        """Get value by key."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key: int) -> bool:
        """Delete key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False''',
    
    'priority_queue': '''class PriorityQueue:
    """Priority queue implementation using heap."""
    def __init__(self):
        self.heap: List[tuple] = []
    
    def push(self, item: any, priority: int) -> None:
        """Add item with priority."""
        from heapq import heappush
        heappush(self.heap, (priority, item))
    
    def pop(self) -> Optional[any]:
        """Remove and return highest priority item."""
        from heapq import heappop
        if self.heap:
            return heappop(self.heap)[1]
        return None
    
    def peek(self) -> Optional[any]:
        """Return highest priority item without removing."""
        if self.heap:
            return self.heap[0][1]
        return None
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.heap) == 0''',
    
    'binary_heap': '''class BinaryHeap:
    """Binary heap (min heap) implementation."""
    def __init__(self):
        self.heap: List[int] = []
    
    def parent(self, i: int) -> int:
        """Get parent index."""
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        """Get left child index."""
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        """Get right child index."""
        return 2 * i + 2
    
    def insert(self, val: int) -> None:
        """Insert value into heap."""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_min(self) -> Optional[int]:
        """Extract minimum value."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root
    
    def _heapify_up(self, i: int) -> None:
        """Maintain heap property upward."""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)
    
    def _heapify_down(self, i: int) -> None:
        """Maintain heap property downward."""
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)''',
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

