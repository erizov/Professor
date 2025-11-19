#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to enhance specific algorithms with full implementations.

This creates working implementations for priority algorithms.
"""

from pathlib import Path


# Full implementations for key algorithms
IMPLEMENTATIONS = {
    "selection_sort": {
        "python": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Selection Sort implementation."""

from typing import List, TypeVar

T = TypeVar('T')


def selection_sort(arr: List[T]) -> List[T]:
    """
    Sort array using selection sort.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list (modifies in-place)
        
    Time: O(n²), Space: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Find minimum element in remaining array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap minimum element with first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def main():
    """Demonstration."""
    print("=" * 70)
    print("SELECTION SORT")
    print("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data}")
    result = selection_sort(data.copy())
    print(f"Sorted:   {result}")
    
    print("\\nComplexity: O(n²) time, O(1) space")


if __name__ == "__main__":
    main()
''',
        "java": """public class Algorithm {
    public static int[] selectionSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                }
            }
            
            int temp = arr[i];
            arr[i] = arr[minIdx];
            arr[minIdx] = temp;
        }
        
        return arr;
    }
    
    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Selection Sort");
        System.out.println("Complexity: O(n²) time, O(1) space");
        selectionSort(data);
    }
}
""",
    },
    "insertion_sort": {
        "python": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insertion Sort implementation."""

from typing import List, TypeVar

T = TypeVar('T')


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Sort array using insertion sort.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
        
    Time: O(n²) worst, O(n) best, Space: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def main():
    """Demonstration."""
    print("=" * 70)
    print("INSERTION SORT")
    print("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data}")
    result = insertion_sort(data.copy())
    print(f"Sorted:   {result}")
    
    print("\\nComplexity: O(n²) worst, O(n) best, O(1) space")


if __name__ == "__main__":
    main()
''',
        "java": """public class Algorithm {
    public static int[] insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
        
        return arr;
    }
    
    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Insertion Sort");
        System.out.println("O(n²) worst, O(n) best");
        insertionSort(data);
    }
}
""",
    },
    "linear_search": {
        "python": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linear Search implementation."""

from typing import List, TypeVar, Optional

T = TypeVar('T')


def linear_search(arr: List[T], target: T) -> Optional[int]:
    """
    Search for target using linear search.
    
    Args:
        arr: List to search in
        target: Element to find
        
    Returns:
        Index if found, None otherwise
        
    Time: O(n), Space: O(1)
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return None


def main():
    """Demonstration."""
    print("=" * 70)
    print("LINEAR SEARCH")
    print("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    target = 22
    
    result = linear_search(data, target)
    print(f"Array: {data}")
    print(f"Target: {target}")
    print(f"Found at index: {result}")
    
    print("\\nComplexity: O(n) time, O(1) space")


if __name__ == "__main__":
    main()
''',
        "java": """public class Algorithm {
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    public static void main(String[] args) {
        int[] data = {64, 34, 25, 12, 22, 11, 90};
        int target = 22;
        
        int result = linearSearch(data, target);
        System.out.println("Linear Search - O(n)");
        System.out.println("Found at index: " + result);
    }
}
""",
    },
}


def enhance_algorithm(semester: str, lecture: str, algorithm: str) -> None:
    """Enhance algorithm with full implementation."""
    if algorithm not in IMPLEMENTATIONS:
        print(f"No implementation available for {algorithm}")
        return

    base_path = Path(f"semester_{semester}") / lecture / algorithm

    if not base_path.exists():
        print(f"Path does not exist: {base_path}")
        return

    impl = IMPLEMENTATIONS[algorithm]

    # Write Python
    with open(base_path / "algorithm.py", "w", encoding="utf-8") as f:
        f.write(impl["python"])

    # Write Java
    with open(base_path / "Algorithm.java", "w", encoding="utf-8") as f:
        f.write(impl["java"])

    print(f"✓ Enhanced: {base_path}")


def main():
    """Enhance priority algorithms."""
    enhancements = [
        ("1", "lecture_01_sorting_fundamentals", "selection_sort"),
        ("1", "lecture_01_sorting_fundamentals", "insertion_sort"),
        ("1", "lecture_04_searching", "linear_search"),
    ]

    print("Enhancing algorithms with full implementations...")
    print("=" * 70)

    for semester, lecture, algorithm in enhancements:
        enhance_algorithm(semester, lecture, algorithm)

    print("=" * 70)
    print("\\nEnhancement complete!")
    print("\\nTo implement more algorithms:")
    print("1. Add implementation to IMPLEMENTATIONS dict")
    print("2. Run this script")
    print("3. Or manually edit algorithm.py and Algorithm.java")


if __name__ == "__main__":
    main()
