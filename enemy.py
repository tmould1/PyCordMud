"""
This module manages the enemies in the game.
"""
import random

from location import LocationContent
from location import Location
from player import PlayerCharacter
from gear import Gear


class EnemyManager():
    """
    Manages the enemies in the game.
    """

    def __init__(self, discord_game):
        self.enemies = []
        self.game = discord_game

    def add_enemy(self, enemy):
        """
        Adds an enemy to the list of enemies.
        
        Args:
            enemy: The enemy object to be added.
        """
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        """
        Removes an enemy from the list of enemies.
        
        Args:
            enemy: The enemy object to be removed.
        """
        self.enemies.remove(enemy)

    def get_enemy(self, name):
        """
        Retrieves an enemy from the list of enemies by name.
        
        Args:
            name: The name of the enemy to retrieve.
        
        Returns:
            The enemy object with the specified name, or None if not found.
        """
        for enemy in self.enemies:
            if enemy.name == name:
                return enemy
        return None

    def initial_seed(self):
        """
        Initializes the seed for enemy creation.
        """
        center = self.game.map.map_location_data[self.game.map_size[0] // 2]\
            [self.game.map_size[1] // 2]
        top_left = self.game.map.map_location_data[0][0]
        bottom_right = self.game.map.map_location_data[self.game.map_size[0] - 1]\
            [self.game.map_size[1] - 1]

        self.create_basic_goblin(center)
        self.create_intermediate_orc(top_left)
        self.create_advanced_troll(bottom_right)

        random_x = random.randint(0, self.game.map_size[0] - 1)
        random_y = random.randint(0, self.game.map_size[1] - 1)
        random_location = self.game.map.map_location_data[random_x][random_y]
        self.create_boss_dragon(random_location)
        
    def update_enemies(self):
        """
        Updates the enemies in the game.
        """
        for enemy in self.enemies:
            enemy.update()

    def create_basic_goblin(self, location: Location):
        """
        Creates a basic goblin enemy.
        """
        gobbo = Enemy('Goblin', location, self)
        gobbo.icon = '👺'
        gobbo.health = 1
        gobbo.power = 1
        gobbo.build_description()
        rusty_gobbo_dagger = Gear('Rusty Gobbo Dagger', 'A rusty dagger that goblins use')
        rusty_gobbo_dagger.icon = '🗡️'
        rusty_gobbo_dagger.offense = 1
        gobbo.drops.append(rusty_gobbo_dagger)
        self.add_enemy(gobbo)
        location.add_content(gobbo)
        return gobbo

    def create_intermediate_orc(self, location: Location):
        """
        Creates an intermediate orc enemy.
        """
        orc = Enemy('Orc', location, self)
        orc.icon = '👹'
        orc.health = 3
        orc.power = 2
        orc.build_description()
        first_orc_armor = Gear('Orcish Armor', 'Armor made from the hides of slain orcs')
        first_orc_armor.icon = '🛡️'
        first_orc_armor.defense = 1
        orc.drops.append(first_orc_armor)
        self.add_enemy(orc)
        location.add_content(orc)
        return orc

    def create_advanced_troll(self, location: Location):
        """
        Creates an advanced troll enemy.
        """
        troll = Enemy('Troll', location, self)
        troll.icon = '🧟'
        troll.health = 5
        troll.power = 3
        troll.build_description()
        first_troll_magic_circlet = Gear('Troll Magic Circlet',
                        'A circlet that enhances the magical abilities of trolls')
        first_troll_magic_circlet.icon = '🔮'
        first_troll_magic_circlet.offense = 5
        first_troll_magic_circlet.defense = 3
        troll.drops.append(first_troll_magic_circlet)
        self.add_enemy(troll)
        location.add_content(troll)
        return troll

    def create_boss_dragon(self, location: Location):
        """
        Creates a boss dragon enemy.
        """
        dragon = Enemy('Dragon', location, self)
        dragon.icon = '🐉'
        dragon.health = 20
        dragon.power = 10
        dragon.build_description()
        first_dragon_armor = Gear('Dragon Scales', 'Armor made from the scales of a dragon')
        first_dragon_armor.icon = '🐲'
        first_dragon_armor.defense = 5
        dragon.drops.append(first_dragon_armor)
        self.add_enemy(dragon)
        location.add_content(dragon)
        return dragon

    def handle_enemy_death(self, enemy):
        """
        Handles the death of an enemy.
        """
        self.remove_enemy(enemy)
        random_new_enemy_location = random.choice(self.game.map.map_location_data)
        random_new_enemy_location = random.choice(random_new_enemy_location)
        if "goblin" in enemy.name.lower():
            self.game.goblin_kills += 1
            self.create_basic_goblin(random_new_enemy_location)
        elif "orc" in enemy.name.lower():
            self.game.orc_kills += 1
            self.create_intermediate_orc(random_new_enemy_location)
        elif "troll" in enemy.name.lower():
            self.game.troll_kills += 1
            self.create_advanced_troll(random_new_enemy_location)
        elif "dragon" in enemy.name.lower():
            self.game.dragon_kills += 1
            self.create_boss_dragon(random_new_enemy_location)

        self.game.update_shown_map()


class Enemy(LocationContent):
    """
    Represents an enemy in the game.
    """

    def __init__(self, name, location: Location, manager: EnemyManager):
        super().__init__()
        self.name = name
        self.icon = '👾'
        self.location = location
        self.manager = manager

        self.power = 1
        self.health = 1

        self.description = self.build_description()

        self.drops = []

    def build_description(self):
        """
        Builds the description of the enemy.
        """
        self.description = f'(❤️{self.health} 💪{self.power})'
        return self.description

    def attack(self, player: PlayerCharacter):
        """
        Performs an attack on the player.
        """
        attack_msg = f'{self.name} attacks {player.name} 🫵!\n'
        attack_msg += player.receive_damage(self.power)
        return attack_msg

    def receive_damage(self, source, damage):
        """
        Receives damage from a source.
        """
        enemy_recv_msg = f'{self.name} receives {damage} damage 💥!\n'
        self.health -= damage
        self.description = f'(❤️{self.health} 💪{self.power})'
        enemy_recv_msg += self.attack(source)
        if self.health <= 0:
            self.health = 0
            self.manager.handle_enemy_death(self)
            enemy_recv_msg += f'💀{self.name} has been defeated\n'
            enemy_recv_msg += self.do_drop_loot()
        else:
            enemy_recv_msg += f'❤️{self.name} has {self.health} health remaining\n'

        self.build_description()
        return enemy_recv_msg

    def do_drop_loot(self):
        """
        Drops loot when the enemy is defeated.
        """
        random_drop = random.choice(self.drops)
        drop_msg = f'{self.name} drops {random_drop.name}.\n'
        self.location.add_content(random_drop)
        return drop_msg

    def update(self):
        """
        Updates the enemy.
        """
        random_roll = random.randint(1, 100)
        # 10% chance to move
        if random_roll <= 10:
            random_x = random.randint(-1, 1)
            random_y = random.randint(-1, 1)
            new_x = self.location.coordinates[0] + random_x
            new_y = self.location.coordinates[1]+ random_y
            if new_x < 0 or new_x >= self.manager.game.map_size[0]:
                new_x = self.location.coordinates[0]
            if new_y < 0 or new_y >= self.manager.game.map_size[1]:
                new_y = self.location.coordinates[1]
            new_location = self.manager.game.map.map_location_data[new_x][new_y]
            self.location.remove_content(self)
            new_location.add_content(self)
            self.location = new_location
            self.manager.game.update_shown_map()
            print(f'{self.name} moved to {self.location.name}\n')
