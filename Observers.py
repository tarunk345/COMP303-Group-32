from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from tiles.base import Observer, GameEvent
    from tiles.base import Door, Exit
    from coord import Coord
from .Enemy import *
from .RoomEvent import *
from .maze_objects import Room, SaunaRoom, StatueRoom, WineCellar, FinalBossRoom

    
class GladiatorSpawner(Observer):
    def __init__(self, center : Coord, room : Map, enemy_count: int = 3):
        self.enemy_count = enemy_count
        self.center = center
        self.gladiators: List[Gladiator] = []
        self.room = room
        self.messages = []
    
    def add_Gladiator(self, gladiator : Gladiator):
        self.gladiators.append(gladiator)
        
    def update_on_notification(self, event: GameEvent):
        if (event == "player_entered"):
            if self.gladiators.count == 0:
                for x in range(self.enemy_count):
                    self.room.add_to_grid(Gladiator(),self.center)

        self.messages = self.room.send_grid_to_players()
        #finish implementing


class DoorController(Observer):
    def __init__(self, entrance_door: Door, exit_door: Exit):
        self.entrance_door: Door = entrance_door
        self.exit_door: Exit = exit_door
    
    def update_on_notification(self,event:RoomEvent):
        pass
        # if event.event_type == 'player_entered':
        #     self.close_entrance_door(event.data['room'])
        # elif event.event_type == 'all_enemies_defeated':
        #         self.open_exit_door(event.data['room'])

    # def close_entrance_door(self, room: Room):
    #     entrance_door.super().set_image_name("door_closed")
    #     room.entrance_door._MapObject__passable = False

    # def open_exit_door(self, room: Room):
    #     room.exit_door.set_image_name("door_open")
    #     room.exit_door._MapObject__passable = True
    #     room.update_door_state(room.exit_door)

class FollowPlayer(Observer):

    def update_on_notification(self, event):
        return super().update_on_notification(event)

#subject notifies observer that something has changed
#Push -> pushing data that changed to observer
#Pull -> passes a reference to itself

