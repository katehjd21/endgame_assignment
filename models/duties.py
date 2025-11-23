class Duties():
    def __init__(self):
        self._duties = []
    
    def add_duty(self, duty):
        for existing_duty in self._duties:
            if existing_duty.number == duty.number:
                return None
        self._duties.append(duty)
        return duty
    
    def get_all_duties(self):
        return self._duties
    
    def delete_duty(self, number):
        updated_duties = []

        for duty in self._duties:
            if duty.number != number:
                updated_duties.append(duty)

        self._duties = updated_duties
    
    def get_duty(self, number):
        for duty in self._duties:
            if duty.number == number:
                return duty
        return None
    
    def edit_duty(self, number, new_description, new_ksbs):
        for duty in self._duties:
            if duty.number == number:
                duty.description = new_description
                duty.ksbs = new_ksbs
                return duty   
        return None 
    
    def reset(self):
        self._duties.clear()
