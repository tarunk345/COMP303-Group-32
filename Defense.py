from .imports import * 
from abc import ABC, abstractmethod
from enum import Enum

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



