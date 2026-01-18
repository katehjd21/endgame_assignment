from models import Coin, Duty, DutyCoin, Knowledge, Skill, Behaviour, DutyKnowledge, DutySkill, DutyBehaviour
from backend.utils.helper_functions import clear_tables
import pytest
import uuid
from peewee import IntegrityError

@pytest.fixture
def duty_with_ksbs():
    duty = Duty.create(name="Duty 1", description="Duty 1 Description")

    knowledge = Knowledge.create(name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(name="Behaviour 1", description="Behaviour 1 Description")

    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    DutySkill.create(duty=duty, skill=skill)
    DutyBehaviour.create(duty=duty, behaviour=behaviour)

    return duty

@pytest.fixture
def coin_with_duty_and_ksbs(duty_with_ksbs):
    coin = Coin.create(name="Automate Coin")
    DutyCoin.create(duty=duty_with_ksbs, coin=coin)
    return coin


@pytest.fixture
def duty_with_multiple_ksbs():
    duty = Duty.create(name="Duty 2", description="Duty 2 Description")

    knowledges = [
        Knowledge.create(name="Knowledge 2", description="Knowledge 2 Description"),
        Knowledge.create(name="Knowledge 3", description="Knowledge 3 Description")
    ]
    for knowledge in knowledges:
        DutyKnowledge.create(duty=duty, knowledge=knowledge)

    skills = [
        Skill.create(name="Skill 2", description="Skill 2 Description"),
        Skill.create(name="Skill 3", description="Skill 3 Description"),
        Skill.create(name="Skill 4", description="Skill 4 Description")
    ]
    for skill in skills:
        DutySkill.create(duty=duty, skill=skill)

    behaviours = [
        Behaviour.create(name="Behaviour 2", description="Behaviour 2 Description"),
        Behaviour.create(name="Behaviour 3", description="Behaviour 3 Description")
    ]
    for behaviour in behaviours:
        DutyBehaviour.create(duty=duty, behaviour=behaviour)

    return duty



def test_duty_has_ksbs(duty_with_ksbs):
    duty = duty_with_ksbs
    knowledges = []
    skills = []
    behaviours = []

    for duty_knowledge in duty.duty_knowledges:
        knowledges.append(duty_knowledge.knowledge)

    for duty_skill in duty.duty_skills:
        skills.append(duty_skill.skill)
    
    for duty_behaviour in duty.duty_behaviours:
        behaviours.append(duty_behaviour.behaviour)
    

    assert len(knowledges) == 1
    assert knowledges[0].name == "Knowledge 1"
    assert knowledges[0].description == "Knowledge 1 Description"

    assert len(skills) == 1
    assert skills[0].name == "Skill 1"
    assert skills[0].description == "Skill 1 Description"

    assert len(behaviours) == 1
    assert behaviours[0].name == "Behaviour 1"
    assert behaviours[0].description == "Behaviour 1 Description"


def test_duty_has_multiple_ksbs(duty_with_multiple_ksbs):
    duty = duty_with_multiple_ksbs
    assert len(list(duty.duty_knowledges)) == 2
    assert len(list(duty.duty_skills)) == 3
    assert len(list(duty.duty_behaviours)) == 2


def test_coin_duty_ksb_chain(coin_with_duty_and_ksbs):
    coin = coin_with_duty_and_ksbs

    duties = []
    for duty_coin in coin.coin_duties:
        duties.append(duty_coin.duty)

    assert len(duties) == 1

    duty = duties[0]
    assert duty.name == "Duty 1"
    assert duty.description == "Duty 1 Description"

    assert len(duty.duty_knowledges) == 1
    assert len(duty.duty_skills) == 1
    assert len(duty.duty_behaviours) == 1

def test_coins_for_given_duty(duty_with_ksbs):
    coin1 = Coin.create(name="Coin 1")
    coin2 = Coin.create(name="Coin 2")
    
    DutyCoin.create(duty=duty_with_ksbs, coin=coin1)
    DutyCoin.create(duty=duty_with_ksbs, coin=coin2)

    coins = []
    for duty_coin in duty_with_ksbs.duty_coins:
        coins.append(duty_coin.coin)
    
    assert len(coins) == 2

    coin_names = []
    for coin in coins:
        coin_names.append(coin.name)

    assert "Coin 1" in coin_names
    assert "Coin 2" in coin_names


def test_duty_id_is_non_integer(duty_with_ksbs):
    duty = duty_with_ksbs
    assert isinstance(duty.id, uuid.UUID)

def test_duty_name_is_unique():
    Duty.create(name="Duty 1", description="Duty 1 Description")
    with pytest.raises(IntegrityError):
        Duty.create(name="Duty 1", description="Duty 1 Description")


def test_duplicate_ksbs_for_same_duty():
    duty = Duty.create(name="Duty 4", description="Duty 4 Description")
    knowledge = Knowledge.create(name="Knowledge 1", description="Knowledge 1 Description")
    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    skill = Skill.create(name="Skill 1", description="Skill 1 Description")
    DutySkill.create(duty=duty, skill=skill)
    behaviour = Behaviour.create(name="Behaviour 1", description="Behaviour 1 Description")
    DutyBehaviour.create(duty=duty, behaviour=behaviour)
    
    with pytest.raises(IntegrityError):
        DutyKnowledge.create(duty=duty, knowledge=knowledge)

def test_update_duty_name(duty_with_ksbs):
    duty = duty_with_ksbs
    duty.name = "Updated Duty Name"
    duty.save()
    assert Duty.get_by_id(duty.id).name == "Updated Duty Name"

def test_update_duty_description(duty_with_ksbs):
    duty = duty_with_ksbs
    duty.description = "Updated Duty Description"
    duty.save()
    assert Duty.get_by_id(duty.id).description == "Updated Duty Description"


def test_deleting_duty_cleans_junction_tables_of_duty():
    duty = Duty.create(name="Duty 5", description="Duty 5 Description")
    coin = Coin.create(name="Going Deeper Coin")
    knowledge = Knowledge.create(name="Knowledge 4", description="Knowledge 4 Description")
    
    DutyCoin.create(duty=duty, coin=coin)
    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    
    duty.delete_instance(recursive=True) 
    
    assert Duty.select().where(Duty.id == duty.id).count() == 0
    assert DutyCoin.select().where(DutyCoin.duty == duty).count() == 0
    assert DutyKnowledge.select().where(DutyKnowledge.duty == duty).count() == 0
