from Defense import Defense
from Armors import *

class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.list_armors : list[Defense] = []
        

    def get_defense_value(self) -> int:
        for armor in self.list_armors:
            defense = defense + armor.get_defense_value()
        
        return defense


    def decrease_defense(self,attack:int)->int:
        
        for armor in self.list_armors:
            attack = armor.decrease_defense(attack)
        
        return attack


