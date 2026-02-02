from utils.helper_functions import serialize_coin, serialize_coin_with_duties, serialize_duty, serialize_ksb, serialize_duty_with_coins, serialize_ksb_with_duties


# SERIALIZE COIN
def test_serialize_coin_has_id_and_name(coin):
    result = serialize_coin(coin)
    assert set(result.keys()) == {"id", "name"}


def test_serialize_coin_has_correct_coin_id_and_name(coin):
    result = serialize_coin(coin)
    assert result["id"] == str(coin.id)
    assert result["name"] == coin.name


# SERIALIZE COIN WITH DUTIES
def test_serialize_coin_with_duties_has_id_name_and_duties(coin_with_duties):
    result = serialize_coin_with_duties(coin_with_duties)
    assert set(result.keys()) == {"id", "name", "duties"}


def test_serialize_coin_with_duties_has_correct_id_name_and_duties(coin_with_duties):
    result = serialize_coin_with_duties(coin_with_duties)
    assert result["id"] == str(coin_with_duties.id)
    assert result["name"] == coin_with_duties.name
    assert len(result["duties"]) == 3
    expected_duties = [
        {"id": str(duty_coin.duty.id), "code": duty_coin.duty.code, "name": duty_coin.duty.name, "description": duty_coin.duty.description}
        for duty_coin in coin_with_duties.coin_duties
    ]
    assert result["duties"] == expected_duties


# SERIALIZE DUTY
def test_serialize_duty_has_id_code_name_and_description(duties):
    duty = duties[0]
    result = serialize_duty(duty)
    assert set(result.keys()) == {"id", "code", "name", "description"}


def test_serialize_duty_has_correct_duty_id_code_name_and_description(duties):
    duty = duties[0]
    result = serialize_duty(duty)
    assert result["id"] == str(duty.id)
    assert result["code"] == duty.code
    assert result["name"] == duty.name
    assert result["description"] == duty.description


# SERIALIZE KSB
def test_serialize_knowledge_returns_expected_keys_and_values(ksbs):
    knowledge = ksbs[0]
    result = serialize_ksb(knowledge, "Knowledge")
    assert set(result.keys()) == {"id", "code", "name", "description", "type"}
    assert result["type"] == "Knowledge"
    assert isinstance(result["id"], str)
    assert result["code"] == knowledge.code
    assert result["name"] == knowledge.name
    assert result["description"] == knowledge.description


def test_serialize_skill_returns_expected_keys_and_values(ksbs):
    skill = ksbs[1]
    result = serialize_ksb(skill, "Skill")
    assert set(result.keys()) == {"id", "code", "name", "description", "type"}
    assert result["type"] == "Skill"
    assert isinstance(result["id"], str)
    assert result["code"] == skill.code
    assert result["name"] == skill.name
    assert result["description"] == skill.description


def test_serialize_behaviour_returns_expected_keys_and_values(ksbs):
    behaviour = ksbs[2]
    result = serialize_ksb(behaviour, "Behaviour")
    assert set(result.keys()) == {"id", "code", "name", "description", "type"}
    assert result["type"] == "Behaviour"
    assert isinstance(result["id"], str)
    assert result["code"] == behaviour.code
    assert result["name"] == behaviour.name
    assert result["description"] == behaviour.description


# SERALIZE DUTY WITH COINS
def test_serialize_duty_with_coins_returns_expected_keys(duty_with_coins):
    result = serialize_duty_with_coins(duty_with_coins)
    assert set(result.keys()) == {"id", "code", "name", "description", "coins"}


def test_serialize_duty_with_coins_ids_are_strings(duty_with_coins):
    result = serialize_duty_with_coins(duty_with_coins)
    assert isinstance(result["id"], str)
    for coin in result["coins"]:
        assert isinstance(coin["id"], str)


def test_serialize_duty_with_coins_has_correct_coins(duty_with_coins):
    result = serialize_duty_with_coins(duty_with_coins)
    expected_coins = [{"id": str(duty_coin.coin.id), "name": duty_coin.coin.name} for duty_coin in duty_with_coins.duty_coins]
    assert result["coins"] == expected_coins


# SERIALIZE KSB WITH DUTIES
def test_serialize_ksb_with_duties_returns_expected_keys(ksbs):
    for ksb in ksbs:
        ksb_type = ksb.__class__.__name__ 
        result = serialize_ksb_with_duties(ksb, ksb_type)
        assert "id" in result
        assert "type" in result
        assert "duties" in result

def test_serialize_ksb_with_duties_ids_are_strings_and_type_correct(ksbs):
    for ksb in ksbs:
        ksb_type = ksb.__class__.__name__
        result = serialize_ksb_with_duties(ksb, ksb_type)
        assert isinstance(result["id"], str)
        assert result["type"] == ksb_type


def test_serialize_ksb_with_duties_has_correct_duties(ksbs_with_duties):
    for ksb_type in ["knowledge", "skill", "behaviour"]:
        ksb = ksbs_with_duties[ksb_type]
        result = serialize_ksb_with_duties(ksb, ksb_type.capitalize())
        if ksb_type == "knowledge":
            expected_duties = [{"id": str(duty.id), "code": duty.code, "name": duty.name, "description": duty.description} for duty in ksbs_with_duties["duties"][:2]]
        else:
            expected_duties = [{"id": str(duty.id), "code": duty.code, "name": duty.name, "description": duty.description} for duty in ksbs_with_duties["duties"]]
        assert result["duties"] == expected_duties