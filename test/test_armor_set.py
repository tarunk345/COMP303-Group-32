import pytest
from ..Defense import Armor_Set, Chest_Plate, Helmet, Boots, maze_player

# Doing this so there is an armor_set and a player each time
@pytest.fixture
def setup_armor_set():
    player = maze_player(defense=50, attack_value=10)
    armor_set = Armor_Set()
    return armor_set, player

# Test that adding multiple armors totals defense and attack correctly
def test_add_armor_and_total_values(setup_armor_set):
    armor_set, player = setup_armor_set
    helmet = Helmet(10, 2, player, "helmet")
    boots = Boots(5, 1, player, "boots")
    armor_set.add_armor(helmet)
    armor_set.add_armor(boots)
    assert armor_set.get_defense_value() == 15
    assert armor_set.get_attack_value() == 3

# If a new armor of the same type has higher stats, it should replace the old one
def test_add_same_type_armor_higher_stats_replaces(setup_armor_set):
    armor_set, player = setup_armor_set
    weak_helmet = Helmet(5, 1, player, "helmet")
    strong_helmet = Helmet(10, 2, player, "helmet")
    armor_set.add_armor(weak_helmet)
    replaced = armor_set.add_armor(strong_helmet)
    assert isinstance(replaced, Helmet)
    assert replaced.get_defense_value() == 5
    assert armor_set.get_defense_value() == 10

# If the new armor is weaker than the current one, it should not replace it
def test_add_same_type_armor_lower_stats_keeps_old(setup_armor_set):
    armor_set, player = setup_armor_set
    strong_helmet = Helmet(10, 2, player, "helmet")
    weak_helmet = Helmet(5, 1, player, "helmet")
    armor_set.add_armor(strong_helmet)
    result = armor_set.add_armor(weak_helmet)
    assert result == weak_helmet  # Rejected
    assert armor_set.get_defense_value() == 10

# Apply some damage and then check how it's distributed across armor
def test_decrease_defense(setup_armor_set):
    armor_set, player = setup_armor_set
    helmet = Helmet(10, 0, player, "helmet")
    boots = Boots(5, 0, player, "boots")
    armor_set.add_armor(helmet)
    armor_set.add_armor(boots)
    leftover = armor_set.decrease_defense(12)
    assert leftover == 0
    assert armor_set.get_defense_value() == 3

# More damage then there is defense and check
def test_decrease_defense_overkill(setup_armor_set):
    armor_set, player = setup_armor_set
    chest = Chest_Plate(5, 1, player, "chest")
    armor_set.add_armor(chest)
    leftover = armor_set.decrease_defense(10)
    assert leftover == 5
    assert armor_set.get_defense_value() == 0

# If armor exists, a potion should be applied and increase stats
def test_add_potion_success(setup_armor_set):
    from COMP303_Group_32.Defense import Attack_potion
    armor_set, player = setup_armor_set
    helmet = Helmet(10, 3, player, "helmet")
    potion = Attack_potion(2, player, "atk_potion")
    armor_set.add_armor(helmet)
    result = armor_set.add_potion(potion)
    assert result is None  # Potion applied
    assert armor_set.get_attack_value() > 3  # Attack value increased

# If no armor exists, the potion should not be applied
def test_add_potion_no_armor_fails(setup_armor_set):
    from COMP303_Group_32.Defense import Defense_potion
    armor_set, player = setup_armor_set
    potion = Defense_potion(2, player, "def_potion")
    result = armor_set.add_potion(potion)
    assert result == potion  # Rejected


# Checking that none is returned when a new piece of armor is added
def test_add_armor_returns_none_when_added(setup_armor_set):
    armor_set, player = setup_armor_set
    helmet = Helmet(10, 3, player, "helmet")
    result = armor_set.add_armor(helmet)
    assert result is None  # Indicates successful addition

# Check that the potion correctly multiplies the attack value
def test_attack_value_with_potion_multiplier(setup_armor_set):
    from COMP303_Group_32.Defense import Attack_potion
    armor_set, player = setup_armor_set
    helmet = Helmet(10, 4, player, "helmet")
    potion = Attack_potion(2, player, "atk_potion")
    armor_set.add_armor(helmet)
    armor_set.add_potion(potion)
    expected_attack = 4 * 2
    assert armor_set.get_attack_value() == expected_attack
