import pytest
from app import app
from controllers.duties_controller import duties_store
from models.duty import Duty

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_automate_duties_page_get(client):
    duties_store._duties.clear()
    duty = Duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])
    duties_store.add_duty(duty)

    response = client.get('/automate')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<td>1</td>" in html
    assert "<td>Test Description</td>" in html
    assert "<td>Knowledge, Skills, Behaviours</td>" in html
    assert "<table>" in html

def test_automate_page_get_multiple_duties(client):
    duties_store._duties.clear()
    duties_store.add_duty(Duty(1, "Duty One Description", ["Knowledge", "Skills", "Behaviours"]))
    duties_store.add_duty(Duty(2, "Duty Two Description", ["Knowledge", "Skills", "Behaviours"]))

    response = client.get('/automate')
    html = response.data.decode()

    assert "<td>1</td>" in html
    assert "<td>2</td>" in html
    assert "Duty One Description" in html
    assert "Duty Two Description" in html
