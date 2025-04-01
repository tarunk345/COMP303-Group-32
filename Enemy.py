from typing import List, TYPE_CHECKING, Literal

from .Defense import *
from .Maze import ExampleHouse
from .imports import * 
if TYPE_CHECKING:
    from Player import HumanPlayer
    from coord import Coord
    from maps.base import Map
    from message import HumanPlayer, Message
    from tiles.base import MapObject
    from tiles.map_objects import *


class Enemy(NPC, Defense, CharacterMapObject):
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

    def player_moved(self, player: HumanPlayer) -> List[Message]:
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
    
class Minotaur(Enemy):
    _instance = None #Singleton

    @staticmethod
    def get_instance():
        if Minotaur._instance is None:
            Minotaur._instance = Minotaur()
        return Minotaur._instance

    def __init__(self):
        if Minotaur._instance is not None:
            raise Exception("Minotaur is a singleton")

        super().__init__(
            defense=100,
            attack_damage=25,
            name="Minotaur",
            image="minotaur",  # Replace with your actual image name
            encounter_text="The final boss has appeared!",
            facing_direction='down',
            staring_distance=5
        )

    def player_interacted(self, player: maze_player) -> List[DialogueMessage]:
        messages = [
            DialogueMessage(self, player, "The Minotaur has attacked you!", self.get_image())
        ]
        messages.extend(self.attack(player))
        return messages

    def get_attack_value(self) -> int:
        return self.__attack_damage

class Gladiator(Enemy):
    def __init__(
        self,
        name: str,
        image: str,
        encounter_text: str,
        attack_damage: int,
        defense: int,
        facing_direction: Literal['up', 'down', 'left', 'right'] = 'down',
        staring_distance: int = 1,
        bg_music: str = ''
    ):
        super().__init__(
            defense=defense,
            attack_damage=attack_damage,
            name=name,
            image=image,
            encounter_text=encounter_text,
            facing_direction=facing_direction,
            staring_distance=staring_distance,
            bg_music=bg_music
        )
