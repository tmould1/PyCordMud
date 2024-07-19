from player import PlayerCharacter

class CommandManager():
    def __init__(self):
        self.commands = []
        self.register_commands()
        
    def register_commands(self):
        look_command = PlayerCommand_ShowPlayerSurroundings()
        attack_command = PlayerCommand_Attack()
        stats_command = PlayerCommand_Stats()
        inventory_command = PlayerCommand_Inventory()
        take_command = PlayerCommand_Take()
        use_command = PlayerCommand_Use()
        move_command = PlayerCommand_Move()
        north_command = PlayerCommand_North()
        south_command = PlayerCommand_South()
        east_command = PlayerCommand_East()
        west_command = PlayerCommand_West()
        
        self.commands.append(look_command)
        self.commands.append(attack_command)
        self.commands.append(stats_command)
        self.commands.append(inventory_command)
        self.commands.append(take_command)
        self.commands.append(use_command)
        self.commands.append(move_command)
        self.commands.append(north_command)
        self.commands.append(south_command)
        self.commands.append(east_command)
        self.commands.append(west_command)
        
    def execute_command(self, command, player : PlayerCharacter):
        for cmd in self.commands:
            # get the first word, even if its the only word
            num_words = len(command.split())
            first_word = command.split()[0]
            args = []
            if num_words > 1:
                args = command.split()[1:]
            if first_word in cmd.keywords:
                return cmd.execute(player, args)
                
        return "Command not found"
        

class GameCommand():
    def __init__(self):
        self.keywords = []
        self.args = []

class PlayerCommand(GameCommand):
    def __init__(self):
        super().__init__()

class PlayerCommand_ShowPlayerSurroundings(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["show", "look", "surroundings", "l"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        look_target = " ".join(args)
        return player.show_surroundings()

class PlayerCommand_Attack(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["attack", "kill", "fight", "k"]
        self.args = ["target_name"]

    def execute(self, player : PlayerCharacter, args : list[str]):
        target_string = " ".join(args)
        return player.attack(target_string)

class PlayerCommand_Stats(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["stats", "status", "health"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        return player.get_player_stats_string()

class PlayerCommand_Inventory(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["inventory", "items", "gear", "i"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        inventory_str = ''
        for gear in player.gear:
            inventory_str += f'{gear.icon} {gear.name} - {gear.description}\n'
        return inventory_str

class PlayerCommand_Take(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["take", "pick", "get"]
        self.args = ["item_name"]

    def execute(self, player : PlayerCharacter, args : list[str]):
        item_name = " ".join(args)
        take_msg = player.take_item(item_name)
        return take_msg

class PlayerCommand_Use(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["use", "consume", "drink", "eat"]
        self.args = ["item_name"]

    def execute(self, player : PlayerCharacter, args : list[str]):
        item_name = " ".join(args)
        use_msg = player.use_consumable(item_name)
        return use_msg

class PlayerCommand_Move(PlayerCommand):
    def __init__(self):
        super().__init__()
        self.keywords = ["move", "go", "walk", "run"]
        self.args = ["direction"]

    def execute(self, player : PlayerCharacter, args : list[str]):
        direction = " ".join(args)
        return player.move(direction)

class PlayerCommand_North(PlayerCommand_Move):
    def __init__(self):
        super().__init__()
        self.keywords = ["north", "n"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        return player.move("north")

class PlayerCommand_South(PlayerCommand_Move):
    def __init__(self):
        super().__init__()
        self.keywords = ["south", "s"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        return player.move("south")

class PlayerCommand_East(PlayerCommand_Move):
    def __init__(self):
        super().__init__()
        self.keywords = ["east", "e"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        return player.move("east")

class PlayerCommand_West(PlayerCommand_Move):
    def __init__(self):
        super().__init__()
        self.keywords = ["west", "w"]
        self.args = []

    def execute(self, player : PlayerCharacter, args : list[str]):
        return player.move("west")
