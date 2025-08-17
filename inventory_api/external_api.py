import requests

def fetch_product_from_openfoodfacts(barcode: str):
    url = f"https://world.openfoodfacts.net/api/v2/product/{barcode}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if "product" in data:
                return data["product"]
        return None
    except requests.RequestException:
        return None