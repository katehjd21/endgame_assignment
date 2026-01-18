import pytest
from models import Duty, Coin, DutyCoin
import uuid

@pytest.fixture
def duties():
    duty1 = Duty.create(name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(name="Duty 2", description="Duty 2 Description")
    return [duty1, duty2]

@pytest.fixture
def coins_with_duties(duties):
    coin1 = Coin.create(name="Automate Coin")
    coin2 = Coin.create(name="Assemble Coin")
    coin3 = Coin.create(name="Going Deeper Coin")
    DutyCoin.create(duty=duties[0], coin=coin1)
    DutyCoin.create(duty=duties[0], coin=coin2)
    DutyCoin.create(duty=duties[1], coin=coin1)
    DutyCoin.create(duty=duties[1], coin=coin2)
    DutyCoin.create(duty=duties[1], coin=coin3)
    return [coin1, coin2, coin3]


# GET DUTIES

def test_get_duties_returns_all_duties(client, duties):
    response = client.get("/duties")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(data) == len(duties)
    assert isinstance(data, list)
    returned_duty_names = [returned_duty["name"] for returned_duty in data]
    for duty in duties:
        assert duty.name in returned_duty_names
    

def test_duties_have_id_name_and_description(client, duties):
    response = client.get("/duties")
    data = response.json

    for duty in data:
        assert set(duty.keys()) == {"id", "name", "description"}

def test_get_duties_returns_correct_duty_descriptions(client, duties):
    response = client.get("/duties")
    data = response.json

    duty_names = {duty["name"]: duty["description"] for duty in data}
    assert duty_names["Duty 1"] == "Duty 1 Description"
    assert duty_names["Duty 2"] == "Duty 2 Description"

def test_duties_have_non_integer_id(client, duties):
    response = client.get("/duties")
    data = response.json

    for duty in data:
        assert isinstance(duty["id"], str)
        uuid.UUID(duty["id"])

def test_get_duties_has_no_duplicates(client, duties):
    response = client.get("/duties")
    data = response.json
    duty_names = [duty["name"] for duty in data]

    assert len(duty_names) == len(set(duty_names))


# GET DUTY BY ID WITH ASSOCIATED COINS

def test_get_duty_by_id_returns_its_associated_coins(client, duties, coins_with_duties):
    duty1_id = duties[0].id
    duty1_response = client.get(f"/duties/{duty1_id}")
    duty1_coin_names = [duty1_coin["name"] for duty1_coin in duty1_response.json["coins"]]

    assert "Automate Coin" in duty1_coin_names
    assert "Assemble Coin" in duty1_coin_names
    assert "Going Deeper Coin" not in duty1_coin_names
    assert len(duty1_coin_names) == 2

    duty2_id = duties[1].id
    duty2_response = client.get(f"/duties/{duty2_id}")
    duty2_coin_names = [duty2_coin["name"] for duty2_coin in duty2_response.json["coins"]]

    assert "Automate Coin" in duty2_coin_names
    assert "Assemble Coin" in duty2_coin_names
    assert "Going Deeper Coin" in duty2_coin_names
    assert len(duty2_coin_names) == 3

def test_get_duty_by_id_returns_duty_name_and_description(client, duties, coins_with_duties):
    duty_id = duties[0].id
    response = client.get(f"/duties/{duty_id}")
    data = response.json

    assert data["name"] == "Duty 1"
    assert data["description"] == "Duty 1 Description"

def test_get_duty_by_id_only_returns_expected_fields(client, duties, coins_with_duties):
    duty_id = duties[0].id
    response = client.get(f"/duties/{duty_id}")
    data = response.json

    assert set(data.keys()) == {"id", "name", "description", "coins"}

def test_duty_coins_return_id_and_name_of_coins(client, duties, coins_with_duties):
    duty_id = duties[0].id
    response = client.get(f"/duties/{duty_id}")
    coin = response.json["coins"][0]

    assert set(coin.keys()) == {"id", "name"}

def test_get_duty_by_id_returns_400_if_invalid_id(client):
    response = client.get("/duties/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Duty ID format. Duty ID must be a UUID (non-integer)."

def test_get_duty_by_id_returns_404_if_not_found(client):
    response = client.get("/duties/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json["description"] == "Duty not found."
