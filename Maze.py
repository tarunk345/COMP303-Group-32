from typing import TYPE_CHECKING
from PIL import Image
from .imports import * 
from .maze_objects import *
if TYPE_CHECKING:
    from resources import Resources, get_resource_path
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class ExampleHouse(Map):
    def __init__(self) -> None:
        super().__init__(
            name="Maze",
            description="",
            size=(73, 73),
            entry_point=Coord(72,63),
            background_tile_image='sandstone3',
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        # creates maze base with walls
        self.__create_maze_base(objects)
        # add a door
        door = Door('int_entrance', linked_room="Trottier Town")
        
        objects.append((door, Coord(72,63)))

        # helmet = Chest_Plate('helmet',5,5,self,'water_2.png')
        # objects.append((helmet, Coord(70,63)))

        return objects
    
    def __create_maze_base(self, objects):
        Resource = Resources()
        image = Image.open(Resource.get_resource_path("maze_template4.png", ext_folder=True))
        rgb_im = image.convert('RGB')
        for x in range(73):
            for y in range(73):
                pixel = rgb_im.getpixel((x,y))
                if pixel == (255,255,255):
                    self.add_to_grid(Wall(),Coord(y,x))
                    # objects.append((Sign(),Coord(x,y)))
