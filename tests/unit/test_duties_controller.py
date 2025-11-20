import pytest
from models.duties import Duties
from models.duty import Duty
from controllers.duties_controller import DutiesController, duties_store

@pytest.fixture
def duty():
    return Duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])

@pytest.fixture
def duties_controller():
    return DutiesController()


def test_duties_controller_can_fetch_all_duties(mocker, duties_controller):
    list_of_duties = [Duty(1, "Description", ["K", "S", "B"]), Duty(2, "Description", ["K", "S", "B"])]
    mocked_get_all_duties = mocker.patch.object(duties_store, "get_all_duties", return_value=list_of_duties)
    fetched_list_of_duties = duties_controller.fetch_all_duties()
    mocked_get_all_duties.assert_called_once()
    assert fetched_list_of_duties == list_of_duties
    assert len(fetched_list_of_duties) == len(list_of_duties)

def test_duties_controller_can_add_a_duty_to_the_duties_store(mocker, duty, duties_controller):
    mocked_add_duty = mocker.patch.object(duties_store, "add_duty", return_value=duty)
    created_duty = duties_controller.create_duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])
    mocked_add_duty.assert_called_once() 
    assert created_duty.number == 1
    assert created_duty.description == "Test Description"
    assert created_duty.ksbs == ["Knowledge", "Skills", "Behaviours"]
    assert created_duty.complete is False


