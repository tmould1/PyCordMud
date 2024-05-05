"""
This module contains the discord/game interface testing logic.
Needs a second client token to connect and create a message to send to the bot
"""
import os
import threading # For running the bot in a separate thread

import discord
from discord.ext import commands

import discord_interface_game

def start_bot_thread(test_game_bot : discord_interface_game.DiscordBot):
    """
    Start the bot in a separate thread.
    """
    discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

    test_game_bot.run(discord_bot_token)

# def test_discordbot_init_has_game():
#     """
#     Test case for initializing the Discord bot with a game.
#     """
#     # Arrange
#     test_bot = discord_interface_game.DiscordBot("Test Bot")

#     # Act
#     game = test_bot.game

#     # Assert
#     assert game is not None

# def test_discordbot_joingame_adds_player():
#     """
#     Test case for joining the game with a player.
#     """
#     # Arrange
#     activity = discord.Game(name="Testing PyCordMud, !help")
#     test_bot = discord_interface_game.DiscordBot(
#         activity=activity,
#         intents=discord.Intents.all(),
#         command_prefix='!'
#     )

#     # Start the bot in a separate thread
#     test_bot_thread = threading.Thread(target=start_bot_thread, args=(test_bot,))
#     test_bot_thread.start()
#     test_bot.wait_until_ready()

#     try :
#         test_context = commands.Context(prefix='!', bot=test_bot, message=None, view=None)
#         test_context.author.name = "Test Player"

#         # Act
#         test_bot.joingame(test_context)

#         # Assert
#         assert test_bot.game.is_playing("Test Player")
#     finally:
#         test_bot.close()
#         test_bot_thread.join()
