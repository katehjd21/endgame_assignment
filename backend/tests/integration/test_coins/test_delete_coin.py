# DELETE COIN
def test_delete_coin_removes_coin_from_database(client, coin):
    response = client.delete(f"/coins/{coin.id}")

    assert response.status_code == 200
    assert response.json["message"] == "Coin has been successfully deleted!"

    get_response = client.get(f"/v1/coins/{coin.id}")
    assert get_response.status_code == 404


def test_delete_coin_returns_400_if_invalid_id(client):
    response = client.delete("/coins/invalid_id")

    assert response.status_code == 400
    assert response.json["description"] == (
        "Invalid Coin ID format. Coin ID must be a UUID (non-integer)."
    )


def test_delete_coin_returns_404_if_not_found(client):
    response = client.delete("/coins/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json["description"] == "Coin not found."