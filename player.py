from typing import Any, Literal
from typing import Optional
from coord import Coord
from maps.base import Map
from message import Literal, Message
from tiles.base import MapObject
from tiles.map_objects import *
from Armor_set import Armor_Set
from Defense import Defense
from Armors import *
from Potions import *


    

class maze_player(HumanPlayer,Defense):
    def __init__(self,defense : int, attack_value: int,attack_value_without_armor:int, 
                 name: str, websocket_state: Any = None, email: str = "", 
                 image: str = 'player1', facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', passable: bool = True) -> None:
        super().__init__(name, websocket_state, email, image, facing_direction, passable)
        self.__attack_value_without_armor:int = attack_value_without_armor
        self.__defense: int  = defense
        self.__attack_value = attack_value
        self.__armor_set: Armor_Set = Armor_Set()

    def get_defense_value(self)->int:
        return self.__defense
    
    def get_attack_value(self) -> int:
        return self.__attack_value


    def decrease_defense(self , attack:int)->int:
        attack = self.__armor_set.decrease_defense(attack)
        if attack < self.__defense:
            self.defense = self.defense - attack
            return 0

        self.__defense = 0
        return 1
    
    def check_armor_player(self, armor : Armor)->Optional[Defense]:
        return self.__armor_set.add_armor(armor)
    

    def check_potion_player(self, potion: Potion):
        return self.__armor_set.add_potion(potion)

        
        
    def update_attack_value(self):
        self.__attack_value = self.__armor_set.get_attack_value()+self.__attack_value_without_armor
