from backend.models import Knowledge, Skill, Behaviour, Duty, DutyKnowledge, DutySkill, DutyBehaviour
import uuid

# GET KSBS
def test_get_ksbs_returns_all_ksbs(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert isinstance(data, list)
    assert len(data) == len(ksbs)

    actual_ksb_names = {ksb["name"] for ksb in data}
    expected_ksb_names = {ksb.name for ksb in ksbs}
    assert actual_ksb_names == expected_ksb_names


def test_ksbs_have_id_code_name_description_and_type(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for ksb in data:
        assert set(ksb.keys()) == {"id", "code", "name", "description", "type"}


def test_get_ksbs_returns_correct_ksb_descriptions_and_codes(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    ksb_map = {ksb["code"]: ksb for ksb in data}

    for expected_ksb in ksbs:
        code = expected_ksb.code
        assert code in ksb_map
        actual_ksb = ksb_map[code]

        assert actual_ksb["code"] == expected_ksb.code
        assert actual_ksb["name"] == expected_ksb.name
        assert actual_ksb["description"] == expected_ksb.description


def test_ksbs_type_is_valid(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    valid_types = {"Knowledge", "Skill", "Behaviour"}
    for actual in data:
        assert actual["type"] in valid_types


def test_ksbs_have_correct_type_values(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for expected_ksb in ksbs:
        actual_ksb = next(ksb for ksb in data if ksb["code"] == expected_ksb.code)
        assert actual_ksb["type"] == expected_ksb.__class__.__name__


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
def test_get_ksb_by_code_returns_its_associated_duties(client, ksbs_with_duties):
    for ksb_type in ["knowledge", "skill", "behaviour"]:
        ksb = ksbs_with_duties[ksb_type]
        response = client.get(f"/ksbs/{ksb.code}")
        data = response.json

        if ksb_type == "knowledge":
            expected_duties = [expected_duty.name for expected_duty in ksbs_with_duties["duties"][:2]]
        else:
            expected_duties = [expected_duty.name for expected_duty in ksbs_with_duties["duties"]]

        actual_duties = [actual_duty["name"] for actual_duty in data["duties"]]

        for duty_name in expected_duties:
            assert duty_name in actual_duties
        assert len(actual_duties) == len(expected_duties)



def test_get_ksb_by_code_returns_empty_duties_when_none_associated(client):
    knowledge = Knowledge.create(code="K10", name="Knowledge 10", description="No Duties")
    response = client.get(f"/ksbs/{knowledge.code}")
    assert response.status_code == 200
    assert response.json["duties"] == []


def test_get_ksb_by_code_returns_ksb_code_name_description_and_type(client, ksbs):
    for expected_ksb in ksbs:
        response = client.get(f"/ksbs/{expected_ksb.code}")
        actual_ksb = response.json

        assert actual_ksb["code"] == expected_ksb.code
        assert actual_ksb["name"] == expected_ksb.name
        assert actual_ksb["description"] == expected_ksb.description
        assert actual_ksb["type"] == expected_ksb.__class__.__name__
        assert "duties" in actual_ksb


def test_get_ksb_by_code_only_returns_expected_fields_including_type(client, ksbs):
    expected_ksb_keys = {"id", "code", "name", "description", "type", "duties"}

    for ksb in ksbs:
        response = client.get(f"/ksbs/{ksb.code}")
        actual_ksb_keys = set(response.json.keys())
        assert actual_ksb_keys == expected_ksb_keys


def test_ksb_duties_return_id_and_name(client, ksbs):
    for ksb in ksbs:
        response = client.get(f"/ksbs/{ksb.code}")
        for duty in response.json["duties"]:
            assert set(duty.keys()) == {"id", "name"}


def test_get_ksb_by_code_with_letter_suffix(client):
    knowledge = Knowledge.create(code="K1A", name="Knowledge 1A", description="Knowledge 1A Description")
    duty1 = Duty.create(code="D10", name="Duty 10", description="Duty 10 Description")
    duty2 = Duty.create(code="D11", name="Duty 11", description="Duty 11 Description")

    DutyKnowledge.create(duty=duty1, knowledge=knowledge)
    DutyKnowledge.create(duty=duty2, knowledge=knowledge)

    response = client.get("/ksbs/k1a")
    actual_ksb = response.json
    expected_ksb = {
        "code": "K1A",
        "name": "Knowledge 1A",
        "description": "Knowledge 1A Description",
        "type": "Knowledge",
    }

    for key, value in expected_ksb.items():
        assert actual_ksb[key] == value


def test_get_ksb_by_code_returns_400_if_invalid_code(client):
    response = client.get("/ksbs/invalid_code")


    assert response.status_code == 400
    assert response.json["description"] == "Invalid KSB Code format. KSB Code must start with 'K', 'S', or 'B', followed by numbers and optionally a letter (e.g., K1, K1a, S2, B3b)."


def test_get_ksb_by_code_returns_404_if_not_found(client):
    response = client.get("/ksbs/k999")
    assert response.status_code == 404
    assert response.json["description"] == "KSB not found."


def test_deleting_knowledge_cascades_duty_knowledge_junction_table(ksbs_with_duties):
    knowledge = ksbs_with_duties["knowledge"]
    knowledge.delete_instance(recursive=True)
    assert Knowledge.select().where(Knowledge.id == knowledge.id).count() == 0
    assert DutyKnowledge.select().where(DutyKnowledge.knowledge == knowledge).count() == 0


def test_deleting_skill_cascades_duty_skill_junction_table(ksbs_with_duties):
    skill = ksbs_with_duties["skill"]
    skill.delete_instance(recursive=True)
    assert Skill.select().where(Skill.id == skill.id).count() == 0
    assert DutySkill.select().where(DutySkill.skill == skill).count() == 0


def test_deleting_behaviour_cascades_duty_behaviour_junction_table(ksbs_with_duties):
    behaviour = ksbs_with_duties["behaviour"]
    behaviour.delete_instance(recursive=True)
    assert Behaviour.select().where(Behaviour.id == behaviour.id).count() == 0
    assert DutyBehaviour.select().where(DutyBehaviour.behaviour == behaviour).count() == 0