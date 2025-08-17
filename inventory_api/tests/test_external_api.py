import pytest
from unittest.mock import patch
from inventory_api.external_api import fetch_product_from_openfoodfacts


@patch("inventory_api.external_api.requests.get")
def test_fetch_product_success(mock_get):
    # Fake API JSON response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "product": {
            "product_name": "Test Chips",
            "brands": "TestBrand"
        }
    }

    product = fetch_product_from_openfoodfacts("12345")

    assert product["id"] == "12345"
    assert product["name"] == "Test Chips"
    assert product["brand"] == "TestBrand"
    assert product["price"] == 0.0
    assert product["stock"] == 0


@patch("inventory_api.external_api.requests.get")
def test_fetch_product_not_found(mock_get):
    # Simulate API returns no product
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {}

    product = fetch_product_from_openfoodfacts("99999")
    assert product is None