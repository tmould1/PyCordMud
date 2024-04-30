import map
import gear

def test_Map_Init_HasLocations():
    # Arrange
    test_map = map.Map()
    
    # Act
    test_map.create_map_location_data()
    
    # Assert
    assert len(test_map.map_location_data) > 0
    
def test_Map_Init_HasIcons():
    # Arrange
    test_map = map.Map()
    
    # Act
    test_map.create_map_location_data()
    test_map.update_map_icons()
    
    # Assert
    assert len(test_map.map_icons) > 0
    
def test_Map_Init_HasMapString():
    # Arrange
    test_map = map.Map()
    
    # Act
    test_map.create_map_location_data()
    test_map.update_map_icons()
    map_str = test_map.get_map_string()
    
    # Assert
    assert len(map_str) > 0
    
def test_MapIcons_AddGear_ShowsIcon():
    # Arrange
    test_map = map.Map()
    test_map.create_map_location_data()
    test_map.update_map_icons()
    test_gear = gear.Gear('Test Gear', 'A test piece of gear')
    test_gear_icon = '🧪'
    test_gear.icon = test_gear_icon
    test_map.map_location_data[0][0].add_content(test_gear)
    
    # Act
    test_map.update_map_icons()
    
    # Assert
    assert test_map.map_location_data[0][0].has_contents() == True
    assert test_map.map_icons[0][0] == test_gear.icon
    
def test_MapIcons_RemoveGear_HidesIcon():
    # Arrange
    test_map = map.Map()
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
    assert test_map.map_location_data[0][0].has_contents() == False
    assert test_map.map_icons[0][0] == initial_icon