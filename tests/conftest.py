import pytest
from app import app
from storage import reset_storage

@pytest.fixture(autouse=True)
def _isolate_storage():
    reset_storage()
    yield
    reset_storage()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        # ensure clean store before each test
        yield c