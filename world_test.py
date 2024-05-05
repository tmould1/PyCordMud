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

def test_map_string_add_gear_shows_icon():
    """
    Test if adding gear shows the corresponding icon on the map string.
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
    map_str = test_map.get_map_string()

    # Assert
    assert test_map.map_location_data[0][0].has_contents() is True
    assert test_map.map_icons[0][0] == test_gear.icon
    assert test_map.map_icons[0][0] in map_str

def test_map_string_remove_gear_hides_icon():
    """
    Test if removing gear hides the corresponding icon on the map string.
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
    map_str = test_map.get_map_string()

    # Assert
    assert test_map.map_location_data[0][0].has_contents() is False
    assert test_map.map_icons[0][0] == initial_icon
    assert test_map.map_icons[0][0] in map_str

def test_map_create_3_by_3_map():
    """
    Test if the map creation logic creates a 3x3 map.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data((3, 3))

    # Assert
    assert len(test_map.map_location_data) == 3
    assert len(test_map.map_location_data[0]) == 3

def test_map_create_5_by_5_map():
    """
    Test if the map creation logic creates a 5x5 map.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data((5, 5))

    # Assert
    assert len(test_map.map_location_data) == 5
    assert len(test_map.map_location_data[0]) == 5

def test_map_create_10_by_10_map():
    """
    Test if the map creation logic creates a 10x10 map.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.create_map_location_data((10, 10))

    # Assert
    assert len(test_map.map_location_data) == 10
    assert len(test_map.map_location_data[0]) == 10

def test_map_build_perlin_map_clamped_to_integers():
    """
    Test if the map creation logic creates a perlin map clamped to integers.
    """
    # Arrange
    test_map = world.Map()

    # Act
    test_map.build_perlin_map_clamped_to_integers()

    # Assert
    assert len(test_map.map_location_data) > 0

def test_map_build_perlin_test_variance():
    """
    Test if the map creation logic creates a perlin map with variance.
    """
    # Arrange
    test_map = world.Map()
    test_map.build_perlin_map_clamped_to_integers()

    # Act
    num_diff_biomes = len({location.biome for row in test_map.map_location_data
                           for location in row})

    # Assert
    assert 0 < num_diff_biomes < len(test_map.biomes)

def test_map_getbiomewithnegative_returnsnone():
    """
    Test if get_biome_with_negative returns None when no negative value is found.
    """
    # Arrange
    test_map = world.Map()
    test_map.build_perlin_map_clamped_to_integers()

    # Act
    biome = test_map.get_biome(-1)

    # Assert
    assert biome is None

def test_map_getbiomewithlargeindex_returnsnone():
    """
    Test if get_biome_with_negative returns None when the index is larger than the biomes list.
    """
    # Arrange
    test_map = world.Map()
    test_map.build_perlin_map_clamped_to_integers()

    # Act
    biome = test_map.get_biome(len(test_map.biomes))

    # Assert
    assert biome is None

def test_map_getbiomewithvalidindex_returnsbiome():
    """
    Test if get_biome_with_negative returns the correct biome when the index is valid.
    """
    # Arrange
    test_map = world.Map()
    test_map.build_perlin_map_clamped_to_integers()

    # Act
    biome = test_map.get_biome(0)

    # Assert
    assert biome is not None
