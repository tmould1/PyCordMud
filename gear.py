from location import LocationContent

class Gear(LocationContent):
    def __init__(self, name, description):
        self.icon = '🛡️'
        self.name = name
        self.description = description
        self.armor = 0
        self.attack = 0
        
    def apply_stats(self, player):
        player.base_attack += self.attack
        player.max_health += self.armor
        
    def remove_stats(self, player):
        player.base_attack -= self.attack
        player.max_health -= self.armor