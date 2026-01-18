from flask import Flask, jsonify, abort, request
from models import Coin
from playhouse.shortcuts import model_to_dict
import uuid


app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"description": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"description": error.description}), 404


@app.get("/coins")
def get_coins():
    coins = Coin.select()

    coin_dicts = []
    for coin in coins:
        coin_dict = model_to_dict(coin)
        coin_dict["id"] = str(coin_dict["id"])
        coin_dicts.append(coin_dict)

    return jsonify(coin_dicts), 200


@app.get("/coins/<coin_id>")
def get_coin_by_id(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400, description="Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    coin_dict = model_to_dict(coin)
    coin_dict["id"] = str(coin.id)
    return jsonify(coin_dict), 200


@app.post("/coins")
def create_coin():
    data = request.json

    if not data or "name" not in data:
        abort(400, description="Missing 'name' key in request body.")

    name = data["name"].strip()

    if not name:
        abort(400, description="Coin name cannot be empty.")

    if Coin.select().where(Coin.name == name).exists():
        abort(400, description="Coin already exists. Please choose another name.")

    new_coin = Coin.create(name=name)

    new_coin_dict = model_to_dict(new_coin)
    new_coin_dict["id"] = str(new_coin_dict["id"])

    return jsonify(new_coin_dict), 201


@app.patch("/coins/<coin_id>")
def update_coin(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400, description="Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

    data = request.json
    if not data or "name" not in data:
        abort(400, description="Missing 'name' key in request body.")

    name = data["name"].strip()
    if not name:
        abort(400, description="Coin name cannot be empty.")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    coin.name = name
    coin.save()

    coin_dict = model_to_dict(coin)
    coin_dict["id"] = str(coin_dict["id"])
    return jsonify(coin_dict), 200


if __name__ == '__main__':
    app.run(debug=True)
