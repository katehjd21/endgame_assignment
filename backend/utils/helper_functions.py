from playhouse.shortcuts import model_to_dict

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


def serialize_duty(duty):
    return {
        "id": str(duty.id),
        "code": duty.code,
        "name": duty.name,
        "description": duty.description
    }


def serialize_ksb(ksb, ksb_type):
    return {
        "id": str(ksb.id),
        "code": ksb.code,
        "name": ksb.name,
        "description": ksb.description,
        "type": ksb_type
    }


def serialize_duty_with_coins(duty):
    duty_dict = model_to_dict(duty)
    duty_dict["id"] = str(duty.id)
    duty_dict["coins"] = [{"id": str(dc.coin.id), "name": dc.coin.name} for dc in duty.duty_coins]
    return duty_dict


def serialize_ksb_with_duties(ksb, ksb_type):
    ksb_dict = model_to_dict(ksb)
    
    ksb_dict["id"] = str(ksb.id)
    ksb_dict["type"] = ksb_type

    if ksb_type == "Knowledge":
        duties = [{"id": str(duty_assoc.duty.id), "code": duty_assoc.duty.code, "name": duty_assoc.duty.name, "description": duty_assoc.duty.description} 
                  for duty_assoc in ksb.knowledge_duties]
    elif ksb_type == "Skill":
        duties = [{"id": str(duty_assoc.duty.id), "code": duty_assoc.duty.code, "name": duty_assoc.duty.name, "description": duty_assoc.duty.description} 
                  for duty_assoc in ksb.skill_duties]
    elif ksb_type == "Behaviour":
        duties = [{"id": str(duty_assoc.duty.id), "code": duty_assoc.duty.code, "name": duty_assoc.duty.name, "description": duty_assoc.duty.description} 
                  for duty_assoc in ksb.behaviour_duties]

    ksb_dict["duties"] = duties
    return ksb_dict