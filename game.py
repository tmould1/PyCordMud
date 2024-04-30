from discord.ext import commands

import random

from player import PlayerInfo
from location import Location
from enemy import EnemyManager
from map import Map

# Handles Context extraction
class DiscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = DiscordGame("JoPy")

    def joingame(self, context : commands.Context):
        joining_player = context.author.name
        self.game.add_player(PlayerInfo(joining_player, self.game))
        
    def show_player_surroundings(self, context : commands.Context):
        return self.game.show_player_surroundings(context.author.name)
    
    def move_player(self, context : commands.Context, direction):
        return self.game.move_player(context.author.name, direction)
    
    def attack_enemy(self, context : commands.Context, target_name):
        return self.game.attack_enemy(context.author.name, target_name)
    
    def show_player_stats(self, context : commands.Context):
        player_name = context.author.name
        return self.game.show_player_stats(player_name)
    
    def show_player_inventory(self, context : commands.Context):
        player_name = context.author.name
        return self.game.show_player_inventory(player_name)
    
    def take_item(self, context : commands.Context, item_name):
        player_name = context.author.name
        return self.game.take_item(player_name, item_name)
    
class DiscordGame():
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
        self.map.create_map_location_data(size = self.map_size)
        
    def update_shown_map(self):
        self.map.update_map_icons()

    def get_map(self):
        return self.map.get_map_string()

    def is_playing(self, player : PlayerInfo):
        return player in self.players
            
    def add_player(self, player : PlayerInfo):
        print(f'Adding player {player.name} to the game')
        self.players.append(player)
        
    def move_player(self, player_name, direction):
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        return player.move(direction)

    def build_player_not_found_msg(self, player_name):
        return f'Player {player_name} not found in these players 🤷‍♂️ Have you joined?'
    
    def show_player_surroundings(self, player_name):
        # get the player from the list
        player = None
        for connected_player in self.players:
            #print(f'Checking player {connected_player.name} against {player_name}')
            if connected_player.name == player_name:
                player = connected_player
                break
        if player is None:
            return self.build_player_not_found_msg(player_name)
        return player.show_surroundings()  

    def show_position_contents(self, position):
        x, y = position
        return self.map[x][y]
    
    def attack_enemy(self, player_name, target_name):
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
        self.players.remove(player)
        return f'{player.name} has died! 💀\n'
 
 