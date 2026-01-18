import pytest
from models import Coin
import uuid

@pytest.fixture
def coins():
    coin_names = [
        "Automate",
        "Assemble",
        "Houston, Prepare to Launch!",
        "Going Deeper",
        "Call Security",
    ]
    coins = []
    for name in coin_names:
        coins.append(Coin.create(name=name))

    return coins


# GET COINS

def test_get_coins(client, coins):
    response = client.get("/coins")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(data) == len(coins)
    assert isinstance(data, list)
    returned_coin_names = [returned_coin["name"] for returned_coin in data]
    for coin in coins:
        assert coin.name in returned_coin_names

def test_coins_have_id_and_name(client, coins):
    response = client.get("/coins")
    data = response.json

    for coin in data:
        assert "id" in coin
        assert "name" in coin

def test_coins_have_non_integer_id(client, coins):
    response = client.get("/coins")
    data = response.json

    for coin in data:
        assert isinstance(coin["id"], str)
        uuid.UUID(coin["id"])

def test_get_coins_has_no_duplicates(client, coins):
    response = client.get("/coins")
    data = response.json
    coin_names = [coin["name"] for coin in data]

    assert len(coin_names) == len(set(coin_names))


# GET COIN BY ID

def test_get_coin_by_id(client, coins):
    coin_id = coins[0].id
    response = client.get(f"/coins/{coin_id}")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert data["id"] == str(coin_id)
    assert data["name"] == coins[0].name


def test_get_coin_by_id_not_found(client):
    response = client.get("/coins/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."

def test_get_coin_by_id_invalid_uuid(client):
    response = client.get("/coins/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."

def test_get_coin_by_id_only_returns_id_and_name(client, coins):
    coin_id = coins[0].id
    response = client.get(f"/coins/{coin_id}")
    data = response.json

    assert "id" in data
    assert "name" in data
    assert len(data) == 2

def test_get_coin_by_id_returns_correct_coin(client, coins):
    coin_id = coins[2].id
    response = client.get(f"/coins/{coin_id}")
    data = response.json

    assert data["name"] == coins[2].name


# POST COIN

def test_post_coin_creates_coin(client):
    response = client.post("/coins", json={"name": "New Coin"})
    data = response.json

    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert data["name"] == "New Coin"
    uuid.UUID(data["id"])

def test_post_coin_returns_400_if_name_key_missing(client):
    response = client.post("/coins", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Missing 'name' key in request body."

def test_post_coin_returns_400_if_missing_coin_name(client):
    response = client.post("/coins", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."

def test_post_coin_returns_400_if_name_is_whitespace(client):
    response = client.post("/coins", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."

def test_post_coin_returns_400_if_duplicate_coin_name(client, coins):
    response = client.post("/coins", json={"name": "Automate"})

    assert response.status_code == 400
    assert response.json["description"] == "Coin already exists. Please choose another name."


# PATCH/UPDATE COIN

def test_patch_coin_updates_coin_name(client, coins):
    coin_id = coins[0].id
    response = client.patch(f"/coins/{coin_id}", json={"name": "Updated Coin Name"})
    data = response.json

    assert response.status_code == 200
    assert data["name"] == "Updated Coin Name"    

def test_patch_coin_returns_400_if_missing_name_key(client, coins):
    coin_id = coins[0].id
    response = client.patch(f"/coins/{coin_id}", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Missing 'name' key in request body."

def test_patch_coin_returns_400_if_name_is_whitespace(client, coins):
    coin_id = coins[0].id
    response = client.patch(f"/coins/{coin_id}", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_patch_returns_400_if_coin_name_empty(client, coins):
    coin_id = coins[0].id
    response = client.patch(f"/coins/{coin_id}", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."

def test_patch_coin_returns_400_if_invalid_id(client):
    response = client.patch("/coins/invalid_id", json={"name": "Updated Coin Name"})

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."

def test_patch_coin_returns_404_if_not_found(client):
    response = client.patch("/coins/00000000-0000-0000-0000-000000000000", json={"name": "Updated Coin Name"})

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."

   
# DELETE COIN

def test_delete_coin_removes_coin_from_database(client, coins):
    coin_id = coins[4].id
    response = client.delete(f"/coins/{coin_id}")

    assert response.status_code == 204

    get_response = client.get(f"/coins/{coin_id}")
    assert get_response.status_code == 404

def test_delete_coin_returns_400_if_invalid_id(client):
    response = client.delete("/coins/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == ("Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

def test_delete_coin_returns_404_if_not_found(client):
    response = client.delete("/coins/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."