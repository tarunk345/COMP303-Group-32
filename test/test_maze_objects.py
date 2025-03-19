import pytest
from ..maze_objects import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from tiles.base import MapObject
    from Player import HumanPlayer

# Dummy subclass to instantiate abstract Room
class DummyRoom(Room):
    def player_entered(self, player) -> list:
        return []

def test_room_add_and_get_objects():
    room = DummyRoom("TestRoom", (5, 5), Coord(0, 0))
    dummy_obj = MapObject("dummy", passable=True)
    room.add_object(dummy_obj, Coord(1, 1))
    objects = room.get_objects()
    assert len(objects) == 1
    assert objects[0][0] == dummy_obj
    assert objects[0][1] == Coord(1, 1)

def test_corridor_initialization():
    corridor = Corridor("TestCorridor", length=10, entry_point=Coord(0, 0))
    assert corridor._size == (1, 10)  # Not a problem

def test_statue_interaction():
    statue = Statue(description="You see a grand statue.")

    class DummyPlayer(HumanPlayer):
        def __init__(self):
        # Call parent constructor with dummy values
            super().__init__(name="Tester")
    messages = statue.player_interacted(DummyPlayer())
    assert len(messages) == 1
    assert "grand statue" in str(messages[0])