from flask import Flask, jsonify, request
from inventory_api.storage import inventory, find_item_by_id, reset_storage
from inventory_api.external_api import fetch_product_from_openfoodfacts

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Inventory API. Use /inventory to get started."})

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
    data = request.get_json()
    if not data or "id" not in data:
        return jsonify({"error": "Invalid input"}), 400
    inventory.append(data)
    return jsonify(data), 201

@app.route("/inventory/<item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    item.update(data)
    return jsonify(item), 200

@app.route("/inventory/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200

@app.route("/inventory/fetch/<barcode>", methods=["GET"])
def fetch_from_external(barcode):
    product = fetch_product_from_openfoodfacts(barcode)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)