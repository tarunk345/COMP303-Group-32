from Defense import Defense
from Armors import *

class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.__list_armors : list[Armor] = []
        

    def get_defense_value(self) -> int:
        defense = 0
        for armor in self.__list_armors:
            defense += armor.get_defense_value()
        
        return defense

    def __str__(self) -> str:
        str = ''
        for armor in self.__list_armors:
            str.__add__(armor.get_name() + ',')
        return str

    def decrease_defense(self,attack:int)->int:
        
        for armor in self.__list_armors:
            attack = armor.decrease_defense(attack)
        
        return attack
    

    # def toString(self)->String:




