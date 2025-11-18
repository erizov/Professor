import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path, find_callable

STR_ALGOS = {
    "kmp_search": [
        "semester_01",
        "lecture_12_string_algorithms",
        "kmp",
        "kmp.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", STR_ALGOS.items())
def test_string_algorithms(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    fn = find_callable(module, [algo_name, "kmp_search"])
    if fn is None:
        pytest.skip(f"No callable function {algo_name} found in {path}")

    text = "abxabcabcaby"
    pattern = "abcaby"
    res = fn(text, pattern)
    # Normalize: allow single index or list of indices
    if isinstance(res, list):
        assert res == [6]
    else:
        assert res == 6
