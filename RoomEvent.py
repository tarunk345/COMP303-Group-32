from typing import TYPE_CHECKING
from .imports import *
if TYPE_CHECKING:
    from tiles.base import GameEvent
    from Player import HumanPlayer

class RoomEvent(GameEvent):

    def __init__(self, event_type: str, data=None):
        super().__init__

class RoomEventsTypes:
    PLAYER_ENTERED = "player_entered"
    ENEMY_DEFEATED = "enemy_defeated"
    ALL_ENEMIES_DEFEATED = "all_enemies_defeated"
    DOOR_STATE_CHANGED = "door_state_changed"