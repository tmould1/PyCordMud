"""
This module contains the gear testing logic.
"""

import gear

def test_gear_init_has_name():
    """
    Test case for initializing the gear with a name.
    """
    # Arrange
    test_gear = gear.Gear("Test Gear", "A test piece of gear")

    # Act
    gear_name = test_gear.name

    # Assert
    assert gear_name == "Test Gear"

def test_gear_init_has_description():
    """
    Test case for initializing the gear with a description.
    """
    # Arrange
    test_description = "A test piece of gear"
    test_gear = gear.Gear("Test Gear", test_description)

    # Act
    gear_description = test_gear.description

    # Assert
    assert gear_description == test_description
    
def test_gear_init_has_icon():
    """
    Test case for initializing the gear with an icon.
    """
    # Arrange
    test_icon = '🧪'
    test_gear = gear.Gear("Test Gear", "A test piece of gear")
    test_gear.icon = test_icon

    # Act
    gear_icon = test_gear.icon

    # Assert
    assert gear_icon == test_icon
    
