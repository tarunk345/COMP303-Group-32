
from .imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from maps.base import Map
    from tiles.base import MapObject
    from tiles.map_objects import *

class ScorePressurePlate(PressurePlate):
    def __init__(self, image_name='pressure_plate'):
        super().__init__(image_name)
    
    def player_entered(self, player) -> list[Message]:
        messages = super().player_entered(player)

        # add score to player
        player.set_state("score", player.get_state("score") + 1)

        return messages

class Colosseum(Map):
    def __init__(self) -> None:
        super().__init__(
            name="Colosseum",
            description="Long Live The Three Emperors",
            size=(30, 30),
            entry_point=Coord(17, 14),
            background_tile_image='cobblestone',
        )
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []

        # add a door
        door = Door('int_entrance', linked_room="Maze")
        objects.append((door, Coord(17, 45)))

        # add a pressure plate
        pressure_plate = ScorePressurePlate()
        objects.append((pressure_plate, Coord(13, 7)))

        return objects
