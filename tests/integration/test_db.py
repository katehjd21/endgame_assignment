from models.db import Db
from models.duty_model import Duty
import pytest

@pytest.fixture 
def duty():
    return Duty("Duty 1", "Test Description", ["Knowledge", "Skills", "Behaviours"])

@pytest.fixture
def db():
    return Db()

def test_user_can_read_all_duties(mocker, duty, db):
    mocker.patch.object(db, "list_all_duties", return_value=[duty])
    assert db.list_all_duties() == [duty]

def test_user_can_save_a_duty(mocker, duty, db):
    mocked_save = mocker.patch.object(db, "save", return_value=True)
    assert db.save(duty) == True
    assert mocked_save.call_count == 1
    mocked_save.assert_called_with(duty)

def test_user_can_read_a_single_duty_by_duty_number(mocker, duty, db):
    mocker.patch.object(db, "read", return_value=duty)
    assert db.read(1) == duty

def test_user_can_update_a_duty(mocker, duty, db):
    mocker.patch.object(db, "update", return_value=duty)
    duty.description = "New Description!"
    updated_duty = db.update()
    assert updated_duty.description == "New Description!"

def test_user_can_delete_a_duty(mocker, db):
    mocked_delete = mocker.patch.object(db, "delete", return_value=None)
    assert db.delete() == None
    assert mocked_delete.call_count == 1


