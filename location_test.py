import location
import gear

def test_LocationContents_Add_HasOneElement():
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    location_content = location.LocationContent()
    location_content.icon = '🧙‍♂️'
    location_content.name = 'Wizard'
    location_content.description = 'A wise wizard'
    
    # Act
    test_location.add_content(location_content)
    
    # Assert
    assert test_location.has_contents() == True
    
def test_LocationContents_Remove_HasNoElements():
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
    assert test_location.has_contents() == False
    
def test_LocationContents_AddGear_HasOneElement():
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    gear_item = gear.Gear("Test Gear", "A test gear item")
    
    # Act
    test_location.add_content(gear_item)
    
    # Assert
    assert test_location.has_contents() == True

def test_LocationContents_RemoveGear_HasNoElements():
    # Arrange
    test_location = location.Location("Test Location", "A test location")
    gear_item = gear.Gear("Test Gear", "A test gear item")
    
    # Act
    test_location.add_content(gear_item)
    test_location.remove_content(gear_item)
    
    # Assert
    assert test_location.has_contents() == False
    