def test_post_and_get_item(client):
    res = client.post("/inventory", json={"id": "1", "name": "Apple", "price": 1.5, "stock": 10})
    assert res.status_code == 201

    res = client.get("/inventory/1")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Apple"

def test_patch_item(client):
    client.post("/inventory", json={"id": "1", "name": "Apple", "price": 1.5, "stock": 10})
    res = client.patch("/inventory/1", json={"price": 2.0})
    assert res.status_code == 200
    assert res.get_json()["price"] == 2.0

def test_delete_item(client):
    client.post("/inventory", json={"id": "1", "name": "Apple", "price": 1.5, "stock": 10})
    res = client.delete("/inventory/1")
    assert res.status_code == 200