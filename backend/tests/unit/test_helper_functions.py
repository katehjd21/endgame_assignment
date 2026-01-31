import pytest
from models import Coin, Duty, DutyCoin
from utils.helper_functions import clear_tables, serialize_coin, serialize_coin_with_duties


@pytest.fixture
def populated_db():
    automate_coin = Coin.create(name="Automate")
    assemble_coin = Coin.create(name="Assemble")
    duty = Duty.create(code="D4", name="Duty 4", description="Duty 4 Description")

    return {
        "coins": [automate_coin, assemble_coin],
        "duties": [duty],
    }

@pytest.fixture
def coin():
    coin = Coin.create(name="Automate Coin")
    return coin

@pytest.fixture
def duties():
    duty1 = Duty.create(code="D1", name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(code="D2", name="Duty 2", description="Duty 2 Description")
    duty3 = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")
    return [duty1, duty2, duty3]

@pytest.fixture
def coin_with_duties(coin, duties):
    for duty in duties:
        DutyCoin.create(coin=coin, duty=duty)
    return coin


def test_clear_tables_removes_all_rows(populated_db):
    assert Coin.select().count() == 2
    assert Duty.select().count() == 1

    clear_tables()

    assert Coin.select().count() == 0
    assert Duty.select().count() == 0

def test_serialize_coin_has_id_and_name(coin):
    result = serialize_coin(coin)
    assert set(result.keys()) == {"id", "name"}

def test_serialize_coin_has_correct_coin_id_and_name(coin):
    result = serialize_coin(coin)
    assert result["id"] == str(coin.id)
    assert result["name"] == "Automate Coin"

def test_serialize_coin_with_duties_has_id_name_and_duties(coin_with_duties):
    result = serialize_coin_with_duties(coin_with_duties)
    assert set(result.keys()) == {"id", "name", "duties"}

def test_serialize_coin_with_duties_has_correct_id_name_and_duties(coin_with_duties):
    result = serialize_coin_with_duties(coin_with_duties)
    assert result["id"] == str(coin_with_duties.id)
    assert result["name"] == "Automate Coin"
    assert len(result["duties"]) == 3
    expected_duties = {(duty_coin.duty.code, duty_coin.duty.name, duty_coin.duty.description) for duty_coin in coin_with_duties.coin_duties}
    actual_duties = {(duty["code"], duty["name"], duty["description"]) for duty in result["duties"]}

    assert actual_duties == expected_duties
        

    