import game
from gear import Gear

def test_Game_Init_HasWorld():
    # Arrange
    test_game = game.DiscordGame("Test Game")
    
    # Act
    test_game.create_map()
    
    # Assert
    assert test_game.get_map() is not None
    
def test_Game_Init_HasEnemies():
    # Arrange
    test_game = game.DiscordGame("Test Game")
    
    # Act
    test_game.create_map()
    
    # Assert
    assert len(test_game.enemy_mgr.enemies) > 0
    
def test_Game_MovePlayer_HasMoved():
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerInfo(tester_name, test_game)
    test_game.add_player(test_player)
    
    # Act
    result = test_game.move_player(tester_name, "north")
    
    # Assert
    assert result is not None
    
def test_ShowPlayerSurroundings_HasContents():
    # Arrange
    test_game = game.DiscordGame("Test Game")
    tester_name = "Tester"
    test_player = game.PlayerInfo(tester_name, test_game)
    test_game.add_player(test_player)
    
    # Act
    result = test_game.show_player_surroundings(tester_name)
    
    # Assert
    assert result is not None
    
def test_ShowPlayerSurroundings_CenterOfWorld():
    # Arrange
    test_game = game.DiscordGame("Test Game", (5, 5))
    tester_name = "Tester"
    test_player = game.PlayerInfo(tester_name, test_game)
    test_player_icon = '🧪'
    test_player.icon = test_player_icon
    test_game.add_player(test_player)
    player_grid = test_player.position
    
    # Act
    result = test_game.show_player_surroundings(tester_name)
    
    player_line = result.split('\n')[player_grid[0]]
    # Assert
    assert test_player_icon in player_line

def test_ShowPlayerSurroundings_DropItemOnFirstLine():
    # Arrange
    test_game = game.DiscordGame("Test Game", (5, 5))
    tester_name = "Tester"
    test_player = game.PlayerInfo(tester_name, test_game)
    test_player_icon = '🧪'
    test_player.icon = test_player_icon
    test_game.add_player(test_player)
    row_index = 1
    test_location = test_game.map.map_location_data[row_index][1]
    test_item = Gear('Test Item', 'A test item')
    test_item.icon = '🧬'
    test_location.add_content(test_item)
    test_game.map.update_map_icons()
    
    # Act
    result = test_game.show_player_surroundings(tester_name)
    
    item_line = result.split('\n')[row_index]
    # Assert
    assert test_item.icon in item_line