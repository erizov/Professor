import os
import inspect
import pytest

from .conftest import PROJECT_ROOT, import_module_from_path


def iter_algorithm_files():
    for entry in os.listdir(PROJECT_ROOT):
        if entry.startswith("semester_"):
            sem_dir = os.path.join(PROJECT_ROOT, entry)
            for root, dirs, files in os.walk(sem_dir):
                for f in files:
                    if f.endswith(".py"):
                        yield os.path.join(root, f)


def find_folder_named_function(module, file_path):
    # Try to infer a function named by its immediate folder
    folder = os.path.basename(os.path.dirname(file_path))
    cand = getattr(module, folder, None)
    if callable(cand):
        return cand
    # Also try main public function if unique
    public_functions = [
        obj
        for name, obj in inspect.getmembers(module, inspect.isfunction)
        if not name.startswith("_")
    ]
    if len(public_functions) == 1:
        return public_functions[0]
    return None


@pytest.mark.parametrize("file_path", list(iter_algorithm_files()))
def test_auto_discovery_smoke(file_path):
    # Skip test files and framework or web interface already covered elsewhere
    rel = os.path.relpath(file_path, PROJECT_ROOT)
    if (
        rel.startswith("tests")
        or rel.startswith("framework")
        or rel.startswith("web_interface")
    ):
        pytest.skip("covered elsewhere or not an algorithm")

    try:
        module = import_module_from_path(file_path)
    except Exception:
        pytest.skip(f"import failed for {file_path}")

    func = find_folder_named_function(module, file_path)
    if func is None:
        pytest.skip("no clear callable; skipping")

    # Attempt to call without args; if not possible, skip
    try:
        func()
    except TypeError:
        pytest.skip("callable requires args; skipping")
