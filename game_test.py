"""
This module contains the game testing logic.
"""

import game
import gear
import consumables

def test_game_init_has_world():
    """
    Test case for initializing the game with a world.
    """
    # Arrange
    test_game = game.MudGame("Test Game")

    # Act
    test_game.create_map((1,1))

    # Assert
    assert test_game.get_map() is not None

def test_game_init_has_enemies():
    """
    Test case for initializing the game with enemies.
    """
    # Arrange
    test_game = game.MudGame("Test Game")

    # Act
    test_game.create_map()

    # Assert
    assert len(test_game.enemy_mgr.enemies) > 0

def test_game_add_player_increases_player_count():
    """
    Test case for adding a player to the game.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"

    # Act
    test_game.add_player(tester_name)

    # Assert
    assert test_game.is_playing(tester_name) is True

def test_game_move_player_has_moved():
    """
    Test case for moving the player.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"
    test_game.add_player(tester_name)

    # Act
    result = test_game.move_player(tester_name, "north")

    # Assert
    assert result is not None

def test_show_player_surroundings_has_contents():
    """
    Test case for showing the player surroundings with contents.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"
    test_player = test_game.add_player(tester_name)

    # Act
    result = test_game.show_player_surroundings(test_player.name)

    # Assert
    assert result is not None

#################################################
### Players, Enemies, Combat, And Consumables ###
#################################################

def test_player_gets_health_potion_on_duplicate_gear_acquisition():
    """
    Test if the player gets a health potion on duplicate gear acquisition.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"
    test_player = test_game.add_player(tester_name)
    test_gear = gear.Gear('Test Gear', 'A test piece of gear')
    cloned_test_gear = gear.Gear('Test Gear', 'A test piece of gear')
    test_health_potion = consumables.HealthPotion("Health Potion", "A potion that restores health.", 10)
    initial_consumables = len(test_player.consumables)

    # Act
    test_player.acquire_gear(test_gear)
    test_player.acquire_gear(cloned_test_gear)

    # Assert
    assert len(test_player.consumables) == initial_consumables + 1
    assert test_player.consumables[-1].name == test_health_potion.name
    
def test_game_get_player_by_name_returns_player():
    """
    Test if the game gets the player by name.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"
    test_player = test_game.add_player(tester_name)

    # Act
    result = test_game.get_player_by_name(tester_name)

    # Assert
    assert result is test_player

def test_game_player_use_potion_restores_health():
    """
    Test if the player's health is restored when using a health potion.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    tester_name = "Tester"
    test_player = test_game.add_player(tester_name)
    test_health_potion = consumables.HealthPotion("Health Potion", "A restorative potion.", 2)
    print(test_player.acquire_consumable(test_health_potion))

    # Act
    test_player.receive_damage(2)
    initial_health = test_player.health
    print(f'Test player consumables: {test_player.consumables}')
    print(test_game.use_consumable(tester_name, test_health_potion.name))

    # Assert
    assert test_player.health == initial_health + test_health_potion.health_points

def test_game_create_map_10_by_10_map():
    """
    Test if the game creates a 10x10 map.
    """
    # Arrange
    test_game = game.MudGame("Test Game")

    # Act
    test_game.create_map((10, 10))

    # Assert
    assert len(test_game.map.map_location_data) == 10
    assert len(test_game.map.map_location_data[0]) == 10

def test_enemy_can_move():
    """
    Test if the enemy can move.
    """
    # Arrange
    test_game = game.MudGame("Test Game")
    test_game.create_map((10, 10))
    coordinates = (5, 5)
    location = test_game.map.map_location_data[coordinates[0]][coordinates[1]]
    test_game.enemy_mgr.create_basic_goblin(location)

    # Act
    test_game.enemy_mgr.enemies[0].move('north')

    # Assert
    assert test_game.enemy_mgr.enemies[0].location != location