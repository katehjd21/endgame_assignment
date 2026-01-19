from flask import Flask, jsonify, abort, request
from models import Coin, Duty, Knowledge, Skill, Behaviour
from playhouse.shortcuts import model_to_dict
import uuid


app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"description": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"description": error.description}), 404


# COINS
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


@app.delete("/coins/<coin_id>")
def delete_coin(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(
            400,
            description="Invalid Coin ID format. Coin ID must be a UUID (non-integer)."
        )

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    coin.delete_instance()

    return "", 204


# GET DUTIES
@app.get("/duties")
def get_duties():
    duties = Duty.select()

    duty_dicts = []
    for duty in duties:
        duty_dict = model_to_dict(duty)
        duty_dict["id"] = str(duty_dict["id"])
        duty_dicts.append(duty_dict)

    return jsonify(duty_dicts), 200

# GET DUTY BY ID WITH ASSOCIATED COINS
@app.get("/duties/<duty_id>")
def get_duty_by_id(duty_id):
    try:
        uuid_obj = uuid.UUID(duty_id)
    except ValueError:
        abort(400, description="Invalid Duty ID format. Duty ID must be a UUID (non-integer).")

    try:
        duty = Duty.get_by_id(uuid_obj)
    except Duty.DoesNotExist:
        abort(404, description="Duty not found.")

    duty_dict = model_to_dict(duty)
    duty_dict["id"] = str(duty.id)

    coins = []
    for duty_coin in duty.duty_coins:
        coins.append({"id": str(duty_coin.coin.id), "name": duty_coin.coin.name})

    duty_dict["coins"] = coins

    return jsonify(duty_dict), 200

# GET KSBS
@app.get("/ksbs")
def get_ksbs():
    knowledges = Knowledge.select()
    skills = Skill.select()
    behaviours = Behaviour.select()

    ksbs = []

    for knowledge in knowledges:
        knowledge_dict = model_to_dict(knowledge)
        knowledge_dict["id"] = str(knowledge.id)
        knowledge_dict["type"] = "Knowledge"
        ksbs.append(knowledge_dict)

    for skill in skills:
        skill_dict = model_to_dict(skill)
        skill_dict["id"] = str(skill.id)
        skill_dict["type"] = "Skill"
        ksbs.append(skill_dict)

    for behaviour in behaviours:
        behaviour_dict = model_to_dict(behaviour)
        behaviour_dict["id"] = str(behaviour.id)
        behaviour_dict["type"] = "Behaviour"
        ksbs.append(behaviour_dict)

    return jsonify(ksbs), 200


if __name__ == '__main__':
    app.run(debug=True)
