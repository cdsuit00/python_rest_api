from click.testing import CliRunner
from inventory_api import cli

def test_add_and_list():
    runner = CliRunner()
    runner.invoke(cli.cli, ["add", "1", "Apple", "1.5", "10"])
    result = runner.invoke(cli.cli, ["list"])
    assert "Apple" in result.output