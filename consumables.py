"""
This module contains the consumables logic.
"""

from location import LocationContent

class Consumable(LocationContent):
    """
    A class to represent a consumable item.

    Attributes:
        name (str): The name of the consumable.
        description (str): The description of the consumable.
        icon (str): The icon of the consumable.
    """

    def __init__(self, name, description):
        """
        Constructs the necessary attributes for the consumable object.

        Args:
            name (str): The name of the consumable.
            description (str): The description of the consumable.
            health_points (int): The health points that the consumable restores.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.icon = '🍎'
        self.charges = 1
        self.max_charges = 1

    def use(self, character):
        """
        Uses the consumable item.

        Returns:
            str: The message that the consumable item was used.
        """
        self.charges -= 1
        if self.charges <= 0:
            character.consumables.remove(self)
        return f'You used {self.icon} {self.name}...... Talk to a dev.'

class HealthPotion(Consumable):
    """
    A class to represent a health potion.

    Attributes:
        name (str): The name of the health potion.
        description (str): The description of the health potion.
        icon (str): The icon of the health potion.
        health_points (int): The health points that the health potion restores.
    """

    def __init__(self, name, description, health_points):
        """
        Constructs the necessary attributes for the health potion object.

        Args:
            name (str): The name of the health potion.
            description (str): The description of the health potion.
            health_points (int): The health points that the health potion restores.
        """
        super().__init__(name, description)
        self.health_points = health_points
        self.icon = '🍺'

    def use(self, character):
        """
        Uses the health potion.

        Returns:
            str: The message that the health potion was used.
        """
        character.health += self.health_points
        if character.health > character.max_health:
            character.health = character.max_health
        super().use(character)
        return f'You used {self.icon} {self.name} and restored {self.health_points} health points.'

class BarkSkinPotion(Consumable):
    """
    A class to represent a bark skin potion.

    Attributes:
        name (str): The name of the bark skin potion.
        description (str): The description of the bark skin potion.
        icon (str): The icon of the bark skin potion.
        defense_points (int): The defense points that the bark skin potion provides.
    """

    def __init__(self, name, description, defense_points):
        """
        Constructs the necessary attributes for the bark skin potion object.

        Args:
            name (str): The name of the bark skin potion.
            description (str): The description of the bark skin potion.
            defense_points (int): The defense points that the bark skin potion provides.
        """
        super().__init__(name, description)
        self.defense_points = defense_points
        self.icon = '🌿'

    def use(self, character):
        """
        Uses the bark skin potion.

        Returns:
            int: The defense points that the bark skin potion provides.
        """
        super().use(character)
        return f'You used {self.icon} {self.name} and gained {self.defense_points} defense points.'
