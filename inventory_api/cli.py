import click
from inventory_api.storage import inventory, find_item_by_id

@click.group()
def cli():
    """Inventory CLI - Manage products from the command line."""
    pass

@cli.command()
@click.argument("item_id")
@click.argument("name")
@click.argument("price", type=float)
@click.argument("stock", type=int)
def add(item_id, name, price, stock):
    """Add a new item to the inventory."""
    inventory.append({"id": item_id, "name": name, "price": price, "stock": stock})
    click.echo(f"Added {name} with ID {item_id}")

@cli.command()
def list():
    """List all inventory items."""
    if not inventory:
        click.echo("Inventory is empty.")
    for item in inventory:
        click.echo(item)

@cli.command()
@click.argument("item_id")
@click.option("--price", type=float, help="New price")
@click.option("--stock", type=int, help="New stock")
def update(item_id, price, stock):
    """Update price or stock for an item."""
    item = find_item_by_id(item_id)
    if not item:
        click.echo("Item not found.")
        return
    if price is not None:
        item["price"] = price
    if stock is not None:
        item["stock"] = stock
    click.echo(f"Updated item {item_id}")

@cli.command()
@click.argument("item_id")
def delete(item_id):
    """Delete an item from the inventory."""
    global inventory
    new_inv = [i for i in inventory if i["id"] != item_id]
    if len(new_inv) == len(inventory):
        click.echo("Item not found.")
    else:
        inventory[:] = new_inv
        click.echo(f"Deleted item {item_id}")

if __name__ == "__main__":
    cli()