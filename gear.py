""" 
Module for providing locationcontent description builder base class access
"""
from location import LocationContent

class Gear(LocationContent):
    """ Base class for gear items. """
    def __init__(self, name, description):
        super().__init__()
        self.icon = '🛡️'
        self.name = name
        self.description = description
        self.offense = 0
        self.defense = 0

    def apply_stats(self, player):
        """ Apply the stats of the gear to the player. """
        player.base_attack += self.offense
        player.max_health += self.defense

    def remove_stats(self, player):
        """ Remove the stats of the gear from the player."""
        player.base_attack -= self.offense
        player.max_health -= self.defense
