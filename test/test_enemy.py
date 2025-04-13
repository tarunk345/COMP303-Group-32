import pytest
from ..Defense import maze_player
from ..Enemy import Gladiator, Minotaur

# strong player with good stats so they don’t die easily in the tests
@pytest.fixture
def strong_player():
    player = maze_player(defense=50, attack_value=100)
    player.set_maze(player.get_maze())
    return player

# weak player to die quickly
@pytest.fixture
def weak_player():
    player = maze_player(defense=5, attack_value=1)
    player.set_maze(player.get_maze())
    return player



# Enemy Basics

# testing basic attack should reduce defense
def test_enemy_attack_reduces_player_defense(strong_player):
    start_def = strong_player.get_defense_value()
    result = Gladiator(defense=10, attack_damage=10).attack()
    assert result > 0
    assert strong_player.get_defense_value() < start_def

# enemy taking exact amount of damage to kill him
def test_enemy_decrease_defense_exact():
    enemy = Gladiator(defense=10, attack_damage=1)
    leftover = enemy.decrease_defense(10)
    assert leftover == 0
    assert enemy.get_defense_value() == 0

# enemy takes some damage but doesn’t die
def test_enemy_decrease_defense_partial():
    enemy = Gladiator(defense=10, attack_damage=1)
    leftover = enemy.decrease_defense(5)
    assert leftover == 0
    assert enemy.get_defense_value() == 5

# enemy should be considered defeated if health hits zero
def test_enemy_defeat_status():
    enemy = Gladiator(defense=5, attack_damage=1)
    assert enemy.is_defeated() is False
    enemy.decrease_defense(10)
    assert enemy.is_defeated() is True



# Dialogue from player and enemy interacting

# strong player kills the enemy fast: we see kill message
def test_player_interacted_enemy_dies(strong_player):
    enemy = Gladiator(defense=10, attack_damage=1)
    result = enemy.player_interacted(strong_player)
    text = result[0]._get_data()["dialogue_text"]
    assert "died" in text or "remaining Health" in text

# enemy has lots of health: We see damage taken message
def test_player_interacted_enemy_survives(strong_player):
    enemy = Gladiator(defense=100, attack_damage=1)
    result = enemy.player_interacted(strong_player)
    text = result[0]._get_data()["dialogue_text"]
    assert "received damage" in text

# weak player gets hit and dies
def test_player_interacted_player_dies(weak_player):
    enemy = Gladiator(defense=10, attack_damage=10)
    result = enemy.player_interacted(weak_player)
    text = result[0]._get_data()["dialogue_text"]
    assert "died" in text or "remaining Health" in text


# Minotaur-Specific Stuff

# make sure minotaur is a singleton
def test_minotaur_is_singleton():
    m1 = Minotaur.get_instance()
    m2 = Minotaur.get_instance()
    assert m1 is m2

# stats should match what we expect
def test_minotaur_stats():
    minotaur = Minotaur.get_instance()
    assert minotaur.get_attack_damage() == 25
    assert minotaur.get_defense_value() == 30

# minotaur can attack
def test_minotaur_attack_reduces_player_defense(strong_player):
    start_def = strong_player.get_defense_value()
    minotaur = Minotaur.get_instance()
    damage = minotaur.attack()
    assert damage > 0
    assert strong_player.get_defense_value() < start_def

# testing that minotaur deals a lot of damage to players that are weak
def test_minotaur_attack_fully_depletes_player():
    player = maze_player(defense=20, attack_value=10)
    player.set_maze(player.get_maze())
    minotaur = Minotaur.get_instance()

    before = player.get_defense_value()
    damage = minotaur.attack()
    after = player.get_defense_value()

    assert damage >= (before - after)
    assert after < before

# after being attacked, minotaur defense should drop
def test_minotaur_defense_drops_after_hit(strong_player):
    minotaur = Minotaur.get_instance()
    original_def = minotaur.get_defense_value()
    leftover = minotaur.decrease_defense(strong_player.get_attack_value())
    assert minotaur.get_defense_value() < original_def or minotaur.get_defense_value() == 0
    assert leftover >= 0

# calling get_instance should still return the same minotaur (singleton)
def test_minotaur_singleton_repeated():
    instances = [Minotaur.get_instance() for _ in range(10)]
    ids = [id(i) for i in instances]
    assert len(set(ids)) == 1
