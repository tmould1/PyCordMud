"""
This module contains the player testing logic.
"""
import game
import gear
import consumables

################################
### Player testing section #####
################################

def test_player_init_has_name():
    """
    Test case for initializing the player with a name.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"

    # Act
    test_player = game.PlayerCharacter(tester_name, test_game)

    # Assert
    assert test_player.name == tester_name

def test_player_show_surroundings_center_of_world():
    """
    Test case for showing the player surroundings at the center of the world.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_game.add_player(test_player)

    # Act
    result = test_player.show_surroundings()

    # Assert
    assert result is not None

#######################################
### Player and Gear testing section ###
#######################################
def test_player_has_no_gear():
    """
    Test case for checking if the player has no gear.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)

    # Act
    gear_count = len(test_player.gear)

    # Assert
    assert gear_count == 0
    
def test_player_add_gear_has_one_gear():
    """
    Test case for adding gear to the player and checking if it has one gear.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_gear = gear.Gear("Test Gear", "A test gear item")

    # Act
    test_player.acquire_gear(test_gear)
    gear_count = len(test_player.gear)

    # Assert
    assert gear_count == 1

def test_player_remove_gear_has_no_gear():
    """
    Test case for removing gear from the player and checking if it has no gear.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_gear = gear.Gear("Test Gear", "A test gear item")
    test_player.acquire_gear(test_gear)

    # Act
    test_player.relinquish_gear(test_gear.name)
    gear_count = len(test_player.gear)

    # Assert
    assert gear_count == 0

def test_player_adding_gear_with_stats_increases_player_stats():
    """
    Test case for adding gear with stats to the player and checking if the player stats increase.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_gear = gear.Gear("Test Gear", "A test gear item")
    test_gear.offense = 5
    test_gear.defense = 5
    base_attack = test_player.base_attack
    max_health = test_player.max_health

    # Act
    test_player.acquire_gear(test_gear)

    # Assert
    assert test_player.get_attack_damage() == base_attack + test_gear.offense
    assert test_player.max_health == max_health + test_gear.defense

def test_player_removing_gear_with_stats_decreases_player_stats():
    """
    Test case for removing gear with stats from the player 
      and checking if the player stats decrease.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_gear = gear.Gear("Test Gear", "A test gear item")
    test_gear.offense = 5
    test_gear.defense = 5
    test_player.acquire_gear(test_gear)
    base_attack = test_player.get_attack_damage()
    max_health = test_player.max_health

    # Act
    test_player.relinquish_gear(test_gear.name)

    # Assert
    assert test_player.get_attack_damage() == base_attack - test_gear.offense
    assert test_player.max_health == max_health - test_gear.defense


#############################################
### Player and Consumable testing section ###
#############################################
def test_player_has_no_consumables():
    """
    Test case for checking if the player has no consumables.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)

    # Act
    consumable_count = len(test_player.consumables)

    # Assert
    assert consumable_count == 0

def test_player_add_consumable_has_one_consumable():
    """
    Test case for adding a consumable to the player and checking if it has one consumable.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_consumable = consumables.Consumable("Test Consumable", "A test consumable item")

    # Act
    test_player.acquire_consumable(test_consumable)
    consumable_count = len(test_player.consumables)

    # Assert
    assert consumable_count == 1

def test_player_use_consumable_has_no_consumables():
    """
    Test case for using a consumable and checking if the player has no consumables left.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_consumable = consumables.Consumable("Test Consumable", "A test consumable item")
    test_player.acquire_consumable(test_consumable)

    # Act
    test_player.use_consumable(test_consumable.name)
    consumable_count = len(test_player.consumables)

    # Assert
    assert consumable_count == 0

def test_player_use_health_potion_restores_missing_health():
    """
    Test case for using a health potion and checking if the player's health is restored.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_consumable = consumables.HealthPotion("Health Potion", "A potion that restores health", 50)
    test_player.health = 50
    test_player.max_health = 100

    # Act
    test_player.acquire_consumable(test_consumable)
    test_player.use_consumable(test_consumable.name)

    # Assert
    assert test_player.health == test_player.max_health

def test_player_use_health_potion_does_not_exceed_max_health():
    """
    Test case for using a health potion and checking if the player's health does not exceed the max health.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_consumable = consumables.HealthPotion("Health Potion", "A potion that restores health", 50)
    test_player.health = 75
    test_player.max_health = 100

    # Act
    test_player.acquire_consumable(test_consumable)
    test_player.use_consumable(test_consumable.name)

    # Assert
    assert test_player.health == test_player.max_health
