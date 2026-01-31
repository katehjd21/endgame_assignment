import uuid

# GET COINS V1
def test_get_coins_v1(client, coins):
    response = client.get("/v1/coins")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(data) == len(coins)
    assert isinstance(data, list)
    returned_coin_names = [returned_coin["name"] for returned_coin in data]
    for coin in coins:
        assert coin.name in returned_coin_names


def test_coins_have_id_and_name_v1(client, coins):
    response = client.get("/v1/coins")
    data = response.json

    for coin in data:
        assert "id" in coin
        assert "name" in coin


def test_coins_have_non_integer_id_v1(client, coins):
    response = client.get("/v1/coins")
    data = response.json

    for coin in data:
        assert isinstance(coin["id"], str)
        uuid.UUID(coin["id"])


def test_get_coins_has_no_duplicates_v1(client, coins):
    response = client.get("/v1/coins")
    data = response.json
    coin_names = [coin["name"] for coin in data]

    assert len(coin_names) == len(set(coin_names))


# GET COINS V2
def test_get_coins_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(data) == len(coins_with_duties)
    assert isinstance(data, list)
    returned_coin_names = [returned_coin["name"] for returned_coin in data]
    for coin in coins_with_duties:
        assert coin.name in returned_coin_names


def test_coins_have_id_name_and_duties_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json

    for coin in data:
        assert "id" in coin
        assert "name" in coin
        assert "duties" in coin


def test_coins_have_non_integer_id_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json

    for coin in data:
        assert isinstance(coin["id"], str)
        uuid.UUID(coin["id"])


def test_get_coins_has_no_duplicates_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json
    coin_names = [coin["name"] for coin in data]

    assert len(coin_names) == len(set(coin_names))


def test_get_coins_returns_correct_coin_duties_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json

    expected_coin_duty_mapping = {
        "Automate": {"D1", "D2"},
        "Assemble": {"D2", "D3"},
        "Houston, Prepare to Launch!": {"D1", "D2", "D3"},
        "Going Deeper": {"D1", "D3"},
        "Call Security": {"D1", "D2", "D3"},
    }
    
    for coin in data:
        returned_duty_codes = {duty["code"] for duty in coin["duties"]}
        assert returned_duty_codes == expected_coin_duty_mapping[coin["name"]]


def test_get_coins_returns_correct_duty_details_v2(client, coins_with_duties):
    response = client.get("/v2/coins")
    data = response.json

    expected = {}
    for coin in coins_with_duties:
        expected[coin.name] = [
            {
                "id": str(duty_coin.duty.id),
                "code": duty_coin.duty.code,
                "name": duty_coin.duty.name,
                "description": duty_coin.duty.description,
            }
            for duty_coin in coin.coin_duties
        ]

    for coin in data:
        coin_name = coin["name"]
        returned_duties = coin["duties"]

        assert len(returned_duties) == len(expected[coin_name])

        for duty in returned_duties:
            assert duty in expected[coin_name]