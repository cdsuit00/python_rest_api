from flask import Flask, jsonify, request
from storage import inventory, find_item_by_id, reset_storage
from external_api import (
    fetch_product_by_barcode,
    search_products_by_name,
    ExternalAPIError,
)
import uuid

app = Flask(__name__)

# ---------- CRUD routes ----------

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not isinstance(name, str) or not isinstance(price, (int, float)) or not isinstance(stock, int):
        return jsonify({"error": "Invalid input. Expect name:str, price:number, stock:int"}), 400

    new_item = {
        "id": str(uuid.uuid4()),
        "name": name.strip(),
        "price": float(price),
        "stock": int(stock),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@app.route("/inventory/<item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True) or {}
    updated = False
    if "price" in data:
        try:
            item["price"] = float(data["price"])
            updated = True
        except (TypeError, ValueError):
            return jsonify({"error": "price must be a number"}), 400
    if "stock" in data:
        try:
            item["stock"] = int(data["stock"])
            updated = True
        except (TypeError, ValueError):
            return jsonify({"error": "stock must be an integer"}), 400

    if not updated:
        return jsonify({"error": "No valid fields to update (price, stock)"}), 400
    return jsonify(item), 200

@app.route("/inventory/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200

# ---------- helper routes ----------

@app.route("/inventory/search", methods=["GET"])
def search_inventory_local():
    """Simple local name contains match."""
    q = (request.args.get("q") or "").strip().lower()
    results = [i for i in inventory if q in i["name"].lower()]
    return jsonify(results), 200

@app.route("/inventory/import", methods=["POST"])
def import_from_off():
    """
    Import an item from OpenFoodFacts (staging by default) by barcode or name.
    - If barcode is provided, fetch a single product.
    - If name is provided, take the first match from search.
    """
    data = request.get_json(silent=True) or {}
    barcode = (data.get("barcode") or "").strip()
    name = (data.get("name") or "").strip()
    price = data.get("price")
    stock = data.get("stock")

    # Basic validation for price/stock because we add to inventory
    if not isinstance(price, (int, float)) or not isinstance(stock, int):
        return jsonify({"error": "Invalid input. Expect price:number and stock:int"}), 400

    try:
        if barcode:
            prod = fetch_product_by_barcode(barcode)
        elif name:
            results = search_products_by_name(name, limit=1)
            if not results:
                return jsonify({"error": "No products found for that name"}), 404
            prod = results[0]
        else:
            return jsonify({"error": "Provide either 'barcode' or 'name'"}), 400
    except ExternalAPIError as e:
        return jsonify({"error": f"OpenFoodFacts error: {e}"}), 502

    item = {
        "id": str(uuid.uuid4()),
        "name": prod.get("name") or "Unknown",
        "brand": prod.get("brands") or "",
        "barcode": prod.get("code") or "",
        "price": float(price),
        "stock": int(stock),
    }
    inventory.append(item)
    return jsonify(item), 201

# Utility only for tests/demo
@app.route("/_admin/reset", methods=["POST"])
def _admin_reset():
    reset_storage()
    return jsonify({"ok": True}), 200

if __name__ == "__main__":
    # for local dev convenience
    app.run(debug=True)