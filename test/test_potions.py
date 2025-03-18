import pytest
from Potions import Potion
from COMP303_Group_32.Maze import Maze
from COMP303_Group_32.player import maze_player
from COMP303_Group_32.Armors import *
from COMP303_Group_32.Armor_set import Armor_Set

@pytest.fixture
def setup():
    player = maze_player("TestPlayer")
    maze = Maze()
    return player, maze

def test_potion_str(setup):
    player, maze = setup
    potion = Potion("Defense Boost", 2, player, maze, "potion.png")
    assert str(potion) == "Defense Boost"

def test_set_and_get_armor(setup):
    player, maze = setup
    potion = Potion("Defense Boost", 2, player, maze, "potion.png")
    helmet = Helmet("Helmet", 10, player, maze, "helmet.png")
    potion.set_armor(helmet)
    assert potion.get_defense_value() == 20
    assert str(potion) == "Helmet"

def test_defense_value_with_zero_armor_defense(setup):
    player, maze = setup
    potion = Potion("Weak Potion", 5, player, maze, "potion.png")
    armor = Helmet("Paper Hat", 0, player, maze, "paper_hat.png")
    potion.set_armor(armor)
    assert potion.get_defense_value() == 0

def test_decrease_defense_partial(setup):
    player, maze = setup
    potion = Potion("Boost", 2, player, maze, "potion.png")
    armor = Helmet("Helmet", 10, player, maze, "helmet.png")
    potion.set_armor(armor)
    remaining = potion.decrease_defense(5)
    assert potion.get_defense_value() == 15
    assert remaining == 0

def test_decrease_defense_full(setup):
    player, maze = setup
    potion = Potion("Boost", 2, player, maze, "potion.png")
    armor = Helmet("Helmet", 10, player, maze, "helmet.png")
    potion.set_armor(armor)
    remaining = potion.decrease_defense(30)
    assert potion.get_defense_value() == 0
    assert remaining == 10

def test_add_potion_to_armor_set(setup):
    player, maze = setup
    potion = Potion("Boost", 2, player, maze, "potion.png")
    armor_set = Armor_Set()
    helmet = Helmet("Helmet", 10, player, maze, "helmet.png")
    armor_set.add_armor(helmet)
    result = armor_set.add_potion(potion)
    assert result is None
    assert armor_set.get_defense_value() == 20  # 2x helmet defense