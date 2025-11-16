import os
import time
import pytest

from .conftest import algorithm_file_path, import_module_from_path

CONCURRENCY_ALGOS = {
    "thread_pool": [
        "semester_2",
        "lecture_12_concurrency_patterns",
        "thread_pool",
        "algorithm.py",
    ],
    "producer_consumer": [
        "semester_2",
        "lecture_12_concurrency_patterns",
        "producer_consumer",
        "algorithm.py",
    ],
    "readers_writers": [
        "semester_2",
        "lecture_12_concurrency_patterns",
        "readers_writers",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", CONCURRENCY_ALGOS.items())
def test_concurrency_patterns(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)

    if algo_name == "thread_pool":
        ThreadPool = getattr(module, "ThreadPool", None)
        if ThreadPool is None:
            pytest.skip("ThreadPool class not found")
        tp = ThreadPool(num_threads=2)

        def add(a, b):
            time.sleep(0.01)
            return a + b

        # Submit a few tasks and ensure no exceptions; we can't easily get results if it's a fire-and-forget
        for i in range(3):
            tp.submit(add, i, i)
        tp.shutdown(wait=True)
        assert True  # If we reached here, basic lifecycle works
    else:
        # Smoke: module imports and defines a top-level function matching folder name
        func = getattr(module, algo_name, None)
        if callable(func):
            # Call without args if possible
            try:
                func()
            except TypeError:
                pytest.skip(f"{algo_name} requires parameters; skipping smoke call")
        else:
            pytest.skip(f"{algo_name} function not found; smoke import only")
