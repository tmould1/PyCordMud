"""
This module contains the biome class.
"""

class Biome():
    """
    This class represents a biome.
    """

    def __init__(self, name, icon = '⬛', dsecription= '', index = 0):
        self.name = name
        self.icon = icon
        self.description = dsecription
        self.index = index

class Meadows(Biome):
    """
    This class represents the meadows biome.
    """

    def __init__(self):
        super().__init__("Meadows", "🌾", "A gentle, rolling meadow.", 1)
class Forest(Biome):
    """
    This class represents the forest biome.
    """

    def __init__(self):
        super().__init__("Forest", "🌲", "A dense forest of trees.", 2)

class Desert(Biome):
    """
    This class represents the desert biome.
    """

    def __init__(self):
        super().__init__("Desert", "🟨", "A parched sea of sand.", 3)

class Mountain(Biome):
    """
    This class represents the mountain biome.
    """

    def __init__(self):
        super().__init__("Mountain", "⛰️ ", "A towering mountain range.", 4)

class Ocean(Biome):
    """
    This class represents the ocean biome.
    """

    def __init__(self):
        super().__init__("Ocean", "🌊", "A vast, open ocean.", 5)
