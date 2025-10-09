# tests/test_app.py
import importlib.util
import sys
import pytest

def _load_app_module():
    """Import app.py dù repo không phải là package."""
    spec = importlib.util.spec_from_file_location("app", "app.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["app"] = mod
    spec.loader.exec_module(mod)
    return mod

@pytest.fixture()
def client():
    mod = _load_app_module()
    app = getattr(mod, "app", None)
    assert app is not None, "Trong app.py phải có biến 'app = Flask(__name__)'"
    app.testing = True
    return app.test_client()

def test_homepage_200(client):
    resp = client.get("/")
    assert resp.status_code == 200
