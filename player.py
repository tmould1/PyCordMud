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
        super().__init__(game, name, '💩💩💩', 3, 1)
        self.icon = '🧙‍♂️'
        self.position = (2, 2)

    def move(self, direction):
        """
        Move the player in the specified direction.
        """
        direction = direction.lower()
        move_msg = f'You move {direction}'

        initial_position = self.position
        if direction == 'north':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'south':
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == 'west':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'east':
            self.position = (self.position[0], self.position[1] + 1)

        # bounds check on map size
        x_min, y_min = 0, 0
        x_max, y_max = self.game.map_size

        if (
            self.position[0] < x_min or
            self.position[0] >= x_max or
            self.position[1] < y_min or
            self.position[1] >= y_max
        ):
            move_msg = f'You cannot move {direction}'
            self.position = initial_position

        return move_msg

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
            f'Attack: {self.base_attack}',
        ]
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
