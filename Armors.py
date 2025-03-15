from .Defense import Defense_type
from Defense import *
from player import maze_player
from Maze import Maze
from tiles.base import MapObject
from message import *
from Potions import Potion



class Armor(Defense, MapObject):
    def __init__(self, name :str, defense_value:int, attack_value:int,defense_type:Defense_type, 
                 player :maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__name: str = name
        self.__defense_value:int = defense_value
        self.__attack_value:int = attack_value
        self.__defense_type:Defense_type = defense_type
        self.__pick_text : str ='You picked up the '+ name +'!\n Defense increased by: ' + str(defense_value) +'!\n Attack increased by: ' + str(attack_value)+'!'
        self.__change_text :  str  = name + 'changed! Defense'
        self.__not_pick_text : str = 'current' + name + 'has more defense!'
        self.__player :maze_player = player
        self.__maze:Maze = maze
    
    def __str__(self)->str:
        return self.__name

    def get_defense_value(self) -> int:
        return self.__defense_value
    
    def get_attack_value(self)->int:
        return self.__attack_value
    
    def get_defense_type(self)->Defense_type:
        return self.__defense_type
    
    def player_entered(self, player: maze_player) -> list[Message]:
        self.__maze.remove_from_grid(self , self._position)
        armor = player.check_armor_player(self)
        if armor is None:
            self.__player.update_attack_value()
            return [DialogueMessage(self, player, self.__pick_text,self.__name)]
        elif armor == self :
            self.__maze.add_to_grid(self,self.get_position())
            return [DialogueMessage(self, player, self.__not_pick_text,self.__name)]
        else:
            if(isinstance(armor,(Armor,Potion))): 
                armor.set_position(self.get_position())
                self.__maze.add_to_grid(armor,armor.get_position())
                defense_changed: int = self.__defense_value - armor.__defense_value
                attack_changed:int = self.__attack_value - armor.__attack_value
                self.__player.update_attack_value()
            return [DialogueMessage(self, player, self.__change_text + str(defense_changed),self.__name)]


    def decrease_defense(self,attack:int)->int:
            if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0 
            attack = attack - self.__defense_value
            self.__defense_value = 0
            return attack



class Pants(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, defense_type: Defense_type, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.PANTS, player, maze, image_name, passable, z_index)



class Chest_Plate(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, defense_type: Defense_type, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.CHEST_PLATE, player, maze, image_name, passable, z_index)
    


class Helmet(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, defense_type: Defense_type, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.HELMET, player, maze, image_name, passable, z_index)


class Boots(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, defense_type: Defense_type, player: maze_player, maze: Maze, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.BOOTS, player, maze, image_name, passable, z_index)
