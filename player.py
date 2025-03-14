from typing import Any, Literal
from typing import Optional
from coord import Coord
from maps.base import Map
from message import Literal
from tiles.base import MapObject
from tiles.map_objects import *
from Armor_set import Armor_Set
from Defense import Defense
from Armors import *
from Potions import *


    

class maze_player(HumanPlayer,Defense):
    def __init__(self,defense : int, attack_damage: int, 
                 name: str, websocket_state: Any = None, email: str = "", 
                 image: str = 'player1', facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', passable: bool = True) -> None:
        super().__init__(name, websocket_state, email, image, facing_direction, passable)
        self.__defense: int  = defense
        self.__attack_damage = attack_damage
        self.__armor_set: Armor_Set = Armor_Set()

    def get_defense_value(self)->int:
        return self.__defense


    def decrease_defense(self , attack:int)->int:
        attack = self.__armor_set.decrease_defense(attack)
        if attack < self.__defense:
            self.defense = self.defense - attack
            return 0

        self.__defense = 0
        return 1
    
    def check_armor_player(self, armor : Armor)->Optional[Armor]:
        return self.__armor_set.add_armor(armor)
    

    def check_potion_player(self, potion: Potion):
        return self.__armor_set.add_potion(potion)

        
        
