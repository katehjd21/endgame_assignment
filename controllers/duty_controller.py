from models.duty_model import Duty


class DutyController:

    def save_duty(self, duty):
        duty.save()

    @staticmethod
    def fetch_duty():
        return Duty.get_duty()
    

