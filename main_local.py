"""
A place to work on main in a local environment, without discord
"""

import time
import threading

import game

class BoundedSemaphoreMessageQueue(threading.BoundedSemaphore):
    def __init__(self, value=1):
        super().__init__(value=value)
        self.message_queue = []

    def add_message(self, message):
        self.acquire()
        self.message_queue.append(message)
        self.release()

    def get_message(self):
        self.acquire()
        if len(self.message_queue) > 0:
            message = self.message_queue.pop(0)
        else:
            message = None
        self.release()
        return message

    def get_all_messages(self):
        self.acquire()
        messages = self.message_queue
        self.message_queue = []
        self.release()
        return messages

    def has_messages(self):
        return len(self.message_queue) > 0
    
def game_message_displayer(player_bound):
    while True:
        if player_bound.has_messages():
            message = player_bound.get_message()
            print(f'Player received message: \n{message}')
        time.sleep(0.1)
    

def main_local():
    print("Hello, main local!")
    game_bound = BoundedSemaphoreMessageQueue(value=1)
    player_bound = BoundedSemaphoreMessageQueue(value=1)
    
    local_game = game.MudGame("Local Game", game_bound_message_semaphore=game_bound, player_bound_message_semaphore=player_bound)
    local_player = local_game.add_player("blacklabel")
    print(local_game.handle_input(local_player, "look"))
    game_thread = None
    game_input_listener_thread = None
    game_message_displayer_thread = None
    try:
        print("Starting game thread")
        game_thread = threading.Thread(target=local_game.game_loop, args=())
        game_thread.start()
        
        print("Starting game input listener")
        game_input_listener_thread = threading.Thread(target=local_game.input_listener, args=())
        game_input_listener_thread.start()
        
        print("Starting game message displayer")
        game_message_displayer_thread = threading.Thread(target=game_message_displayer, args=(player_bound,))
        game_message_displayer_thread.start()
        
        # client loop
        while local_game.update():
            user_input = input(">")
            print("Adding message")
            game_bound.add_message(local_player.name + " " + user_input)
    except KeyboardInterrupt:
        print ("Keyboard interrupt detected")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        if game_thread is not None:
            game_thread.join()
        if game_input_listener_thread is not None:
            game_input_listener_thread.join()
        if game_message_displayer_thread is not None:
            game_message_displayer_thread.join()

        
    game_thread.join()
    
    print("Shutting down local game!")

main_local()
