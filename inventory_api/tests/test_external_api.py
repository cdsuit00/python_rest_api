import pytest
import requests
from unittest.mock import patch
from inventory_api.external_api import fetch_product_from_openfoodfacts

@patch("inventory_api.external_api.requests.get")
def test_fetch_product_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"product": {"id": "123", "name": "Test"}}
    product = fetch_product_from_openfoodfacts("123")
    assert product["id"] == "123"

@patch("inventory_api.external_api.requests.get")
def test_fetch_product_not_found(mock_get):
    mock_get.return_value.status_code = 404
    product = fetch_product_from_openfoodfacts("999")
    assert product is None