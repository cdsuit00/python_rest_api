inventory = []

def find_item_by_id(item_id: str):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def reset_storage():
    inventory.clear()