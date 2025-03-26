from abc import ABC
from typing import TYPE_CHECKING
from .imports import * 
if TYPE_CHECKING:
    from message import *
    from coord import Coord
    from command import MenuCommand
    from tiles.base import MapObject, Exit, Observer, Tile
    from NPC import NPC
    from maps.base import Map


class Room(Map, ABC): 
    #A generic room that can contain objects and players

    def __init__(self, name: str = "DefaultRoom", size: tuple[int, int] = (10,10), entry_point: Coord = Coord(0,0), background_tile: str = "cobblestone"):
        #Constructor for new room
        super().__init__(name=name, 
                         description="", size=size, entry_point=entry_point, background_tile_image=background_tile)
        self.__objects: list[tuple[MapObject, Coord]] = []

    def add_object(self, obj: MapObject, position: Coord) -> None:
        #Add a new object in the room
        self.__objects.append((obj, position))

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        #Return all objects in the room
        return []
     
    def player_entered(self, player: "HumanPlayer"):
        pass


class Statue(MapObject):
    #Statue
    def __init__(self, description: str, image_name: str = "statue"):
        #Constructor for new statue
        super().__init__(f'tile/statue/{image_name}', passable=False)
        self.__description = description

    def player_interacted(self, player: HumanPlayer):
        return [ServerMessage(player, self.__description)]

class Wall(MapObject):
    def __init__(self, image_name: str = "wall", passable: bool = False):
        super().__init__(image_name=image_name,passable=passable, z_index=1)

class Floor(MapObject):
    def __init__(self, image_name: str = "cobblestone", passable: bool = True):
        super().__init__(image_name=image_name,passable=passable,z_index=0)




class SaunaRoom(Room):
    def __init__(self): #, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        super().__init__(name="Sauna Room", size=(19,16), entry_point=Coord(34,15), background_tile="cobblestone")
        self.__heat_level = 10

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Sauna.")]

    def change_heat_intensity(self, heat: int) -> str:
      self.__heat_level += heat
      self.__heat_level = max(0, min(self.__heat_level, 10))
      if self.__heat_level > 8:
        return "scorching hot"
      elif self.__heat_level > 5:
        return "warming and relaxing"
      else:
        return "lukewarm"

    #add a taking damage method in here

class StatueRoom(Room):
    def __init__(self):
        super().__init__(name="StatueRoom", size=(5,18), entry_point=Coord(6,70), background_tile="cobblestone")

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Room of Statues.")]
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        return super().get_objects()

class WineCellar(Room):
    def __init__(self):
        super().__init__(name="WineCellar", size=(5,9), entry_point=Coord(53,14), background_tile="cobblestone")

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Wine Cellar.")]
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        return super().get_objects()