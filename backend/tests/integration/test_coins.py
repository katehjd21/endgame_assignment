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
    data = response.get_json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert len(data) == len(coins)
    assert isinstance(data, list)
    returned_coin_names = [returned_coin["name"] for returned_coin in data]
    for coin in coins:
        assert coin.name in returned_coin_names

def test_coins_have_id_and_name(client, coins):
    response = client.get("/coins")
    data = response.get_json()

    for coin in data:
        assert "id" in coin
        assert "name" in coin

def test_coins_have_non_integer_id(client, coins):
    response = client.get("/coins")
    data = response.get_json()

    for coin in data:
        assert isinstance(coin["id"], str)
        uuid.UUID(coin["id"])

def test_get_coins_has_no_duplicates(client, coins):
    response = client.get("/coins")
    data = response.get_json()
    coin_names = [coin["name"] for coin in data]
    assert len(coin_names) == len(set(coin_names))