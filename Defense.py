from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod
from enum import Enum
import random
from .imports import * 
if TYPE_CHECKING:
    from coord import Coord
    from Player import HumanPlayer
    from tiles.base import MapObject
    from message import *
    from .Maze import ExampleHouse
    from message import Message
    from tiles.base import Subject




class Defense_type(Enum):
    PANTS = 1
    CHEST_PLATE = 2
    HELMET = 3
    BOOTS = 4
    DEFENSE_POTION = 5
    ATTACK_POTION = 6









class Defense(ABC):

    @abstractmethod
    def get_defense_value(self)-> int:
        pass

    @abstractmethod
    def get_attack_value(self)-> int:
        pass

    @abstractmethod
    def decrease_defense(self,attack:int)->int:
        pass





class maze_player(Defense, Subject, RecipientInterface):
    def __init__(self,defense : int, attack_value: int,) -> None:
        super().__init__()
        self.__init_defense: int = defense
        self.__defense_value: int  = defense
        self.__attack_value = attack_value 
        self.__armor_set: Armor_Set = Armor_Set()
        self.__maze:"ExampleHouse" 

    def set_maze(self,maze:"ExampleHouse"):
        self.__maze = maze

    def get_maze(self):
        return self.__maze

    def get_defense_value(self)->int:
        total_defence_value = self.__defense_value
        total_defence_value += self.__armor_set.get_defense_value()
        return total_defence_value
    
    
    def get_attack_value(self) -> int:
        total_attack_value = self.__attack_value
        total_attack_value += self.__armor_set.get_attack_value()
        return total_attack_value

    def add_potion(self, potion: "Potion") -> None:
        self.__armor_set.add_potion

    def decrease_defense(self , attack:int)->int:
        """first attack is applied on armor set then 
            if still some attack damage is left then it is applied on player"""
        
        """defense value is not updated because when the enemy attack player 
            the defense value can be subtracted from each armor individually 
            and if defense value of one armor is less than it can changed with an armor of same type"""
        
        attack = self.__armor_set.decrease_defense(attack)
        if attack < self.__defense_value:
            self.__defense_value = self.__defense_value - attack
            return 0

        self.__defense_value = 0
        return 1
    
    def check_armor_player(self, armor : "Armor")->Optional[Defense]:
        """return None if armor added
            return old armor if armor is changes
            return new armor if armor is not added"""        
        return self.__armor_set.add_armor(armor)
    

    def check_potion_player(self, potion: "Potion"):
        """return None if potion added
            return new potion if potion is not added"""
        return self.__armor_set.add_potion(potion)
    
    def heal(self, heal_amt: int) -> int:
        """Returns player defense after healing.
        """
        self.__defense += heal_amt
        if self.__init_defense < self.__defense:
            self.__defense = self.__init_defense
        return self.__defense
    

    






class Armor(Defense, MapObject):
    @abstractmethod
    def __init__(self, defense_value:int, attack_value:int,defense_type:Defense_type,player:"maze_player", 
                 image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__defense_value:int = defense_value
        self.__attack_value:int = attack_value
        self.__defense_type:Defense_type = defense_type
        self.__player:"maze_player" = player
    
    def __str__(self)->str:
        return self.get_image_name()
    
    @abstractmethod
    def copy(self)-> "Armor":
        pass

    def get_player(self):
        return self.__player
    
    def get_defense_value(self) -> int:
        return self.__defense_value
    
    def get_attack_value(self)->int:
        return self.__attack_value
    
    def get_defense_type(self)->Defense_type:
        return self.__defense_type
    
    def player_interacted(self, player: HumanPlayer) -> list[Message]:
        """if armor added then update attack value of player and return pick text
            if armor not added put the the armor back on grid and return not pick text
            if armor changed then put the old armor back on grid,update attack value of player and return change text"""
        player.get_current_room().remove_from_grid(self , self._position)
        armor = self.__player.check_armor_player(self)
        if armor is None:
            pick_text : str ='You picked up the '+ self.get_image_name() +'!\n Defense increased by: ' + str(self.__defense_value) +'!\n Attack increased by: ' + str(self.__attack_value)+'!'
            return [DialogueMessage(self, player, pick_text,self.get_image_name())]
        elif armor == self :
            player.get_current_room().add_to_grid(self,player.get_current_position())
            not_pick_text : str = 'current ' + self.get_defense_type().name + ' has more defense!'
            return [DialogueMessage(self, player, not_pick_text,self.get_image_name())]
        else:
            if(isinstance(armor,(Armor,Potion))): 
                player.get_current_room().add_to_grid(armor,player.get_current_position())
                defense_changed: int = self.__defense_value - armor.__defense_value
                attack_changed:int = self.__attack_value - armor.__attack_value
                if defense_changed>=0 and attack_changed>=0:
                    change_text = armor.get_image_name() + ' changed! Defense increased by ' + str(defense_changed)+'\n' + ' attack increased by ' + str(attack_changed)+'!'
                elif defense_changed<0: 
                    change_text = armor.get_image_name() + ' changed! Defense decreased by ' + str(abs(defense_changed))+'\n' + ' attack increased by ' + str(attack_changed)+'!'
                elif attack_changed<0:
                    change_text = armor.get_image_name() + ' changed! Defense increased by ' + str(defense_changed)+'\n' + ' attack decreased by ' + str(abs(attack_changed))+'!'

            return [DialogueMessage(self, player, change_text,self.get_image_name())]


    def decrease_defense(self,attack:int)->int:
            """if attack>defense value then remaining attack is returned"""
            if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0 
            attack = attack - self.__defense_value
            self.__defense_value = 0
            return attack



class Chest_Plate(Armor):
    def __init__(self, defense_value: int, attack_value: int, player: "maze_player", image_name: str) -> None:
        super().__init__(defense_value, attack_value, Defense_type.CHEST_PLATE, player, image_name)
    def copy(self):
        return Chest_Plate(self.get_defense_value(),self.get_attack_value(),self.get_player(),self.get_image_name())
        


class Helmet(Armor):
    def __init__(self, defense_value: int, attack_value: int, player: "maze_player", image_name: str) -> None:
        super().__init__(defense_value, attack_value, Defense_type.HELMET, player, image_name)

    def copy(self):
        return Helmet(self.get_defense_value(),self.get_attack_value(),self.get_player(),self.get_image_name())
    
class Boots(Armor):
    def __init__(self, defense_value: int, attack_value: int, player: "maze_player", image_name: str) -> None:
        super().__init__(defense_value, attack_value, Defense_type.BOOTS, player, image_name)

    def copy(self):
        return Boots(self.get_defense_value(),self.get_attack_value(),self.get_player(),self.get_image_name())







class Potion(Defense, MapObject):
    @abstractmethod
    def __init__(self,multiplier:int, defense_type:Defense_type,player:"maze_player",  
                 image_name: str, passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__multiplier:int = multiplier
        self.__defense_type:Defense_type = defense_type
        self.__armor:Defense
        self.__defense_value:int
        self.__attack_value:int
        self.__player:"maze_player" = player


    @abstractmethod
    def copy(self):
        pass

    def get_player(self):
        return self.__player


    def get_defense_value(self) -> int:
        return self.__defense_value
    
    def set_defense_value(self,defense:int):
        self.__defense_value = defense

    def get_attack_value(self) -> int:
        return self.__attack_value
    
    def get_multiplier(self):
        return self.__multiplier
    
    def get_armor(self)->Defense:
        return self.__armor
    
    def get_defense_type(self) -> Defense_type:
        return self.__defense_type
    
    def set_armor(self, armor: Defense):
        self.__armor = armor

    def set_fields(self):
        armor = self.__armor
        if(isinstance(armor,(Armor,Potion))):
            self.set_image_name(armor.get_image_name())
            self.__defense_type = armor.get_defense_type()
            self.__defense_value =armor.get_defense_value()
            self.__attack_value = armor.get_attack_value()            

    def decrease_defense(self, attack: int) -> int:
        if attack < self.__defense_value:
                self.__defense_value = self.__defense_value - attack
                return 0 
        attack = attack - self.__defense_value
        self.__defense_value = 0
        return attack
    

    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        """if potion not added put the the potion back on grid and return pick text
            if potion added then update attack value of player,update the fields of potion and return not pick text"""

        player.get_current_room().remove_from_grid(self , self._position)
        potion = self.__player.check_potion_player(self)
        if  potion is not None:
            player.get_current_room().add_to_grid(self,self.get_position())
            not_pick_text : str = 'Cannot pick up the potion! No armor to put potion on!'
            return [DialogueMessage(self, player, not_pick_text,self.get_image_name())]
        
        return[]

    
    
class Defense_potion(Potion):

    def __init__(self,multiplier: int, player: "maze_player",  image_name: str) -> None:
        super().__init__(multiplier, Defense_type.DEFENSE_POTION, player,image_name)

    def copy(self):
        return Defense_potion(self.get_multiplier(),self.get_player(),self.get_image_name())
    
         
    def set_fields(self):
        super().set_fields()
        self.set_defense_value(self.get_multiplier()*self.get_armor().get_defense_value())

    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        message = super().player_interacted(player)
        if message != []:
            return message
        
        armor = self.get_armor()
        image_name = self.get_image_name()
        defense_increase = (self.get_multiplier()*armor.get_defense_value()) - armor.get_defense_value()
        pick_text = 'You picked up the '+ self.get_image_name() +'!\nIt is applied to ' + str(armor)+ '.\nDefense increased by ' + str(defense_increase)+'!' 
        self.set_fields()
        return [DialogueMessage(self, player, pick_text, image_name)]

class Attack_potion(Potion):

    def __init__(self, multiplier: int, player: "maze_player",  image_name: str) -> None:
        super().__init__(multiplier, Defense_type.ATTACK_POTION, player,image_name)

    def copy(self):
        return Attack_potion(self.get_multiplier(),self.get_player(),self.get_image_name())

    def get_attack_value(self) -> int:
        return self.get_multiplier() * self.get_armor().get_attack_value()

    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        message = super().player_interacted(player)
        if message != []:
            return message
        
        armor = self.get_armor()
        image_name = self.get_image_name()
        attack_increase = (self.get_multiplier()*armor.get_attack_value()) - armor.get_attack_value()
        pick_text = 'You picked up the '+ self.get_image_name() +'!\nIt is applied to ' + str(armor)+ '.\nAttack increased by ' + str(attack_increase)+'!'
        self.set_fields() 
        return [DialogueMessage(self, player, pick_text, image_name)]
    


class Armor_Set(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.__list_armors : list[Defense] = []
        

    def get_defense_value(self) -> int:
        defense = 0
        for armor in self.__list_armors:
            defense += armor.get_defense_value()
        
        return defense
    
    def get_attack_value(self) -> int:

        attack = 0
        for armor in self.__list_armors:
            attack += armor.get_attack_value()
        
        return attack
        


    def decrease_defense(self,attack:int)->int:
        """remainging attack is returned"""
        
        for armor in self.__list_armors:
            attack = armor.decrease_defense(attack)
        
        return attack
    
    def __str__(self) -> str:
        string = ''
        for armor in self.__list_armors:
            string.__add__(str(armor) + ',')
        return string
    
    
    def add_armor(self, armor : Armor)->Optional[Defense]  :
        """return None if armor added
            return old armor if armor is changes
            return new armor if armor is not added"""
        armor_stats = armor.get_defense_value() + armor.get_attack_value()

        for check_armor in self.__list_armors:
            if isinstance(check_armor,(Potion,Armor)): 
                if check_armor.get_defense_type() == armor.get_defense_type():
                    check_armor_stats = check_armor.get_defense_value()+check_armor.get_attack_value()
                    if check_armor_stats<armor_stats:
                        self.__list_armors.remove(check_armor)
                        self.__list_armors.append(armor)
                        return check_armor
                    else :
                        return armor
                
        self.__list_armors.append(armor)
        return None
    
    def add_potion(self, potion : Potion)->Optional[Potion]  :
        """return None if potion added
            return new potion if potion is not added"""
        """potion can be applied on armors which already has potion applied to them"""

        if len(self.__list_armors) == 0:
            return potion
        
        for armor in self.__list_armors:
            if isinstance(armor,(Armor)):
                potion.set_armor(armor)
                self.__list_armors.remove(armor)
                self.__list_armors.append(potion)
                return None

        
    
        return potion
    



    
Maze_Player = maze_player(11,5)    
Gold_chest_plate = Chest_Plate(20,20,Maze_Player,"Gold Chest Plate")
Gold_Helmet = Helmet(20,20,Maze_Player,"Gold Helmet")        
Gold_Boots = Boots(20,20,Maze_Player,"Gold Boots")        
Silver_chest_plate = Chest_Plate(10,10,Maze_Player,"Silver Chest Plate")        
Silver_Helmet = Helmet(10,10,Maze_Player,"Silver Helmet")
Silver_Boots = Boots(10,10,Maze_Player,"Silver Boots")
Bronze_chest_plate = Chest_Plate(2,2,Maze_Player,"Bronze Chest Plate")        
Bronze_Helmet = Helmet(2,2,Maze_Player,"Bronze Helmet")        
Bronze_Boots = Boots(2,2,Maze_Player,"Bronze Boots")        
Iron_chest_plate = Chest_Plate(5,5,Maze_Player,"Iron Chest Plate")
Iron_Helmet = Helmet(5,5,Maze_Player,"Iron Helmet")
Iron_Boots = Boots(5,5,Maze_Player,"Iron Boots")

Attack_potion_1 = Attack_potion(2,Maze_Player,'Attack Potion')
Attack_potion_2 = Attack_potion(3, Maze_Player,image_name='Attack Potion')
Defense_potion_1 = Defense_potion(2, Maze_Player, image_name='Defense Potion')
Defense_potion_2 = Defense_potion(2, Maze_Player, image_name='Defense Potion')



list_Defense : list[Armor] = []
list_Defense.append(Gold_chest_plate)
list_Defense.append(Gold_Helmet)
list_Defense.append(Gold_Boots)

list_Defense.append(Silver_chest_plate)
list_Defense.append(Silver_Helmet)
list_Defense.append(Silver_Boots)


list_Defense.append(Bronze_chest_plate)
list_Defense.append(Bronze_Helmet)
list_Defense.append(Bronze_Boots)

list_Defense.append(Iron_chest_plate)
list_Defense.append(Iron_Helmet)
list_Defense.append(Iron_Boots)
