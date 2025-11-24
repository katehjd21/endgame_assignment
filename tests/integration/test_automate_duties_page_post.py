import pytest
from app import app
from controllers.duties_controller import DutiesController, duties_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_automate_duties_page_post_duties(client):
    DutiesController.reset_duties()

    response = client.post('/automate', data={
        'number': '1',
        'description': 'Duty 1 Description',
        'ksbs': 'Knowledge, Skills, Behaviours'
    }, follow_redirects=True)

    html = response.data.decode()
    assert response.status_code == 200

    all_duties = DutiesController.fetch_all_duties()
    for duty in all_duties:
        assert f"<td>{duty.number}</td>" in html
        assert f"<td>{duty.description}</td>" in html
        assert f"<td>{', '.join(duty.ksbs)}</td>" in html



def test_automate_duties_page_post_duties_with_empty_description(client):
    DutiesController.reset_duties()
    response = client.post('/automate', data={
        'number': '1',
        'description': '',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    html = response.data.decode()

    assert response.status_code == 200

    all_duties = DutiesController.fetch_all_duties()
    for duty in all_duties:
        assert f"<td>{duty.number}</td>" in html
        assert f"<td>{duty.description}</td>" in html
        assert f"<td>{', '.join(duty.ksbs)}</td>" in html


def test_automate_duties_rejects_non_integer_number(client):
    DutiesController.reset_duties()

    response = client.post('/automate', data={
        'number': 'abc',               
        'description': 'Test duty',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    html = response.data.decode()
    assert response.status_code == 200

    assert "Duty number must be a whole number" in html
    assert len(DutiesController.fetch_all_duties()) == 0

def test_automate_duties_rejects_float_number(client):
    DutiesController.reset_duties()

    response = client.post('/automate', data={
        'number': '1.5',
        'description': 'Test duty',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    html = response.data.decode()
    assert "Duty number must be a whole number" in html
    assert len(DutiesController.fetch_all_duties()) == 0

def test_reset_duties_clears_table(client):
    DutiesController.reset_duties()
    client.post('/automate', data={
        'number': '1',
        'description': 'Test Duty Description',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    assert len(DutiesController.fetch_all_duties()) == 1

    response = client.post('/reset_duties', follow_redirects=True)
    assert response.status_code == 200

    assert len(DutiesController.fetch_all_duties()) == 0
    html = response.data.decode()
    assert "<tbody>" in html
    assert "<td>" not in html

def test_mark_duty_complete(client):
    DutiesController.reset_duties()
    client.post('/automate', data={
        'number': '1',
        'description': 'Test Duty',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    duty = DutiesController.fetch_all_duties()[0]
    assert duty.complete is False

    response = client.post(f'/complete_duty/{duty.number}', follow_redirects=True)
    assert response.status_code == 200

    duty = DutiesController.fetch_all_duties()[0]
    assert duty.complete is True


def test_delete_duty(client):
    DutiesController.reset_duties()
    
    client.post('/automate', data={
        'number': '1',
        'description': 'Test Duty',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    client.post('/automate', data={
        'number': '2',
        'description': 'Test Duty 2',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)
    
    assert len(DutiesController.fetch_all_duties()) == 2
   
    response = client.post('/delete_duty/1', follow_redirects=True)
    assert response.status_code == 200
    
    remaining_duty_numbers = []
    for duty in DutiesController.fetch_all_duties():
        remaining_duty_numbers.append(duty.number)

    assert 1 not in remaining_duty_numbers
    assert 2 in remaining_duty_numbers

def test_edit_existing_duty(client):
    DutiesController.reset_duties()

    client.post('/automate', data={
        'number': '1',
        'description': 'Original Duty',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    duty = DutiesController.get_duty(1)
    assert duty.description == 'Original Duty'
    assert duty.ksbs == ['K', 'S', 'B']

    client.post('/edit_duty/1', data={
        'description': 'Updated Duty',
        'ksbs': 'K1, S1, B1'
    }, follow_redirects=True)

    duty = DutiesController.get_duty(1)
    assert duty.description == 'Updated Duty'
    assert duty.ksbs == ['K1', 'S1', 'B1']

def test_edit_nonexistent_duty(client):
    DutiesController.reset_duties()

    response = client.post('/edit_duty/999', data={
        'description': 'Does not exist',
        'ksbs': 'K, S, B'
    }, follow_redirects=True)

    duty = DutiesController.get_duty(999)
    assert duty is None