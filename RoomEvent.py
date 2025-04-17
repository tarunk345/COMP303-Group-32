from typing import TYPE_CHECKING
from .imports import *
if TYPE_CHECKING:
    from tiles.base import GameEvent
    from Player import HumanPlayer

class RoomEvent(GameEvent):

    def __init__(self, event_type: str, data=None):
        super().__init__
