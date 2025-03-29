# import pytest
from ..Defense import *
from ..Maze import ExampleHouse

# @pytest.fixture
# def setup():
#     player1 = maze_player(defense=50, attack_value=10)
#     player = HumanPlayer("hello")
#     maze = ExampleHouse()
#     return player, maze

def test_armor_str():
    player1 = maze_player(defense=50, attack_value=10)
    player = HumanPlayer("hello")
    maze = ExampleHouse()
    Gold_chest_plate = Chest_Plate(5,5,Coord(60,63),player1,maze,"Gold Chest Plate")
    Gold_chest_plate.player_entered(player)
    Silver_chest_plate = Chest_Plate(10,10,Coord(62,63),player1,maze,"Silver Chest Plate")
    Silver_chest_plate.player_entered(player)

if __name__ == "__main__":
    test_armor_str()

#     armor = Armor("Steel Chest", 20,0, player, maze, "steel_chest")
#     assert str(armor) == "Steel Chest"

# def test_get_defense_value(setup):
#     player, maze = setup
#     armor = Armor("Shield", 15,0, player, maze, "shield")
#     assert armor.get_defense_value() == 15

# def test_decrease_defense_partial(setup):
#     player, maze = setup
#     armor = Armor("Light Armor", 20,0, player, maze, "light")
#     leftover = armor.decrease_defense(5)
#     assert leftover == 0
#     assert armor.get_defense_value() == 15

# def test_decrease_defense_full(setup):
#     player, maze = setup
#     armor = Armor("Weak Armor", 10,0, player, maze, "weak")
#     leftover = armor.decrease_defense(20)
#     assert leftover == 10
#     assert armor.get_defense_value() == 0

# def test_helmet_inheritance(setup):
#     player, maze = setup
#     helmet = Helmet("Helmet", 10,0, player, maze, "helmet")
#     assert isinstance(helmet, Armor)
#     assert str(helmet) == "Helmet"
#     assert helmet.get_defense_value() == 10

# def test_chest_plate_inheritance(setup):
#     player, maze = setup
#     chest = Chest_Plate("Chest", 25,0, player, maze, "chest")
#     assert isinstance(chest, Armor)
#     assert str(chest) == "Chest"
#     assert chest.get_defense_value() == 25

# def test_boots_inheritance(setup):
#     player, maze = setup
#     boots = Boots("Boots", 5,0, player, maze, "boots")
#     assert isinstance(boots, Armor)
#     assert str(boots) == "Boots"
#     assert boots.get_defense_value() == 5

# def test_pants_inheritance(setup):
#     player, maze = setup
#     pants = Pants("Pants", 8,0, player, maze, "pants")
#     assert isinstance(pants, Armor)
#     assert str(pants) == "Pants"
#     assert pants.get_defense_value() == 8