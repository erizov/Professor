import os
import importlib.util
import pytest

from .conftest import algorithm_file_path


@pytest.fixture
def app_module():
    path = algorithm_file_path("web_interface", "app.py")
    if not os.path.exists(path):
        pytest.skip("web_interface/app.py not found")
    spec = importlib.util.spec_from_file_location("web_app", path)
    if spec is None or spec.loader is None:
        pytest.skip("Cannot import web app module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


@pytest.fixture
def client(app_module):
    app = getattr(app_module, "app", None)
    if app is None:
        pytest.skip("Flask app object not found in app.py")
    app.testing = True
    return app.test_client()


def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Algorithms" in resp.data or len(resp.data) > 0


def test_api_algorithms(client):
    resp = client.get("/api/algorithms")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_api_run_smoke(client):
    # Try running a trivial algorithm if available; otherwise expect 400/404 gracefully
    payload = {"path": "", "language": "python"}
    resp = client.post("/api/run", json=payload)
    assert resp.status_code in (200, 400, 404)


def test_api_readme_smoke(client):
    resp = client.get("/api/readme/invalid/path")
    assert resp.status_code in (200, 400, 404)
