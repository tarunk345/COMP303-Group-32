import pytest
from ..Defense import (
    maze_player,
    Chest_Plate,
    Defense_potion,
    Attack_potion
)

@pytest.fixture
def player():
    return maze_player(defense=20, attack_value=10)

@pytest.fixture
def base_armor(player):
    return Chest_Plate(defense_value=10, attack_value=5, player=player, image_name="Chest Plate")

# ------------------------
# Defense Potion Tests
# ------------------------

def test_defense_potion_fields_are_set_correctly(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    expected_defense = base_armor.get_defense_value() * 2
    assert potion.get_defense_value() == expected_defense
    assert potion.get_attack_value() == base_armor.get_attack_value()

def test_defense_potion_damage_reduction(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    potion.decrease_defense(5)
    assert potion.get_defense_value() == 15  # Started at 20

def test_defense_potion_overkill_returns_remaining_damage(player, base_armor):
    potion = Defense_potion(multiplier=1, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    remaining = potion.decrease_defense(100)
    assert potion.get_defense_value() == 0
    assert remaining > 0

# ------------------------
# Attack Potion Tests
# ------------------------

def test_attack_potion_attack_is_multiplied(player, base_armor):
    potion = Attack_potion(multiplier=3, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    expected_attack = base_armor.get_attack_value() * 3
    assert potion.get_attack_value() == expected_attack

def test_attack_potion_damage_reduction(player, base_armor):
    potion = Attack_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    potion.decrease_defense(4)
    assert potion.get_defense_value() == base_armor.get_defense_value() - 4

def test_attack_potion_overkill_returns_remaining_damage(player, base_armor):
    potion = Attack_potion(multiplier=1, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()

    remaining = potion.decrease_defense(99)
    assert potion.get_defense_value() == 0
    assert remaining > 0