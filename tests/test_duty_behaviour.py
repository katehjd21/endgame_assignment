import unittest
from morelia import run, verify
from models.duty_model import Duty

class DutyTestCase(unittest.TestCase):
    duty = Duty.get_duty()
    def test_duty_complete_behaviour(self):
        verify('tests/duty.feature', self)
    
    def step_I_complete_a_duty(self):
        r'I complete a duty'      
        self.duty.complete()

           
    def step_the_result_should_be_Duty_Completed_on_the_display(self):
        r'the result should be \'Duty Completed!\' on the display'
        self.assertEqual(self.duty.is_complete(), 'Duty Complete!')

