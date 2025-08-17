import pytest
from inventory_api.app import app
from inventory_api.storage import reset_storage

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            reset_storage()
        yield client