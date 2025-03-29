from typing import TYPE_CHECKING
from PIL import Image
from .imports import * 
from .maze_objects import *
from .Defense import *
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
        player = maze_player(5,5)
        Gold_chest_plate = Chest_Plate(5,5,Coord(60,63),player,self,"Gold Chest Plate")
        objects.append((Gold_chest_plate, Coord(60,63)))
        Gold_Helmet = Helmet(20,20,Coord(50,63),player,self,"Gold Helmet")
        objects.append((Gold_Helmet, Coord(50,63)))
        Gold_Boots = Boots(20,20,Coord(60,63),player,self,"Gold Boots")
        objects.append((Gold_Boots, Coord(20,63)))

        Silver_chest_plate = Chest_Plate(10,10,Coord(62,63),player,self,"Silver Chest Plate")
        objects.append((Silver_chest_plate, Coord(62,63)))
        Silver_Helmet = Helmet(5,5,Coord(60,63),player,self,"Silver Helmet")
        objects.append((Silver_Helmet, Coord(60,15)))
        Silver_Boots = Boots(5,5,Coord(60,63),player,self,"Silver Boots")
        objects.append((Silver_Boots, Coord(20,20)))


        Bronze_chest_plate = Chest_Plate(5,5,Coord(60,63),player,self,"Bronze Chest Plate")
        objects.append((Bronze_chest_plate, Coord(30,30)))
        Bronze_Helmet = Helmet(5,5,Coord(60,63),player,self,"Bronze Helmet")
        objects.append((Bronze_Helmet, Coord(10,63)))
        Bronze_Boots = Boots(5,5,Coord(60,63),player,self,"Bronze Boots")
        objects.append((Bronze_Boots, Coord(70,50)))

        Iron_chest_plate = Chest_Plate(5,5,Coord(60,63),player,self,"Iron Chest Plate")
        objects.append((Iron_chest_plate, Coord(50,50)))
        Iron_Helmet = Helmet(5,5,Coord(60,63),player,self,"Iron Helmet")
        objects.append((Iron_Helmet, Coord(65,50)))
        Iron_Boots = Boots(5,5,Coord(60,63),player,self,"Iron Boots")
        objects.append((Iron_Boots, Coord(35,20)))


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

