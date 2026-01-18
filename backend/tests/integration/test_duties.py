import pytest
from models import Duty, Coin, DutyCoin
import uuid

@pytest.fixture
def duties():
    duty1 = Duty.create(name="Duty 1")
    duty2 = Duty.create(name="Duty 2")
    return [duty1, duty2]

@pytest.fixture
def coins_with_duties(duties):
    coin = Coin.create(name="Automate Coin")
    DutyCoin.create(duty=duties[0], coin=coin)
    DutyCoin.create(duty=duties[1], coin=coin)
    return coin


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
    

def test_duties_have_id_and_name(client, duties):
    response = client.get("/duties")
    data = response.json

    for duty in data:
        assert "id" in duty
        assert "name" in duty

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