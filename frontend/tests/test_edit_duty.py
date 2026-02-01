import unittest
from morelia import verify
from controllers.duties_controller import DutiesController
import os

FEATURE_DIR = os.path.dirname(__file__)

class TestEditDuty(unittest.TestCase):
    def test_add_edit_duty_feature(self):
        verify(os.path.join(FEATURE_DIR, 'edit_duty.feature'), self)

    def step_Given_there_is_a_duty_with_number_1_and_description_Original_Duty_Description_and_KSBs_K_S_B(self):
        r'there is a duty with number 1 and description "Original Duty Description" and KSBs "K, S, B"'
        DutiesController.reset_duties()
        DutiesController.create_duty(1, "Original Duty Description", ["K", "S", "B"])

    def step_When_I_edit_the_duty_with_number_1_to_have_description_Updated_Duty_Description_and_KSBs_K1_S1_B1(self):
        r'I edit the duty with number 1 to have description "Updated Duty Description" and KSBs "K1, S1, B1"'
        self.edit_result = DutiesController.edit_duty(1, "Updated Duty Description", ["K1", "S1", "B1"])

    def step_Then_the_duty_with_number_1_should_have_description_Updated_Duty_Description(self):
        r'the duty with number 1 should have description "Updated Duty Description"'
        duty = DutiesController.get_duty(1)
        assert duty.description == "Updated Duty Description"

    def step_And_the_duty_with_number_1_should_have_KSBs_K1_S1_B1(self):
        r'the duty with number 1 should have KSBs "K1, S1, B1"'
        duty = DutiesController.get_duty(1)
        assert duty.ksbs == ["K1", "S1", "B1"]

    def step_When_I_try_to_edit_a_duty_with_number_999_to_have_description_Duty_Does_Not_Exist_and_KSBs_K_S_B(self):
        r'I try to edit a duty with number 999 to have description "Duty Does Not Exist" and KSBs "K, S, B"'
        self.edit_result = DutiesController.edit_duty(999, "Duty Does Not Exist",["K", "S", "B"])

    def step_Then_the_edit_should_fail(self):
        r'the edit should fail'
        assert self.edit_result is None
