"""
This module contains the player logic.
"""
import math

from character import Character
from gear import Gear
from consumables import HealthPotion

class PlayerCharacter(Character):
    """
    Represents information about a player.
    """
    def __init__(self, name, game):
        self.defaults = {
            'health': 3,
            'attack_power': 1
        }
        super().__init__(game, name, '💩💩💩', health = self.defaults['health'], attack_power=self.defaults['attack_power'])
        self.icon = '🧙‍♂️'
        center_of_map = (math.floor(game.map_size[0] / 2), math.floor(game.map_size[1] / 2))
        self.position = center_of_map
        self.game = game
    
    def reset_player(self):
        """
        Reset the player to the initial state.
        """
        self.health = self.defaults['health']
        self.base_attack = self.defaults['attack_power']
        self.position = (math.floor(self.game.map_size[0] / 2), math.floor(self.game.map_size[1] / 2))
        self.gear = []
        self.consumables = []
        self.description = '💩💩💩'

    def show_surroundings(self):
        """
        Show the surroundings of the player.
        """
        grid_display_size = (5, 5)
        x, y = self.position
        surroundings = ''
        lower_x = x - math.floor((grid_display_size[0])/2)
        upper_x = x + math.ceil((grid_display_size[0])/2)
        lower_y = y - math.floor((grid_display_size[1])/2)
        upper_y = y + math.ceil((grid_display_size[1])/2)
        for i in range(lower_x, upper_x):
            for j in range(lower_y, upper_y):
                if (
                    i < 0 or
                    i >= self.game.map_size[0] or
                    j < 0 or
                    j >= self.game.map_size[1]
                ):
                    surroundings += self.game.map.out_of_bounds
                elif i == x and j == y:
                    surroundings += self.icon
                else:
                    surroundings += self.game.map.map_icons[i][j]
            surroundings += '\n'
        location_data = self.game.map.map_location_data[x][y]
        # print the name of the location and then its contents
        surroundings += f'You are at {location_data.name}. {location_data.description}\n'
        surroundings += location_data.build_content_string()
        return surroundings

    def acquire_gear(self, new_gear : Gear):
        """
        Acquire new gear.
        """
        acquire_msg = f'You pick up {new_gear.name}.\n'
        # if we already have the gear, heal the player
        heal_amount = 2
        for gear_piece in self.gear:
            if gear_piece.name == new_gear.name:
                health_potion = HealthPotion('Health Potion', 'Heals 2 health', heal_amount)
                acquire_msg += (
                    f'{new_gear.name} glows brightly then transforms in a flash, '
                    f'in its place is a Health Potion ❤️\n'
                )
                self.acquire_consumable(health_potion)
                return acquire_msg
        self.gear.append(new_gear)
        new_gear.apply_stats(self)
        num_gear = len(self.gear)
        max_gear = 3
        num_poop = max_gear - num_gear
        num_diamonds = num_gear
        description_str = '💎' * num_diamonds + '💩' * num_poop
        self.description = description_str
        return acquire_msg

    def relinquish_gear(self, gear_name):
        """
        Relinquish gear by name.
        """
        relinquish_msg = ''
        gear_to_remove = None
        for gear in self.gear:
            if gear.name.lower() == gear_name.lower():
                gear_to_remove = gear
                break
        if gear_to_remove is None:
            return f'No gear named {gear_name} found in your inventory'
        self.gear.remove(gear_to_remove)
        gear_to_remove.remove_stats(self)
        num_gear = len(self.gear)
        max_gear = 3
        num_poop = max_gear - num_gear
        num_diamonds = num_gear
        description_str = '💎' * num_diamonds + '💩' * num_poop
        self.description = description_str
        relinquish_msg = f'You drop {gear_name}.\n'
        return relinquish_msg

    def get_player_stats_string(self):
        """
        Get the string representation of the player's stats.
        """
        stat_strings = [
            f'Player: {self.name}',
            f'Description: {self.description}',
        ]

        # Build attack string with base attack and gear attack
        attack_string_emojis = '⚔️' * self.get_attack_damage()
        stat_strings.append(f'Attack: {attack_string_emojis}')

        health_string_emojis = '❤️' * self.health + '🩶' * (self.max_health - self.health)
        stat_strings.append(f'Health: {health_string_emojis}')

        gear_str = '[Gear]\n'
        for gear in self.gear:
            gear_str += f'{gear.icon} {gear.name} - {gear.description}\n'
        stat_strings.append(gear_str)
        stat_msg = '\n'.join(stat_strings)

        consumables_str = '[Consumables]\n'
        for consumable in self.consumables:
            consumables_str += f'{consumable.icon} {consumable.name} - {consumable.description}\n'
        stat_msg += consumables_str
        return stat_msg

    def take_item(self, item_name):
        """
        Take an item with the given name using the player.
        """
        take_msg = ''
        location = self.game.map.map_location_data[self.position[0]][self.position[1]]
        item = None
        for content in location.contents:
            if item_name.lower() in content.name.lower():
                item = content
                break
        if item is None:
            return f'No item named {item_name} found here'

        take_msg = self.acquire_gear(item)
        location.remove_content(item)
        self.game.update_shown_map()
        return take_msg

    def get_prompt_status(self):
        """
        Show the status of the player in the prompt.
        """
        health_string_emojis = '❤️' * self.health + '🩶' * (self.max_health - self.health)
        prompt_status = f'{self.icon} {self.name} {health_string_emojis}\n'
        return prompt_status

    def receive_message(self, msg):
        """
        Receives a message.
        """
        super().receive_message(msg)
        self.game.send_message_to_player(self, msg)
        