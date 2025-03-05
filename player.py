from typing import Any, Literal
from coord import Coord
from maps.base import Map
from message import Literal
from tiles.base import MapObject
from tiles.map_objects import *
from Armor_set import Armor_Set
from Defense import Defense


    

class player(HumanPlayer,Defense):
    def __init__(self,defense : int, attack_damage: int, name: str, websocket_state: Any = None, email: str = "", image: str = 'player1', facing_direction: Literal['up'] | Literal['down'] | Literal['left'] | Literal['right'] = 'down', passable: bool = True) -> None:
        super().__init__(name, websocket_state, email, image, facing_direction, passable)
        self.defense: int  = defense
        self.armor_set :Armor_Set = Armor_Set()

    def get_defence_value(self)->int:
        defense : int = self.defense
        defense= defense + self.armor_set.get_defence_value()
        return defense










    