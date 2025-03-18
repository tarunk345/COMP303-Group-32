from Enemy import Enemy
from coord import Coord
from message import DialogueMessage
from typing import List

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
            image="minotaur.png",  # Replace with your actual image name
            encounter_text="The final boss has appeared!",
            facing_direction='down',
            staring_distance=5
        )

    def player_interacted(self, player) -> List[DialogueMessage]:
        messages = [
            DialogueMessage(self, player, "The Minotaur has attacked you!", self.get_image())
        ]
        messages.extend(self.attack(player))
        return messages