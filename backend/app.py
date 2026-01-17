from flask import Flask, jsonify, abort
from models import Coin
from playhouse.shortcuts import model_to_dict
import uuid


app = Flask(__name__)


@app.get("/coins")
def get_coins():
    coins = Coin.select()

    coin_dicts = []
    for coin in coins:
        coin_dict = model_to_dict(coin)
        coin_dict["id"] = str(coin.id)
        coin_dicts.append(coin_dict)

    return jsonify(coin_dicts)

@app.get("/coins/<coin_id>")
def get_coin_by_id(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400)

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404)

    coin_dict = model_to_dict(coin)
    coin_dict["id"] = str(coin.id)
    return jsonify(coin_dict)


if __name__ == '__main__':
    app.run(debug=True)
