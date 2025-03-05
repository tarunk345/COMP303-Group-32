from abc import ABC, abstractmethod


class Defense(ABC):

    @abstractmethod
    def get_defense_value(self)-> int:
        pass

    @abstractmethod
    def decrease_defense(self,attack:int)->int:
        pass