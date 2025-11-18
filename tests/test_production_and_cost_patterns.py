import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path

PROD_COST_ALGOS = {
    # Inference optimization
    "model_caching": [
        "semester_06",
        "lecture_36_inference_optimization",
        "model_caching",
        "algorithm.py",
    ],
    # Cost optimization
    "autoscaling": [
        "semester_06",
        "lecture_37_cost_optimization",
        "autoscaling",
        "algorithm.py",
    ],
    "serverless_ml": [
        "semester_06",
        "lecture_37_cost_optimization",
        "serverless_ml",
        "algorithm.py",
    ],
    "cost_analysis": [
        "semester_06",
        "lecture_37_cost_optimization",
        "cost_analysis",
        "algorithm.py",
    ],
    # Monitoring production
    "prometheus_ml": [
        "semester_06",
        "lecture_38_monitoring_production",
        "prometheus_ml",
        "algorithm.py",
    ],
    "grafana_dashboards": [
        "semester_06",
        "lecture_38_monitoring_production",
        "grafana_dashboards",
        "algorithm.py",
    ],
    "performance_profiling": [
        "semester_06",
        "lecture_38_monitoring_production",
        "performance_profiling",
        "algorithm.py",
    ],
    "alerting": [
        "semester_06",
        "lecture_38_monitoring_production",
        "alerting",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", PROD_COST_ALGOS.items())
def test_production_and_cost_patterns_smoke(algo_name, path_parts):
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
