from Defense import Defense


class Armor(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.armor_value:int 

    def get_defence_value(self) -> int:
        return self.armor_value
    
    