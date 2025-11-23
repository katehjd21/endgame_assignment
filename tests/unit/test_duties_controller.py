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


def test_can_fetch_all_duties(mocker, duties_controller):
    list_of_duties = [Duty(1, "Description", ["K", "S", "B"]), Duty(2, "Description", ["K", "S", "B"])]
    mocked_get_all_duties = mocker.patch.object(duties_store, "get_all_duties", return_value=list_of_duties)
    fetched_list_of_duties = duties_controller.fetch_all_duties()

    mocked_get_all_duties.assert_called_once()
    assert fetched_list_of_duties == list_of_duties
    assert len(fetched_list_of_duties) == len(list_of_duties)

def test_can_add_a_duty_to_the_duties_store_if_duty_number_is_unique(mocker, duty, duties_controller):
    mocked_add_duty = mocker.patch.object(duties_store, "add_duty", return_value=duty)
    created_duty = duties_controller.create_duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])

    mocked_add_duty.assert_called_once() 
    assert created_duty.number == 1
    assert created_duty.description == "Test Description"
    assert created_duty.ksbs == ["Knowledge", "Skills", "Behaviours"]
    assert created_duty.complete is False

def test_does_not_add_duties_with_duplicate_numbers_to_duties_store(mocker, duty, duties_controller):
    mocker.patch.object(duties_store, "add_duty", side_effect=[duty, None])

    created_duty = duties_controller.create_duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])
    assert created_duty == duty

    duplicate_duty = duties_controller.create_duty(1, "Test Description", ["Knowledge", "Skills", "Behaviours"])
    assert duplicate_duty is None

def test_can_delete_a_duty(mocker, duties_controller):
    mocked_delete = mocker.patch.object(duties_store, "delete_duty")

    duties_controller.delete_duty(1)

    mocked_delete.assert_called_once_with(1)

def test_controller_can_get_a_duty(mocker, duties_controller):
    mocked_get_duty = mocker.patch.object(duties_store, "get_duty", return_value="mocked duty")

    result = duties_controller.get_duty(1)

    mocked_get_duty.assert_called_once_with(1)
    assert result == "mocked duty"

def test_controller_can_edit_a_duty(mocker, duties_controller):
    mocked_edit_duty = mocker.patch.object(duties_store, "edit_duty", return_value="updated duty")

    updated_duty = duties_controller.edit_duty(1, "Updated Duty Description",["K", "S", "B"])

    mocked_edit_duty.assert_called_once_with(1, "Updated Duty Description", ["K", "S", "B"])
    assert updated_duty == "updated duty"

def test_can_reset_all_duties(mocker, duties_controller):
    mocked_reset = mocker.patch.object(duties_store, "reset")

    duties_controller.reset_duties()

    mocked_reset.assert_called_once()
    