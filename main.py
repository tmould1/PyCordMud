"""
This file is the entry point for attaching the discordbot to the discord server.
It requires an access token to be stored in the os environment variable DISCORD_TOKEN.
If you don't have this token yet, local_run.py is an entry point for local testing.
The main things being done here are:
- Setting up the discord bot.
- Registering event handlers to tie discord commands to python game functions
  through the DiscordBot object. 
- Event handlers verify discord data before passing to game.DiscordBot.

Main Flow:
1) Setup the discord game bot with the token and activity.
2) Register event handlers for the bot.
3) Run the bot with the token.
"""

import os
import random

from discord.ext import commands
import discord.utils

import discord_interface_game

TOKEN = os.getenv('DISCORD_TOKEN') # This token comes from the Discord Developer Portal
GUILD = "test"
GAME_CHANNEL = "game"

#######################################################
### 1) Discord Bot Setup and Initialization Below  ####
#######################################################

activity = discord.Game(name="PyCordMud, !help")
game_bot = discord_interface_game.DiscordBot(
    activity=activity,
    intents=discord.Intents.all(),
    command_prefix='!'
)

#######################################################
### 2) Event Handlers and Command Definitions Below ###
#######################################################
@game_bot.event
async def on_ready():
    """ Event handler for when the bot is ready. """
    proper_guild = discord.utils.get(game_bot.guilds, name=GUILD)

    print(
        f'{game_bot.user} has connected to Discord!\n'
        f'{proper_guild.name}(id: {proper_guild.id})'
    )

    members = '\n - '.join([member.name for member in proper_guild.members])
    print(f'Guild Members:\n - {members}')

@game_bot.event
async def on_member_join(member):
    """ Event handler for when a member joins the server. """
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! 💯💯💯'
    )

@game_bot.command(name='playgame', help='Starts a game in the game channel')
async def playgame(context):
    """ Command to start a game in the game channel. """
    print(f'Received playgame command from {context.author.name} in channel {context.channel.name}')
    is_game_channel = context.channel == discord.utils.get(game_bot.get_all_channels(), name=GAME_CHANNEL)
    is_dm_channel = isinstance(context.channel, discord.DMChannel)
    if not is_game_channel and not is_dm_channel:
        # Send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, please use the {GAME_CHANNEL} channel '
            f'to "!playgame".'
        )
        return

    await context.send("Adding you to the game... 🎮")

    if game_bot.game.is_playing(context.author.name) is False:
        game_bot.joingame(context)

    connected_players = [player.name for player in game_bot.game.players]
    connected_players_string = (
        f' Players Online ({len(connected_players)}):\n '
        f'{"\n".join(connected_players)}'
    )
    await context.send(connected_players_string)

    member = game_bot.get_player_discord_member(context.author.name)
    first_messages = [
        "Welcome to the game! 🎮", "Let's play!",
        "Here's the map:", 
        game_bot.show_player_surroundings(context)
    ]
    await member.send('\n'.join(first_messages))

@game_bot.command(name='rolldice', help='Rolls some dice')
async def roll_dice(context, number_of_dice: int, number_of_sides: int):
    """ Command to roll some dice. """
    dice = (
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    )
    await context.send(', '.join(dice))
    await context.send(f'Total: {sum(int(die) for die in dice)}')

@game_bot.command(name='createchannel', help='Creates a new channel')
@commands.has_role('admin')
async def create_channel(context, channel_name):
    """ Command to create a new channel. """
    guild = context.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await context.send(f'Channel {channel_name} created')
    else:
        await context.send(f'Channel {channel_name} already exists')

@game_bot.event
async def on_command_error(context, error):
    """ Event handler for when a command error occurs. """
    if isinstance(error, commands.errors.CheckFailure):
        await context.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await context.send('Please pass in all required arguments.')
    else:
        print(f'An error occurred: {error}')

@game_bot.command(name='move', help='Move your player on the map')
async def move(context, direction : str):
    """ Command to move the player on the map. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    member = game_bot.get_player_discord_member(context.author.name)
    move_msg = game_bot.move_player(context, direction)
    await member.send(move_msg)
    await member.send(game_bot.show_player_surroundings(context))

@game_bot.command(name='showmap', help='Show the map')
async def show_map(context):
    """ Command to show the map. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send(game_bot.show_player_surroundings(context))

@game_bot.command(name='attack', help='Attack an enemy')
async def attack(context, target_name):
    """ Command to attack an enemy. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    attack_msg = game_bot.attack_enemy(context, target_name)
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send(attack_msg)

@game_bot.command(name='stats', help='Show player stats')
async def stats(context):
    """ Command to show player stats. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    stats_msg = game_bot.show_player_stats(context)
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send(stats_msg)

@game_bot.command(name='take', help='Take an item')
async def take(context, item_name):
    """ Command to take an item from a location. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    take_msg = game_bot.take_item(context, item_name)
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send(take_msg)

@game_bot.command(name='use', help='Use a consumable from your inventory')
async def use(context, consumable_name):
    """ Command to use a consumable from the player's inventory. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    use_msg = game_bot.use_consumable(context, consumable_name)
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send(use_msg)
    
@game_bot.command(name='testcheats', help='Test cheats')
async def test_cheats(context):
    """ Command to test cheats. """
    wrong_channel_msg = 'You must use DMs for this command.'
    if not isinstance(context.channel, discord.DMChannel):
        # send the user a DM directing them to the game channel
        await context.author.create_dm()
        await context.author.dm_channel.send(
            f'Hi {context.author.name}, {wrong_channel_msg}'
        )
        return
    member = game_bot.get_player_discord_member(context.author.name)
    await member.send("Testing cheats...")
    game_bot.game.test_cheats(context.author.name, context.message.content)
    await member.send(game_bot.show_player_surroundings(context))

#######################################################
### 3) Run the Bot with the Token Below            ####
#######################################################

game_bot.run(TOKEN)
