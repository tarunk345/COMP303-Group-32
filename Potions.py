from Defense import Defense
from Armors import *
from typing import Optional
from tiles.base import MapObject


class Potion(Defense, MapObject):
    def __init__(self, name :str, defense_multiplier:int, 
                 player :maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__name: str = name
        self.__defense_multiplier:int = defense_multiplier
        self.__defense_value:int
        self.__armor: Defense
        self.__pick_text : str ='You picked up the '+ name +'! It is applied to '
        self.__not_pick_text : str = 'Cannot pick up the potion! No armor to put potion on!'
        self.__player :maze_player = player
        self.__maze:Maze = maze

    
    def __str__(self)->str:
        return self.__name

    def get_defense_value(self) -> int:
        return self.__defense_value
    
    
    def set_armor(self, armor: Defense):
        self.__armor = armor
        self.__defense_value = self.__defense_multiplier * self.__armor.get_defense_value()
        self.__name = str(self.__armor)
        if(isinstance(self.__armor,(Armor,Potion))):
            self.set_image_name(self.__armor.get_image_name())

    
    def player_entered(self, player: maze_player) -> list[Message]:

        self.__maze.remove_from_grid(self , self._position)
        potion = player.check_potion_player(self)

        if potion is None:
            defense_increase = self.get_defense_value() - self.__armor.get_defense_value()
            self.__pick_text = self.__pick_text + str(self.__armor)+ '.\nDefense increased by ' + str(defense_increase) 
            return [DialogueMessage(self, player, self.__pick_text, self.__name)]
        else :
            self.__maze.add_to_grid(self,self.get_position())
            return [DialogueMessage(self, player, self.__not_pick_text,self.__name)]
        
    def decrease_defense(self,attack:int)->int:
            if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0
            attack = attack - self.__defense_value
            self.__defense_value = 0
            return attack
