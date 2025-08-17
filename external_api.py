import os
import base64
import requests

# Default to STAGING. Can override with OFF_ENV=production.
OFF_ENV = os.getenv("OFF_ENV", "staging").lower()
USER_AGENT = os.getenv("OFF_USER_AGENT", "InventoryAPI/1.0 (blackace0011@gmail.com)")

# API v2 for product by barcode. For name search, v1 search endpoint.
BASE_PROD = "https://world.openfoodfacts.net" if OFF_ENV == "staging" else "https://world.openfoodfacts.org"
API_V2 = f"{BASE_PROD}/api/v2"
SEARCH_V1 = f"{BASE_PROD}/cgi/search.pl"

# Staging requires http basic auth off/off (per official docs).
# You may set OFF_BASIC_AUTH="user:pass" to override if needed.
DEFAULT_STAGING_CREDS = "off:off"
BASIC_AUTH = os.getenv("OFF_BASIC_AUTH", DEFAULT_STAGING_CREDS if OFF_ENV == "staging" else "")

class ExternalAPIError(Exception):
    pass

def _headers():
    headers = {"User-Agent": USER_AGENT}
    if OFF_ENV == "staging" and BASIC_AUTH:
        b64 = base64.b64encode(BASIC_AUTH.encode()).decode()
        headers["Authorization"] = f"Basic {b64}"
    return headers

def fetch_product_by_barcode(barcode: str) -> dict:
    """Return minimal normalized fields for a single product via API v2."""
    if not barcode:
        raise ExternalAPIError("barcode required")
    url = f"{API_V2}/product/{barcode}.json"
    try:
        r = requests.get(url, headers=_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise ExternalAPIError(str(e)) from e

    product = data.get("product") or {}
    if not product:
        raise ExternalAPIError("Product not found")
    return {
        "name": product.get("product_name"),
        "brands": product.get("brands"),
        "code": product.get("code") or barcode,
        "categories": product.get("categories"),
    }

def search_products_by_name(name: str, limit: int = 5) -> list[dict]:
    """
    Use v1 search for full-text name search:
    /cgi/search.pl?search_terms=...&search_simple=1&action=process&json=1
    Returns a list of minimal normalized product dicts.
    """
    if not name:
        raise ExternalAPIError("name required")
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
        # tip: add nocache=1 if you need fresh results
    }
    try:
        r = requests.get(SEARCH_V1, params=params, headers=_headers(), timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        raise ExternalAPIError(str(e)) from e

    prods = []
    for p in data.get("products", [])[:limit]:
        prods.append({
            "name": p.get("product_name"),
            "brands": p.get("brands"),
            "code": p.get("code"),
            "categories": p.get("categories"),
        })
    return prods