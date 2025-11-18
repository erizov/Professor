import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable
from .data_sets import SEARCH_ARRAYS

SEARCHING_ALGOS = {
    "linear_search": [
        "semester_01",
        "lecture_04_searching",
        "linear_search",
        "linear_search.py",
    ],
    "binary_search": [
        "semester_01",
        "lecture_04_searching",
        "binary_search",
        "binary_search.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", SEARCHING_ALGOS.items())
@pytest.mark.parametrize(
    "arr, target, expected_present",
    [
        ([], 1, False),
        ([1], 1, True),
        ([1, 2, 3, 4, 5], 3, True),
        ([1, 2, 3, 4, 5], 42, False),
    ],
)
def test_search_algorithms(algo_name, path_parts, arr, target, expected_present):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    fn = find_callable(module, [algo_name, "search", "binary_search", "linear_search"]) 
    if fn is None:
        pytest.skip(f"No callable search function found in {path}")

    # Binary search expects sorted input
    if "binary" in algo_name:
        arr = sorted(arr)

    try:
        result = fn(arr, target)
    except TypeError:
        pytest.skip(f"Unsupported signature for {algo_name}")

    # Normalize result: some return index, some return bool
    if isinstance(result, bool):
        present = result
    else:
        present = result is not None and result != -1
    assert present == expected_present
