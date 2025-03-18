import pytest
from COMP303_Group_32.Armors import *
from COMP303_Group_32.player import maze_player
from COMP303_Group_32.Maze import Maze

@pytest.fixture
def setup():
    player = maze_player(defense=50, attack_damage=10, name="TestPlayer")
    maze = Maze()
    return player, maze

def test_armor_str(setup):
    player, maze = setup
    armor = Armor("Steel Chest", 20, player, maze, "steel_chest")
    assert str(armor) == "Steel Chest"

def test_get_defense_value(setup):
    player, maze = setup
    armor = Armor("Shield", 15, player, maze, "shield")
    assert armor.get_defense_value() == 15

def test_decrease_defense_partial(setup):
    player, maze = setup
    armor = Armor("Light Armor", 20, player, maze, "light")
    leftover = armor.decrease_defense(5)
    assert leftover == 0
    assert armor.get_defense_value() == 15

def test_decrease_defense_full(setup):
    player, maze = setup
    armor = Armor("Weak Armor", 10, player, maze, "weak")
    leftover = armor.decrease_defense(20)
    assert leftover == 10
    assert armor.get_defense_value() == 0

# --- Subclass checks ---

def test_helmet_inheritance(setup):
    player, maze = setup
    helmet = Helmet("Helmet", 10, player, maze, "helmet")
    assert isinstance(helmet, Armor)
    assert str(helmet) == "Helmet"
    assert helmet.get_defense_value() == 10

def test_chest_plate_inheritance(setup):
    player, maze = setup
    chest = Chest_Plate("Chest", 25, player, maze, "chest")
    assert isinstance(chest, Armor)
    assert str(chest) == "Chest"
    assert chest.get_defense_value() == 25

def test_boots_inheritance(setup):
    player, maze = setup
    boots = Boots("Boots", 5, player, maze, "boots")
    assert isinstance(boots, Armor)
    assert str(boots) == "Boots"
    assert boots.get_defense_value() == 5

def test_pants_inheritance(setup):
    player, maze = setup
    pants = Pants("Pants", 8, player, maze, "pants")
    assert isinstance(pants, Armor)
    assert str(pants) == "Pants"
    assert pants.get_defense_value() == 8