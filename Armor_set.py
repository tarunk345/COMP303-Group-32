from Defense import Defense
from Armors import *

class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.list_armors : list[Defense] = []
        

    def get_defence_value(self) -> int:
        for armor in self.list_armors:
            defense = defense + armor.get_defence_value()
        
        return defense




