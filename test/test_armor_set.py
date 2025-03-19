import pytest
from Armor_set import Armor_Set
from Armors import Armor
from player import maze_player
from Maze import Maze
from Defense import Defense_type

@pytest.fixture
def setup():
    player = maze_player(50, 10, 10, "TestPlayer")
    maze = Maze()
    return player, maze

def test_initial_defense_is_zero():
    armor_set = Armor_Set()
    assert armor_set.get_defense_value() == 0

def test_add_single_armor(setup):
    player, maze = setup
    armor = Armor("Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    armor_set = Armor_Set()
    result = armor_set.add_armor(armor)
    assert result is None
    assert armor_set.get_defense_value() == 10

def test_add_stronger_duplicate_replaces_old(setup):
    player, maze = setup
    armor1 = Armor("Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    armor2 = Armor("Helmet", 20, 3, Defense_type.HELMET, player, maze, "helmet")
    armor_set = Armor_Set()
    armor_set.add_armor(armor1)
    result = armor_set.add_armor(armor2)
    assert result == armor1
    assert armor_set.get_defense_value() == 20