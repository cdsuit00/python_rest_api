import click
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

@click.group()
def cli():
    """CLI for Inventory Management API"""

@cli.command("list")
def list_items():
    r = requests.get(f"{API_URL}/inventory", timeout=10)
    click.echo(r.json())

@cli.command("add")
@click.option("--name", prompt=True)
@click.option("--price", prompt=True, type=float)
@click.option("--stock", prompt=True, type=int)
def add_item(name, price, stock):
    r = requests.post(f"{API_URL}/inventory", json={"name": name, "price": price, "stock": stock}, timeout=10)
    click.echo(r.status_code)
    click.echo(r.json())

@cli.command("get")
@click.argument("item_id")
def get_item(item_id):
    r = requests.get(f"{API_URL}/inventory/{item_id}", timeout=10)
    click.echo(r.status_code)
    click.echo(r.json())

@cli.command("update")
@click.argument("item_id")
@click.option("--price", type=float)
@click.option("--stock", type=int)
def update_item(item_id, price, stock):
    payload = {}
    if price is not None: payload["price"] = price
    if stock is not None: payload["stock"] = stock
    r = requests.patch(f"{API_URL}/inventory/{item_id}", json=payload, timeout=10)
    click.echo(r.status_code)
    click.echo(r.json())

@cli.command("delete")
@click.argument("item_id")
def delete_item(item_id):
    r = requests.delete(f"{API_URL}/inventory/{item_id}", timeout=10)
    click.echo(r.status_code)
    click.echo(r.json())

@cli.command("find-off")
@click.option("--barcode", help="Product barcode")
@click.option("--name", help="Product name")
@click.option("--price", type=float, required=True, help="Price to set in inventory")
@click.option("--stock", type=int, required=True, help="Stock to set in inventory")
def find_off(barcode, name, price, stock):
    """Find item on OpenFoodFacts and import it into local inventory."""
    if not barcode and not name:
        raise click.ClickException("Provide --barcode or --name.")
    r = requests.post(
        f"{API_URL}/inventory/import",
        json={"barcode": barcode, "name": name, "price": price, "stock": stock},
        timeout=15,
    )
    click.echo(r.status_code)
    click.echo(r.json())

if __name__ == "__main__":
    cli()