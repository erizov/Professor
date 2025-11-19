import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path


def test_select_sorting_algorithm_basic():
    path = algorithm_file_path("framework", "constraint_selector.py")
    if not os.path.exists(path):
        pytest.skip("constraint_selector.py not found")
    module = import_module_from_path(path)

    AlgorithmSelector = getattr(module, "AlgorithmSelector", None)
    ResourceLevel = getattr(module, "ResourceLevel", None)
    Constraints = getattr(module, "Constraints", None)
    if not (AlgorithmSelector and ResourceLevel and Constraints):
        pytest.skip("Required classes not found in constraint_selector")

    # Low resources should prefer simpler algorithms (e.g., insertion/bubble for tiny datasets)
    constraints = Constraints(
        resource_level=ResourceLevel.LOW,
        dataset_size=100,
        memory_limit_mb=64,
        real_time=False,
    )
    rec = AlgorithmSelector.select_sorting_algorithm(constraints)
    assert isinstance(rec, dict)
    assert "name" in rec and "reason" in rec

    # High resources, large dataset should prefer O(n log n)
    constraints = Constraints(
        resource_level=ResourceLevel.HIGH,
        dataset_size=100000,
        memory_limit_mb=8192,
        real_time=False,
    )
    rec2 = AlgorithmSelector.select_sorting_algorithm(constraints)
    assert isinstance(rec2, dict)
    assert rec2["name"].lower() in {
        "merge sort",
        "quick sort",
        "heap sort",
        "timsort",
        "radix sort",
    }


def test_select_ml_algorithm_basic():
    path = algorithm_file_path("framework", "constraint_selector.py")
    if not os.path.exists(path):
        pytest.skip("constraint_selector.py not found")
    module = import_module_from_path(path)

    AlgorithmSelector = getattr(module, "AlgorithmSelector", None)
    ResourceLevel = getattr(module, "ResourceLevel", None)
    Constraints = getattr(module, "Constraints", None)
    if not (AlgorithmSelector and ResourceLevel and Constraints):
        pytest.skip("Required classes not found in constraint_selector")

    constraints = Constraints(
        resource_level=ResourceLevel.MEDIUM,
        dataset_size=5000,
        memory_limit_mb=2048,
        real_time=True,
    )
    rec = AlgorithmSelector.select_ml_algorithm(constraints)
    assert isinstance(rec, dict)
    assert "name" in rec and "reason" in rec
