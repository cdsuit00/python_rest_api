from click.testing import CliRunner
import cli
from unittest.mock import patch

API = "http://127.0.0.1:5000"

def test_cli_add_and_list(monkeypatch):
    runner = CliRunner()

    class FakeResp:
        def __init__(self, status_code=201, payload=None):
            self.status_code = status_code
            self._payload = payload or {}
        def json(self):
            return self._payload

    # mock requests.post for add
    with patch("cli.requests.post") as mpost, patch("cli.requests.get") as mget:
        mpost.return_value = FakeResp(201, {"id": "1", "name": "Apple", "price": 1.2, "stock": 10})
        mget.return_value = FakeResp(200, [{"id": "1", "name": "Apple", "price": 1.2, "stock": 10}])

        res = runner.invoke(cli.add_item, input="Apple\n1.2\n10\n")
        assert res.exit_code == 0
        out = res.output
        assert "201" in out

        res = runner.invoke(cli.list_items)
        assert res.exit_code == 0
        assert "Apple" in res.output

def test_cli_find_off_by_barcode():
    runner = CliRunner()

    class FakeResp:
        def __init__(self, status_code=201, payload=None):
            self.status_code = status_code
            self._payload = payload or {}
        def json(self):
            return self._payload

    with patch("cli.requests.post") as mpost:
        mpost.return_value = FakeResp(201, {"id": "xyz", "name": "Imported", "barcode": "123"})
        res = runner.invoke(cli.find_off, ["--barcode", "123", "--price", "2.5", "--stock", "3"])
        assert res.exit_code == 0
        assert "201" in res.output
        assert "Imported" in res.output