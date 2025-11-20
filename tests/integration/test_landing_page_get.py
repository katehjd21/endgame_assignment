import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_landing_page_get(client):
    response = client.get('/')
    html = response.data.decode()
    coins = ["Automate", "Houston", "Security", "GoingDeeper", "Assemble"]

    assert response.status_code == 200
    for coin in coins:
        assert coin in html
    assert 'href="/automate"' in html
    
