import pytest
from app import app
from controllers.duties_controller import duties_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_automate_duty_to_automate_duties_page_post(client):
    duties_store._duties.clear()

    response = client.post('/automate', data={
        'number': '2',
        'description': 'New Duty Description',
        'ksbs': 'Knowledge, Skills, Behaviours'
    }, follow_redirects=True)

    html = response.data.decode()

    assert response.status_code == 200
    assert "<td>2</td>" in html
    assert "<td>New Duty Description</td>" in html
    assert "<td>Knowledge, Skills, Behaviours</td>" in html

    all_duties = duties_store.get_all_duties()
    duty_numbers = []
    for duty in all_duties:
        duty_numbers.append(duty.number)
    assert "2" in duty_numbers


def test_automate_post_to_automate_duties_page_with_empty_ksbs(client):
    duties_store._duties.clear()
    response = client.post('/automate', data={
        'number': '4',
        'description': 'No KSBS Duty',
        'ksbs': ''
    }, follow_redirects=True)

    html = response.data.decode()
    assert response.status_code == 200
    assert "<td></td>" in html