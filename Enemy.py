from typing import List, TYPE_CHECKING, Literal
import random
from .Defense import *
from .imports import * 
if TYPE_CHECKING:
    from Player import HumanPlayer
    from coord import Coord
    from maps.base import Map
    from message import HumanPlayer, Message
    from tiles.base import MapObject
    from tiles.map_objects import *


class Enemy(NPC, CharacterMapObject):
    def __init__(self, defense: int, attack_damage: int, name: str, image: str, encounter_text : str, facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', staring_distance: int = 0, bg_music=''): 
        super().__init__(name=name,image=image,encounter_text=encounter_text,facing_direction=facing_direction,staring_distance=staring_distance,bg_music=bg_music)
        self.__attack_damage = attack_damage
        self.__defense = defense
        self.__maze_player = Maze_Player
    
    def get_maze_player(self):
        return self.__maze_player
    

    def get_defense_value(self)->int:
        return self.__defense
    

    def get_attack_damage(self) -> int:
        return self.__attack_damage


    
    def decrease_defense(self , attack:int)->int:
        if attack >= self.__defense:
            remaining_damage = attack - self.__defense
            self.__defense = 0  # Defense is fully depleted
            
            return remaining_damage
        else:
            self.__defense -= attack
            return 0  # No remaining damage



    def attack(self)->int:
        return self.__maze_player.decrease_defense(self.__attack_damage)
    
    def is_defeated(self) -> bool:
        return self.__defense <= 0
    
    def drop_armor(self, player: "HumanPlayer",coord:Coord)->"Armor":
        armor = random.choice(list_Defense)
        armor_copy = armor.copy()
        player.get_current_room().add_to_grid(armor_copy,coord)
        return armor_copy
        
    

    def player_interacted(self, player: "HumanPlayer") -> List[Message]:
        self.decrease_defense(self.__maze_player.get_attack_value())
      
        if self.__defense == 0:
            player.get_current_room().remove_from_grid(self,self.get_current_position())
            armor_drop = self.drop_armor(player,player.get_current_position())
            return [DialogueMessage(self, player,self.get_name() + " died!"+"\n"+str(armor_drop)+" dropped!\n"+player.get_name()+" remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())]
        
        if self.attack() > 0:
            player.change_room(self.__maze_player.get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,player.get_name() + "died!",self.get_image_name())]

        return [DialogueMessage(self, player,self.get_name() + " received damage! \n"+self.get_name()+" remaining Health:"+str(self.__defense)+"\n"+player.get_name() + " received damage! \n"+player.get_name()+" remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())] 
       
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
            defense=30,
            attack_damage=25,
            name="Minotaur",
            image="minotaur",  # Replace with your actual image name
            encounter_text="The final boss has appeared!",
            facing_direction='down',
            staring_distance=5
        )

    def player_interacted(self, player: "HumanPlayer") -> List[Message]:
        self.decrease_defense(self.get_maze_player().get_attack_value())
      
        if self.get_defense_value() == 0:
            # return [DialogueMessage(self, player, f"{self.get_name()} attacks you for {self.__attack_damage} damage!", self.get_image())]
            player.get_current_room().remove_from_grid(self,self.get_current_position())
            player.change_room(self.get_maze_player().get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,self.get_name() + " died! You have cleared the Maze!",self.get_image_name())]
        
        if self.attack() > 0:
            player.change_room(self.get_maze_player().get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,player.get_name() + "died!",self.get_image_name())]

        return [DialogueMessage(self, player,self.get_name() + " received damage! \n"+self.get_name()+" remaining Health:"+str(self.get_defense_value())+"\n"+player.get_name() + " received damage! \n"+player.get_name()+" remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())] 


    

class Gladiator(Enemy):
    def __init__(
        self,
        name: str,
        image: str ,
        encounter_text: str,
        attack_damage: int,
        defense: int,
        facing_direction: Literal['up', 'down', 'left', 'right'],
        staring_distance: int,
        bg_music: str
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



    
    def custom_copy(self,attack,defense)-> "Gladiator":
        return Gladiator ("Gladiator","gladiator","a Gladiator appears before you!",attack,defense,self.get_facing_direction(),1,'')
    
    

Gladiator_Prototype = Gladiator("Gladiator","gladiator","a Gladiator appears before you!",10,10,'down',1,'')
