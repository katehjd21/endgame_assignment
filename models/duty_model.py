class Duty:
    def __init__(self, number, description, ksbs):
        self.number = number
        self.description = description
        self.ksbs = ksbs
        self.complete = False
    
    @staticmethod
    def get_duty():
      return Duty("Duty 1", "Random Duty Description", ["Knowledge", "Skills", "Behaviours"])

    def mark_complete(self):
        self.complete = True

    def save(self):
      print(f"Duty {self.number} has been saved!")
  
    def is_complete(self):
      if self.complete:
        return "Duty Complete!"
      else:
        return "Duty Not Completed!"