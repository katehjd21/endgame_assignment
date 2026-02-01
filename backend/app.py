from flask import Flask, jsonify, abort, request
from models import Coin, Duty, Knowledge, Skill, Behaviour, DutyCoin
from utils.helper_functions import serialize_coin, serialize_coin_with_duties, serialize_duty, serialize_ksb, serialize_duty_with_coins, serialize_ksb_with_duties
from playhouse.shortcuts import model_to_dict
import uuid
import re
from pg_db_connection import pg_db, database 
import os
from peewee import DoesNotExist

database.initialize(pg_db)
app = Flask(__name__)

@app.before_request
def before_request():
    if os.getenv("TESTING"):
        return
    if pg_db.is_closed(): 
        pg_db.connect(reuse_if_open=True)

@app.teardown_request
def teardown_request(exception):
    if not os.getenv("TESTING") and not pg_db.is_closed():
        pg_db.close()

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"description": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"description": error.description}), 404


# GET COINS
@app.get("/v1/coins")
def get_coins_v1():
    coins = Coin.select()
    coins_list = [serialize_coin(coin) for coin in coins]
    return jsonify(coins_list), 200

@app.get("/v2/coins")
def get_coins_v2():
    coins = Coin.select()
    coins_list = [serialize_coin_with_duties(coin) for coin in coins]
    return jsonify(coins_list), 200


# GET COIN BY ID
@app.get("/v1/coins/<coin_id>")
def get_coin_by_id_v1(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400, description="Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    coin_dict = serialize_coin(coin)
    return jsonify(coin_dict), 200


@app.get("/v2/coins/<coin_id>")
def get_coin_by_id_v2(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400, description="Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    coin_dict = serialize_coin_with_duties(coin)
    return jsonify(coin_dict), 200


# POST COIN
@app.post("/v1/coins")
def create_coin_v1():
    data = request.json

    if not data or "name" not in data:
        abort(400, description="Missing 'name' key in request body.")

    name = data["name"].strip()

    if not name:
        abort(400, description="Coin name cannot be empty.")

    if Coin.select().where(Coin.name == name).exists():
        abort(400, description="Coin already exists. Please choose another name.")

    new_coin = Coin.create(name=name)

    new_coin_dict = serialize_coin(new_coin)
    return jsonify(new_coin_dict), 201


@app.post("/v2/coins")
def create_coin_v2():
    data = request.json

    if not data or "name" not in data:
        abort(400, description="Missing 'name' key in request body.")

    name = data["name"].strip()
    if not name:
        abort(400, description="Coin name cannot be empty.")

    if Coin.select().where(Coin.name == name).exists():
        abort(400, description="Coin already exists. Please choose another name.")

    new_coin = Coin.create(name=name)

    duty_codes = data.get("duty_codes", []) 
    for code in duty_codes:
        try:
            duty_obj = Duty.get(Duty.code == code.upper())
            DutyCoin.create(coin=new_coin, duty=duty_obj)
        except DoesNotExist:
            abort(400, description=f"Duty with code '{code}' does not exist.")

    coin_dict = serialize_coin_with_duties(new_coin)
    return jsonify(coin_dict), 201


# PATCH/UPDATE COIN
@app.patch("/v1/coins/<coin_id>")
def update_coin_v1(coin_id):
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

    coin_dict = serialize_coin(coin)
    return jsonify(coin_dict), 200


@app.patch("/v2/coins/<coin_id>")
def update_coin_v2(coin_id):
    try:
        uuid_obj = uuid.UUID(coin_id)
    except ValueError:
        abort(400, description="Invalid Coin ID format. Coin ID must be a UUID (non-integer).")

    data = request.json
    if not data:
        abort(400, description="Request body is empty.")

    name = data.get("name")
    duty_codes = data.get("duty_codes")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    if name is not None:
        name = name.strip()
        if not name:
            abort(400, description="Coin name cannot be empty.")
        coin.name = name
        coin.save()

    if duty_codes is not None:
        if not isinstance(duty_codes, list):
            abort(400, description="'duty_codes' must be a list of duty codes")
        
        DutyCoin.delete().where(DutyCoin.coin == coin).execute()

        for code in duty_codes:
            try:
                duty = Duty.get(Duty.code == code.upper())
                DutyCoin.create(duty=duty, coin=coin)
            except Duty.DoesNotExist:
                abort(400, description=f"Invalid duty code: {code}")

    coin_dict = serialize_coin_with_duties(coin)
    return jsonify(coin_dict), 200


# DELETE COIN
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

    return jsonify({"message": "Coin has been successfully deleted!"}), 200


# GET DUTIES
@app.get("/duties")
def get_duties():
    duties = Duty.select()
    duties_list = [serialize_duty(duty) for duty in duties]

    return jsonify(duties_list), 200


# GET DUTY BY CODE WITH ASSOCIATED COINS
@app.get("/duties/<duty_code>")
def get_duty_by_code(duty_code):
    duty_code = duty_code.upper()

    regex = r"^D\d+$"
    if not re.match(regex, duty_code):
        abort(400, description="Invalid Duty Code format. Duty Code must start with a 'D' (case-insensitive) followed by numbers (e.g., D7 or d7).")

    try:
        duty = Duty.get(Duty.code == duty_code)
    except Duty.DoesNotExist:
        abort(404, description="Duty not found.")

    duty_dict = serialize_duty_with_coins(duty)
    return jsonify(duty_dict), 200


# GET KSBS
@app.get("/ksbs")
def get_ksbs():
    ksbs_list = []

    for model, ksb_type in [(Knowledge, "Knowledge"), (Skill, "Skill"), (Behaviour, "Behaviour")]:
        for ksb in model.select():
            ksbs_list.append(serialize_ksb(ksb, ksb_type))

    return jsonify(ksbs_list), 200


# GET KSB BY KSB CODE WITH ASSOCIATED DUTIES
@app.get("/ksbs/<ksb_code>")
def get_ksb_by_code(ksb_code):
    ksb_code = ksb_code.upper()
    regex = r"^[KSB]\d+[a-zA-Z]?$"
    if not re.match(regex, ksb_code):
        abort(400, description="Invalid KSB Code format. KSB Code must start with 'K', 'S', or 'B', followed by numbers and optionally a letter (e.g., K1, K1a, S2, B3b).")
    
    ksb = None
    ksb_type = None

    for model, ksb_type_name in [
        (Knowledge, "Knowledge"),
        (Skill, "Skill"),
        (Behaviour, "Behaviour"),
    ]:
        try:
            ksb = model.get(model.code == ksb_code)
            ksb_type = ksb_type_name
            break
        except model.DoesNotExist:
            ksb = None

    if not ksb:
        abort(404, description="KSB not found.")

    ksb_dict = serialize_ksb_with_duties(ksb, ksb_type)
    return jsonify(ksb_dict), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)