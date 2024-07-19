"""
This module defines Locations and LocationContents in the game.
"""

class LocationContent():
    """
    Represents the content of a location.
    """
    def __init__(self):
        """
        Initializes a new LocationContent instance.
        """
        self.name = ''
        self.icon = ''
        self.description = ''
        self.biome = None

    def location_display(self):
        """
        Returns the display string for the location.
        """
        return f'{self.icon} {self.name} is here. {self.description}'

    def receive_message(self, msg):
        """
        Receives a message.
        """
        pass

class Location():
    """
    Represents a location.
    """

    def __init__(self, name, description, coordinates=(0, 0), biome=None):
        """
        Initializes a new Location instance.
        """
        self.name = name
        self.description = description
        self.default_icon = '🟦'
        self.map_icon = biome.icon if biome is not None else self.default_icon
        self.contents = []
        self.coordinates = coordinates
        self.biome = biome

    def add_content(self, content):
        """
        Adds content to the location.
        """
        self.contents.append(content)

    def remove_content(self, content):
        """
        Removes content from the location.
        """
        for c in self.contents:
            if c.name == content.name:
                #print(f'Removing {c.name} from {self.name}')
                self.contents.remove(c)
                #remaining_content = self.build_content_string()
                #print(f'Contents remaining: {remaining_content}')
                break

    def build_content_string(self):
        """
        Builds a string representation of the location's contents.
        """
        content_str = ''
        for c in self.contents:
            content_str += c.location_display() + '\n'
        return content_str

    def has_contents(self):
        """
        Checks if the location has contents.
        """
        return len(self.contents) > 0

    def get_contents(self):
        """
        Returns the contents of the location.
        """
        return self.contents

    def has_enemies(self):
        """
        Checks if the location has enemies.
        """
        from enemy import Enemy

        for c in self.contents:
            if isinstance(c, Enemy):
                return True
        return False

    def get_enemies(self):
        """
        Returns the enemies in the location.
        """
        from enemy import Enemy

        enemies = []
        for c in self.contents:
            if isinstance(c, Enemy):
                enemies.append(c)
        return enemies

    def send_message_to_contents(self, message):
        """
        Sends a message to the contents of the location.
        """
        for c in self.contents:
            c.receive_message(message)
