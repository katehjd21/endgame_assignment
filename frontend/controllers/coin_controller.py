from models.coin import Coin    

class CoinController():
    @staticmethod
    def fetch_all_coins():
        return Coin.list_all_coins()