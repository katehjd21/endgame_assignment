import uuid

# GET COIN BY ID V1
def test_get_coin_by_id_v1(client, coin):
    response = client.get(f"/v1/coins/{coin.id}")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert data["id"] == str(coin.id)
    assert data["name"] == coin.name


def test_coin_has_non_integer_id_v1(client, coin):
    response = client.get(f"/v1/coins/{coin.id}")
    data = response.json

    assert isinstance(data["id"], str)
    uuid.UUID(data["id"])


def test_get_coin_by_id_not_found_v1(client):
    response = client.get("/v1/coins/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."


def test_get_coin_by_id_invalid_uuid_v1(client):
    response = client.get("/v1/coins/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."


def test_get_coin_by_id_only_returns_id_and_name_v1(client, coin):
    response = client.get(f"/v1/coins/{coin.id}")
    data = response.json

    assert "id" in data
    assert "name" in data
    assert len(data) == 2

def test_get_coin_by_id_returns_correct_id_and_name(client, coin):
    response = client.get(f"/v1/coins/{coin.id}")
    data = response.json
    print(data)

    assert str(coin.id) == data["id"] 
    assert coin.name == data["name"] 


# GET COIN BY ID V2
def test_get_coin_by_id_v2(client, coin_with_duties):
    response = client.get(f"/v2/coins/{coin_with_duties.id}")
    data = response.json

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert data["id"] == str(coin_with_duties.id)
    assert data["name"] == coin_with_duties.name


def test_get_coin_by_id_returns_associated_duties_v2(client, coin_with_duties):
    response = client.get(f"/v2/coins/{coin_with_duties.id}")
    data = response.json

    assert response.status_code == 200
    assert "duties" in data

    expected_duties = []
    for duty_coin in coin_with_duties.coin_duties:
        expected_duties.append({
            "id": str(duty_coin.duty.id),
            "code": duty_coin.duty.code,
            "name": duty_coin.duty.name,
            "description": duty_coin.duty.description
        })

    assert data["duties"] == expected_duties


def test_get_coin_by_id_returns_empty_duties_list_if_none_v2(client, coin_without_duties):
    response = client.get(f"/v2/coins/{coin_without_duties.id}")
    data = response.json

    assert response.status_code == 200
    assert data["duties"] == []


def test_coin_has_non_integer_id_v2(client, coin_with_duties):
    response = client.get(f"/v2/coins/{coin_with_duties.id}")
    data = response.json

    assert isinstance(data["id"], str)
    uuid.UUID(data["id"])


def test_get_coin_by_id_not_found_v2(client):
    response = client.get("/v2/coins/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."


def test_get_coin_by_id_invalid_uuid_v2(client):
    response = client.get("/v2/coins/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."


def test_get_coin_by_id_returns_id_name_and_associated_duties_v2(client, coin_with_duties):
    response = client.get(f"/v2/coins/{coin_with_duties.id}")
    data = response.json

    assert set(data.keys()) == {"id", "name", "duties"}
    assert len(data) == 3