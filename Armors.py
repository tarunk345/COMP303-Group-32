from Defense import Defense


class Armor(Defense):
    def __init__(self) -> None:
        super().__init__()
        self.armor_value:int 

    def get_defense_value(self) -> int:
        return self.armor_value
    

def decrease_defense(self,attack:int)->int:
        if attack>= self.get_defence_value():
            self.armor_value = self.armor_value - attack
            return 0

        attack = attack - self.armor_value
        self.armor_value = 0
        return attack




