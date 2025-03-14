from Defense import Defense
from Armors import *
from typing import Optional

class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.__list_armors : list[Defense] = []
        

    def get_defense_value(self) -> int:
        defense = 0
        for armor in self.__list_armors:
            defense += armor.get_defense_value()
        
        return defense


    def decrease_defense(self,attack:int)->int:
        
        for armor in self.__list_armors:
            attack = armor.decrease_defense(attack)
        
        return attack
    
    def __str__(self) -> str:
        string = ''
        for armor in self.__list_armors:
            string.__add__(str(armor) + ',')
        return string
    
    
    def add_armor(self, armor : Armor)->Optional[Armor]  :

        for check_armor in self.__list_armors:


            if isinstance(check_armor, armor.__class__):

                if check_armor.get_defense_value()<armor.get_defense_value():
                    self.__list_armors.remove(check_armor)
                    self.__list_armors.append(armor)
                    return check_armor
                else :
                    return armor
                
        
        return None










