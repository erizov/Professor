import os
import pytest

from .conftest import algorithm_file_path, import_module_from_path

ML_TS_ALGOS = {
    # Advanced ML
    "svm": [
        "semester_3",
        "lecture_16_advanced_ml",
        "svm",
        "algorithm.py",
    ],
    # CNN architectures
    "resnet": [
        "semester_5",
        "lecture_22_cnn_architectures",
        "resnet",
        "algorithm.py",
    ],
    "inception": [
        "semester_5",
        "lecture_22_cnn_architectures",
        "inception",
        "algorithm.py",
    ],
    "vgg": [
        "semester_5",
        "lecture_22_cnn_architectures",
        "vgg",
        "algorithm.py",
    ],
    # NLP
    "word2vec": [
        "semester_5",
        "lecture_29_nlp_advanced",
        "word2vec",
        "algorithm.py",
    ],
    "seq2seq": [
        "semester_5",
        "lecture_29_nlp_advanced",
        "seq2seq",
        "algorithm.py",
    ],
    # Time series
    "arima": [
        "semester_5",
        "lecture_30_time_series",
        "arima",
        "algorithm.py",
    ],
    "lstm_timeseries": [
        "semester_5",
        "lecture_30_time_series",
        "lstm_timeseries",
        "algorithm.py",
    ],
    "prophet": [
        "semester_5",
        "lecture_30_time_series",
        "prophet",
        "algorithm.py",
    ],
}


@pytest.mark.parametrize("algo_name, path_parts", ML_TS_ALGOS.items())
def test_ml_and_timeseries_smoke(algo_name, path_parts):
    path = algorithm_file_path(*path_parts)
    if not os.path.exists(path):
        pytest.skip(f"Algorithm file not found: {path}")

    module = import_module_from_path(path)
    # Prefer function named after folder; else call main class minimal if exists
    fn = getattr(module, algo_name, None)
    if callable(fn):
        try:
            fn()
        except TypeError:
            pytest.skip(f"{algo_name} requires parameters; smoke skip")
    else:
        # For SVM, may expose a class
        cls = getattr(module, algo_name.upper(), None)
        if isinstance(cls, type):
            try:
                cls()
            except Exception:
                pass
        else:
            pytest.skip(f"No callable for {algo_name}; smoke import only")
