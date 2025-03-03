from typing import Any, TYPE_CHECKING

from message import *
from coord import Coord
from command import MenuCommand
from tiles.base import MapObject, Exit, Observer

if TYPE_CHECKING:
    from NPC import NPC
    from maps.base import Map


class Room(Map): 
    #A generic room that can contain objects and players

    def __init__(self, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        #Constructor for new room
        super().__init__(name=name, description="", size=size, entry_point=entry_point, background_tile_image=background_tile)
        self.objects: list[tuple[MapObject, Coord]] = []

    def add_object(self, obj: MapObject, position: Coord) -> None:
        #Add a new object in the room
        self.objects.append((obj, position))

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        #Return all objects in the room
        return self.objects
     
    @abstractmethod
    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return []
    
class Statue(MapObject):
    #Statue

    def __init__(self, image_name: str = "statue"):
        #Constructor for new statue
        super().__init__(f'tile/statue/{image_name}', passable=False)

        
class Corridor(Room):
    #Creates a new corridor

    def __init__(self, name: str, length: int, entry_point: Coord):
        #Cunstroctor for new corridor
        super().__init__(name=name, size=(1, length), entry_point=entry_point, background_tile="stone")

class Door(MapObject):
    #A door that connects rooms.

    def __init__(self, image_name: str, linked_room: str = ""):
        super().__init__(f'tile/door/{image_name}', passable=True, z_index=0)
        self.__connected_room = None
        self.__linked_room = linked_room

    def connect_to(self, connected_room: Room, new_entry_point: Coord) -> None:
        #Links this door to another room.
        self.__connected_room = connected_room
        self.__new_entry_point = new_entry_point

    def player_entered(self, player) -> list:
        #Moves player to linked room if connected.
        if self.__connected_room is None or self.__new_entry_point is None:
            print("Door has no link")
            return []

        return player.change_room(self.__connected_room, entry_point=self.__new_entry_point)


class SaunaRoom(Room):
    def __init__(self, heat_level: int, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        super().__init__(name=name, size=size, entry_point=entry_point, background_tile=background_tile)
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

    #add a taking damage method in here

class StatueRoom(Room):
    def __init__(self, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        super().__init__(name=name, size=size, entry_point=entry_point, background_tile=background_tile)

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Room of Statues.")]

class WineCellar(Room):
    def __init__(self, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        super().__init__(name=name, size=size, entry_point=entry_point, background_tile=background_tile)

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Wine Cellar.")]
      
