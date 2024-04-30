import math

from location import LocationContent
from gear import Gear

class PlayerInfo(LocationContent):
    def __init__(self, name, game):
        self.icon = '🧙‍♂️'
        self.name = name
        self.position = (2, 2)
        self.game = game
        self.description = '💩💩💩'
        
        self.max_health = 3
        self.base_attack = 1
        self.gear = []

        self.health = self.max_health
    
    def move(self, direction):
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
        
        if self.position[0] < x_min or self.position[0] >= x_max or self.position[1] < y_min or self.position[1] >= y_max:
            move_msg = f'You cannot move {direction}'
            self.position = initial_position
        
        return move_msg
    
    def show_surroundings(self):
        grid_display_size = (5, 5)
        x, y = self.position
        surroundings = ''
        lower_x = x - math.floor((grid_display_size[0])/2)
        upper_x = x + math.ceil((grid_display_size[0])/2)
        lower_y = y - math.floor((grid_display_size[1])/2)
        upper_y = y + math.ceil((grid_display_size[1])/2)
        for i in range(lower_x, upper_x):
            for j in range(lower_y, upper_y):
                if i < 0 or i >= self.game.map_size[0] or j < 0 or j >= self.game.map_size[1]:
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
    
    def attack(self, target_name):
        #print(f'Player {self.name} attacking {target_name}')
        target_name = target_name.lower()
        attack_msg = ''
        # is the target in our location? if so, attack it
        location = self.game.map.map_location_data[self.position[0]][self.position[1]]
        enemy = None
        for content in location.contents:
            if target_name in content.name.lower():
                enemy = content
                break
        if enemy is None:
            return f'No enemy named {target_name} found here'
        
        if len(self.gear) <= 0:
            attack_msg += f'You attack {enemy.name} with your bare hands! 💪\n'
        attack_msg += enemy.receive_damage(self, self.get_attack_damage())
        
        # is enemy dead?
        if enemy.health <= 0:
            location.remove_content(enemy)
            self.game.update_shown_map()
            
        return attack_msg
    
    def get_attack_damage(self):
        return self.base_attack
    
    def acquire_gear(self, new_gear : Gear):
        acquire_msg = f'You pick up {new_gear.name}.\n'
        # if we already have the gear, heal the player
        heal_amount = 2
        for gear_piece in self.gear:
            if gear_piece.name == new_gear.name:
                self.health += heal_amount
                if self.health > self.max_health:
                    self.health = self.max_health
                acquire_msg += f'{new_gear.name} glows brightly then disappears in a flash, healing you for ⛑️ {heal_amount} health\n'
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
    
    def receive_damage(self, damage : int):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return self.game.handle_player_death(self)
        return f'🫵 {self.name} takes {damage} damage! 💥\n'
  
    def get_player_stats_string(self):
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
        return stat_msg