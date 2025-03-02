from tiles.base import MapObject
from coord import Coord
from Room import Room 

class Door(MapObject):
    #A door that connects rooms.

    def __init__(self, image_name: str, linked_room: str = ""):
        super().__init__(f'tile/door/{image_name}', passable=True, z_index=0)
        self.__connected_room = None
        self.__linked_room = linked_room

    def connect_to(self, connected_room: Room, new_entry_point: Coord) -> None:
        #Links this door to another room.
        self.__connected_room = connected_room
        self.__new_entry_point = new_entry_point

    def player_entered(self, player) -> list:
        #Moves player to linked room if connected.
        if self.__connected_room is None or self.__new_entry_point is None:
            print("Door has no link")
            return []

        return player.change_room(self.__connected_room, entry_point=self.__new_entry_point)
