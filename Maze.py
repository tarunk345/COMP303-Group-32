from typing import TYPE_CHECKING
from PIL import Image
from .imports import * 
from .maze_objects import *
from .Defense import *
from .Enemy import *
if TYPE_CHECKING:
    from message import Message
    from resources import Resources, get_resource_path
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *


class ExampleHouse(Map):
    MAIN_ENTRANCE = True
    def __init__(self) -> None:
        super().__init__(
            name="Maze",
            description="",
            size=(73, 73),
            entry_point=Coord(72,63),
            background_tile_image='sandstone3',
        )
        self.__gladiators : list[Gladiator] = []

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        messages = []
        return messages

    def add_gladiator(self) -> None:
        self.__gladiators.append(Gladiator())

    def update(self) -> list[Message]:
        messages = []
        playerlist : list[HumanPlayer] = self.get_human_players()
        if playerlist.__len__() >= 2:
            self.remove_player(playerlist[1])
            
        for gladiator in self.__gladiators:
            if gladiator.is_defeated():
                self.remove_from_grid(gladiator, gladiator.get_position())
                self.send_grid_to_players()
                messages.extend("Gladiator defeated!")
        return messages
        
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        # creates maze base with walls
        self.__create_maze_base(objects)
        # add a door
        door = Door('int_entrance', linked_room="Trottier Town", is_main_entrance=True)
        objects.append((door, Coord(72,63)))
        Maze_Player.set_maze(self)

         # entering tile
        # entering_tile = Entering_tile('Gold Boots',True,0)
        # objects.append((entering_tile, Coord(71, 63)))

        # self.add_player(Gladiator(),Coord(50,62))
        
        
        
        objects.append((Gold_chest_plate, Coord(60,63)))
        objects.append((Gold_Helmet, Coord(50,63)))
        objects.append((Gold_Boots, Coord(20,63)))

        objects.append((Silver_chest_plate, Coord(62,63)))
        objects.append((Silver_Helmet, Coord(60,15)))
        objects.append((Silver_Boots, Coord(20,20)))


        objects.append((Bronze_chest_plate, Coord(30,30)))
        objects.append((Bronze_Helmet, Coord(10,63)))
        objects.append((Bronze_Boots, Coord(70,50)))

        objects.append((Iron_chest_plate, Coord(50,50)))
        objects.append((Iron_Helmet, Coord(65,50)))
        objects.append((Iron_Boots, Coord(35,20)))

        ##Doors
        door = Door("wooden_door","Sauna Room")
        #objects.append((door, Coord(70,57)))
        objects.append((door, Coord(34,15)))

        door2 = Door("wooden_door", "Wine Cellar")
        objects.append((door2, Coord(53,14)))
        #objects.append((door2, Coord(70,57)))

        door3 = Door("wooden_door", "Statue Room")
        objects.append((door3, Coord(6,70)))
        #objects.append((door3, Coord(70,57)))
        
        door4 = Door("wooden_door", "Armory")
        #objects.append((door4, Coord(70,57)))
        objects.append((door4, Coord(34, 33)))

        door5 = Door("golden_door", "Final Boss Room")
        # objects.append((door5, Coord(70,57)))
        objects.append((door5, Coord(0,23)))

        
        objects.append((Gladiator(), Coord(70,57)))
        objects.append((Gladiator(), Coord(67, 57)))
        objects.append((Gladiator(), Coord(67,61)))
        objects.append((Gladiator(), Coord(59,40)))
        objects.append((Gladiator(), Coord(46,7)))


        objects.append((Attack_potion_1, Coord(71,56)))
        objects.append((Attack_potion_2, Coord(69,48)))
        objects.append((Defense_potion_1, Coord(69,49)))        
        objects.append((Defense_potion_2, Coord(60,7)))

       

        return objects
    
    def getRandomCoords(self, count : int) -> list[Coord]:
        coords : list[Coord] = []
        for i in range (count):
            x = random.randint(0,72)
            y = random.randint(0,72)
            if (self.get_map_objects_at(Coord(x,y)).__class__ == Background):
                coords.append(Coord(x,y))
        return coords

    def __create_maze_base(self, objects):
        Resource = Resources()
        image = Image.open(Resource.get_resource_path("maze_template4.png", ext_folder=True))
        rgb_im = image.convert('RGB')
        for x in range(73):
            for y in range(73):
                pixel = rgb_im.getpixel((x,y))
                if pixel == (255,255,255):
                    self.add_to_grid(Wall(),Coord(y,x))

