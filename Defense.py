from abc import ABC, abstractmethod


class Defense(ABC):

    @abstractmethod
    def get_defence_value(self)-> int:
        pass

  