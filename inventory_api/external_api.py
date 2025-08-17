import requests

def fetch_product_from_openfoodfacts(barcode: str):
    """Fetch product details from OpenFoodFacts API using barcode."""
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"
    resp = requests.get(url, timeout=5)

    if resp.status_code != 200:
        return None

    data = resp.json()
    if "product" not in data:
        return None

    product = data["product"]
    return {
        "id": barcode,
        "name": product.get("product_name", "Unknown Product"),
        "brand": product.get("brands", "Unknown Brand"),
        "price": 0.0,   # default until updated
        "stock": 0      # default until updated
    }