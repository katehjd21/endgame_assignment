import pytest
from app import app
from controllers.duties_controller import DutiesController
from models.duty import Duty

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_automate_duties_page_get_duties(client):
    DutiesController.reset_duties()
    duty = DutiesController.create_duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])

    response = client.get('/automate')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<table>" in html

    all_duties = DutiesController.fetch_all_duties()
    for duty in all_duties:
        assert f"<td>{duty.number}</td>" in html
        assert f"<td>{duty.description}</td>" in html
        assert f"<td>{', '.join(duty.ksbs)}</td>" in html

def test_automate_page_get_multiple_duties(client):
    DutiesController.reset_duties()
    DutiesController.create_duty(1, "Duty One Description", ["Knowledge", "Skills", "Behaviours"])
    DutiesController.create_duty(2, "Duty Two Description", ["Knowledge", "Skills", "Behaviours"])

    response = client.get('/automate')
    html = response.data.decode()

    assert response.status_code == 200
    assert "<table>" in html

    all_duties = DutiesController.fetch_all_duties()
    for duty in all_duties:
        assert f"<td>{duty.number}</td>" in html
        assert f"<td>{duty.description}</td>" in html
        assert f"<td>{', '.join(duty.ksbs)}</td>" in html
