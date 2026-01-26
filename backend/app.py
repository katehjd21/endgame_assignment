from flask import Flask, jsonify, abort, request
from models import Coin, Duty, Knowledge, Skill, Behaviour, DutyCoin
from playhouse.shortcuts import model_to_dict
import uuid
import re


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

    duties = []
    for duty_coin in coin.coin_duties:
        duties.append({"id": str(duty_coin.duty.id), "name": duty_coin.duty.name})

    coin_dict["duties"] = duties

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

    duty_ids = data.get("duty_ids", [])
    for duty_id in duty_ids:
        try:
            duty_uuid = uuid.UUID(duty_id)
            duty = Duty.get_by_id(duty_uuid)
            DutyCoin.create(duty=duty, coin=new_coin)
        except (ValueError, Duty.DoesNotExist):
            abort(400, description=f"Invalid duty_id: {duty_id}")

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
    
    duty_ids = data.get("duty_ids")
    if duty_ids is not None and not isinstance(duty_ids, list):
        abort(400, description="duty_ids must be a list of UUID strings.")

    try:
        coin = Coin.get_by_id(uuid_obj)
    except Coin.DoesNotExist:
        abort(404, description="Coin not found.")

    if name is not None:
        coin.name = name
        coin.save()
    
    if duty_ids is not None:
        DutyCoin.delete().where(DutyCoin.coin == coin).execute()
    
    for duty_id in duty_ids:
            try:
                duty_uuid = uuid.UUID(duty_id)
                duty = Duty.get_by_id(duty_uuid)
                DutyCoin.create(duty=duty, coin=coin)
            except (ValueError, Duty.DoesNotExist):
                abort(400, description=f"Invalid duty_id: {duty_id}")

    coin_dict = model_to_dict(coin)
    coin_dict["id"] = str(coin_dict["id"])

    duties = []
    for duty_coin in coin.coin_duties:
        duties.append({"id": str(duty_coin.duty.id), "name": duty_coin.duty.name})

    coin_dict["duties"] = duties

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
# @app.get("/duties/<duty_id>")
# def get_duty_by_id(duty_id):
#     try:
#         uuid_obj = uuid.UUID(duty_id)
#     except ValueError:
#         abort(400, description="Invalid Duty ID format. Duty ID must be a UUID (non-integer).")

#     try:
#         duty = Duty.get_by_id(uuid_obj)
#     except Duty.DoesNotExist:
#         abort(404, description="Duty not found.")

#     duty_dict = model_to_dict(duty)
#     duty_dict["id"] = str(duty.id)

#     coins = []
#     for duty_coin in duty.duty_coins:
#         coins.append({"id": str(duty_coin.coin.id), "name": duty_coin.coin.name})

#     duty_dict["coins"] = coins

#     return jsonify(duty_dict), 200

# GET DUTY BY CODE WITH ASSOCIATED COINS
@app.get("/duties/<duty_code>")
def get_duty_by_code(duty_code):
    duty_code = duty_code.upper()

    regex = r"^D\d+$"
    if not re.match(regex, duty_code):
        abort(400, description="Invalid Duty Code format. Duty Code must start with a 'D' or 'd' followed by numbers (e.g., D7 or d7).")

    try:
        duty = Duty.get(Duty.code == duty_code)
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

# GET KSB BY ID WITH ASSOCIATED DUTIES
@app.get("/ksbs/<ksb_id>")
def get_ksb_by_id(ksb_id):
    try:
        uuid_obj = uuid.UUID(ksb_id)
    except ValueError:
        abort(400, description="Invalid KSB ID format. KSB ID must be a UUID (non-integer).")
    
    ksb = None
    ksb_type = None

    for model, ksb_type_name in [
        (Knowledge, "Knowledge"),
        (Skill, "Skill"),
        (Behaviour, "Behaviour"),
    ]:
        try:
            ksb = model.get_by_id(uuid_obj)
            ksb_type = ksb_type_name
            break
        except model.DoesNotExist:
            ksb = None

    if not ksb:
        abort(404, description="KSB not found.")

    ksb_dict = model_to_dict(ksb)
    ksb_dict["id"] = str(ksb.id)
    ksb_dict["type"] = ksb_type

    duties = []

    if ksb_type == "Knowledge":
        for knowledge_duty in ksb.knowledge_duties:
            duties.append({"id": str(knowledge_duty.duty.id), "name": knowledge_duty.duty.name})

    elif ksb_type == "Skill":
        for skill_duties in ksb.skill_duties:
            duties.append({"id": str(skill_duties.duty.id), "name": skill_duties.duty.name})

    elif ksb_type == "Behaviour":
        for behaviour_duty in ksb.behaviour_duties:
            duties.append({"id": str(behaviour_duty.duty.id), "name": behaviour_duty.duty.name})

    ksb_dict["duties"] = duties

    return jsonify(ksb_dict), 200

if __name__ == '__main__':
    app.run(debug=True)
