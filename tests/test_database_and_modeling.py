import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path

DATA_ALGOS = {
    # Database operations
    "performance_tuning": [
        "semester_08",
        "lecture_53_database_operations",
        "performance_tuning",
        "algorithm.py",
    ],
    # Data modeling
    "dimensional_modeling": [
        "semester_08",
        "lecture_54_data_modeling",
        "dimensional_modeling",
        "algorithm.py",
    ],
    "data_warehousing": [
        "semester_08",
        "lecture_54_data_modeling",
        "data_warehousing",
        "algorithm.py",
    ],
    "data_lakes": [
        "semester_08",
        "lecture_54_data_modeling",
        "data_lakes",
        "algorithm.py",
    ],
    "data_governance": [
        "semester_08",
        "lecture_54_data_modeling",
        "data_governance",
        "algorithm.py",
    ],
    "etl_processes": [
        "semester_08",
        "lecture_54_data_modeling",
        "etl_processes",
        "algorithm.py",
    ],
    "entity_relationship": [
        "semester_08",
        "lecture_54_data_modeling",
        "entity_relationship",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", DATA_ALGOS.items())
def test_database_and_modeling_smoke(algo_name, path_parts):
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
