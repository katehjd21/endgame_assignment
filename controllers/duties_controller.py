from models.duties import Duties
from models.duty import Duty

duties_store = Duties()

class DutiesController():

    @staticmethod
    def fetch_all_duties():
        return duties_store.get_all_duties()
    
    @staticmethod
    def create_duty(number, description, ksbs):
        duty = Duty(number, description, ksbs)
        created_duty = duties_store.add_duty(duty)
        return created_duty
    
    @staticmethod
    def delete_duty(number):
        return duties_store.delete_duty(number)
    
    @staticmethod
    def edit_duty(number, new_description, new_ksbs):
        return duties_store.edit_duty(number, new_description, new_ksbs)

    @staticmethod
    def get_duty(number):
        return duties_store.get_duty(number)

    @staticmethod
    def reset_duties():
        duties_store.reset()
