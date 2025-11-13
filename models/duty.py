class Duty:
    def __init__(self, number, description, ksbs):
        self.number = number
        self.description = description
        self.ksbs = ksbs
        self.complete = False
    
    @staticmethod
    def get_duty():
      return Duty(1, "Random Duty Description", ["K", "S", "B"])

    def mark_complete(self):
        self.complete = True

    def save(duty):
      print(f"Duty {duty.number} has been saved!")
  
    def is_complete(self):
      if self.complete:
        return "Duty Complete!"
      else:
        return "Duty Not Completed!"