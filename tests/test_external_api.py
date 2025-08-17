from unittest.mock import patch, Mock
import external_api as off

@patch("external_api.requests.get")
def test_fetch_product_by_barcode_success(mock_get):
    fake = Mock()
    fake.raise_for_status.return_value = None
    fake.json.return_value = {"product": {"product_name": "Test", "brands": "BrandX", "code": "123"}}
    mock_get.return_value = fake

    data = off.fetch_product_by_barcode("123")
    assert data["name"] == "Test"
    assert data["brands"] == "BrandX"
    assert data["code"] == "123"

@patch("external_api.requests.get")
def test_search_products_by_name_success(mock_get):
    fake = Mock()
    fake.raise_for_status.return_value = None
    fake.json.return_value = {
        "products": [
            {"product_name": "Alpha", "brands": "A", "code": "111"},
            {"product_name": "Beta", "brands": "B", "code": "222"},
        ]
    }
    mock_get.return_value = fake
    res = off.search_products_by_name("something", limit=1)
    assert len(res) == 1
    assert res[0]["name"] == "Alpha"

def test_fetch_product_by_barcode_input_validation():
    try:
        off.fetch_product_by_barcode("")
    except off.ExternalAPIError as e:
        assert "barcode" in str(e).lower()