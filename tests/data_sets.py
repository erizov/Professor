from typing import List

# Common datasets for sorting tests
SORT_CASES: List[List[int]] = [
    [],
    [1],
    [2, 1],
    [3, 1, 2],
    [5, 3, 8, 1, 2, 7, 4, 6],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 3, 2, 1, 2, 3, 1],
]

# Datasets for searching
SEARCH_ARRAYS: List[List[int]] = [
    [],
    [1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
]
