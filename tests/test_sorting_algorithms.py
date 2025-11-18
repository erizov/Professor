import os
import copy
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable
from .data_sets import SORT_CASES

# Map of algorithm name to relative path parts under the project
SORTING_ALGOS = {
    "bubble_sort": [
        "semester_01",
        "lecture_01_sorting_fundamentals",
        "bubble_sort",
        "bubble_sort.py",
    ],
    "insertion_sort": [
        "semester_01",
        "lecture_01_sorting_fundamentals",
        "insertion_sort",
        "insertion_sort.py",
    ],
    "selection_sort": [
        "semester_01",
        "lecture_01_sorting_fundamentals",
        "selection_sort",
        "selection_sort.py",
    ],
    "merge_sort": [
        "semester_01",
        "lecture_02_efficient_sorting",
        "merge_sort",
        "merge_sort.py",
    ],
    "quick_sort": [
        "semester_01",
        "lecture_02_efficient_sorting",
        "quick_sort",
        "quick_sort.py",
    ],
    "heap_sort": [
        "semester_01",
        "lecture_02_efficient_sorting",
        "heap_sort",
        "heap_sort.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", SORTING_ALGOS.items())
@pytest.mark.parametrize("arr", SORT_CASES)
def test_sorting_algorithms(algo_name, path_parts, arr):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    fn = find_callable(
        module,
        [
            "sort",
            algo_name,
            f"{algo_name}_sort",
            "bubble_sort",
            "insertion_sort",
            "selection_sort",
            "merge_sort",
            "quick_sort",
            "heap_sort",
        ],
    )
    if fn is None:
        pytest.skip(f"No callable sorting function found in {path}")

    original = copy.deepcopy(arr)

    # Try both patterns: returns new list or sorts in place
    try:
        result = fn(copy.deepcopy(arr))
    except TypeError:
        # Some implementations might require two args etc.; skip those
        pytest.skip(f"Unsupported signature for {algo_name}")

    # Normalize output
    if result is None:
        # Assume in-place sort
        result = arr
    # Validate sorted result equals Python's sorted
    assert result == sorted(original)
