import pytest
from backend.pg_db_connection import database, TEST_DB
from app import app as flask_app
from models import Coin, Duty, Knowledge, Skill, Behaviour, DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour


@pytest.fixture(scope="function", autouse=True)
def use_test_db():
    database.initialize(TEST_DB)
    TEST_DB.connect()
    
    TEST_DB.create_tables([
        Coin, Duty, Knowledge, Skill, Behaviour,
        DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
    ])
    
    yield  
    
    TEST_DB.drop_tables([
        Coin, Duty, Knowledge, Skill, Behaviour,
        DutyCoin, DutyKnowledge, DutySkill, DutyBehaviour
    ])
    TEST_DB.close()


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def coins():
    coin_names = [
        "Automate",
        "Assemble",
        "Houston, Prepare to Launch!",
        "Going Deeper",
        "Call Security",
    ]
    coins = []
    for name in coin_names:
        coins.append(Coin.create(name=name))

    return coins


@pytest.fixture
def coin():
    coin = Coin.create(name="Test Coin")
    return coin


@pytest.fixture
def duties():
    duty1 = Duty.create(code="D1", name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(code="D2", name="Duty 2", description="Duty 2 Description")    
    duty3 = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")

    return [duty1, duty2, duty3]


@pytest.fixture
def coin_with_duties(coin, duties):
    for duty in duties:
        DutyCoin.create(coin=coin, duty=duty)
    return coin


@pytest.fixture
def coins_with_duties(coins, duties):
    coin_duty_map = {
        coins[0]: [duties[0], duties[1]],
        coins[1]: [duties[1], duties[2]],
        coins[2]: [duties[0], duties[1], duties[2]],
        coins[3]: [duties[0], duties[2]],
        coins[4]: [duties[0], duties[1], duties[2]],
    }
    for coin, duty_list in coin_duty_map.items():
        for duty in duty_list:
            DutyCoin.create(coin=coin, duty=duty)
    return coins


@pytest.fixture
def coin_without_duties():
    coin = Coin.create(name="No Duty Coin")
    return coin


@pytest.fixture
def duty_with_coins(duties, coins):
    duty = duties[0]
    for coin in coins[:2]:  
        DutyCoin.create(coin=coin, duty=duty)
    return duty


@pytest.fixture
def ksbs():
    knowledge = Knowledge.create(code="K1", name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(code="S1", name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(code="B1", name="Behaviour 1", description="Behaviour 1 Description")
    return [knowledge, skill, behaviour]


@pytest.fixture
def duty_with_ksb(duties):
    duty = duties[0]

    knowledge = Knowledge.create(code="K1", name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(code="S1", name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(code="B1", name="Behaviour 1", description="Behaviour 1 Description")

    DutyKnowledge.create(duty=duty, knowledge=knowledge)
    DutySkill.create(duty=duty, skill=skill)
    DutyBehaviour.create(duty=duty, behaviour=behaviour)

    return duty, knowledge, skill, behaviour


@pytest.fixture
def ksbs_with_duties():
    duty1 = Duty.create(code="D1", name="Duty 1", description="Duty 1 Description")
    duty2 = Duty.create(code="D2", name="Duty 2", description="Duty 2 Description")
    duty3 = Duty.create(code="D3", name="Duty 3", description="Duty 3 Description")

    knowledge = Knowledge.create(code="K1", name="Knowledge 1", description="Knowledge 1 Description")
    skill = Skill.create(code="S1", name="Skill 1", description="Skill 1 Description")
    behaviour = Behaviour.create(code="B1", name="Behaviour 1", description="Behaviour 1 Description")

    DutyKnowledge.create(duty=duty1, knowledge=knowledge)
    DutyKnowledge.create(duty=duty2, knowledge=knowledge)
    for duty in [duty1, duty2, duty3]:
        DutySkill.create(duty=duty, skill=skill)
        DutyBehaviour.create(duty=duty, behaviour=behaviour)

    return {
        "duties": [duty1, duty2, duty3],
        "knowledge": knowledge,
        "skill": skill,
        "behaviour": behaviour,
    }