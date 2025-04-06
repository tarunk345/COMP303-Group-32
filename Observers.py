from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from tiles.base import Observer, GameEvent
    from tiles.base import Door, Exit
    from coord import Coord
from .Enemy import *
from .RoomEvent import *
from .maze_objects import Room, SaunaRoom, StatueRoom, WineCellar, FinalBossRoom


#subject notifies observer that something has changed
#Push -> pushing data that changed to observer
#Pull -> passes a reference to itself

