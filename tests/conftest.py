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


def import_module_from_path(module_path: str) -> ModuleType:
    """Dynamically import a Python module from a file path."""
    spec = importlib.util.spec_from_file_location("_dynamic_module", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def find_callable(module: ModuleType, candidates: List[str]) -> Optional[Callable[..., Any]]:
    """Return the first callable attribute in module that matches any of candidates."""
    for name in candidates:
        fn = getattr(module, name, None)
        if callable(fn):
            return fn
    # Fallback: find a single public function
    public_functions = [
        obj for _, obj in inspect.getmembers(module, inspect.isfunction) if not _.startswith("_")
    ]
    if len(public_functions) == 1:
        return public_functions[0]
    return None


def algorithm_file_path(*parts: str) -> str:
    """Build an absolute file path for an algorithm given its folder structure under semesters."""
    root = PROJECT_ROOT
    return os.path.join(root, *parts)
