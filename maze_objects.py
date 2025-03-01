from typing import Any, TYPE_CHECKING

from ..message import *
from ..coord import Coord
from ..command import MenuCommand
from ..tiles.base import MapObject, Exit, Observer

if TYPE_CHECKING:
    from NPC import NPC
    from maps.base import Map


class Room(MapObject):
    def __init__(self, image_name: str, passable: bool = True, puzzle: str = None):
        super().__init__(image_name, passable)
        self.puzzle = puzzle

    @abstractmethod
    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return []

class SaunaRoom(Room):
    def __init__(self, image_name: str, passable: bool = True, heat_level: int):
        super().__init__(image_name, passable)
        self.heat_level = heat_level

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Sauna.")]

    def change_heat_intensity(self, heat: int) -> str:
      self.heat_level += heat;
      self.heat_level = max(0, min(self.heat_level, 10))
      if self.heat_level > 8:
        return "scorching hot"
      elif self.heat_level > 5:
        return "warming and relaxing"
      else:
        return "lukewarm"
      
