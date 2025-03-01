from maps.base import Map  # Ensure maps.base is accessible
from coord import Coord
from tiles.base import MapObject

class Room(Map):
    """A generic room that can contain objects and players."""

    def __init__(self, name: str, size: tuple[int, int], entry_point: Coord, background_tile: str = "floor"):
        """Initialize a new room."""
        super().__init__(name=name, description="", size=size, entry_point=entry_point, background_tile_image=background_tile)
        self.objects: list[tuple[MapObject, Coord]] = []

    def add_object(self, obj: MapObject, position: Coord) -> None:
        """Add an object to the room at a specific coordinate."""
        self.objects.append((obj, position))

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        """Return all objects placed in the room."""
        return self.objects
    def go():
        print("Hello")