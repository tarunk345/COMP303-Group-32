from coord import Coord
from maps.base import Map
from tiles.base import MapObject
from tiles.map_objects import *


class Enemy(NPC):
    def __init__(self, health: int, attack_damage: int, name: str, image: str, encounter_text : str, facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', staring_distance: int = 0, bg_music=''): 
        super().__init__(name=name,image=image,encounter_text=encounter_text,facing_direction=facing_direction,staring_distance=staring_distance,bg_music=bg_music)
        self.health = health
        self.attack_damage = attack_damage
    
    #def damage_player(self, player: HumanPlayer):
