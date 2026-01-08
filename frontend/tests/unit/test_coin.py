import pytest
from models.coin import Coin

@pytest.fixture
def coin():
    return Coin("Houston")

def test_coin_has_name(coin):
    assert coin.name == 'Houston'

def test_coin_can_list_all_coins(coin):
    list_of_coins = coin.list_all_coins()
    expected_coin_names = ["Automate", "Houston", "Security", "GoingDeeper", "Assemble"]
    actual_coin_names = []
    for coin in list_of_coins:
        actual_coin_names.append(coin.name)
    
    assert len(list_of_coins) == len(expected_coin_names)
    assert actual_coin_names == expected_coin_names
    
