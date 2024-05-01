"""
This module contains the consumables testing logic.
"""
import consumables

def test_consumable_init_has_name():
    """
    Test case for initializing the consumable with a name.
    """
    # Arrange
    test_consumable = consumables.Consumable("Test Consumable", "A test consumable item")

    # Act
    consumable_name = test_consumable.name

    # Assert
    assert consumable_name == "Test Consumable"

def test_consumable_init_has_description():
    """
    Test case for initializing the consumable with a description.
    """
    # Arrange
    test_description = "A test consumable item"
    test_consumable = consumables.Consumable("Test Consumable", test_description)

    # Act
    consumable_description = test_consumable.description

    # Assert
    assert consumable_description == test_description

def test_consumable_init_has_icon():
    """
    Test case for initializing the consumable with an icon.
    """
    # Arrange
    test_icon = '🍎'
    test_consumable = consumables.Consumable("Test Consumable", "A test consumable item")
    test_consumable.icon = test_icon

    # Act
    consumable_icon = test_consumable.icon

    # Assert
    assert consumable_icon == test_icon
