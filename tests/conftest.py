import importlib.util
import inspect
import os
import sys
from types import ModuleType
from typing import Any, Callable, List, Optional

# Ensure project root is on sys.path for imports when running pytest from repo root
PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Long-running tests tracking
_LONG_TESTS: list[tuple[str, float]] = []
_LONG_THRESHOLD: float = float(os.getenv("LONG_TEST_THRESHOLD_SECONDS", "30"))


def import_module_from_path(module_path: str) -> ModuleType:
    """Dynamically import a Python module from a file path."""
    spec = importlib.util.spec_from_file_location("_dynamic_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def find_callable(
    module: ModuleType, candidates: List[str]
) -> Optional[Callable[..., Any]]:
    """Return the first callable attribute in module that matches any of candidates."""
    for name in candidates:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn
    # Fallback: find a single public function
    public_functions = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isfunction)
        if not _.startswith("_")
    ]
    if len(public_functions) == 1:
        return public_functions[0]
    return None


def algorithm_file_path(*parts: str) -> str:
    """Build an absolute file path for an algorithm given its folder structure under semesters."""
    root = PROJECT_ROOT
    return os.path.join(root, *parts)


# Pytest hooks for long-running test tracking
def pytest_runtest_logreport(report):  # type: ignore
    if report.when == "call" and hasattr(report, "duration"):
        duration = float(getattr(report, "duration", 0.0))
        if duration > _LONG_THRESHOLD:
            _LONG_TESTS.append((report.nodeid, duration))


def pytest_sessionfinish(session, exitstatus):  # type: ignore
    if not _LONG_TESTS:
        return
    out_dir = os.path.join(PROJECT_ROOT, "tests")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "long_running_tests.txt")
    _LONG_TESTS.sort(key=lambda x: x[1], reverse=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Long-running tests (>{}s)\n".format(_LONG_THRESHOLD))
        for nodeid, dur in _LONG_TESTS:
            f.write(f"{dur:.2f}s\t{nodeid}\n")
    # Print concise summary
    print(
        "\n[long-tests] {} tests exceeded {}s. Report: {}".format(
            len(_LONG_TESTS), _LONG_THRESHOLD, out_path
        )
    )
