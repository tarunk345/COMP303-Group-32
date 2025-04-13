import pytest
from ..Defense import Helmet, Boots, Chest_Plate, Armor, maze_player, Defense_type, Armor_Set

#Will use this for all of them
#Just sets up the player so I can attach armor
@pytest.fixture
def setup():
    player = maze_player(defense=50, attack_value=10)
    return player

# Check that the armor returns the correct attack value
def test_get_attack_value(setup):
    player = setup
    armor = Helmet(20, 7, player, "helmet")
    assert armor.get_attack_value() == 7

# Make sure the defense type of Helmet is set correctly
def test_get_defense_type_helmet(setup):
    player = setup
    helmet = Helmet(10, 3, player, "helmet")
    assert helmet.get_defense_type() == Defense_type.HELMET

# Confirm the armor holds a correct reference to the player
def test_get_player(setup):
    player = setup
    armor = Helmet(10, 0, player, "helmet")
    assert armor.get_player() == player

# Checking that copying a helmet works
def test_copy_helmet(setup):
    player = setup
    helmet = Helmet(12, 4, player, "helmet")
    helmet_copy = helmet.copy()
    assert isinstance(helmet_copy, Helmet)
    assert helmet_copy.get_defense_value() == 12
    assert helmet_copy.get_attack_value() == 4
    assert helmet_copy.get_player() == player
    assert helmet_copy.get_image_name() == "helmet"

# Test inheritance and value access for Chest_Plate
def test_chest_plate_inheritance(setup):
    player = setup
    chest = Chest_Plate(25, 6, player, "chest")
    assert isinstance(chest, Armor)
    assert str(chest) == "chest"
    assert chest.get_defense_value() == 25
    assert chest.get_attack_value() == 6

# Test inheritance and values for Boots
def test_boots_inheritance(setup):
    player = setup
    boots = Boots(8, 2, player, "boots")
    assert isinstance(boots, Armor)
    assert str(boots) == "boots"
    assert boots.get_defense_value() == 8
    assert boots.get_attack_value() == 2

# Simulate partial damage to armor and confirm defense drops correctly
def test_decrease_defense_partial(setup):
    player = setup
    armor = Helmet(15, 2, player, "helmet")
    leftover = armor.decrease_defense(5)
    assert leftover == 0
    assert armor.get_defense_value() == 10

# Apply more damage than the armor has and check leftover value
def test_decrease_defense_overkill(setup):
    player = setup
    armor = Helmet(10, 2, player, "helmet")
    leftover = armor.decrease_defense(15)
    assert leftover == 5
    assert armor.get_defense_value() == 0

# Confirm copy works properly for Chest_Plate
def test_copy_chest_plate(setup):
    player = setup
    chest = Chest_Plate(18, 5, player, "chest")
    chest_copy = chest.copy()
    assert isinstance(chest_copy, Chest_Plate)
    assert chest_copy.get_defense_value() == 18
    assert chest_copy.get_attack_value() == 5
    assert chest_copy.get_player() == player
    assert chest_copy.get_image_name() == "chest"

# Make sure Chest_Plate correctly reports its defense type
def test_get_defense_type_chest(setup):
    player = setup
    chest = Chest_Plate(20, 5, player, "chest")
    assert chest.get_defense_type() == Defense_type.CHEST_PLATE

# Checking that opy works for Boots
def test_copy_boots(setup):
    player = setup
    boots = Boots(10, 1, player, "boots")
    boots_copy = boots.copy()
    assert isinstance(boots_copy, Boots)
    assert boots_copy.get_defense_value() == 10
    assert boots_copy.get_attack_value() == 1
    assert boots_copy.get_image_name() == "boots"

# Check that exact damage reduces armor defense to zero with no leftover
def test_decrease_defense_exact(setup):
    player = setup
    armor = Helmet(8, 2, player, "helmet")
    leftover = armor.decrease_defense(8)
    assert leftover == 0
    assert armor.get_defense_value() == 0

# Add multiple armors and confirm total attack value is calculated
def test_attack_value_total(setup):
    player, maze = setup
    from COMP303_Group_32.Defense import Helmet, Boots
    armor_set = Armor_Set()
    helmet = Helmet(5, 2, player, "helmet")  # 2 attack
    boots = Boots(3, 1, player, "boots")     # 1 attack
    armor_set.add_armor(helmet)
    armor_set.add_armor(boots)
    assert armor_set.get_attack_value() == 3

# Test successful potion addition when armor exists
def test_add_potion_success(setup):
    player, maze = setup
    from COMP303_Group_32.Defense import Helmet, Attack_potion
    armor_set = Armor_Set()
    helmet = Helmet(10, 2, player, "helmet")
    potion = Attack_potion(2, player, "atk_potion")
    armor_set.add_armor(helmet)
    result = armor_set.add_potion(potion)
    assert result is None  # Potion was applied
    assert armor_set.get_attack_value() > 2  # Attack is boosted

# Checking that you cant add a potion when there is no armor
def test_add_potion_fails_if_no_armor(setup):
    player, maze = setup
    from COMP303_Group_32.Defense import Defense_potion
    armor_set = Armor_Set()
    potion = Defense_potion(2, player, "def_potion")
    result = armor_set.add_potion(potion)
    assert result == potion  # Potion was not applied

# Confirm that stronger armor replaces weaker armor
def test_add_armor_replaces_weaker(setup):
    player = setup
    armor_set = Armor_Set()
    weak_helmet = Helmet(5, 1, player, "helmet")
    strong_helmet = Helmet(10, 3, player, "helmet")
    armor_set.add_armor(weak_helmet)
    replaced = armor_set.add_armor(strong_helmet)
    assert replaced == weak_helmet
    assert armor_set.get_defense_value() == 10
    assert armor_set.get_attack_value() == 3