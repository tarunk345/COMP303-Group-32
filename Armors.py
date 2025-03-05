from Defense import Defense
from Player import HumanPlayer
from message import Message
from tiles.map_objects import PressurePlate 
from player import maze_player
from Maze import Maze
from tiles.base import MapObject
from message import *



class Armor(Defense, MapObject):
    def __init__(self,player :maze_player,maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__armor_value:int 
        self.__pick_text='You picked up the Armor! Defense increased by:'
        self.__player :maze_player = player
        self.__maze:Maze = maze
    

    def toString(self)->str:
        return "Armor"

    def get_defense_value(self) -> int:
        return self.__armor_value
    

    def player_entered(self, player: maze_player) -> list[Message]:
        player.add_armor(self)
        self.__maze.remove_from_grid(self , self._position)
        return []



def decrease_defense(self,attack:int)->int:
        if attack>= self.get_defence_value():
            self.armor_value = self.armor_value - attack
            return 0
        attack = attack - self.armor_value
        self.armor_value = 0
        return attack


class Pants(Armor):

    def __init__(self, player: maze_player, maze: Maze, image_name: str = 'Pants', passable: bool = True, z_index: int = 0) -> None:
        super().__init__(player, maze, image_name, passable, z_index)
        self.armor_value:int = 7
        str='You picked up the  Pants! Defense increased by : 7! '


    def player_entered(self, player: maze_player) -> list[Message]:
        super().player_entered(player)

        return [DialogueMessage(self, player, self.__pick_text,'Pants')]

    
    def toString(self)->str:
        return 'Pants'


class Chest_Plate(Armor):

    def __init__(self, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(player, maze, image_name, passable, z_index)
        self.armor_value:int = 7
        str='You picked up the  Chest Plate! Defense increased by : 7! '


    def player_entered(self, player: maze_player) -> list[Message]:
        super().player_entered(player)

        return [DialogueMessage(self, player, self.__pick_text,'Chest Plate')]



    def toString(self)->str:
        return 'Chest Plate'
    
class Helmet(Armor):

    def __init__(self, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(player, maze, image_name, passable, z_index)
        self.armor_value:int = 10
        str='You picked up the  Chest Helmet! Defense increased by : 10! '


    def player_entered(self, player: maze_player) -> list[Message]:
        super().player_entered(player)

        return [DialogueMessage(self, player, self.__pick_text,'Helmet')]



    def toString(self)->str:
        return 'Helmet'

class Boots(Armor):

    def __init__(self, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(player, maze, image_name, passable, z_index)
        self.armor_value:int = 15
        str='You picked up the  Chest Boots! Defense increased by : 5! '

    def player_entered(self, player: maze_player) -> list[Message]:
        super().player_entered(player)

        return [DialogueMessage(self, player, self.__pick_text,'Boots')]



    def toString(self)->str:
        return 'Boots'