import pytest
from COMP303_Group_32.Armor_set import Armor_Set
from COMP303_Group_32.Armors import Armor
from COMP303_Group_32.player import maze_player
from COMP303_Group_32.Maze import Maze

@pytest.fixture
def setup():
    player = maze_player(50, 10, "TestPlayer")
    maze = Maze()
    return player, maze

def test_initial_defense_is_zero():
    armor_set = Armor_Set()
    assert armor_set.get_defense_value() == 0

def test_add_single_armor(setup):
    player, maze = setup
    armor = Armor("Helmet", 10, player, maze, "helmet")
    armor_set = Armor_Set()
    result = armor_set.add_armor(armor)
    assert result is None
    assert armor_set.get_defense_value() == 10

def test_add_stronger_duplicate_replaces_old(setup):
    player, maze = setup
    armor1 = Armor("Helmet", 10, player, maze, "helmet")
    armor2 = Armor("Helmet", 20, player, maze, "helmet")
    armor_set = Armor_Set()
    armor_set.add_armor(armor1)
    result = armor_set.add_armor(armor2)
    assert result == armor1
    assert armor_set.get_defense_value() == 20

def test_add_weaker_duplicate_is_rejected(setup):
    player, maze = setup
    armor1 = Armor("Helmet", 20, player, maze, "helmet")
    armor2 = Armor("Helmet", 10, player, maze, "helmet")
    armor_set = Armor_Set()
    armor_set.add_armor(armor1)
    result = armor_set.add_armor(armor2)
    assert result == armor2
    assert armor_set.get_defense_value() == 20

def test_decrease_defense_damages_all_armors(setup):
    player, maze = setup
    armor1 = Armor("Helmet", 10, player, maze, "helmet")
    armor2 = Armor("Boots", 5, player, maze, "boots")
    armor_set = Armor_Set()
    armor_set.add_armor(armor1)
    armor_set.add_armor(armor2)
    leftover = armor_set.decrease_defense(12)
    assert leftover == 0
    assert armor_set.get_defense_value() == 3

def test_decrease_defense_not_enough_armor(setup):
    player, maze = setup
    armor1 = Armor("Helmet", 5, player, maze, "helmet")
    armor_set = Armor_Set()
    armor_set.add_armor(armor1)
    leftover = armor_set.decrease_defense(10)
    assert leftover == 5
    assert armor_set.get_defense_value() == 0