import pytest
from player import maze_player
from Defense import Defense_type
from Maze import Maze
from Armors import Helmet

@pytest.fixture
def setup():
    player = maze_player(50, 10,10, "TestPlayer")
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
    helmet = Helmet("Helmet", 10, 2, Defense_type.HELMET, player, maze, "helmet")
    result = player.check_armor_player(helmet)
    assert result is None
    assert player.get_defense_value() == 60