from models import Knowledge, Skill, Behaviour, Duty, DutyKnowledge, DutySkill, DutyBehaviour
import pytest
import uuid

@pytest.fixture
def ksbs():
    knowledge = Knowledge.create(code="K1", name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(code="S1", name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(code="B1", name="Behaviour 1", description="Behaviour 1 Description")
    return [knowledge, skill, behaviour]

@pytest.fixture
def duties_with_ksbs(ksbs):
    duty1 = Duty.create(code="D1", name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(code="D2", name="Duty 2", description="Duty 2 Description")    
    duty3 = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")
    DutyKnowledge.create(duty=duty1, knowledge=ksbs[0])
    DutyKnowledge.create(duty=duty2, knowledge=ksbs[0])
    DutySkill.create(duty=duty1, skill=ksbs[1])
    DutySkill.create(duty=duty2, skill=ksbs[1])
    DutySkill.create(duty=duty3, skill=ksbs[1])
    DutyBehaviour.create(duty=duty1, behaviour=ksbs[2])
    DutyBehaviour.create(duty=duty2, behaviour=ksbs[2])
    DutyBehaviour.create(duty=duty3, behaviour=ksbs[2])
    return [duty1, duty2, duty3]

# GET KSBS
def test_get_ksbs_returns_all_ksbs(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert isinstance(data, list)
    assert len(data) == len(ksbs)
    returned_ksb_names = [returned_ksb["name"] for returned_ksb in data]
    for ksb in ksbs:
        assert ksb.name in returned_ksb_names

def test_ksbs_have_id_code_name_and_description(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for ksb in data:
        assert set(ksb.keys()) == {"id", "code", "name", "description", "type"}

def test_get_ksbs_returns_correct_ksb_descriptions(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    ksb_names = {ksb["name"]: ksb["description"] for ksb in data}
    assert ksb_names["Knowledge 1"] == "Knowledge 1 Description"
    assert ksb_names["Skill 1"] == "Skill 1 Description"
    assert ksb_names["Behaviour 1"] == "Behaviour 1 Description"

def test_get_ksbs_returns_correct_ksb_codes(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    ksb_names = {ksb["name"]: ksb["code"] for ksb in data}
    assert ksb_names["Knowledge 1"] == "K1"
    assert ksb_names["Skill 1"] == "S1"
    assert ksb_names["Behaviour 1"] == "B1"

def test_ksbs_have_type_field(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for ksb in data:
        assert "type" in ksb

def test_ksbs_type_is_valid(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    valid_types = {"Knowledge", "Skill", "Behaviour"}

    for ksb in data:
        assert ksb["type"] in valid_types

def test_ksbs_have_correct_type_values(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    expected_types = {"Knowledge 1": "Knowledge", "Skill 1": "Skill", "Behaviour 1": "Behaviour"}

    for ksb in data:
        assert ksb["type"] == expected_types[ksb["name"]]

def test_ksbs_have_non_integer_id(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for ksb in data:
        assert isinstance(ksb["id"], str)
        uuid.UUID(ksb["id"])

def test_get_ksbs_has_no_duplicates(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    ksb_names = [ksb["name"] for ksb in data]
    assert len(ksb_names) == len(set(ksb_names))



# GET KSB BY KSB CODE WITH ASSOCIATED DUTIES
def test_get_ksb_by_code_returns_its_associated_duties(client, ksbs, duties_with_ksbs):
    ksb1_code = ksbs[0].code
    ksb1_response = client.get(f"/ksbs/{ksb1_code}")
    ksb1_duty_names = [ksb1_duty["name"] for ksb1_duty in ksb1_response.json["duties"]]

    assert "Duty 1" in ksb1_duty_names
    assert "Duty 2" in ksb1_duty_names
    assert "Duty 3" not in ksb1_duty_names
    assert len(ksb1_duty_names) == 2

    ksb2_code = ksbs[1].code
    ksb2_response = client.get(f"/ksbs/{ksb2_code}")
    ksb2_duty_names = [ksb2_duty["name"] for ksb2_duty in ksb2_response.json["duties"]]

    assert "Duty 1" in ksb2_duty_names
    assert "Duty 2" in ksb2_duty_names
    assert "Duty 3" in ksb2_duty_names
    assert len(ksb2_duty_names) == 3

    ksb3_code = ksbs[2].code
    ksb3_response = client.get(f"/ksbs/{ksb3_code}")
    ksb3_duty_names = [ksb3_duty["name"] for ksb3_duty in ksb3_response.json["duties"]]

    assert "Duty 1" in ksb3_duty_names
    assert "Duty 2" in ksb3_duty_names
    assert "Duty 3" in ksb3_duty_names
    assert len(ksb3_duty_names) == 3

def test_get_ksb_by_code_returns_empty_duties_when_none_associated(client):
    knowledge = Knowledge.create(code="K10", name="Knowledge 10", description="No Duties")
    response = client.get(f"/ksbs/{knowledge.code}")
    assert response.status_code == 200
    assert response.json["duties"] == []

def test_get_ksb_by_code_returns_ksb_code_name_and_description(client, ksbs, duties_with_ksbs):
    ksb1_code = ksbs[0].code
    ksb_1_response = client.get(f"/ksbs/{ksb1_code}")
    ksb1_data = ksb_1_response.json
    
    assert ksb1_data["code"] == "K1"
    assert ksb1_data["name"] == "Knowledge 1"
    assert ksb1_data["description"] == "Knowledge 1 Description"

    ksb2_code = ksbs[1].code
    ksb_2_response = client.get(f"/ksbs/{ksb2_code}")
    ksb2_data = ksb_2_response.json
    
    assert ksb2_data["code"] == "S1"
    assert ksb2_data["name"] == "Skill 1"
    assert ksb2_data["description"] == "Skill 1 Description"

    ksb3_code = ksbs[2].code
    ksb_3_response = client.get(f"/ksbs/{ksb3_code}")
    ksb3_data = ksb_3_response.json
    
    assert ksb3_data["code"] == "B1"
    assert ksb3_data["name"] == "Behaviour 1"
    assert ksb3_data["description"] == "Behaviour 1 Description"

def test_get_ksb_by_code_only_returns_expected_fields_including_type(client, ksbs, duties_with_ksbs):
    ksb_code = ksbs[0].code
    response = client.get(f"/ksbs/{ksb_code}")
    data = response.json

    assert set(data.keys()) == {"id", "code", "name", "description", "type", "duties"}

def test_knowledge_duties_return_id_and_name_of_duties(client, ksbs, duties_with_ksbs):
    ksb_code = ksbs[0].code
    response = client.get(f"/ksbs/{ksb_code}")
    duty = response.json["duties"][0]

    assert set(duty.keys()) == {"id", "name"}

def test_skill_duties_return_id_and_name_of_duties(client, ksbs, duties_with_ksbs):
    ksb_code = ksbs[1].code
    response = client.get(f"/ksbs/{ksb_code}")
    duty = response.json["duties"][0]

    assert set(duty.keys()) == {"id", "name"}

def test_behaviour_duties_return_id_and_name_of_duties(client, ksbs, duties_with_ksbs):
    ksb_code = ksbs[2].code
    response = client.get(f"/ksbs/{ksb_code}")
    duty = response.json["duties"][0]

    assert set(duty.keys()) == {"id", "name"}

def test_get_ksb_by_code_with_letter_suffix(client):
    knowledge = Knowledge.create(code="K1A", name="Knowledge 1A", description="Knowledge 1A Description")
    duty1 = Duty.create(code="D10", name="Duty 10", description="Duty 10 Description")
    duty2 = Duty.create(code="D11", name="Duty 11", description="Duty 11 Description")

    DutyKnowledge.create(duty=duty1, knowledge=knowledge)
    DutyKnowledge.create(duty=duty2, knowledge=knowledge)

    response = client.get("/ksbs/k1a")
    data = response.json

    assert data["code"] == "K1A"
    assert data["name"] == "Knowledge 1A"
    assert data["description"] == "Knowledge 1A Description"
    assert data["type"] == "Knowledge"

def test_get_ksb_by_code_returns_400_if_invalid_code(client):
    response = client.get("/ksbs/invalid_code")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid KSB Code format. KSB Code must start with 'K', 'S', or 'B', followed by numbers and optionally a letter (e.g., K1, K1a, S2, B3b)."

def test_get_ksb_by_code_returns_404_if_not_found(client):
    response = client.get("/ksbs/k999")
    assert response.status_code == 404
    assert response.json["description"] == "KSB not found."

def test_deleting_knowledge_cascades_duty_knowledge_junction_table():
    duty = Duty.create(code="D4", name="Duty 4", description="Duty 4 Description")
    knowledge = Knowledge.create(code="K2", name="Knowledge 2", description="Knowledge 2 Description")

    DutyKnowledge.create(duty=duty, knowledge=knowledge)

    knowledge.delete_instance(recursive=True)  

    assert Knowledge.select().where(Knowledge.id == knowledge.id).count() == 0
    assert DutyKnowledge.select().where(DutyKnowledge.knowledge == knowledge).count() == 0

def test_deleting_skill_cascades_duty_skill_junction_table():
    duty = Duty.create(code="D4", name="Duty 4", description="Duty 4 Description")
    skill = Skill.create(code="S2", name="Skill 2", description="Skill 2 Description")

    DutySkill.create(duty=duty, skill=skill)

    skill.delete_instance(recursive=True)  

    assert Skill.select().where(Skill.id == skill.id).count() == 0
    assert DutySkill.select().where(DutySkill.skill == skill).count() == 0

def test_deleting_behaviour_cascades_duty_behaviour_junction_table():
    duty = Duty.create(code="D4", name="Duty 4", description="Duty 4 Description")
    behaviour = Behaviour.create(code="B2", name="Behaviour 2", description="Behaviour 2 Description")

    DutyBehaviour.create(duty=duty, behaviour=behaviour)

    behaviour.delete_instance(recursive=True)  

    assert Behaviour.select().where(Behaviour.id == behaviour.id).count() == 0
    assert DutyBehaviour.select().where(DutyBehaviour.behaviour == behaviour).count() == 0
