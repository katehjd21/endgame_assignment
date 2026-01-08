class Coin:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def list_all_coins():
        return [
            Coin("Automate"),
            Coin("Houston"),
            Coin("Security"),
            Coin("GoingDeeper"),
            Coin("Assemble")
        ]
    
