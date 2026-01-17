from models import Duty, Knowledge, Skill, Behaviour, DutyKnowledge, DutySkill, DutyBehaviour
import pytest
from peewee import IntegrityError
import uuid
from utils.helper_functions import clear_tables

@pytest.fixture
def duty_with_ksbs():
    duty = Duty.create(name="Duty 1")
    knowledge = Knowledge.create(name="Knowledge 1")
    skill = Skill.create(name="Skill 1")
    behaviour = Behaviour.create(name="Behaviour 1")

    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    DutySkill.create(duty=duty, skill=skill)
    DutyBehaviour.create(duty=duty, behaviour=behaviour)

    return duty

def test_ksbs_id_is_non_integer(duty_with_ksbs):
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

    for knowledge in knowledges:
        assert isinstance(knowledge.id, uuid.UUID)

    for skill in skills:
        assert isinstance(skill.id, uuid.UUID)
    
    for behaviour in behaviours:
        assert isinstance(behaviour.id, uuid.UUID)

def test_knowledge_name_is_unique():
    Knowledge.create(name="Knowledge 1")
    with pytest.raises(IntegrityError):
        Knowledge.create(name="Knowledge 1")

def test_skill_name_is_unique():
    Skill.create(name="Skill 1")
    with pytest.raises(IntegrityError):
        Skill.create(name="Skill 1")


def test_behaviour_name_is_unique():
    Behaviour.create(name="Behaviour 1")
    with pytest.raises(IntegrityError):
        Behaviour.create(name="Behaviour 1")


def test_duty_has_all_ksbs(duty_with_ksbs):
    duty = duty_with_ksbs
    assert len(list(duty.duty_knowledges)) == 1
    assert len(list(duty.duty_skills)) == 1
    assert len(list(duty.duty_behaviours)) == 1

def test_skill_name_is_unique():
    Skill.create(name="Skill 1")
    with pytest.raises(IntegrityError):
        Skill.create(name="Skill 1")


def test_behaviour_name_is_unique():
    Behaviour.create(name="Behaviour 1")
    with pytest.raises(IntegrityError):
        Behaviour.create(name="Behaviour 1")

def test_update_knowledge_name(duty_with_ksbs):
    knowledge = list(duty_with_ksbs.duty_knowledges)[0].knowledge
    knowledge.name = "Updated Knowledge Name"
    knowledge.save()
    assert Knowledge.get_by_id(knowledge.id).name == "Updated Knowledge Name"

def test_deleting_knowledge_cleans_junction(duty_with_ksbs):
    knowledge = list(duty_with_ksbs.duty_knowledges)[0].knowledge
    knowledge.delete_instance(recursive=True)
    assert DutyKnowledge.select().where(DutyKnowledge.knowledge == knowledge.id).count() == 0

def test_duties_for_given_knowledge(duty_with_ksbs):
    knowledge = list(duty_with_ksbs.duty_knowledges)[0].knowledge
    duties = []
    for duty_knowledge in knowledge.knowledge_duties:
        duties.append(duty_knowledge.duty)
    assert duty_with_ksbs in duties

def test_duties_for_given_skill(duty_with_ksbs):
    skill = list(duty_with_ksbs.duty_skills)[0].skill
    duties = []
    for duty_skill in skill.skill_duties:
        duties.append(duty_skill.duty)
    assert duty_with_ksbs in duties

def test_duties_for_given_behaviour(duty_with_ksbs):
    behaviour = list(duty_with_ksbs.duty_behaviours)[0].behaviour
    duties = []
    for duty_behaviour in behaviour.behaviour_duties:
        duties.append(duty_behaviour.duty)
    assert duty_with_ksbs in duties
