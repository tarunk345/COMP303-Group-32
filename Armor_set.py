from Defense import Defense
from Armors import Armor
from typing import Optional
from Potions import Potion
import random

class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.__list_armors : list[Defense] = []
        

    def get_defense_value(self) -> int:
        defense = 0
        for armor in self.__list_armors:
            defense += armor.get_defense_value()
        
        return defense
    
    def get_attack_value(self) -> int:

        attack = 0
        for armor in self.__list_armors:
            attack += armor.get_attack_value()
        
        return attack
        


    def decrease_defense(self,attack:int)->int:
        """remainging attack is returned"""
        
        for armor in self.__list_armors:
            attack = armor.decrease_defense(attack)
        
        return attack
    
    def __str__(self) -> str:
        string = ''
        for armor in self.__list_armors:
            string.__add__(str(armor) + ',')
        return string
    
    
    def add_armor(self, armor : Armor)->Optional[Defense]  :
        """return None if armor added
            return old armor if armor is changes
            return new armor if armor is not added"""
        armor_stats = armor.get_defense_value() + armor.get_attack_value()

        for check_armor in self.__list_armors:
            if isinstance(check_armor,(Potion,Armor)): 
                if check_armor.get_defense_type() == armor.get_defense_type():
                    check_armor_stats = check_armor.get_defense_value()+check_armor.get_attack_value()
                    if check_armor_stats<armor_stats:
                        self.__list_armors.remove(check_armor)
                        self.__list_armors.append(armor)
                        return check_armor
                    else :
                        return armor
                
        
        return None
    
    def add_potion(self, potion : Potion)->Optional[Potion]  :
        """return None if potion added
            return new potion if potion is not added"""
        """potion can be applied on armors which already has potion applied to them"""

        if len(self.__list_armors) == 0:
            return potion
        
        armor = random.choice(self.__list_armors)
        potion.set_armor(armor)
        self.__list_armors.remove(armor)
        self.__list_armors.append(potion)
    
        return None
    

    
        










