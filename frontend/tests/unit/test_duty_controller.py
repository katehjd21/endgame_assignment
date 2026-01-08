import pytest
from models.duty import Duty
from controllers.duty_controller import DutyController

@pytest.fixture 
def duty():
    return Duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])
 
@pytest.fixture
def duty_controller():
    return DutyController()

def test_duty_controller_can_save_duty(mocker, duty, duty_controller):
    mocked_save = mocker.patch("models.duty.Duty.save", return_value=True)
    duty_controller.save_duty(duty)
    assert mocked_save.call_count == 1

def test_duty_controller_can_fetch_duty(mocker, duty, duty_controller):
    mocked_get_duty = mocker.patch("models.duty.Duty.get_duty", return_value=duty)
    fetched_duty = duty_controller.fetch_duty()
    assert mocked_get_duty.call_count == 1
    assert fetched_duty == duty
    assert fetched_duty.number == 1
    assert fetched_duty.description == "Test Description"
    assert fetched_duty.ksbs == ["Knowledge", "Skills", "Behaviours"]
    assert fetched_duty.complete is False

