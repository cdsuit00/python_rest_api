# python_rest_api
A minimal Flask REST API + CLI for managing inventory with OpenFoodFacts (OFF) integration. Uses a temporary in-memory list (no DB) to match assignment scope.

## Features
- CRUD routes:
  - `GET /inventory`
  - `GET /inventory/<id>`
  - `POST /inventory`
  - `PATCH /inventory/<id>`
  - `DELETE /inventory/<id>`
- Helper routes:
  - `GET /inventory/search?q=...` – local name contains
  - `POST /inventory/import` – import from OFF by `barcode` or `name` then set local `price` & `stock`
- External API:
  - OFF **staging** by default (`world.openfoodfacts.net`) with Basic Auth `off/off`
  - Barcode lookup via API v2
  - Name search via v1 `search.pl`
- CLI: add/list/get/update/delete; find+import from OFF
- Tests: API, CLI, external API (pytest + unittest.mock)

## Install & Run (local venv)
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run the API (default: http://127.0.0.1:5000)
export FLASK_APP=app.py
flask run

Environment
# OFF_ENV: staging (default) or production
export OFF_ENV=staging
# For staging, basic auth is required; default off:off is used automatically.
# OFF_USER_AGENT is recommended (requests header)
export OFF_USER_AGENT="InventoryDemo/1.0 (you@example.com)"
# API_URL for CLI (default http://127.0.0.1:5000)
export API_URL="http://127.0.0.1:5000"

CLI usage
# list items
python cli.py list

# add item
python cli.py add --name "Apple" --price 1.25 --stock 10

# get item
python cli.py get <item_id>

# update price or stock
python cli.py update <item_id> --price 1.5
python cli.py update <item_id> --stock 20

# delete
python cli.py delete <item_id>

# find on OFF by barcode and import
python cli.py find-off --barcode 3017624010701 --price 3.99 --stock 6

# find on OFF by name and import (first match)
python cli.py find-off --name "nutella" --price 4.49 --stock 4