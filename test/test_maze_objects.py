import pytest
from ..Defense import maze_player
from ..Maze import Coord
from ..maze_objects import (
    Statue, Wall, Barrel, Column, HotTub,
    SaunaRoom, StatueRoom, WineCellar, Armory, FinalBossRoom,
    ArmorStand, ArrowStand, Target
)
from ..Enemy import Gladiator

# Create a player to use in the tests, to avoid repeated code
@pytest.fixture
def player():
    return maze_player(50, 10)

# Helper to check if any message contains expected text, simplifies the code later on
def message_contains(messages, expected_text, key="text"):
    for msg in messages:
        data = msg._get_data()
        if key in data and expected_text in data[key]:
            return True
    return False



# Maze Object Interaction Tests

# Statue should return a message with its description
def test_statue_interaction_returns_dialogue(player):
    statue = Statue("A cool statue", "statue_img")
    messages = statue.player_interacted(player)
    assert len(messages) == 1
    assert message_contains(messages, "A cool statue", key="dialogue_text")

# Wall should not be passable and have correct image
def test_wall_properties():
    wall = Wall()
    assert wall.is_passable() is False
    assert wall.get_image_name() == "wall5"

# Barrel should also not be passable and use correct image
def test_barrel_properties():
    barrel = Barrel()
    assert barrel.is_passable() is False
    assert barrel.get_image_name() == "barrel"

# Columns should have default z-index and image
def test_column_has_image_and_zindex():
    column = Column()
    assert column.get_image_name() == "column"
    assert column.get_z_index() == 0

# HotTub should be passable and send relaxation message
def test_hottub_entry_returns_message(player):
    tub = HotTub()
    assert tub.is_passable() is True
    messages = tub.player_entered(player)
    assert message_contains(messages, "relaxes your spirits", key="dialogue_text")

# ArmorStand should not be walkable
def test_armor_stand_is_not_passable():
    stand = ArmorStand()
    assert stand.is_passable() is False
    assert stand.get_image_name() == "armorstand"

# Target should exist and not be passable
def test_target_basics():
    target = Target()
    assert target.get_image_name() == "target"
    assert target.is_passable() is False



# Room Content Tests

# Sauna Room should have at least one HotTub and Gladiator
def test_sauna_room_has_objects():
    room = SaunaRoom()
    objects = room.get_objects()

    has_hottub = any(isinstance(obj, HotTub) for obj, _ in objects)
    has_gladiator = any(obj.__class__.__name__ == "Gladiator" for obj, _ in objects)

    assert has_hottub
    assert has_gladiator

# Statue Room should include at least one statue
def test_statue_room_has_statues():
    room = StatueRoom()
    objects = room.get_objects()

    has_statue = any(isinstance(obj, Statue) for obj, _ in objects)
    assert has_statue

# Wine Cellar needs barrels and a potion
def test_wine_cellar_has_barrels_and_potions():
    room = WineCellar()
    objects = room.get_objects()

    barrels = [obj for obj, _ in objects if isinstance(obj, Barrel)]
    has_potion = any("Potion" in obj.__class__.__name__ for obj, _ in objects)

    assert len(barrels) >= 10
    assert has_potion

# Armory must contain both targets and armor stands
def test_armory_has_targets_and_stands():
    room = Armory()
    objects = room.get_objects()

    found_target = any(isinstance(obj, Target) for obj, _ in objects)
    found_stand = any(isinstance(obj, ArmorStand) for obj, _ in objects)

    assert found_target
    assert found_stand

# Final Boss Room needs to have a Minotaur
def test_final_boss_room_has_minotaur():
    room = FinalBossRoom()
    objects = room.get_objects()

    found_minotaur = any(obj.__class__.__name__ == "Minotaur" for obj, _ in objects)
    assert found_minotaur



# Room Entry Dialogue Tests

# Entering Sauna Room should return proper message
def test_sauna_entry_message(player):
    room = SaunaRoom()
    messages = room.player_entered(player)
    assert message_contains(messages, "entered the Sauna")

# Statue Room should identify itself in message
def test_statue_room_entry_message(player):
    room = StatueRoom()
    messages = room.player_entered(player)
    assert message_contains(messages, "Room of Statues")

# Wine Cellar message should say its name
def test_wine_cellar_entry_message(player):
    room = WineCellar()
    messages = room.player_entered(player)
    assert message_contains(messages, "Wine Cellar")

# Armory message currently says Wine Cellar, might be a mistake
def test_armory_entry_message(player):
    room = Armory()
    messages = room.player_entered(player)
    assert message_contains(messages, "Wine Cellar")  # Wine Cellar lol?

# Final Boss Room should give a quiet atmosphere message
def test_final_boss_room_entry_message(player):
    room = FinalBossRoom()
    messages = room.player_entered(player)
    assert message_contains(messages, "air is still")
