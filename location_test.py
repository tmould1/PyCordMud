"""
This module contains the location testing logic.
"""
import location
import gear

def test_location_contents_add_has_one_element():
    """
    Test case for adding a location content and checking if it has one element.
    """
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    location_content = location.LocationContent()
    location_content.icon = '🧙‍♂️'
    location_content.name = 'Wizard'
    location_content.description = 'A wise wizard'

    # Act
    test_location.add_content(location_content)

    # Assert
    assert test_location.has_contents() is True

def test_location_contents_remove_has_no_elements():
    """
    Test case for removing a location content and checking if it has no elements.
    """
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    location_content = location.LocationContent()
    location_content.icon = '🧙‍♂️'
    location_content.name = 'Wizard'
    location_content.description = 'A wise wizard'

    # Act
    test_location.add_content(location_content)
    test_location.remove_content(location_content)

    # Assert
    assert test_location.has_contents() is False

def test_location_contents_add_gear_has_one_element():
    """
    Test case for adding a gear item as a location content and checking if it has one element.
    """
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    gear_item = gear.Gear("Test Gear", "A test gear item")

    # Act
    test_location.add_content(gear_item)

    # Assert
    assert test_location.has_contents() is True

def test_location_contents_remove_gear_has_no_elements():
    """
    Test case for removing a gear item as a location content and checking if it has no elements.
    """
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    gear_item = gear.Gear("Test Gear", "A test gear item")

    # Act
    test_location.add_content(gear_item)
    test_location.remove_content(gear_item)

    # Assert
    assert test_location.has_contents() is False
