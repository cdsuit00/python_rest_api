import pytest
from unittest.mock import patch
from click.testing import CliRunner
from inventory_api.cli import cli
from inventory_api.storage import reset_storage, inventory


@pytest.fixture(autouse=True)
def run_around_tests():
    reset_storage()
    yield
    reset_storage()


@patch("inventory_api.cli.fetch_product_from_openfoodfacts")
def test_cli_find_success(mock_fetch):
    mock_fetch.return_value = {
        "id": "12345",
        "name": "CLI Chips",
        "brand": "CLIbrand",
        "price": 0.0,
        "stock": 0
    }

    runner = CliRunner()
    result = runner.invoke(cli, ["find", "12345"])

    assert result.exit_code == 0
    assert "Added CLI Chips" in result.output
    assert len(inventory) == 1


@patch("inventory_api.cli.fetch_product_from_openfoodfacts")
def test_cli_find_not_found(mock_fetch):
    mock_fetch.return_value = None

    runner = CliRunner()
    result = runner.invoke(cli, ["find", "00000"])

    assert result.exit_code == 0
    assert "Product not found" in result.output
    assert len(inventory) == 0