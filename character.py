"""
This module contains the character logic for the game.
Characters are the entities that interact with the game world.
Players and Enemies are both characters.
"""

from location import LocationContent

class Character(LocationContent):
    """
    A class to represent a character in the game.

    Attributes:
        name (str): The name of the character.
        description (str): The description of the character.
        icon (str): The icon of the character.
        health (int): The health points of the character.
        attack_power (int): The attack power of the character.
    """

    def __init__(self, game, name, description, health, attack_power):
        """
        Constructs the necessary attributes for the character object.

        Args:
            name (str): The name of the character.
            description (str): The description of the character.
            health (int): The health points of the character.
            attack_power (int): The attack power of the character.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.icon = '👤'
        self.game = game
        self.max_health = health
        self.health = health
        self.base_attack = attack_power

        self.gear = []
        self.consumables = []
        
        self.status_effects = []
        
        ## To be phased out:
        self.position = (0, 0)

    def attack(self, target_name):
        """
        Attack the specified target.
        """
        target_name = target_name.lower()
        attack_msg = ''
        # is the target in our location? if so, attack it
        location = self.game.map.map_location_data[self.position[0]][self.position[1]]
        target_of_attack = None
        for content in location.contents:
            if target_name in content.name.lower():
                target_of_attack = content
                break
        if target_of_attack is None:
            return f'No enemy named {target_name} found here'

        if len(self.gear) <= 0:
            attack_msg += f'You attack {target_of_attack.name} with your bare hands! 💪\n'
        attack_msg += target_of_attack.receive_damage(self, self.get_attack_damage())

        # is enemy dead?
        if target_of_attack.health <= 0:
            location.remove_content(target_of_attack)
            self.game.update_shown_map()

        return attack_msg

    def get_attack_damage(self):
        """
        Get the attack damage of the player.
        """
        base_attack = self.base_attack
        gear_attack = sum([gear.offense for gear in self.gear])
        
        total_attack = base_attack + gear_attack
        return total_attack

    def is_alive(self):
        """
        Checks if the character is alive.

        Returns:
            bool: True if the character is alive, False otherwise.
        """
        return self.health > 0
    
    def receive_damage(self, damage):
        """
        Receive damage from a source by an amount.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return self.game.handle_character_death(self)
        return f'🫵 {self.name} takes {damage} damage! 💥\n'

    def acquire_consumable(self, consumable):
        """
        Acquire a consumable.
        """
        self.consumables.append(consumable)
        noun_participle = 'an' if consumable.name[0].lower() in 'aeiou' else 'a'
        return f'You acquire {noun_participle} {consumable.name}'

    def use_consumable(self, consumable_name):
        """
        Use a consumable by name.
        """
        consumable_to_use = None
        #print(f'Checking {consumable_name} against {self.consumables}')
        for consumable in self.consumables:
            #print(f'Checking {consumable.name} against {consumable_name}')
            if consumable_name.lower() in consumable.name.lower():
                consumable_to_use = consumable
                break
        if consumable_to_use is None:
            return f'No consumable named {consumable_name} found in your inventory'
        # Consumable will remove itself after charges are consumed
        return consumable_to_use.use(self)

    def heal(self, amount):
        """
        Heal the character by an amount.
        """
        self.health += amount
        overheal = self.health - self.max_health
        if self.health > self.max_health:
            self.health = self.max_health
        return f'🩹 {self.name} heals {amount} health ({overheal} overhealed)! ❤️\n'

    def move(self, direction):
        """
        Move the player in the specified direction.
        """
        old_location = self.game.map.map_location_data[self.position[0]][self.position[1]]
        direction = direction.lower()
        move_msg = f'You move {direction}'
        

        initial_position = self.position
        arriving_direction = ''
        if direction == 'north':
            self.position = (self.position[0] - 1, self.position[1])
            arriving_direction = 'south'
        elif direction == 'south':
            self.position = (self.position[0] + 1, self.position[1])
            arriving_direction = 'north'
        elif direction == 'west':
            self.position = (self.position[0], self.position[1] - 1)
            arriving_direction = 'east'
        elif direction == 'east':
            self.position = (self.position[0], self.position[1] + 1)
            arriving_direction = 'west'

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


        new_location = self.game.map.map_location_data[self.position[0]][self.position[1]]
        if old_location != new_location:
            old_location.remove_content(self)
            old_location.send_message_to_contents(f'{self.name} moves {direction}\n')
            new_location.send_message_to_contents(f'{self.name} arrives from the {arriving_direction}\n')
            new_location.add_content(self)
            self.position = (new_location.coordinates[0], new_location.coordinates[1])

        return move_msg