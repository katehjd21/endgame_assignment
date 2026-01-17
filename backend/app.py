from flask import Flask, jsonify
from models import Coin
from pg_db_connection import pg_db
from playhouse.shortcuts import model_to_dict


app = Flask(__name__)


@app.get("/coins")
def get_coins():
    coins = Coin.select()

    coin_dicts = []
    for coin in coins:
        coin_dict = model_to_dict(coin)
        coin_dict["id"] = str(coin_dict["id"])
        coin_dicts.append(coin_dict)

    return jsonify(coin_dicts)



if __name__ == '__main__':
    app.run(debug=True)
