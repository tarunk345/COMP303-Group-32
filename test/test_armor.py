import pytest
from Armors import *
from player import maze_player
from Maze import Maze

@pytest.fixture
def setup():
    player = maze_player(defense=50, attack_damage=10, name="TestPlayer")
    maze = Maze()
    return player, maze

def test_armor_str(setup):
    player, maze = setup
    armor = Armor("Steel Chest", 20, 5, Defense_type.CHEST_PLATE, player, maze, "steel_chest")
    assert str(armor) == "Steel Chest"

def test_get_defense_value(setup):
    player, maze = setup
    armor = Armor("Shield", 15, 3, Defense_type.BOOTS, player, maze, "shield")
    assert armor.get_defense_value() == 15

def test_decrease_defense_partial(setup):
    player, maze = setup
    armor = Armor("Light Armor", 20, 2, Defense_type.PANTS, player, maze, "light")
    leftover = armor.decrease_defense(5)
    assert leftover == 0
    assert armor.get_defense_value() == 15

def test_decrease_defense_full(setup):
    player, maze = setup
    armor = Armor("Weak Armor", 10, 1, Defense_type.HELMET, player, maze, "weak")
    leftover = armor.decrease_defense(20)
    assert leftover == 10
    assert armor.get_defense_value() == 0

def test_helmet_inheritance(setup):
    player, maze = setup
    helmet = Helmet("Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    assert isinstance(helmet, Armor)
    assert str(helmet) == "Helmet"
    assert helmet.get_defense_value() == 10

def test_chest_plate_inheritance(setup):
    player, maze = setup
    chest = Chest_Plate("Chest", 25, 4, Defense_type.CHEST_PLATE, player, maze, "chest")
    assert isinstance(chest, Armor)
    assert str(chest) == "Chest"
    assert chest.get_defense_value() == 25

def test_boots_inheritance(setup):
    player, maze = setup
    boots = Boots("Boots", 5, 1, Defense_type.BOOTS, player, maze, "boots")
    assert isinstance(boots, Armor)
    assert str(boots) == "Boots"
    assert boots.get_defense_value() == 5

def test_pants_inheritance(setup):
    player, maze = setup
    pants = Pants("Pants", 8, 3, Defense_type.PANTS, player, maze, "pants")
    assert isinstance(pants, Armor)
    assert str(pants) == "Pants"
    assert pants.get_defense_value() == 8