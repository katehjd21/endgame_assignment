# PATCH/UPDATE COIN V1
def test_patch_coin_updates_coin_name_v1(client, coin):
    response = client.patch(f"/v1/coins/{coin.id}", json={"name": "Updated Coin Name"})
    data = response.json

    assert response.status_code == 200
    assert data["name"] == "Updated Coin Name"  


def test_patch_coin_returns_400_if_missing_name_key_v1(client, coin):
    response = client.patch(f"/v1/coins/{coin.id}", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Missing 'name' key in request body."


def test_patch_coin_returns_400_if_name_is_whitespace_v1(client, coin):
    response = client.patch(f"/v1/coins/{coin.id}", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_patch_returns_400_if_coin_name_empty_v1(client, coin):
    response = client.patch(f"/v1/coins/{coin.id}", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_patch_coin_returns_400_if_invalid_id_v1(client):
    response = client.patch("/v1/coins/invalid_id", json={"name": "Updated Coin Name"})

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."


def test_patch_coin_returns_404_if_not_found_v1(client):
    response = client.patch("/v1/coins/00000000-0000-0000-0000-000000000000", json={"name": "Updated Coin Name"})

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."


# PATCH/UPDATE COIN V2
def test_patch_coin_updates_coin_name_v2(client, coin):
    response = client.patch(f"/v2/coins/{coin.id}", json={"name": "Updated Coin Name"})
    data = response.json

    assert response.status_code == 200
    assert data["name"] == "Updated Coin Name" 


def test_patch_coin_updates_duties_v2(client, coin_with_duties, duties):
    coin = coin_with_duties  
    
    response = client.patch(f"/v2/coins/{coin.id}", json={
        "duty_codes": [duties[2].code]  
    })

    data = response.json

    assert response.status_code == 200
    assert "duties" in data  
    assert len(data["duties"]) == 1

    updated_duty = data["duties"][0]
    assert updated_duty["code"] == duties[2].code
    assert updated_duty["name"] == duties[2].name 


def test_patch_coin_updates_name_and_duties_v2(client, coin_with_duties, duties):
    coin = coin_with_duties

    response = client.patch(f"/v2/coins/{coin.id}", json={
        "name": "Updated Coin Name",
        "duty_codes": [duties[2].code]  
    })

    data = response.json

    assert response.status_code == 200
    assert data["name"] == "Updated Coin Name"
    assert "duties" in data
    assert len(data["duties"]) == 1
    assert data["duties"][0]["code"] == duties[2].code


def test_patch_coin_removes_all_duties_v2(client, coin_with_duties):
    coin = coin_with_duties

    response = client.patch(f"/v2/coins/{coin.id}", json={
        "duty_codes": []
    })

    data = response.json

    assert response.status_code == 200
    assert data["duties"] == []
    

def test_patch_coin_accepts_lowercase_duty_codes_v2(client, coin, duties):
    response = client.patch(f"/v2/coins/{coin.id}", json={
        "duty_codes": [duties[0].code.lower()]
    })

    data = response.json
    assert response.status_code == 200
    assert data["duties"][0]["code"] == duties[0].code


def test_patch_coin_returns_400_if_missing_name_key_v2(client, coin):
    response = client.patch(f"/v2/coins/{coin.id}", json={})

    assert response.status_code == 400
    assert response.json["description"] == "Request body is empty."


def test_patch_coin_returns_400_if_name_is_whitespace_v2(client, coin):
    response = client.patch(f"/v2/coins/{coin.id}", json={"name": "   "})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_patch_returns_400_if_coin_name_empty_v2(client, coin):
    response = client.patch(f"/v2/coins/{coin.id}", json={"name": ""})

    assert response.status_code == 400
    assert response.json["description"] == "Coin name cannot be empty."


def test_patch_coin_returns_400_if_invalid_id_v2(client):
    response = client.patch("/v2/coins/invalid_id", json={"name": "Updated Coin Name"})

    assert response.status_code == 400
    assert response.json["description"] == "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."


def test_patch_coin_returns_400_for_invalid_duty_id_v2(client, coin):
    response = client.patch(f"/v2/coins/{coin.id}", json={
       "duty_codes": ["InvalidCode"]
    })

    assert response.status_code == 400


def test_patch_coin_returns_404_if_not_found_v2(client):
    response = client.patch("/v2/coins/00000000-0000-0000-0000-000000000000", json={"name": "Updated Coin Name"})

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."