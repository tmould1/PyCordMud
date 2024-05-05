""" 
This module contains the map logic for the game.
"""

import math

from perlin_noise import PerlinNoise

from location import Location
import biome

class Map():
    """
    This class represents a map.
    """

    def __init__(self):
        self.map_location_data = []
        self.map_icons = []
        self.map_size = (1, 1)
        self.out_of_bounds = '⬛'

        self.biomes = [
            biome.Desert(),
            biome.Meadows(),
            biome.Ocean(),
            biome.Forest(),
            biome.Mountain()
        ]

    def create_map_location_data(self, size=(5, 5)):
        """
        Create the map location data.
        """
        self.map_size = size
        center_position = self.map_size[0] // 2, self.map_size[1] // 2
        center_position_icon = '🟨'
        surrounding_positions_icon = '🟦'

        # map_data will hold all the object data for the world
        self.map_location_data = []
        for i in range(self.map_size[0]):
            row = []
            for j in range(self.map_size[1]):
                if i == center_position[0] and j == center_position[1]:
                    center_location = Location('Center', 'The center of the world', center_position)
                    center_location.map_icon = center_position_icon
                    row.append(center_location)
                else:
                    location = Location('Surrounding', 'The surrounding world', (i, j))
                    location.map_icon = surrounding_positions_icon
                    row.append(location)
            self.map_location_data.append(row)

    def build_perlin_map_clamped_to_integers(self, size=(5, 5), octaves=8):
        """
        Build a perlin map clamped to integers.
        """
        self.map_size = size
        noise = PerlinNoise(octaves=octaves, seed=1)
        self.map_location_data = []
        scale = len(self.biomes)
        offset = 0.5
        for i in range(self.map_size[0]):
            row = []
            for j in range(self.map_size[1]):
                noise_val = noise([i / scale, j / scale]) + offset
                closest_int = math.floor(noise_val * scale)
                if closest_int >= scale:
                    closest_int = scale - 1
                selected_biome = self.get_biome(closest_int)
                location = Location(selected_biome.name, selected_biome.description, (i, j), selected_biome)
                location.map_icon = selected_biome.icon
                row.append(location)
            self.map_location_data.append(row)

    def get_biome(self, index):
        """
        Get the biome by index.
        """
        if 0 <= index < len(self.biomes):
            return self.biomes[int(index)]
        return None

    def update_map_icons(self):
        """
        Update the map icons.
        """
        # map will only hold the icons for quick lookups, map_data must be built first
        self.map_icons = []
        for i, row in enumerate(self.map_location_data):
            for j, map_location in enumerate(row):
                fitness_rating = 0
                best_fit = None
                if map_location.has_contents():
                    if map_location.has_enemies():
                        location_enemies = map_location.get_enemies()
                        for enemy in location_enemies:
                            enemy_rating = enemy.power + enemy.health
                            if enemy_rating > fitness_rating:
                                best_fit = enemy
                        self.map_location_data[i][j].map_icon = best_fit.icon
                    else:
                        self.map_location_data[i][j].map_icon = map_location.contents[0].icon
                else:
                    self.map_location_data[i][j].map_icon = (
                        map_location.biome.icon if map_location.biome is not None else self.out_of_bounds
                    )
        self.map_icons = [
            [map_location.map_icon for map_location in row]
            for row in self.map_location_data
        ]

    def get_map_string(self):
        """
        Get the map string.
        """
        map_str = ''
        for row in self.map_icons:
            map_str += ' '.join(row) + '\n'
        return map_str
