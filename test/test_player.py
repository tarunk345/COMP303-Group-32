import pytest
from COMP303_Group_32.player import maze_player
from COMP303_Group_32.Maze import Maze
from COMP303_Group_32.Armors import Helmet
from COMP303_Group_32.Potions import Potion

@pytest.fixture
def setup():
    player = maze_player(50, 10, "TestPlayer")
    maze = Maze()
    return player, maze

def test_get_defense_value(setup):
    player, _ = setup
    assert player.get_defense_value() == 50

def test_decrease_defense_partial(setup):
    player, _ = setup
    leftover = player.decrease_defense(30)
    assert leftover == 0
    assert player.get_defense_value() == 20

def test_decrease_defense_overkill(setup):
    player, _ = setup
    leftover = player.decrease_defense(100)
    assert leftover == 1
    assert player.get_defense_value() == 0

def test_check_armor_player_adds_armor(setup):
    player, maze = setup
    helmet = Helmet("Helmet", 10, player, maze, "helmet")
    result = player.check_armor_player(helmet)
    assert result is None
    assert player.get_defense_value() > 50 

def test_check_potion_player_rejects_if_no_armor(setup):
    player, maze = setup
    potion = Potion("Potion", 2, player, maze, "potion")
    result = player.check_potion_player(potion)
    assert result == potion  #No armor so should just be equal