from models import Coin, Duty, DutyCoin
from pg_db_connection import pg_db
from backend.utils.helper_functions import clear_tables
import pytest
import uuid
from peewee import IntegrityError

@pytest.fixture(autouse=True)
def clean_db():
    clear_tables()

@pytest.fixture
def coin_with_single_duty():

    coin = Coin.create(name="Automate Coin")
    duty = Duty.create(name="Duty 1")
    DutyCoin.create(duty=duty, coin=coin)

    return coin

@pytest.fixture
def coin_with_multiple_duties():

    coin = Coin.create(name="Automate Coin")
    duties = [
        Duty.create(name="Duty 1"),
        Duty.create(name="Duty 2"),
        Duty.create(name="Duty 3"),
    ]

    for duty in duties:
        DutyCoin.create(duty=duty, coin=coin)

    return coin


def test_coin_creation(coin_with_single_duty):
    coin = coin_with_single_duty
    assert coin.name == "Automate Coin"


def test_coin_has_one_duty(coin_with_single_duty):
    coin = coin_with_single_duty
    duties = []
    for duty_coin in coin.coin_duties:
        duties.append(duty_coin.duty)
    assert len(duties) == 1
    assert duties[0].name == "Duty 1"


def test_coin_has_multiple_duties(coin_with_multiple_duties):
    coin = coin_with_multiple_duties
    duties = []
    for duty_coin in coin.coin_duties:
        duties.append(duty_coin.duty)
    assert len(duties) == 3
    assert duties[0].name == "Duty 1"
    assert duties[1].name == "Duty 2"
    assert duties[2].name == "Duty 3"


def test_multiple_coins_can_have_same_duty():
    duty = Duty.create(name="Duty 4")
    assembleCoin = Coin.create(name="Assemble Coin")
    securityCoin = Coin.create(name="Security Coin")
    
    DutyCoin.create(duty=duty, coin=assembleCoin)
    DutyCoin.create(duty=duty, coin=securityCoin)
    
    assert len(list(assembleCoin.coin_duties)) == 1
    assert len(list(securityCoin.coin_duties)) == 1
    
    assert len(list(duty.duty_coins)) == 2

    coin_names = []
    for duty_coin in duty.duty_coins:
        coin_names.append(duty_coin.coin.name)
    assert "Assemble Coin" in coin_names
    assert "Security Coin" in coin_names


def test_coin_id_is_non_integer(coin_with_single_duty):
    coin = coin_with_single_duty
    assert isinstance(coin.id, uuid.UUID)


def test_coin_name_is_unique():
    Coin.create(name="Automate Coin")
    with pytest.raises(IntegrityError):
        Coin.create(name="Automate Coin")


def test_duplicate_coin_duty():
    duty = Duty.create(name="Duty 1")
    coin = Coin.create(name="Automate Coin")
    
    DutyCoin.create(duty=duty, coin=coin)

    with pytest.raises(IntegrityError):
        DutyCoin.create(duty=duty, coin=coin)


def test_update_coin_name(coin_with_single_duty):
    coin = coin_with_single_duty
    coin.name = "Updated Coin Name"
    coin.save()
    updated_coin = Coin.get_by_id(coin.id)
    assert updated_coin.name == "Updated Coin Name"


def test_deleting_coin_cleans_dutycoin_junction_table():
    duty = Duty.create(name="Duty 4")
    coin = Coin.create(name="Going Deeper Coin")
    DutyCoin.create(duty=duty, coin=coin)
    
    coin.delete_instance(recursive=True)  
    
    assert Coin.select().where(Coin.id == coin.id).count() == 0
    assert Duty.select().where(Duty.id == duty.id).count() == 1
    assert DutyCoin.select().where(DutyCoin.coin == coin.id).count() == 0

