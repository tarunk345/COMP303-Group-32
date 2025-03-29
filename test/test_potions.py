import pytest
from Potions import Potion
from Maze import Maze
from player import maze_player
from Armors import *
from Armor_set import Armor_Set
from Defense import Defense_type

@pytest.fixture
def setup():
    player = maze_player(40, 8, 8, "TestPlayer")
    maze = Maze()
    return player, maze

def test_potion_str(setup):
    player, maze = setup
    potion = Defense_potion("Defense Boost", 2, Defense_type.DEFENSE_POTION, player, maze, "potion")
    assert str(potion) == "Defense Boost"

def test_set_and_get_armor(setup):
    player, maze = setup
    potion = Defense_potion("Defense Boost", 2, Defense_type.DEFENSE_POTION, player, maze, "potion")
    helmet = Helmet("Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    potion.set_armor(helmet)
    assert potion.get_defense_value() == 20
    assert str(potion) == "Helmet"

def test_defense_value_with_zero_armor_defense(setup):
    player, maze = setup
    potion = Defense_potion("Weak Potion", 5, Defense_type.DEFENSE_POTION, player, maze, "potion")
    armor = Helmet("Paper Hat", 0, 1, Defense_type.HELMET, player, maze, "paper_hat")
    potion.set_armor(armor)
    assert potion.get_defense_value() == 0

    def test_potion_with_attack_potion_type(setup):
    player, maze = setup
    potion = Attack_potion("Attack Potion", 5, Defense_type.ATTACK_POTION, player, maze, "potion")
    assert str(potion) == "Attack Potion"
    assert potion.get_defense_value() == 0  # No armor assigned

def test_potion_set_armor_twice_overwrites(setup):
    player, maze = setup
    potion = Potion("Swap Potion", 3, Defense_type.DEFENSE_POTION, player, maze, "potion")
    armor1 = Helmet("Helmet1", 5, 2, Defense_type.HELMET, player, maze, "helmet1")
    armor2 = Helmet("Helmet2", 12, 2, Defense_type.HELMET, player, maze, "helmet2")
    potion.set_armor(armor1)
    potion.set_armor(armor2)
    assert potion.get_defense_value() == 24
    assert str(potion) == "Helmet2"

def test_potion_with_zero_defense_multiplier(setup):
    player, maze = setup
    potion = Potion("Useless Potion", 0, Defense_type.DEFENSE_POTION, player, maze, "potion")
    armor = Helmet("Basic Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    potion.set_armor(armor)
    assert potion.get_defense_value() == 0

def test_defense_decrease_to_exact_zero(setup):
    player, maze = setup
    potion = Potion("Exact Down", 2, Defense_type.DEFENSE_POTION, player, maze, "potion")
    armor = Helmet("Exact", 10, 1, Defense_type.HELMET, player, maze, "exact")
    potion.set_armor(armor)
    leftover = potion.decrease_defense(20)
    assert leftover == 0
    assert potion.get_defense_value() == 0

def test_multiple_decrease_steps(setup):
    player, maze = setup
    potion = Potion("Drainer", 2, Defense_type.DEFENSE_POTION, player, maze, "potion")
    armor = Helmet("Durable", 15, 1, Defense_type.HELMET, player, maze, "durable")
    potion.set_armor(armor)
    potion.decrease_defense(5)
    potion.decrease_defense(5)
    remaining = potion.decrease_defense(10)
    assert remaining == 5
    assert potion.get_defense_value() == 0

def test_add_multiple_potions_to_armor_set(setup):
    player, maze = setup
    potion1 = Potion("First", 2, Defense_type.DEFENSE_POTION, player, maze, "p1")
    potion2 = Potion("Second", 3, Defense_type.DEFENSE_POTION, player, maze, "p2")
    armor_set = Armor_Set()
    helmet = Helmet("Helmet", 10, 1, Defense_type.HELMET, player, maze, "h")
    armor_set.add_armor(helmet)
    armor_set.add_potion(potion1)
    armor_set.add_potion(potion2)
    assert armor_set.get_defense_value() == 30  # 10 + 2*10 + 3*10

def test_potion_str_returns_name_after_set_armor(setup):
    player, maze = setup
    potion = Potion("Custom", 3, Defense_type.DEFENSE_POTION, player, maze, "pot")
    armor = Helmet("Custom Armor", 7, 1, Defense_type.HELMET, player, maze, "cust")
    potion.set_armor(armor)
    assert str(potion) == "Custom Armor"