
from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *
    from PIL import Image
    from maze_objects import *

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
        door = Door('int_entrance', linked_room="Trottier Town")
        objects.append((door, Coord(63,0)))

        door2 = Door('int_entrace', linked_room="Trottier Town")
        objects.append((door2,Coord(23,72)))

        # add a statue
        return objects
    
    def create_maze_base(self):
        image = Image.open(get_resource_path("maze_template", ext_folder=True))
        
        for y in range(73):
            for x in range(73):
                pixel = image.getpixel((x,y))
                if pixel == (0,0,0):
                    self.add_to_grid(Wall(),Coord(x,y))
