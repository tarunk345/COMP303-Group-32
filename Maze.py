
from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class Maze(Map):
    def __init__(self) -> None:
        super().__init__(
            name="Maze",
            description="",
            size=(73, 73),
            entry_point=Coord(17, 14),
            background_tile_image='cobblestone',
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('int_entrance', linked_room="Maze")
        objects.append((door, Coord(17, 45)))

        # add a statue
        return objects
