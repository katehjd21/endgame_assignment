import pytest
from models.coin import Coin
from controllers.coin_controller import CoinController

@pytest.fixture
def list_of_coins():
    return [
            Coin("Automate"),
            Coin("Houston"),
            Coin("Security"),
            Coin("GoingDeeper"),
            Coin("Assemble")
        ]

@pytest.fixture
def coin_controller():
    return CoinController()

def test_coin_controller_can_fetch_all_coins(mocker, list_of_coins, coin_controller):
    mocked_list_all_coins = mocker.patch("models.coin.Coin.list_all_coins", return_value=list_of_coins)
    fetched_coins = coin_controller.fetch_all_coins()
    assert mocked_list_all_coins.call_count == 1
    assert fetched_coins == list_of_coins
    assert fetched_coins[0].name == "Automate"
    assert fetched_coins[1].name == "Houston"
    assert fetched_coins[2].name == "Security"
    assert fetched_coins[3].name == "GoingDeeper"
    assert fetched_coins[4].name == "Assemble"