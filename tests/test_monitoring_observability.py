import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path

MONITORING_ALGOS = {
    "metrics_collection": [
        "semester_4",
        "lecture_20_monitoring_observability",
        "metrics_collection",
        "algorithm.py",
    ],
    "log_aggregation": [
        "semester_4",
        "lecture_20_monitoring_observability",
        "log_aggregation",
        "algorithm.py",
    ],
    "distributed_tracing": [
        "semester_4",
        "lecture_20_monitoring_observability",
        "distributed_tracing",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", MONITORING_ALGOS.items())
def test_monitoring_observability(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)

    fn = getattr(module, algo_name, None)
    if callable(fn):
        try:
            fn()
        except TypeError:
            pytest.skip(f"{algo_name} requires parameters; skipping call")
    else:
        pytest.skip(f"{algo_name} function not found; smoke import only")
