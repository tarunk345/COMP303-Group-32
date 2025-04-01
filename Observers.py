from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from tiles.base import Observer, GameEvent
    from tiles.base import Door, Exit
    from coord import Coord
from .Enemy import *
from .RoomEvent import *
from .maze_objects import Room, SaunaRoom, StatueRoom, WineCellar, FinalBossRoom

class EnemySpawner(Observer):
    def __init__(self, enemy_count: int = 3):
        self.enemy_count = enemy_count
        self.enemies: List[Enemy] = []
    
    def update_on_notification(self, event: RoomEvent, enemy: Enemy.__class__):
        #if event.event_type == 'player_entered':
            #coords :List[Coord] = getRandomCoords(self, 50)
            #self.spawn_enemy(enemy, coords)
        pass
    
    def spawn_enemy(self, enemy : Enemy.__class__, coords: List[Coord]):    
        self.enemies.clear()
        for coord in coords:
            pass
             
        #finish implementing
    
    def notify(self):
        pass

    def on_enemy_defeated(self, room: Room, enemy: 'Enemy'):
    # Find the spawner observer
        for observer in room._observers:
            if isinstance(observer, EnemySpawner):
                if enemy in observer.enemies:
                    observer.enemies.remove(enemy)
                    print(f"{enemy} defeated, {len(observer.enemies)} remaining")
                    
                    # if not observer.enemies:
                    #     room.notify(GameEvent(
                    #         RoomEventsTypes.ALL_ENEMIES_DEFEATED,
                    #         {'room': room}
                    #     ))
                break

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

