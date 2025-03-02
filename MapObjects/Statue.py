from tiles.base import MapObject

class Statue(MapObject):
    #Statue

    def __init__(self, image_name: str = "statue"):
        #Constructor for new statue
        super().__init__(f'tile/statue/{image_name}', passable=False)