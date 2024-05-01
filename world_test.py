"""
This module contains the world testing logic.
"""
import world
import gear

def test_map_init_has_locations():
    """
    Test if the map initialization has locations.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data()

    # Assert
    assert len(test_map.map_location_data) > 0

def test_map_init_has_icons():
    """
    Test if the map initialization has icons.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data()
    test_map.update_map_icons()

    # Assert
    assert len(test_map.map_icons) > 0

def test_map_init_has_map_string():
    """
    Test if the map initialization has a map string.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data()
    test_map.update_map_icons()
    map_str = test_map.get_map_string()

    # Assert
    assert len(map_str) > 0

def test_map_icons_add_gear_shows_icon():
    """
    Test if adding gear shows the corresponding icon on the map.
    """
    # Arrange
    test_map = world.Map()
    test_map.create_map_location_data()
    test_map.update_map_icons()
    test_gear = gear.Gear('Test Gear', 'A test piece of gear')
    test_gear_icon = '🧪'
    test_gear.icon = test_gear_icon
    test_map.map_location_data[0][0].add_content(test_gear)

    # Act
    test_map.update_map_icons()

    # Assert
    assert test_map.map_location_data[0][0].has_contents() is True
    assert test_map.map_icons[0][0] == test_gear.icon

def test_map_icons_remove_gear_hides_icon():
    """
    Test if removing gear hides the corresponding icon on the map.
    """
    # Arrange
    test_map = world.Map()
    test_map.create_map_location_data()
    test_map.update_map_icons()
    test_gear = gear.Gear('Test Gear', 'A test piece of gear')
    test_gear_icon = '🧪'
    test_gear.icon = test_gear_icon
    initial_icon = test_map.map_location_data[0][0].map_icon
    test_map.map_location_data[0][0].add_content(test_gear)

    # Act
    test_map.update_map_icons()
    test_map.map_location_data[0][0].remove_content(test_gear)
    test_map.update_map_icons()


    # Assert
    assert test_map.map_location_data[0][0].has_contents() is False
    assert test_map.map_icons[0][0] == initial_icon
