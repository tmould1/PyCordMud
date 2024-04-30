
class LocationContent():
    def location_display(self):
        return f'{self.icon} {self.name} is here. {self.description}'
    
class Location():
    def __init__(self, name, description, coordinates=(0, 0)):
        self.name = name
        self.description = description
        self.default_icon = '🟦'
        self.map_icon = self.default_icon
        self.contents = []
        self.coordinates = coordinates
        
    def add_content(self, content):
        self.contents.append(content)
        
    def remove_content(self, content):
        for content in self.contents:
            if content.name == content.name:
                print(f'Removing {content.name} from {self.name}')
                self.contents.remove(content)
                remaining_content = self.build_content_string()
                print(f'Contents remaining: {remaining_content}')
                break
        
    def build_content_string(self):
        content_str = ''
        for content in self.contents:
            content_str += content.location_display() + '\n'
        return content_str
    
    def has_contents(self):
        return len(self.contents) > 0
    
    def get_contents(self):
        return self.contents
    
    def has_enemies(self):
        from enemy import Enemy

        for content in self.contents:
            if isinstance(content, Enemy):
                return True
        return False
    
    def get_enemies(self):
        from enemy import Enemy

        enemies = []
        for content in self.contents:
            if isinstance(content, Enemy):
                enemies.append(content)
        return enemies