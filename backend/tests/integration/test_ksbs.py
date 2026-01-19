from models import Knowledge, Skill, Behaviour
import pytest
import uuid

@pytest.fixture
def ksbs():
    knowledge = Knowledge.create(name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(name="Behaviour 1", description="Behaviour 1 Description")
    return [knowledge, skill, behaviour]

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

def test_ksbs_have_id_name_and_description(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    for ksb in data:
        assert set(ksb.keys()) == {"id", "name", "description", "type"}

def test_get_ksbs_returns_correct_ksb_descriptions(client, ksbs):
    response = client.get("/ksbs")
    data = response.json

    ksb_names = {ksb["name"]: ksb["description"] for ksb in data}
    assert ksb_names["Knowledge 1"] == "Knowledge 1 Description"
    assert ksb_names["Skill 1"] == "Skill 1 Description"
    assert ksb_names["Behaviour 1"] == "Behaviour 1 Description"

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
