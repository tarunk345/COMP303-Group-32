import pytest
from ..Defense import *
from ..Maze import ExampleHouse

# Create a new player each time with a maze set up
@pytest.fixture
def setup_player():
    player = maze_player(defense=50, attack_value=10)
    maze = ExampleHouse()
    player.set_maze(maze)
    return player, maze


# Maze Player Core Stat Tests

# Check basic stats for player
def test_player_initial_stats(setup_player):
    player, _ = setup_player
    assert player.get_attack_value() == 10
    assert player.get_defense_value() == 50

# Confirm maze can be stored and retrieved
def test_set_and_get_maze(setup_player):
    player, maze = setup_player
    assert player.get_maze() == maze

# Lower defense value by a set amount
def test_decrease_defense(setup_player):
    player, _ = setup_player
    player.decrease_defense(30)
    assert player.get_defense_value() == 20

# If defense goes below zero, get leftover damage
def test_decrease_defense_to_zero(setup_player):
    player, _ = setup_player
    leftover = player.decrease_defense(60)
    assert player.get_defense_value() == 0
    assert leftover == 10

# Test healing up some amount
def test_heal_player(setup_player):
    player, _ = setup_player
    player.decrease_defense(30)
    player.heal(20)
    assert player.get_defense_value() == 40

# Healing should cap at 100, not go above
def test_heal_beyond_max(setup_player):
    player, _ = setup_player
    player.heal(100)
    assert player.get_defense_value() == 100


# Armor Integration Tests

# Armor should be added successfully
def test_check_armor_player_returns_none_on_success(setup_player):
    player, _ = setup_player
    boots = Boots(5, 1, player, "boots")
    result = player.check_armor_player(boots)
    assert result is None

# Armor boosts both stats
def test_add_armor_and_boost_stats(setup_player):
    player, _ = setup_player
    boots = Boots(5, 1, player, "boots")
    player.check_armor_player(boots)
    assert player.get_attack_value() == 15
    assert player.get_defense_value() == 60

# Better armor should override weak one
def test_replace_with_better_armor(setup_player):
    player, _ = setup_player
    weak = Boots(2, 1, player, "boots")
    strong = Boots(5, 2, player, "boots")
    player.check_armor_player(weak)
    replaced = player.check_armor_player(strong)
    assert replaced == weak
    assert player.get_attack_value() == 15
    assert player.get_defense_value() == 62

# Weaker armor should be rejected
def test_reject_weaker_armor(setup_player):
    player, _ = setup_player
    strong = Boots(5, 2, player, "boots")
    weak = Boots(2, 1, player, "boots")
    player.check_armor_player(strong)
    rejected = player.check_armor_player(weak)
    assert rejected == weak
    assert player.get_attack_value() == 15
    assert player.get_defense_value() == 62

# Armor with defense only shouldn’t change attack
def test_armor_only_adds_defense(setup_player):
    player, _ = setup_player
    helmet = Helmet(0, 10, player, "helmet")
    player.check_armor_player(helmet)
    assert player.get_attack_value() == 10
    assert player.get_defense_value() == 60



# Potion Integration Tests

# Potion should replace armor
def test_potion_replaces_armor(setup_player):
    player, _ = setup_player
    helmet = Helmet(10, 2, player, "helmet")
    potion = Attack_potion(2, player, "helmet")
    player.check_armor_player(helmet)
    replaced = player.check_potion_player(potion)
    assert replaced == helmet
    assert player.get_attack_value() == 12
    assert player.get_defense_value() == 50

# Potion should fail if there's no armor
def test_potion_fails_if_no_armor(setup_player):
    player, _ = setup_player
    potion = Attack_potion(2, player, "helmet")
    result = player.check_potion_player(potion)
    assert result == potion

# Working potion boosts attack
def test_potion_boosts_attack(setup_player):
    player, _ = setup_player
    helmet = Helmet(10, 2, player, "helmet")
    potion = Attack_potion(3, player, "helmet")
    player.check_armor_player(helmet)
    result = player.check_potion_player(potion)
    assert result == helmet
    assert player.get_attack_value() == 13
    assert player.get_defense_value() == 50

# Defense potion should stack with armor
def test_potion_boosts_defense(setup_player):
    player, _ = setup_player
    chest = Chest_Plate(20, 0, player, "chest")
    potion = Defense_potion(5, player, "chest")
    player.check_armor_player(chest)
    result = player.check_potion_player(potion)
    assert result == chest
    assert player.get_attack_value() == 30
    assert player.get_defense_value() == 55

# Fails when no armor of that type exists
def test_potion_fails_if_type_not_present(setup_player):
    player, _ = setup_player
    potion = Defense_potion(3, player, "boots")
    result = player.check_potion_player(potion)
    assert result == potion

# Stronger potion should override weaker one
def test_potion_replaces_weaker_potion(setup_player):
    player, _ = setup_player
    helmet = Helmet(10, 2, player, "helmet")
    weak = Attack_potion(1, player, "helmet")
    strong = Attack_potion(3, player, "helmet")
    player.check_armor_player(helmet)
    player.check_potion_player(weak)
    result = player.check_potion_player(strong)
    assert result is None
    assert player.get_attack_value() == 13

# Can't stack same type of potion twice
def test_no_double_stack_same_type_potion(setup_player):
    player, _ = setup_player
    helmet = Helmet(10, 2, player, "helmet")
    potion1 = Attack_potion(2, player, "helmet")
    potion2 = Attack_potion(3, player, "helmet")
    player.check_armor_player(helmet)
    player.check_potion_player(potion1)
    result = player.check_potion_player(potion2)
    assert result is None
    assert player.get_attack_value() == 13
