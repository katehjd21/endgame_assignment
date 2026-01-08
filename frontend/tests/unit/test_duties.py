import pytest
from models.duties import Duties
from models.duty import Duty

@pytest.fixture
def duties():
    return Duties()

@pytest.fixture
def duty1():
    return Duty(1, "Test description 1", ["Knowledge", "Skills", "Behaviours"])

@pytest.fixture
def duty2():
    return Duty(2, "Test description 2", ["Knowledge", "Skills", "Behaviours"])

def test_add_duty(duties, duty1):
    assert duties.add_duty(duty1) == duty1
    assert duties.get_all_duties() == [duty1]

def test_add_multiple_unique_duties(duties, duty1, duty2):
    added_duty_1 = duties.add_duty(duty1)
    added_duty_2 = duties.add_duty(duty2)
    assert duties.get_all_duties() == [added_duty_1, added_duty_2]

def test_add_duty_ensures_no_duties_have_same_number(duties, duty1):
    added_duty_1 = duties.add_duty(duty1)
    duplicate_duty = duties.add_duty(duty1)
    assert duplicate_duty == None
    assert duties.get_all_duties() == [added_duty_1]

def test_duplicate_number_with_different_description(duties, duty1):
    duty1_different_description = Duty(1, "Different description", ["K1", "S1", "B1"])
    duties.add_duty(duty1)
    assert duties.add_duty(duty1_different_description) is None
    assert duties.get_all_duties() == [duty1]

def test_get_all_duties(duties, duty1):
    duties.add_duty(duty1)
    assert duties.get_all_duties() == [duty1]

def test_delete_duty(duties, duty1, duty2):
    duties.add_duty(duty1)
    duties.add_duty(duty2)
    duties.delete_duty(2)

    remaining_duty_numbers = []
    for duty in duties.get_all_duties():
        remaining_duty_numbers.append(duty.number)
    
    assert len(remaining_duty_numbers) == 1
    assert remaining_duty_numbers[0] == duty1.number

def test_delete_nonexistent_duty_does_nothing(duties, duty1):
    duties.add_duty(duty1)
    duties.delete_duty(111)
    
    all_duty_numbers = []
    for duty in duties.get_all_duties():
        all_duty_numbers.append(duty.number)
    
    assert 1 in all_duty_numbers
    assert len(all_duty_numbers) == 1

def test_get_duty_returns_correct_duty(duties, duty1, duty2):
    duties.add_duty(duty1)
    duties.add_duty(duty2)
    retrieved_duty = duties.get_duty(1)
    other_retrieved_duty = duties.get_duty(2)

    assert retrieved_duty is duty1
    assert retrieved_duty.description == "Test description 1"
    assert other_retrieved_duty is duty2
    assert other_retrieved_duty.description == "Test description 2"

def test_get_duty_returns_none_if_not_found(duties):
    assert duties.get_duty(999) is None

def test_edit_duty_updates_fields(duties, duty1):
    duties.add_duty(duty1)

    updated_duty = duties.edit_duty(1,"Updated Duty Description",["New K", "New S", "New B"])

    assert updated_duty.description == "Updated Duty Description"
    assert updated_duty.ksbs == ["New K", "New S", "New B"]

def test_edit_nonexistent_duty_returns_none(duties):
    updated_duty = duties.edit_duty(999, "Non-existent Duty", ["K", "S", "B"])
    assert updated_duty is None

def test_reset_all_duties(duties, duty1, duty2):
    duties.add_duty(duty1)
    duties.add_duty(duty2)
    assert len(duties.get_all_duties()) == 2  

    duties.reset()

    assert duties.get_all_duties() == []
    assert len(duties.get_all_duties()) == 0
