"""
This module contains the biome testing logic.
"""

import biome

def test_biome_initmeadows_hasname():
    """
    Test if the meadows biome has a name.
    """
    # Arrange
    test_biome = biome.Meadows()

    # Act
    biome_name = test_biome.name

    # Assert
    assert biome_name == 'Meadows'

def test_biome_initmeadows_hasdescription():
    """
    Test if the meadows biome has a description.
    """
    # Arrange
    test_biome = biome.Meadows()

    # Act
    biome_description = test_biome.description

    # Assert
    assert "meadow" in biome_description.lower()

def test_biome_initmeadows_hasicon():
    """
    Test if the meadows biome has an icon.
    """
    # Arrange
    test_biome = biome.Meadows()

    # Act
    biome_icon = test_biome.icon

    # Assert
    assert biome_icon == '🌾'
