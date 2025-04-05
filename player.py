# from typing import TYPE_CHECKING, Any, Literal, Optional
# from .Armor_set import Armor_Set
# from .Defense import Defense
# from .Armors import Armor
# from .imports import * 
# if TYPE_CHECKING:
#     from coord import Coord
#     from maps.base import Map
#     from message import Literal, Message
#     from tiles.base import MapObject
#     from tiles.map_objects import *
#     from .Potions import Potion



    

# class maze_player(HumanPlayer,Defense):
#     def __init__(self,defense : int, attack_value: int,
#                  name: str, websocket_state: Any = None, email: str = "", 
#                  image: str = 'player1', facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', passable: bool = True) -> None:
#         super().__init__(name, websocket_state, email, image, facing_direction, passable)
#         self.__defense_value: int  = defense
#         self.__attack_value = attack_value
#         self.__armor_set: Armor_Set = Armor_Set()

#     def get_defense_value(self)->int:
#         total_defence_value = self.__defense_value
#         total_defence_value += self.__armor_set.get_defense_value()
#         return total_defence_value
    
#     def get_attack_value(self) -> int:
#         total_attack_value = self.__attack_value
#         total_attack_value += self.__armor_set.get_attack_value()
#         return total_attack_value


#     def decrease_defense(self , attack:int)->int:
#         """first attack is applied on armor set then 
#             if still some attack damage is left then it is applied on player"""
        
#         """defense value is not updated because when the enemy attack player 
#             the defense value can be subtracted from each armor individually 
#             and if defense value of one armor is less than it can changed with an armor of same type"""
        
#         attack = self.__armor_set.decrease_defense(attack)
#         if attack < self.__defense_value:
#             self.defense = self.defense - attack
#             return 0

#         self.__defense_value = 0
#         return 1
    
#     def check_armor_player(self, armor : Armor)->Optional[Defense]:
#         """return None if armor added
#             return old armor if armor is changes
#             return new armor if armor is not added"""        
#         return self.__armor_set.add_armor(armor)
    

#     def check_potion_player(self, potion: 'Potion'):
#         """return None if potion added
#             return new potion if potion is not added"""
#         return self.__armor_set.add_potion(potion)

