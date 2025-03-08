from typing import Any, Literal
from coord import Coord
from maps.base import Map
from message import Literal
from tiles.base import MapObject
from tiles.map_objects import *
from Armor_set import Armor_Set
from Defense import Defense
from Armors import *
from Enemy import Enemy


    

class maze_player(HumanPlayer, Defense):
    def __init__(self,defense : int, attack_damage: int, name: str, websocket_state: Any = None, email: str = "", image: str = 'player1', facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', passable: bool = True) -> None:
        super().__init__(name, websocket_state, email, image, facing_direction, passable)
        self.__defense: int  = defense
        self.__attack_damage = attack_damage
        self.armor_set : Armor_Set = Armor_Set()

    def get_defense_value(self)->int:
        defense : int = self.__defense
        defense = defense + self.armor_set.get_defense_value()
        return defense

    def decrease_defense(self , attack:int)->int:
        attack = self.armor_set.decrease_defense(attack)
        if attack>= self.get_defense_value():
            self.defense = self.defense - attack
            return 0

        attack = attack - self.__defense
        self.__defense = 0
        return attack

    def add_armor(self , armor : Armor):
        self.armor_set.__list_armors.append(armor)

    def attack(self, enemy: Enemy):
        enemy.decrease_defense(self.__attack_damage)
        return        








    