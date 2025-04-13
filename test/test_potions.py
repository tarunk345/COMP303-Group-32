import pytest
from ..Defense import (
    maze_player,
    Chest_Plate,
    Defense_potion,
    Attack_potion
)

# Create a basic maze player with default stats
@pytest.fixture
def player():
    return maze_player(defense=20, attack_value=10)

# Base armor that can be reused across potion tests
@pytest.fixture
def base_armor(player):
    return Chest_Plate(defense_value=10, attack_value=5, player=player, image_name="Chest Plate")

# Defense Potion Tests

# Set base armor and multiply defense by 2, check stats are updated correctly
def test_defense_potion_fields_are_set_correctly(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    assert potion.get_defense_value() == base_armor.get_defense_value() * 2
    assert potion.get_attack_value() == base_armor.get_attack_value()

# Deal some damage and see that defense is reduced as expected
def test_defense_potion_damage_reduction(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    potion.decrease_defense(5)
    assert potion.get_defense_value() == 15

# Apply more damage than defense and check leftover
def test_defense_potion_overkill_returns_remaining_damage(player, base_armor):
    potion = Defense_potion(multiplier=1, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    remaining = potion.decrease_defense(100)
    assert potion.get_defense_value() == 0
    assert remaining > 0

# Just check image and player were stored correctly
def test_defense_potion_image_and_player_reference(player):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    assert potion.get_player() == player
    assert potion.get_image_name() == "Potion"

# Check get_armor() gives us back the right object
def test_defense_potion_get_armor(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    assert potion.get_armor() == base_armor

# After calling set_fields, the image and type should be copied from armor
def test_defense_potion_set_fields_updates_image_and_type(player, base_armor):
    potion = Defense_potion(multiplier=2, player=player, image_name="temp")
    potion.set_armor(base_armor)
    potion.set_fields()
    assert potion.get_image_name() == base_armor.get_image_name()
    assert potion.get_defense_type() == base_armor.get_defense_type()


# Attack Potion Tests

# Multiply the attack value and check it's what we expect
def test_attack_potion_attack_is_multiplied(player, base_armor):
    potion = Attack_potion(multiplier=3, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    assert potion.get_attack_value() == base_armor.get_attack_value() * 3

# Deal damage and check reduction
def test_attack_potion_damage_reduction(player, base_armor):
    potion = Attack_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    potion.decrease_defense(4)
    assert potion.get_defense_value() == base_armor.get_defense_value() - 4

# More damage than defense, check remaining damage is returned
def test_attack_potion_overkill_returns_remaining_damage(player, base_armor):
    potion = Attack_potion(multiplier=1, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    potion.set_fields()
    remaining = potion.decrease_defense(99)
    assert potion.get_defense_value() == 0
    assert remaining > 0

# Make sure player and image name are stored properly
def test_attack_potion_image_and_player_reference(player):
    potion = Attack_potion(multiplier=2, player=player, image_name="Potion")
    assert potion.get_player() == player
    assert potion.get_image_name() == "Potion"

# Ensure potion gives back the correct armor it’s modifying
def test_attack_potion_get_armor(player, base_armor):
    potion = Attack_potion(multiplier=2, player=player, image_name="Potion")
    potion.set_armor(base_armor)
    assert potion.get_armor() == base_armor

# This should crash if we didn’t set armor before calling get_attack_value
def test_attack_potion_get_attack_raises_if_no_armor(player):
    potion = Attack_potion(multiplier=2, player=player, image_name="Potion")
    with pytest.raises(AttributeError):
        potion.get_attack_value()