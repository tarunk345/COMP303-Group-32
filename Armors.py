from typing import TYPE_CHECKING
from .imports import *
if TYPE_CHECKING:
    from tiles.base import MapObject
    from message import *
    from .player import maze_player
from .Defense import *
from .Maze import ExampleHouse
from .Potions import Potion

class Armor(Defense, MapObject):
    @abstractmethod
    def __init__(self, name :str, defense_value:int, attack_value:int,defense_type:Defense_type, maze: ExampleHouse, image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__name: str = name
        self.__defense_value:int = defense_value
        self.__attack_value:int = attack_value
        self.__defense_type:Defense_type = defense_type
        self.__maze:ExampleHouse = maze
    
    def __str__(self)->str:
        return self.__name

    def get_defense_value(self) -> int:
        return self.__defense_value
    
    def get_attack_value(self)->int:
        return self.__attack_value
    
    def get_defense_type(self)->Defense_type:
        return self.__defense_type
    
    def player_entered(self, player: 'maze_player') -> list[Message]:
        """if armor added then update attack value of player and return pick text
            if armor not added put the the armor back on grid and return not pick text
            if armor changed then put the old armor back on grid,update attack value of player and return change text"""
        self.__maze.remove_from_grid(self , self._position)
        armor = player.check_armor_player(self)
        if armor is None:
            pick_text : str ='You picked up the '+ self.__name +'!\n Defense increased by: ' + str(self.__defense_value) +'!\n Attack increased by: ' + str(self.__attack_value)+'!'
            return [DialogueMessage(self, player, pick_text,self.get_image_name())]
        elif armor == self :
            self.__maze.add_to_grid(self,self.get_position())
            not_pick_text : str = 'current' + self.__name + 'has more defense!'
            return [DialogueMessage(self, player, not_pick_text,self.get_image_name())]
        else:
            if(isinstance(armor,(Armor,Potion))): 
                armor.set_position(self.get_position())
                self.__maze.add_to_grid(armor,armor.get_position())
                defense_changed: int = self.__defense_value - armor.__defense_value
                attack_changed:int = self.__attack_value - armor.__attack_value
                if defense_changed>=0 and attack_changed>=0:
                    change_text = self.__name + 'changed! Defense' +'increased by' + str(defense_changed)+'\n' + 'attack increased by' + str(attack_changed)+'!'
                elif defense_changed<0: 
                    change_text = self.__name + 'changed! Defense' +'decreased by' + str(abs(defense_changed))+'\n' + 'attack increased by' + str(attack_changed)+'!'
                elif attack_changed<0:
                    change_text = self.__name + 'changed! Defense' +'increased by' + str(defense_changed)+'\n' + 'attack decreased by' + str(abs(attack_changed))+'!'

            return [DialogueMessage(self, player, change_text,self.get_image_name())]


    def decrease_defense(self,attack:int)->int:
            """if attack>defense value then remaining attack is returned"""
            if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0 
            attack = attack - self.__defense_value
            self.__defense_value = 0
            return attack



class Pants(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, maze: ExampleHouse, image_name: str) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.PANTS, maze, image_name)



class Chest_Plate(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, maze: ExampleHouse, image_name: str) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.CHEST_PLATE, maze, image_name)
    


class Helmet(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, maze: ExampleHouse, image_name: str) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.HELMET, maze, image_name)


class Boots(Armor):
    def __init__(self, name: str, defense_value: int, attack_value: int, maze: ExampleHouse, image_name: str) -> None:
        super().__init__(name, defense_value, attack_value, Defense_type.BOOTS, maze, image_name)