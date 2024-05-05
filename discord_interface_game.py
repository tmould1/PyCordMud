"""
This module contains the DiscordBot class for handling the Discord bot functionality.
"""

from discord.ext import commands

import game

# Handles Context extraction
class DiscordBot(commands.Bot):
    """
    DiscordBot class for handling the Discord bot functionality.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game.DiscordGame("JoPy")

    def get_player_discord_member(self, player_name):
        """
        Get the Discord member for the player with the given name.
        """
        member = None

        for guild in self.guilds:
            member = guild.get_member_named(player_name)
            if member:
                break

        return member

    def joingame(self, context : commands.Context):
        """
        Join the game with the given context.
        """
        joining_player = context.author.name
        self.game.add_player(joining_player)

    def show_player_surroundings(self, context : commands.Context):
        """
        Show the surroundings of the player with the given context.
        """
        return self.game.show_player_surroundings(context.author.name)

    def move_player(self, context : commands.Context, direction):
        """
        Move the player with the given context in the specified direction.
        """
        return self.game.move_player(context.author.name, direction)

    def attack_enemy(self, context : commands.Context, target_name):
        """
        Attack the enemy with the given context and target name.
        """
        return self.game.attack_enemy(context.author.name, target_name)

    def show_player_stats(self, context : commands.Context):
        """
        Show the stats of the player with the given context.
        """
        player_name = context.author.name
        return self.game.show_player_stats(player_name)

    def show_player_inventory(self, context : commands.Context):
        """
        Show the inventory of the player with the given context.
        """
        player_name = context.author.name
        return self.game.show_player_inventory(player_name)

    def take_item(self, context : commands.Context, item_name):
        """
        Take the item with the given name using the player with the given context.
        """
        player_name = context.author.name
        return self.game.take_item(player_name, item_name)

    def use_consumable(self, context : commands.Context, consumable_name):
        """
        Use the consumable with the given name using the player with the given context.
        """
        player_name = context.author.name
        return self.game.use_consumable(player_name, consumable_name)

    def test_cheats(self, context : commands.Context):
        """
        Test cheats for the player with the given context.
        """
        player_name = context.author.name
    
        testers = [ "blacklabel" ]
        if player_name not in testers:
            return "You are not authorized to use this command."

        return self.game.test_cheats(player_name, context.message.content)

