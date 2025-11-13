import pytest
from models.duty import Duty

@pytest.fixture
def duty():
    return Duty(1, "Test description", ["Knowledge", "Skills", "Behaviours"])

def test_duty_creation(duty):
    assert duty.number == 1
    assert duty.description == "Test description"
    assert duty.ksbs == ["Knowledge", "Skills", "Behaviours"]
    assert duty.complete is False

def test_mark_duty_complete(duty):
    duty.mark_complete()
    assert duty.complete is True

def test_get_duty():
    retrieved_duty = Duty.get_duty()
    assert retrieved_duty.number == 1
    assert retrieved_duty.description == "Random Duty Description"
    assert retrieved_duty.ksbs == ["K", "S", "B"]
    assert retrieved_duty.complete is False

def test_duty_is_complete():
    duty = Duty(1, "Test", ["K", "S", "B"])
    duty.mark_complete()
    assert duty.is_complete() == "Duty Complete!"

def test_duty_is_not_complete():
    duty = Duty(2, "Test Description", ["K", "S", "B"])
    assert duty.is_complete() == "Duty Not Completed!"