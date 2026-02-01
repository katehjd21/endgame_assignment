import unittest
from morelia import verify
from controllers.duties_controller import DutiesController
import os

FEATURE_DIR = os.path.dirname(__file__)

class DutiesTestCase(unittest.TestCase):

    def test_add_duties_feature(self):
        verify(os.path.join(FEATURE_DIR, 'duties.feature'), self)

    def step_an_empty_duties_collection(self):
        r'an empty duties collection'
        DutiesController.reset_duties()

# Scenario: Add a new duty successfully
    def step_I_add_a_duty_with_number_1_description_Test_Duty_and_KSBs_K_S_B(self):
        r'I add a duty with number 1, description "Test Duty", and KSBs "K, S, B"'
        DutiesController.create_duty(1, "Test Duty", ["K", "S", "B"])

    def step_the_duties_collection_should_contain_1_duty(self):
        r'the duties collection should contain 1 duty'
        all_duties = DutiesController.fetch_all_duties()
        assert len(all_duties) == 1

    def step_the_duty_s_number_should_be_1(self):
        r'the duty\'s number should be 1'
        all_duties = DutiesController.fetch_all_duties()
        assert all_duties[0].number == 1

    def step_the_duty_s_description_should_be_Test_Duty(self):
        r'the duty\'s description should be "Test Duty"'
        all_duties = DutiesController.fetch_all_duties()
        assert all_duties[0].description == "Test Duty"

    def step_the_duty_s_KSBs_should_be_K_S_B(self):
        r'the duty\'s KSBs should be "K, S, B"'
        all_duties = DutiesController.fetch_all_duties()
        assert all_duties[0].ksbs == ["K", "S", "B"]


#  Scenario: Prevent adding a duplicate duty
    def step_the_duties_collection_contains_a_duty_with_number_1_and_description_Existing_Duty(self):
        r'the duties collection contains a duty with number 1 and description "Existing Duty"'
        DutiesController.create_duty(1, "Existing Duty", ["K", "S", "B"])

    def step_I_try_to_add_a_duty_with_number_1_and_description_Duplicate_Duty(self):
        r'I try to add a duty with number 1 and description "Duplicate Duty"'
        duty = DutiesController.create_duty(1, "Duplicate Duty", ["K", "S", "B"])
        if duty is None:
            self.duty_was_added = False
        else:
            self.duty_was_added = True

    def step_the_addition_of_this_duty_should_fail(self):
        r'the addition of this duty should fail'
        assert self.duty_was_added is False


    def step_the_duties_collection_should_still_contain_1_duty(self):
        r'the duties collection should still contain 1 duty'
        all_duties = DutiesController.fetch_all_duties()
        assert len(all_duties) == 1


# Scenario: Delete a duty
    def step_the_duties_collection_contains_a_duty_with_number_1(self):
        r'the duties collection contains a duty with number 1'
        DutiesController.create_duty(1, "Duty to be Deleted", ["K", "S", "B"])

    def step_I_delete_the_duty_with_number_1(self):
        r'I delete the duty with number 1'
        DutiesController.delete_duty(1)

    def step_the_duties_collection_should_contain_0_duties(self):
        r'the duties collection should contain 0 duties'
        all_duties = DutiesController.fetch_all_duties()
        assert len(all_duties) == 0


# Scenario: List all duties
    def step_the_duties_collection_contains_Duty_1_and_Duty_2(self):
        r'the duties collection contains "Duty 1" and "Duty 2"'
        DutiesController.create_duty(1, "Duty 1 Description", ["K", "S", "B"])
        DutiesController.create_duty(2, "Duty 2 Description", ["K", "S", "B"])

    def step_I_list_all_duties(self):
        r'I list all duties'
        self.all_duties = DutiesController.fetch_all_duties()

    def step_I_should_see_2_duties_with_numbers_1_and_2(self):
        r'I should see 2 duties with numbers 1 and 2'
        assert len(self.all_duties) == 2
        assert self.all_duties[0].number == 1
        assert self.all_duties[1].number == 2


# Scenario: Reset all duties
    def step_the_duties_collection_contains_a_list_of_3_duties(self):
        r'the duties collection contains a list of 3 duties'
        DutiesController.create_duty(1, "Duty 1 Description", ["K", "S", "B"])
        DutiesController.create_duty(2, "Duty 2 Description", ["K", "S", "B"])
        DutiesController.create_duty(3, "Duty 3 Description", ["K", "S", "B"])

    def step_I_reset_all_duties(self):
        r'I reset all duties'
        DutiesController.reset_duties()