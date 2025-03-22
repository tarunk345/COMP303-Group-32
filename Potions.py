from typing import TYPE_CHECKING
from .imports import * 
if TYPE_CHECKING:
    from message import *
    from typing import Optional
    from tiles.base import MapObject

from .Defense import Defense_type, Defense
from .Maze import Maze
from .Armors import Armor
from .player import maze_player



class Potion(Defense, MapObject):
    @abstractmethod
    def __init__(self, name :str,multiplier:int, defense_type:Defense_type,  
                 maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__name: str = name
        self.__multiplier:int = multiplier
        self.__defense_type:Defense_type = defense_type
        self.__armor:Defense
        self.__defense_value:int
        self.__attack_value:int
        self.__maze:Maze = maze

    
    def __str__(self)->str:
        return self.__name

    def get_defense_value(self) -> int:
        return self.__defense_value
    
    def set_defense_value(self,defense:int)->None:
        self.__defense_value = defense

    
    def get_attack_value(self) -> int:
        return self.__attack_value
    
    def set_attack_value(self,attack:int)->None:
        self.__attack_value = attack

    def get_multiplier(self)->int:
        return self.__multiplier
    
    def get_armor(self)->Defense:
        return self.__armor
    
    def get_defense_type(self) -> Defense_type:
        return self.__defense_type
    
    
    def set_armor(self, armor: Defense)->None:
        self.__armor = armor

    def set_fields(self):
        armor = self.__armor
        self.__name = str(armor)
        
        if(isinstance(armor,(Armor,Potion))):
            self.set_image_name(armor.get_image_name())
            self.__defense_type = armor.get_defense_type()
            self.__defense_value = armor.get_defense_value()
            self.__attack_value = armor.get_attack_value()
            

    def decrease_defense(self, attack: int) -> int:
        if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0 
        attack = attack - self.__defense_value
        self.__defense_value = 0
        return attack


    def player_entered(self, player: maze_player) -> list[Message]:
        """if potion not added put the the potion back on grid and return pick text
            if potion added then update attack value of player,update the fields of potion and return not pick text"""

        self.__maze.remove_from_grid(self , self._position)
        potion = player.check_potion_player(self)
        
        if  potion is not None:
            self.__maze.add_to_grid(self,self.get_position())
            not_pick_text : str = 'Cannot pick up the potion! No armor to put potion on!'
            return [DialogueMessage(self, player, not_pick_text,self.__name)]
        
        return[]

    
    
    

class Defense_potion(Potion):
         
    def __init__(self, name: str, multiplier: int, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, multiplier, Defense_type.DEFENSE_POTION, maze, image_name, passable, z_index)
         


    def set_fields(self):
        super().set_fields()
        self.set_defense_value(self.get_multiplier()*self.get_defense_value())


    def player_entered(self, player: maze_player) -> list[Message]:
        message = super().player_entered(player)
        if message != []:
            return message
        
        armor = self.get_armor()
        potion_image_name = self.get_image_name()
        defense_increase = (self.get_multiplier()*armor.get_defense_value()) - armor.get_defense_value()
        pick_text : str ='You picked up the '+ self.get_name() +'! It is applied to ' + str(armor)+ '.\nDefense increased by ' + str(defense_increase)+'!' 
        self.set_fields()
        return [DialogueMessage(self, player, pick_text, potion_image_name)]






class Attack_potion(Potion):

    def __init__(self, name: str, multiplier: int, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, multiplier, Defense_type.ATTACK_POTION, maze, image_name, passable, z_index)


    def set_fields(self):
        super().set_fields()
        self.set_attack_value(self.get_multiplier()*self.get_attack_value())

    def player_entered(self, player: maze_player) -> list[Message]:
        message = super().player_entered(player)
        if message != []:
            return message
        
        armor = self.get_armor()
        potion_image_name = self.get_image_name()
        attack_increase = (self.get_multiplier()*armor.get_attack_value()) - armor.get_attack_value()
        pick_text : str ='You picked up the '+ self.get_name() +'! It is applied to ' + str(armor)+ '.\nAttack increased by ' + str(attack_increase)+'!'
        self.set_fields() 
        return [DialogueMessage(self, player, pick_text, potion_image_name)]




    

    

