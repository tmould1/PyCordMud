"""
This module contains the game testing logic.
"""

import game

def test_game_init_has_world():
    """
    Test case for initializing the game with a world.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")

    # Act
    test_game.create_map()

    # Assert
    assert test_game.get_map() is not None

def test_game_init_has_enemies():
    """
    Test case for initializing the game with enemies.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")

    # Act
    test_game.create_map()

    # Assert
    assert len(test_game.enemy_mgr.enemies) > 0

def test_game_add_player_increases_player_count():
    """
    Test case for adding a player to the game.
    """
    # Arrange
    test_game = game.DiscordGame("Test Game")
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
    test_game = game.DiscordGame("Test Game")
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
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerCharacter(tester_name, test_game)
    test_game.add_player(test_player)

    # Act
    result = test_game.show_player_surroundings(tester_name)

    # Assert
    assert result is not None
