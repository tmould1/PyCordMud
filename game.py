"""
This module contains the DiscordBot class and DiscordGame class.
"""

from player import PlayerCharacter
from enemy import EnemyManager
from world import Map
 
class DiscordGame():
    """
    DiscordGame class for handling the game logic.
    """
    def __init__(self, name, size = (5, 5)):
        print(f'Initializing game {name}')
        self.name = name
        self.players = []
        self.map_size = size
        self.map = Map()
        self.create_map()
        self.enemy_mgr = EnemyManager(self)
        self.enemy_mgr.initial_seed()
        self.goblin_kills = 0
        self.orc_kills = 0
        self.troll_kills = 0
        self.dragon_kills = 0
        self.update_shown_map()
        print(f'Game {name} initialized successfully! 🎮')
        
    def create_map(self):
        """
        Create the game map.
        """
        self.map.create_map_location_data(size = self.map_size)
        
    def update_shown_map(self):
        """
        Update the shown map.
        """
        self.map.update_map_icons()

    def get_map(self):
        """
        Get the game map.
        """
        return self.map.get_map_string()

    def is_playing(self, player_name):
        """
        Check if the player is playing the game.
        """
        return player_name in [player.name for player in self.players]
            
    def add_player(self, player_name):
        """
        Add a player to the game.
        """
        if self.is_playing(player_name):
            return f'Player {player_name} is already in the game'
        new_player = PlayerCharacter(player_name, self)
        print(f'Adding player {new_player.name} to the game')
        self.players.append(new_player)
        
    def move_player(self, player_name, direction):
        """
        Move the player with the given name in the specified direction.
        """
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        return player.move(direction)

    def build_player_not_found_msg(self, player_name):
        """
        Build a message for a player not found.
        """
        return f'Player {player_name} not found in these players 🤷‍♂️ Have you joined?'
    
    def show_player_surroundings(self, player_name):
        """
        Show the surroundings of the player with the given name.
        """
        player = None
        for connected_player in self.players:
            if connected_player.name == player_name:
                player = connected_player
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)
        return player.show_surroundings()  
    
    def attack_enemy(self, player_name, target_name):
        """
        Attack the enemy with the given name using the player with the given name.
        """
        attack_msg = ''
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)
        attack_msg = player.attack(target_name)
        return attack_msg
    
    def show_player_stats(self, player_name):
        """
        Show the stats of the player with the given name.
        """
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)

        stat_msg = player.get_player_stats_string()
        return stat_msg

    def show_player_inventory(self, player_name):
        """
        Show the inventory of the player with the given name.
        """
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)
        
        inventory_str = ''
        for gear in player.gear:
            inventory_str += f'{gear.icon} {gear.name} - {gear.description}\n'
        return inventory_str
    
    def take_item(self, player_name, item_name):
        """
        Take an item with the given name using the player with the given name.
        """
        take_msg = ''
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)
        
        location = self.map.map_location_data[player.position[0]][player.position[1]]
        item = None
        for content in location.contents:
            if item_name.lower() in content.name.lower():
                item = content
                break
        if item is None:
            return f'No item named {item_name} found here'
        
        take_msg = player.acquire_gear(item)
        location.remove_content(item)
        self.update_shown_map()

        return take_msg

    def handle_player_death(self, player):
        """
        Handle the death of a player.
        """
        self.players.remove(player)
        return f'{player.name} has died! 💀\n'
    
    def handle_character_death(self, character):
        """
        Handle the death of a character.
        """
        if isinstance(character, PlayerCharacter):
            return self.handle_player_death(character)
        return f'{character.name} has died! 💀\n'