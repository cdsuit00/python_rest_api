# python_rest_api
A simple Flask REST API and CLI tool to manage an in-memory inventory.  
Supports adding items, listing items, deleting items, and fetching product details from the OpenFoodFacts API.

---

## Installation & Setup

1. Clone this repository and navigate inside:

  git clone git@github.com:cdsuit00/python_rest_api.git
  cd inventory_api

2. Create and activate a virtual environment:

  python3 -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows

3. Install dependencies:
  pip install -r requirements.txt

4. Running the Flask API
   flask --app inventory_api.app run -- By default it runs on: http://127.0.0.1:5000



API Endpoints

GET /inventory → List all items
POST /inventory → Add a new item
GET /inventory/<id> → Get item by ID
DELETE /inventory/<id> → Delete item by ID
POST /inventory/fetch/<barcode> → Fetch product from OpenFoodFacts and add it to inventory


Using the CLI

python -m inventory_api.cli [command] [options]

Available Commands

list → Show all items
add <id> <name> <brand> [--price <price>] [--stock <stock>]
get <id> → Get item by ID
delete <id> → Remove item by ID
find <barcode> → Fetch from OpenFoodFacts and add to inventory

Examples
# Add an item manually
python -m inventory_api.cli add 101 "Chips" "SnackCo" --price 2.99 --stock 5

# List items
python -m inventory_api.cli list

# Fetch from OpenFoodFacts by barcode
python -m inventory_api.cli find 737628064502

