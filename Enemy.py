from typing import List

from Player import HumanPlayer
from coord import Coord
from maps.base import Map
from message import HumanPlayer, Message
from tiles.base import MapObject
from tiles.map_objects import *
from Defense import Defense
from player import maze_player
from Maze import Maze


class Enemy(NPC, Defense, MapObject):
    def __init__(self, defense: int, attack_damage: int, name: str, image: str, encounter_text : str, facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', staring_distance: int = 0, bg_music=''): 
        super().__init__(name=name,image=image,encounter_text=encounter_text,facing_direction=facing_direction,staring_distance=staring_distance,bg_music=bg_music)
        self.__attack_damage = attack_damage
        self.__defense = defense
        self.__init_defense = defense
    
    def get_defense_value(self)->int:
        return self.__defense
    
    def get_attack_damage(self) -> int:
        return self.__attack_damage
    
    def get_image(self) -> str:
        return self._image_name
    
    def decrease_defense(self , attack:int)->int:
        if attack >= self.__defense:
            remaining_damage = attack - self.__defense
            self.__defense = 0  # Defense is fully depleted
            
            return remaining_damage
        else:
            self.defense -= attack
            return 0  # No remaining damage

    def player_moved(self, player: maze_player) -> List[Message]:
        """Handle the event of the player moving. If the player is within a certain distance, the enemy attacks."""
        messages: List[Message] = super().player_moved(player)  # Call the parent class's method

        if type(player) != maze_player:
            return messages

        dist = self._current_position.distance(player.get_current_position())
        if dist <= self.__staring_distance:

            attack_messages = self.attack(player)
            messages.extend(attack_messages)

        return messages 

    def attack(self, player: maze_player):
        player.decrease_defense(self.__attack_damage)
        return [DialogueMessage(self, player, f"{self.get_name()} attacks you for {self.__attack_damage} damage!", self.get_image())]
    
    def is_defeated(self) -> bool:
        return self.__defense <= 0
    
    def heal(self, heal_amt) -> int:
        self.__defense += heal_amt
        if self.__init_defense < self.__defense:
            self.__defense = self.__init_defense
        return self.__defense
    

    