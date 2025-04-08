from typing import List, TYPE_CHECKING, Literal

from .Defense import *
from .imports import * 
if TYPE_CHECKING:
    from Player import HumanPlayer
    from coord import Coord
    from maps.base import Map
    from message import HumanPlayer, Message
    from tiles.base import MapObject
    from tiles.map_objects import *


class Enemy(NPC, CharacterMapObject):
    def __init__(self, defense: int, attack_damage: int, name: str, image: str, encounter_text : str, facing_direction: Literal['up', 'down', 'left', 'right'] = 'down', staring_distance: int = 0, bg_music=''): 
        super().__init__(name=name,image=image,encounter_text=encounter_text,facing_direction=facing_direction,staring_distance=staring_distance,bg_music=bg_music)
        self.__attack_damage = attack_damage
        self.__defense = defense
        self.__maze_player = player
    
    def get_maze_player(self):
        return self.__maze_player
    

    def get_defense_value(self)->int:
        return self.__defense
    

    def get_attack_damage(self) -> int:
        return self.__attack_damage
    
    def get_image(self) -> str:
        return self._image_name
    
    def decrease_defense(self , attack:int)->int:
        if attack >= self.__defense:
            remaining_damage = attack - self.__defense
            self.__defense = 0  # Defense is fully depleted
            
            return remaining_damage
        else:
            self.__defense -= attack
            return 0  # No remaining damage

    # def player_moved(self, player: "HumanPlayer") -> List[Message]:
    #     """Handle the event of the player moving. If the player is within a certain distance, the enemy attacks."""
    #     messages: List[Message] = super().player_moved(player)  # Call the parent class's method

    #     if type(player) != HumanPlayer:
    #         return []

    #     dist = self._current_position.distance(player.get_current_position())
    #     if dist <= self.__staring_distance:

    #         attack_messages = self.attack()
    #         messages.extend(attack_messages)

    #     return messages 

    def attack(self)->int:
        return self.__maze_player.decrease_defense(self.__attack_damage)
        # return [DialogueMessage(self, player, f"{self.get_name()} attacks you for {self.__attack_damage} damage!", self.get_image())]
    
    def is_defeated(self) -> bool:
        return self.__defense <= 0
    

    def player_interacted(self, player: "HumanPlayer") -> List[Message]:
        self.decrease_defense(self.__maze_player.get_attack_value())
      
        if self.__defense == 0:
            # return [DialogueMessage(self, player, f"{self.get_name()} attacks you for {self.__attack_damage} damage!", self.get_image())]
            player.get_current_room().remove_from_grid(self,self.get_current_position())
            return [DialogueMessage(self, player,self.get_name() + "died!"+player.get_name() + "received damage! \n"+player.get_name()+"remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())]
        
        if self.attack() > 0:
            # player.change_room("Trottier Town")
            # player.update_position(,self.__maze_player.get_maze())
            player.change_room(self.__maze_player.get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,player.get_name() + "died!",self.get_image_name())]

        return [DialogueMessage(self, player,self.get_name() + "received damage! \n"+self.get_name()+"remaining Health:"+str(self.__defense)+"\n"+player.get_name() + "received damage! \n"+player.get_name()+"remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())] 
       
class Minotaur(Enemy):
    _instance = None #Singleton

    @staticmethod
    def get_instance():
        if Minotaur._instance is None:
            Minotaur._instance = Minotaur()
        return Minotaur._instance

    def __init__(self):
        if Minotaur._instance is not None:
            raise Exception("Minotaur is a singleton")

        super().__init__(
            defense=100,
            attack_damage=25,
            name="Minotaur",
            image="minotaur",  # Replace with your actual image name
            encounter_text="The final boss has appeared!",
            facing_direction='down',
            staring_distance=5
        )

    def player_interacted(self, player: "HumanPlayer") -> List[Message]:
        self.decrease_defense(self.__maze_player.get_attack_value())
      
        if self.__defense == 0:
            # return [DialogueMessage(self, player, f"{self.get_name()} attacks you for {self.__attack_damage} damage!", self.get_image())]
            player.get_current_room().remove_from_grid(self,self.get_current_position())
            player.change_room(self.__maze_player.get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,self.get_name() + "died! You have cleared the Maze!",self.get_image_name())]
        
        if self.attack() > 0:
            # player.change_room("Trottier Town")
            # player.update_position(,self.__maze_player.get_maze())
            player.change_room(self.__maze_player.get_maze())
            player.move_to(Coord(70,62))
            return [DialogueMessage(self, player,player.get_name() + "died!",self.get_image_name())]

        return [DialogueMessage(self, player,self.get_name() + "received damage! \n"+self.get_name()+"remaining Health:"+str(self.__defense)+"\n"+player.get_name() + "received damage! \n"+player.get_name()+"remaining Health:"+str(self.get_maze_player().get_defense_value()),self.get_image_name())] 

    # def player_interacted(self, player: "HumanPlayer") -> List[DialogueMessage]:
    #     messages = [
    #         DialogueMessage(self, player, "The Minotaur has attacked you!", self.get_image())
    #     ]
    #     messages.extend(self.attack())
    #     return messages

    

class Gladiator(Enemy):
    def __init__(
        self,
        name: str = "Gladiator",
        image: str = "gladiator",
        encounter_text: str = "a Gladiator appears before you!",
        attack_damage: int = 10,
        defense: int = 10,
        facing_direction: Literal['up', 'down', 'left', 'right'] = 'down',
        staring_distance: int = 1,
        bg_music: str = ''
    ):
        super().__init__(
            defense=defense,
            attack_damage=attack_damage,
            name=name,
            image=image,
            encounter_text=encounter_text,
            facing_direction=facing_direction,
            staring_distance=staring_distance,
            bg_music=bg_music
        )
        # self.__aggro_range = 5
        # self.__attack_cooldown = 0
        # self.__target = None
    

    # def update(self) -> list[Message]:
    #     messages = []
    #     if self.__attack_cooldown > 0:
    #         self.__attack_cooldown -= 1
            
    #     if not self.__target:
    #         self.__target = self.__find_nearest_player()
            
    #     if self.__target:
    #         messages.extend(self.__move_toward_target())
    #         if self.__can_attack():
    #             maze_player = self.get_maze_player()
    #             maze = self.__target.get_current_room()
    #             remaing_health = maze_player.decrease_defense(self.get_attack_damage())
    #             if remaing_health>0:
    #                 maze.remove_player(self.__target)
    #             return [DialogueMessage(self, self.__target, f"{self.get_name()} attacks you  {self.__attack_damage} damage!", self.get_image())]
                
    #     return messages

    # def __find_nearest_player(self) -> Optional[HumanPlayer]:
    #     current_room = self.get_current_room()
    #     # if not isinstance(current_room, Room):
    #     #     return None
        
    #     nearest = None
    #     min_dist = float('inf')
    #     my_pos = self.get_position()

    #     for player in current_room.get_human_players():
    #         dist = player.get_position().distance(my_pos)
    #         if dist < self.__aggro_range and dist < min_dist:
    #             nearest = player
    #             min_dist = dist
                
    #     return nearest

    # def __move_toward_target(self) -> list[Message]:
    #     if not self.__target:
    #         return []
            
    #     my_pos = self.get_position()
    #     target_pos = self.__target.get_position()
    #     direction = self.__calculate_move_direction(my_pos, target_pos)
        
    #     # Try to move in calculated direction
    #     new_pos = my_pos + direction
    #     if self.__can_move_to(new_pos):
    #         self.get_current_room().move_object(self, new_pos)
    #         return [ServerMessage(None, f"The gladiator moves {direction.name}!")]
    #     return []
    
    # def __calculate_move_direction(self, from_pos: Coord, to_pos: Coord) -> Coord:
    #     dx = to_pos.x - from_pos.x
    #     dy = to_pos.y - from_pos.y
        
    #     if abs(dx) > abs(dy):
    #         return Coord(1 if dx > 0 else -1, 0)
    #     else:
    #         return Coord(0, 1 if dy > 0 else -1)
            
    # def __can_attack(self) -> bool:
    #     if self.__attack_cooldown > 0 or not self.__target:
    #         return False
            
    #     return self.get_position().distance_to(
    #         self.__target.get_position()
    #     ) <= 1  # Adjacent
