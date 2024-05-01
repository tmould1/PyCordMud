"""
This module contains the local running logic for the game.
"""
import game

def main():
    """
    Main function for running the game.
    """
    game_instance = game.DiscordGame("Test Game")
    player = game.PlayerInfo("Tester", game_instance)
    game_instance.add_player(player)
    print(game_instance.get_map())
    game_instance.attack_enemy("Tester", "Goblin")
    game_instance.take_item("Tester", "Rusty Gobbo Dagger")
    game_instance.show_player_stats("Tester")
    
if __name__ == '__main__':
    main()

