import pytest
from models import Duty, Knowledge, Skill, Behaviour, Coin, DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
import uuid

@pytest.fixture
def duties():
    duty1 = Duty.create(code="D1", name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(code="D2", name="Duty 2", description="Duty 2 Description")
    return [duty1, duty2]

@pytest.fixture
def coins_with_duties(duties):
    coin1 = Coin.create(name="Automate Coin")
    coin2 = Coin.create(name="Assemble Coin")
    coin3 = Coin.create(name="Going Deeper Coin")
    DutyCoin.create(duty=duties[0], coin=coin1)
    DutyCoin.create(duty=duties[0], coin=coin2)
    DutyCoin.create(duty=duties[1], coin=coin1)
    DutyCoin.create(duty=duties[1], coin=coin2)
    DutyCoin.create(duty=duties[1], coin=coin3)
    return [coin1, coin2, coin3]


# GET DUTIES

def test_get_duties_returns_all_duties(client, duties):
    response = client.get("/duties")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(data) == len(duties)
    assert isinstance(data, list)
    returned_duty_names = [returned_duty["name"] for returned_duty in data]
    for duty in duties:
        assert duty.name in returned_duty_names
    

def test_duties_have_id_code_name_and_description(client, duties):
    response = client.get("/duties")
    data = response.json

    for duty in data:
        assert set(duty.keys()) == {"id", "code", "name", "description"}

def test_get_duties_returns_correct_duty_descriptions(client, duties):
    response = client.get("/duties")
    data = response.json

    duty_names = {duty["name"]: duty["description"] for duty in data}
    assert duty_names["Duty 1"] == "Duty 1 Description"
    assert duty_names["Duty 2"] == "Duty 2 Description"

def test_get_duties_returns_correct_duty_codes(client, duties):
    response = client.get("/duties")
    data = response.json

    duty_names = {duty["name"]: duty["code"] for duty in data}
    assert duty_names["Duty 1"] == "D1"
    assert duty_names["Duty 2"] == "D2"


def test_duties_have_non_integer_id(client, duties):
    response = client.get("/duties")
    data = response.json

    for duty in data:
        assert isinstance(duty["id"], str)
        uuid.UUID(duty["id"])

def test_get_duties_has_no_duplicates(client, duties):
    response = client.get("/duties")
    data = response.json
    duty_names = [duty["name"] for duty in data]

    assert len(duty_names) == len(set(duty_names))


# GET DUTY BY ID WITH ASSOCIATED COINS
# def test_get_duty_by_id_returns_its_associated_coins(client, duties, coins_with_duties):
#     duty1_id = duties[0].id
#     duty1_response = client.get(f"/duties/{duty1_id}")
#     duty1_coin_names = [duty1_coin["name"] for duty1_coin in duty1_response.json["coins"]]

#     assert "Automate Coin" in duty1_coin_names
#     assert "Assemble Coin" in duty1_coin_names
#     assert "Going Deeper Coin" not in duty1_coin_names
#     assert len(duty1_coin_names) == 2

#     duty2_id = duties[1].id
#     duty2_response = client.get(f"/duties/{duty2_id}")
#     duty2_coin_names = [duty2_coin["name"] for duty2_coin in duty2_response.json["coins"]]

#     assert "Automate Coin" in duty2_coin_names
#     assert "Assemble Coin" in duty2_coin_names
#     assert "Going Deeper Coin" in duty2_coin_names
#     assert len(duty2_coin_names) == 3

# def test_get_duty_by_id_returns_empty_coins_when_none_associated(client):
#     duty = Duty.create(code="D10", name="Duty 10", description="No Coins")
#     response = client.get(f"/duties/{duty.id}")
#     assert response.status_code == 200
#     assert response.json["coins"] == []

# def test_get_duty_by_id_returns_duty_code_name_and_description(client, duties, coins_with_duties):
#     duty_id = duties[0].id
#     response = client.get(f"/duties/{duty_id}")
#     data = response.json

#     assert data["code"] == "D1"
#     assert data["name"] == "Duty 1"
#     assert data["description"] == "Duty 1 Description"

# def test_get_duty_by_id_only_returns_expected_fields(client, duties, coins_with_duties):
#     duty_id = duties[0].id
#     response = client.get(f"/duties/{duty_id}")
#     data = response.json

#     assert set(data.keys()) == {"id", "code", "name", "description", "coins"}

# def test_duty_coins_return_id_and_name_of_coins(client, duties, coins_with_duties):
#     duty_id = duties[0].id
#     response = client.get(f"/duties/{duty_id}")
#     coin = response.json["coins"][0]

#     assert set(coin.keys()) == {"id", "name"}

# def test_get_duty_by_id_returns_400_if_invalid_id(client):
#     response = client.get("/duties/invalid_id")

#     assert response.status_code == 400
#     assert response.json["description"] == "Invalid Duty ID format. Duty ID must be a UUID (non-integer)."

# def test_get_duty_by_id_returns_404_if_not_found(client):
#     response = client.get("/duties/00000000-0000-0000-0000-000000000000")
#     assert response.status_code == 404
#     assert response.json["description"] == "Duty not found."

# def test_deleting_duty_cascades_all_ksb_junction_tables():
#     duty = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")
#     knowledge = Knowledge.create(code="K3", name="Knowledge 3", description="Knowledge 3 Description")
#     skill = Skill.create(code="S3", name="Skill 3", description="Skill 3 Description")
#     behaviour = Behaviour.create(code="B3", name="Behaviour 3", description="Behaviour 3 Description")

#     DutyKnowledge.create(duty=duty, knowledge=knowledge)
#     DutySkill.create(duty=duty, skill=skill)
#     DutyBehaviour.create(duty=duty, behaviour=behaviour)

#     duty.delete_instance()  

#     assert Duty.select().where(Duty.id == duty.id).count() == 0
#     assert DutyKnowledge.select().where(DutyKnowledge.duty == duty).count() == 0
#     assert DutySkill.select().where(DutySkill.duty == duty).count() == 0
#     assert DutyBehaviour.select().where(DutyBehaviour.duty == duty).count() == 0

# GET DUTY BY DUTY CODE WITH ASSOCIATED COINS
def test_get_duty_by_code_returns_its_associated_coins(client, duties, coins_with_duties):
    duty1_code = duties[0].code
    duty1_response = client.get(f"/duties/{duty1_code}")
    duty1_coin_names = [duty1_coin["name"] for duty1_coin in duty1_response.json["coins"]]

    assert "Automate Coin" in duty1_coin_names
    assert "Assemble Coin" in duty1_coin_names
    assert "Going Deeper Coin" not in duty1_coin_names
    assert len(duty1_coin_names) == 2

    duty2_code = duties[1].code
    duty2_response = client.get(f"/duties/{duty2_code}")
    duty2_coin_names = [duty2_coin["name"] for duty2_coin in duty2_response.json["coins"]]

    assert "Automate Coin" in duty2_coin_names
    assert "Assemble Coin" in duty2_coin_names
    assert "Going Deeper Coin" in duty2_coin_names
    assert len(duty2_coin_names) == 3

def test_get_duty_by_code_returns_empty_coins_when_none_associated(client):
    duty = Duty.create(code="D10", name="Duty 10", description="No Coins")
    response = client.get(f"/duties/{duty.code}")
    assert response.status_code == 200
    assert response.json["coins"] == []

def test_get_duty_by_code_returns_duty_code_name_and_description(client, duties, coins_with_duties):
    duty_code = duties[0].code
    response = client.get(f"/duties/{duty_code}")
    data = response.json

    assert data["code"] == "D1"
    assert data["name"] == "Duty 1"
    assert data["description"] == "Duty 1 Description"

def test_get_duty_by_code_only_returns_expected_fields(client, duties, coins_with_duties):
    duty_code = duties[0].code
    response = client.get(f"/duties/{duty_code}")
    data = response.json

    assert set(data.keys()) == {"id", "code", "name", "description", "coins"}

def test_duty_coins_return_id_and_name_of_coins(client, duties, coins_with_duties):
    duty_code = duties[0].code
    response = client.get(f"/duties/{duty_code}")
    coin = response.json["coins"][0]

    assert set(coin.keys()) == {"id", "name"}

def test_get_duty_by_code_returns_400_if_invalid_code(client):
    response = client.get("/duties/invalid_code")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Duty Code format. Duty Code must start with a 'D' or 'd' followed by numbers (e.g., D7 or d7)."

def test_get_duty_by_code_returns_400_if_invalid_format(client):
    for code in ["d", "D", "Dabc", "D1A", "123"]:
        response = client.get(f"/duties/{code}")
        assert response.status_code == 400

def test_get_duty_by_code_returns_404_if_not_found(client):
    response = client.get("/duties/D999")
    assert response.status_code == 404
    assert response.json["description"] == "Duty not found."

def test_deleting_duty_cascades_all_ksb_junction_tables():
    duty = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")
    knowledge = Knowledge.create(code="K3", name="Knowledge 3", description="Knowledge 3 Description")
    skill = Skill.create(code="S3", name="Skill 3", description="Skill 3 Description")
    behaviour = Behaviour.create(code="B3", name="Behaviour 3", description="Behaviour 3 Description")

    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    DutySkill.create(duty=duty, skill=skill)
    DutyBehaviour.create(duty=duty, behaviour=behaviour)

    duty.delete_instance()  

    assert Duty.select().where(Duty.id == duty.id).count() == 0
    assert DutyKnowledge.select().where(DutyKnowledge.duty == duty).count() == 0
    assert DutySkill.select().where(DutySkill.duty == duty).count() == 0
    assert DutyBehaviour.select().where(DutyBehaviour.duty == duty).count() == 0