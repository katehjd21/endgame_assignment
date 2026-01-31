from models import DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour, Coin, Duty, Knowledge, Skill, Behaviour
from playhouse.shortcuts import model_to_dict

def clear_tables():
    tables_to_clear = [
        DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour,
        Coin, Duty, Knowledge, Skill, Behaviour
    ]
    for table in tables_to_clear:
        table.delete().execute()

def serialize_coin(coin):
    coin_dict = model_to_dict(coin)
    coin_dict["id"] = str(coin_dict["id"])
    return coin_dict

def serialize_coin_with_duties(coin):
    coin_dict = serialize_coin(coin)

    duties = []
    for duty_coin in coin.coin_duties:
        duties.append({"id": str(duty_coin.duty.id), "code": duty_coin.duty.code, "name": duty_coin.duty.name, "description": duty_coin.duty.description})

    coin_dict["duties"] = duties
    return coin_dict
