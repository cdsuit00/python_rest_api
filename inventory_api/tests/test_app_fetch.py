import pytest
from unittest.mock import patch
from inventory_api.app import app
from inventory_api.storage import reset_storage, inventory


@pytest.fixture(autouse=True)
def run_around_tests():
    reset_storage()
    yield
    reset_storage()


@patch("inventory_api.app.fetch_product_from_openfoodfacts")
def test_fetch_and_add_success(mock_fetch):
    mock_fetch.return_value = {
        "id": "12345",
        "name": "Mock Cola",
        "brand": "MockBrand",
        "price": 0.0,
        "stock": 0
    }

    client = app.test_client()
    response = client.post("/inventory/fetch/12345")

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Mock Cola"
    assert len(inventory) == 1


@patch("inventory_api.app.fetch_product_from_openfoodfacts")
def test_fetch_and_add_not_found(mock_fetch):
    mock_fetch.return_value = None

    client = app.test_client()
    response = client.post("/inventory/fetch/00000")

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert len(inventory) == 0