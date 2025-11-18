import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable

DP_ALGOS = {
    "fibonacci": [
        "semester_01",
        "lecture_11_dynamic_programming",
        "fibonacci",
        "fibonacci.py",
    ],
    "edit_distance": [
        "semester_01",
        "lecture_11_dynamic_programming",
        "edit_distance",
        "edit_distance.py",
    ],
    "knapsack": [
        "semester_01",
        "lecture_11_dynamic_programming",
        "knapsack",
        "knapsack.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", DP_ALGOS.items())
def test_dp_algorithms(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    fn = find_callable(module, [algo_name])
    if fn is None:
        pytest.skip(f"No callable function {algo_name} found in {path}")

    if algo_name == "fibonacci":
        assert fn(0) == 0
        assert fn(1) == 1
        assert fn(10) == 55
    elif algo_name == "edit_distance":
        assert fn("kitten", "sitting") == 3
        assert fn("", "abc") == 3
        assert fn("abc", "abc") == 0
    elif algo_name == "knapsack":
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 5
        best = fn(weights, values, capacity)
        assert best in (7, (7, [0, 1]))  # allow value or (value, items)
