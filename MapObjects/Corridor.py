from Room import Room
from coord import Coord

class Corridor(Room):
    #Creates a new corridor

    def __init__(self, name: str, length: int, entry_point: Coord):
        #Cunstroctor for new corridor
        super().__init__(name=name, size=(1, length), entry_point=entry_point, background_tile="stone")