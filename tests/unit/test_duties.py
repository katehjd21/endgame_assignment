import pytest
from models.duties import Duties
from models.duty import Duty

@pytest.fixture
def duties():
    return Duties()

@pytest.fixture
def duty():
    return Duty(1, "Test description", ["Knowledge", "Skills", "Behaviours"])

def test_add_duty(duties, duty):
    assert duties.add_duty(duty) == duty

def test_get_all_duties(duties, duty):
    duties.add_duty(duty)
    assert duties.get_all_duties() == [duty]

