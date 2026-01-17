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


# GET COINS BY ID

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

def test_get_coin_by_id_invalid_uuid(client):
    response = client.get("/coins/invalid_id")
    assert response.status_code == 400

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