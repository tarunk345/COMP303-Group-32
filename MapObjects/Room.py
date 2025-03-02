from maps.base import Map
from coord import Coord
from tiles.base import MapObject

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