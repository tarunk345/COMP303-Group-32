from abc import ABC
from typing import TYPE_CHECKING


from .imports import *
from .Defense import Potion, Attack_potion, Defense_potion, maze_player, Defense_type
from .Enemy import *
if TYPE_CHECKING:
    from message import *
    from coord import Coord
    from command import MenuCommand
    from tiles.base import MapObject, Exit, Observer, Tile, Subject, GameEvent, Door
    from tiles.map_objects import Water
    from NPC import NPC
    from maps.base import Map


class Room(Map, ABC, Subject): 
    #A generic room that can contain objects and players

    def __init__(self, entrance_door : Optional[Door] = None, name: str = "DefaultRoom", size: tuple[int, int] = (10,10), entry_point: Coord = Coord(0,0), background_tile: str = "cobblestone"):
        #Constructor for new room
        self.enemies_defeated = False
        self._entrance_door = entrance_door
        self._exit_door = None
        self._player_entered = False
        super().__init__(name=name, 
                         description="", size=size, entry_point=entry_point, background_tile_image=background_tile)
        Subject.__init__(self)
    
    def __setup(self) -> None:
        raise NotImplementedError


    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        #Return all objects in the room
        return []
     
    def player_entered(self, player: "HumanPlayer"):
        event = GameEvent('door_close')
        self.notify_each(event)
    
    def update(self):
        messages = super().update()
        return messages
        #if self.enemies and all(e.is_defeated() for e in self.enemies):

class doorLocker(Observer):
    def __init__(self, door: Door, room : Room) -> None:
        self.__door = door
        self.room = room
        self.__door_pos = self.__door.get_position()

    def update_on_notification(self, event):
        messages = []
        if event == 'player_entered':
            self.room.remove_from_grid(self.__door, self.__door.get_position())
            self.room.send_grid_to_players()
            for player in self.room.get_human_players():
                messages.append(ServerMessage(player, "The door locks behind you!"))
        if event == 'enemy_defeated':
            self.room.add_to_grid(self.__door, self.__door_pos)
            self.room.send_grid_to_players()
            for player in self.room.get_human_players():
                messages.append(ServerMessage(player, "Congratulations! You've defeated the Maze!"))
        return messages

class GladiatorSpawner(Observer):
    def __init__(self, center : Coord, room : Map, enemy_count: int = 3):
        self.enemy_count = enemy_count
        self.center = center
        self.gladiators: List[Gladiator] = []
        self.room = room
        self.messages = []
        self.has_spawned = False
    
    def add_Gladiator(self, gladiator : Gladiator):
        self.gladiators.append(gladiator)
        
    def update_on_notification(self, event: GameEvent):
        messages = []
        if (event == 'player_entered'):
            if self.gladiators.count == 0 and not self.has_spawned:
                self.has_spawned = True
                messages.extend(self._spawn_gladiators())
                messages.extend(self.room.send_grid_to_players())
        return messages

    def _spawn_gladiators(self) -> list[Message]:
        messages =[]
        for i in range(self.enemy_count):
            gladiator = Gladiator_Prototype.custom_copy(10,10)
            offset = Coord(i-self.enemy_count//2,0)
            position = self.center + offset
            try:
                self.add_Gladiator(gladiator)
                self.room.__objects.add(gladiator)
                self.room.add_to_grid(gladiator, position)
                for player in self.room.get_human_players():
                    messages.append(ServerMessage(player, f"A gladiator appears at {position}!"))
                messages.extend(self.room.send_grid_to_players())
            except Exception as e:
                for player in self.room.get_human_players():
                    messages.append(ServerMessage(player,f"Failed to spawn gladiator: {str(e)}"))
                            
        return messages   

class Statue(MapObject):
    #Statue
    def __init__(self, description: str, image_name: str, passable: bool = False, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
        self.__description = description

    def player_interacted(self, player: HumanPlayer):
        return [DialogueMessage(self, player, self.__description, self.get_image_name())]

class Wall(MapObject):
    def __init__(self, image_name: str = "wall5", passable: bool = False):
        super().__init__(image_name=image_name,passable=passable, z_index=1)

class Barrel(MapObject):
    def __init__(self, image_name: str = "barrel", passable: bool = False):
        super().__init__(image_name=image_name,passable=passable, z_index=1)

class Column(MapObject):
    def __init__(self, image_name: str = "column", passable: bool = False, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)

class HotTub(MapObject):
    def __init__(self, image_name: str = "hottub", passable: bool = True, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
    
    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [DialogueMessage(self,player, f"The water relaxes your spirits....", self.get_image_name())]

class SaunaRoom(Room):
    def __init__(self): #, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        super().__init__(entrance_door=Door("wooden_door", "Example House"), name="Sauna Room", size=(19,17), entry_point=Coord(34,15), background_tile="saunatile")
    
    def update(self):
        players : list[HumanPlayer] = self.get_human_players()
        #if players.__len__
        for observer in self._observers:
            observer.update_on_notification

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Sauna.")]
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject,Coord]] = []
        door = Door("wooden_door", "Example House")
        objects.append((door,Coord(18,15)))

        objects.append((HotTub(),Coord(3,3)))
        objects.append((HotTub(),Coord(3,10)))
        objects.append((HotTub(),Coord(10,3)))
        objects.append((HotTub(),Coord(10,10)))

        objects.append((Gladiator_Prototype.custom_copy(1,12), Coord(8,8)))
        objects.append((Gladiator_Prototype.custom_copy(5,7), Coord(8,4)))
        objects.append((Gladiator_Prototype.custom_copy(15,10), Coord(8,12)))

        objects.append((Gladiator_Prototype.custom_copy(14,12), Coord(15,8)))
        objects.append((Gladiator_Prototype.custom_copy(13,12), Coord(15,4)))
        objects.append((Gladiator_Prototype.custom_copy(15,13), Coord(15,12)))

        for x in range(0,17,2):
            objects.append((Column(), Coord(x,0)))
            objects.append((Column(),Coord(0,x)))
            objects.append((Column(),Coord(x,16)))

        for x in range(17):
            if (x != 15):
                objects.append((Column(image_name="columntop"), Coord(18,x)))
        return objects
    
class StatueRoom(Room):
    def __init__(self):
        super().__init__(entrance_door=Door("wooden_door", "Example House"), name="Statue Room", size=(5,18), entry_point=Coord(6,70), background_tile="sandstone")
        self.__setup()
        
    def __setup(self) -> None:
        if (self._observers.__len__ == 0):
            self.attach(GladiatorSpawner(room=self, center=Coord(7,5)))
            
    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        return [ServerMessage(player, f"You have entered the Room of Statues.")]
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects : list[tuple[MapObject,Coord]] = []

        door = Door("wooden_door", "Example House")
        objects.append((door,Coord(4,17)))

        objects.append((Statue(description="Emperor Nero", image_name="statue2"), Coord(1, 14)))
        objects.append((Statue(description="Octavius", image_name="statue3"), Coord(1, 10)))
        objects.append((Statue("Anthony", "statue4"), Coord(1, 6)))
        objects.append((Statue("Marcus Aurelius", "statue5"), Coord(1, 2)))

        objects.append((Gladiator_Prototype.custom_copy(5,15), Coord(2,12)))
        objects.append((Gladiator_Prototype.custom_copy(7,20), Coord(2,8)))
        objects.append((Gladiator_Prototype.custom_copy(13,12), Coord(2,4)))


        return objects

class WineCellar(Room):
    def __init__(self):
        super().__init__(entrance_door=Door("wooden_door", "Example House"), name="Wine Cellar", size=(5,9), entry_point=Coord(53,14), background_tile="cobblestone")
        self.__setup()
        
    def __setup(self) -> None:
        if (self._observers.__len__ == 0):
            self.attach(GladiatorSpawner(room=self, center=Coord(7,5)))

    def update(self):
        messages = []
        if self._observers.count == 0:
             self.attach(GladiatorSpawner(Coord(2,4),self))
        return messages
        

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        messages = []
        messages.extend([ServerMessage(player, f"You have entered the Wine Cellar.")])
        for observer in self._observers:
            messages.extend(observer.update_on_notification('player_entered'))
        return messages
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        
        door = Door("wooden_door", "Example House")
        objects.append((door,Coord(2,0)))

        objects.append((Gladiator_Prototype.custom_copy(10,10), Coord(1,4)))
        objects.append((Gladiator_Prototype.custom_copy(10,10), Coord(2,4)))

        objects.append((Barrel(), Coord(0,0)))
        objects.append((Barrel(), Coord(0,1)))
        objects.append((Barrel(),Coord(0,2)))
        objects.append((Barrel(),Coord(0,3)))
        objects.append((Barrel(),Coord(0,4)))
        objects.append((Barrel(),Coord(0,5)))
        objects.append((Barrel(),Coord(0,6)))
        objects.append((Barrel(),Coord(0,7)))
        objects.append((Barrel(),Coord(0,8)))
        objects.append((Barrel(),Coord(4,0)))
        objects.append((Barrel(),Coord(4,1)))
        objects.append((Barrel(),Coord(4,2)))
        objects.append((Barrel(),Coord(4,3)))
        objects.append((Barrel(),Coord(4,4)))
        objects.append((Barrel(),Coord(4,5)))
        objects.append((Barrel(),Coord(4,6)))
        objects.append((Barrel(),Coord(4,7)))
        objects.append((Barrel(),Coord(4,8)))

        objects.append((Defense_potion(2, Maze_Player,image_name='Defense Potion'), Coord(3,8)))

        return objects

class ArmorStand(MapObject):
    def __init__(self, image_name: str = "armorstand", passable: bool = False, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)

class ArrowStand(MapObject):
    def __init__(self, image_name: str = "arrowstand", passable: bool = False, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)
    
    def player_interacted(self, player: "HumanPlayer") -> list[Message]:
        return [DialogueMessage(self, player, f"Arrow Stand: Coming Soon!", self.get_image_name())]

class Target(MapObject):
    def __init__(self, image_name: str = "target", passable: bool = False, z_index: int = 0) -> None:
        super().__init__(image_name, passable, z_index)

class Armory(Room):
    def __init__(self):
        entrance_door = Door("wooden_door", "Example House")
        super().__init__(entrance_door=entrance_door, name="Armory",size=(13,11), entry_point=Coord(0,2), background_tile="cobblestone")     
        self.__setup()
        
    def __setup(self) -> None:
        if (self._observers.__len__ == 0):
            self.attach(GladiatorSpawner(room=self, center=Coord(7,5)))

    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        messages = []
        messages.extend([ServerMessage(player, f"You have entered the Wine Cellar.")])
        for observer in self._observers:
            messages.extend(observer.update_on_notification('player_entered'))
        return messages
    
    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects : list[tuple[MapObject, Coord]] = []

        door = Door("wooden_door", "Example House")
        objects.append((door,Coord(0,2)))
        objects.append((ArmorStand(), Coord(0,0)))    
        objects.append((ArmorStand(), Coord(3,0)))    
        objects.append((ArmorStand(), Coord(5,0)))    
        objects.append((ArmorStand(), Coord(7,0)))    
        objects.append((ArmorStand(), Coord(9,0)))    
        objects.append((ArrowStand(), Coord(0,3)))

        objects.append((ArmorStand(), Coord(3,3)))    
        objects.append((ArmorStand(), Coord(5,3)))    
        objects.append((ArmorStand(), Coord(7,3)))    
        objects.append((ArmorStand(), Coord(9,3)))

        objects.append((ArmorStand(), Coord(3,6)))    
        objects.append((ArmorStand(), Coord(5,6)))    
        objects.append((ArmorStand(), Coord(7,6)))    
        objects.append((ArmorStand(), Coord(9,6)))    

        objects.append((ArmorStand(), Coord(0,9)))    
        objects.append((ArmorStand(), Coord(3,9)))    
        objects.append((ArmorStand(), Coord(5,9)))    
        objects.append((ArmorStand(), Coord(7,9)))    
        objects.append((ArmorStand(), Coord(9,9)))
        
        objects.append((Target(), Coord(11,1)))
        objects.append((Target(), Coord(11,4)))
        objects.append((Target(), Coord(11,7)))
        objects.append((Target(), Coord(11,10)))

        objects.append((Gladiator_Prototype.custom_copy(12,12), Coord(8,8)))
        objects.append((Gladiator_Prototype.custom_copy(13,15), Coord(8,4)))
        objects.append((Gladiator_Prototype.custom_copy(15,16), Coord(6,8)))
        objects.append((Gladiator_Prototype.custom_copy(11,17), Coord(4,8)))
        objects.append((Gladiator_Prototype.custom_copy(5,13), Coord(10,8)))
        objects.append((Gladiator_Prototype.custom_copy(18,12), Coord(6,4)))


        
        return objects

class FinalBossRoom(Room):
    def __init__(self):
        self._entrance_door = Door("wooden_door", "Example House")
        super().__init__(entrance_door = self._entrance_door, name="Final Boss Room",size=(10,30),entry_point=Coord(0,23),background_tile="sand")
        self.__setup()
        
    def __setup(self) -> None:
        if (self._observers.__len__ == 0):
            self.attach(doorLocker(self._entrance_door, self))
            #self.registerObserver(doorLocker(self._entrance_door, self))
            
    def player_entered(self, player: "HumanPlayer") -> list[Message]:
        messages = []
        messages.extend([ServerMessage(player, f"The air is still...")])
        for observer in self._observers:
            messages.extend(observer.update_on_notification('player_entered'))
        return messages


    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects : list[tuple[MapObject, Coord]] = []
        
        objects.append((self._entrance_door,Coord(9,1)))

        objects.append((Minotaur().get_instance(), Coord(5, 10)))

        return objects