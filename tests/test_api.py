def test_post_and_get_roundtrip(client):
    # create
    r = client.post("/inventory", json={"name": "Apple", "price": 1.25, "stock": 10})
    assert r.status_code == 201
    item = r.get_json()
    # list
    r = client.get("/inventory")
    assert r.status_code == 200
    items = r.get_json()
    assert any(i["id"] == item["id"] for i in items)
    # get single
    r = client.get(f"/inventory/{item['id']}")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Apple"

def test_patch_update_and_delete(client):
    # seed
    created = client.post("/inventory", json={"name": "Milk", "price": 2.0, "stock": 5}).get_json()
    # patch price
    r = client.patch(f"/inventory/{created['id']}", json={"price": 2.5})
    assert r.status_code == 200
    assert r.get_json()["price"] == 2.5
    # patch stock
    r = client.patch(f"/inventory/{created['id']}", json={"stock": 9})
    assert r.status_code == 200
    assert r.get_json()["stock"] == 9
    # delete
    r = client.delete(f"/inventory/{created['id']}")
    assert r.status_code == 200
    # ensure gone
    r = client.get(f"/inventory/{created['id']}")
    assert r.status_code == 404

def test_invalid_inputs(client):
    r = client.post("/inventory", json={"name": "Bad", "price": "free", "stock": "a lot"})
    assert r.status_code == 400
    r = client.patch("/inventory/not-found", json={"price": 1})
    assert r.status_code == 404
    r = client.patch("/inventory/anything", json={})
    # item doesn't exist, so first ensure it
    created = client.post("/inventory", json={"name": "Ok", "price": 1, "stock": 1}).get_json()
    r = client.patch(f"/inventory/{created['id']}", json={})
    assert r.status_code == 400

def test_helper_search_local(client):
    client.post("/inventory", json={"name": "Banana Chips", "price": 3.4, "stock": 3})
    client.post("/inventory", json={"name": "Chocolate Bar", "price": 2.1, "stock": 5})
    r = client.get("/inventory/search?q=bar")
    assert r.status_code == 200
    names = [x["name"].lower() for x in r.get_json()]
    assert "chocolate bar" in names