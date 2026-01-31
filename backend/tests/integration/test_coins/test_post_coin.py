import uuid

# POST COIN V1
def test_post_coin_creates_coin_v1(client):
    response = client.post("/v1/coins", json={"name": "New Coin"})
    data = response.json

    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert data["name"] == "New Coin"
    uuid.UUID(data["id"])


def test_post_coin_returns_400_if_name_key_missing_v1(client):
    response = client.post("/v1/coins", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Missing 'name' key in request body."


def test_post_coin_returns_400_if_missing_coin_name_v1(client):
    response = client.post("/v1/coins", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_post_coin_returns_400_if_name_is_whitespace_v1(client):
    response = client.post("/v1/coins", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_post_coin_returns_400_if_duplicate_coin_name_v1(client, coins):
    response = client.post("/v1/coins", json={"name": "Automate"})

    assert response.status_code == 400
    assert response.json["description"] == "Coin already exists. Please choose another name."



# POST COIN V2
def test_post_coin_creates_coin_v2(client):
    response = client.post("/v2/coins", json={"name": "New Coin"})
    data = response.json

    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert data["name"] == "New Coin"
    uuid.UUID(data["id"])


def test_post_coin_creates_coin_with_duties_v2(client, duties):
    duty_codes = [duty.code for duty in duties]

    response = client.post("/v2/coins", json={
        "name": "New Coin With Duties",
        "duty_codes": duty_codes
    })

    data = response.json
    assert response.status_code == 201

    assert "duties" in data
    assert len(data["duties"]) == len(duties)

    returned_codes = [duty["code"] for duty in data["duties"]]
    for code in duty_codes:
        assert code in returned_codes
    
    for duty in data["duties"]:
        uuid.UUID(duty["id"])


def test_post_coin_creates_coin_with_no_duties_v2(client):
    response = client.post("/v2/coins", json={"name": "Coin No Duties", "duty_codes": []})
    data = response.json
    assert response.status_code == 201
    assert data["duties"] == []
    

def test_post_coin_accepts_lowercase_duty_codes_v2(client, duties):
    response = client.post("/v2/coins", json={
        "name": "Coin With Lowercase Duties",
        "duty_codes": [duties[0].code.lower()] 
    })

    data = response.json
    assert response.status_code == 201
    assert "duties" in data
    assert len(data["duties"]) == 1
    assert data["duties"][0]["code"] == duties[0].code 
    assert data["duties"][0]["name"] == duties[0].name
    assert data["duties"][0]["description"] == duties[0].description


def test_post_coin_returns_400_if_name_key_missing_v2(client):
    response = client.post("/v2/coins", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Missing 'name' key in request body."


def test_post_coin_returns_400_if_missing_coin_name_v2(client):
    response = client.post("/v2/coins", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_post_coin_returns_400_if_name_is_whitespace_v2(client):
    response = client.post("/v2/coins", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_post_coin_returns_400_if_duplicate_coin_name_v2(client, coins):
    response = client.post("/v2/coins", json={"name": "Automate"})

    assert response.status_code == 400
    assert response.json["description"] == "Coin already exists. Please choose another name."


def test_post_coin_returns_400_if_invalid_duty_code_v2(client):
    response = client.post("/v2/coins", json={
        "name": "Coin Invalid Duty",
        "duty_codes": ["NON_EXISTENT_DUTY_CODE"]
    })

    assert response.status_code == 400
    assert response.json["description"] == "Duty with code 'NON_EXISTENT_DUTY_CODE' does not exist."