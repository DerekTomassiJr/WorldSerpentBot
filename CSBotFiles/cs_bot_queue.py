import random
import string
import json
import os
import cs_map
from enumerations import CSMapPool
from enumerations import CSMapOriginalGame
from enumerations import CSMapScenario

class cs_bot_queue():
    def __init__(self):
        # loading map data from json data file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "csmaps.json")

        with open(file_path, "r") as file:
            data = json.load(file)
            self.map_factory(data.maps)
        
        # logging channel information
        print("CS Bot Queue Activated!")
        print(f"Text Channel Detected: {self.channel.name}")

    def map_factory(self, map_data):
        print("Starting Map Factory!")

        for map in map_data:
            map_name: string = list(map.keys())[0]
            map_pool: CSMapPool = map[map_name]["map_pool"]
            map_original_game: CSMapOriginalGame = map[map_name]["original_game"]
            map_scenario: CSMapScenario = map[map_name]["scenario"]
            self.maps.append(cs_map(map_name, map_pool, map_original_game, map_scenario))
            
    def process_add_tag(self):
        raise NotImplementedError()
        
    def process_remove_tag(self):
        raise NotImplementedError()
        
    def process_random_tag(self):
        raise NotImplementedError()
    
    def command_parser(self, command):
        command_tag_functions: dict = {
            self.ADD_TAG: self.process_add_tag,
            self.REMOVE_TAG: self.process_remove_tag,
            self.RANDOM_TAG: self.process_random_tag
        }
        
        command_tags: list = command.split()

        if (command_tags[0] != self.QUEUE_COMMAND or len(command_tags < 2)):
            raise ValueError("Invalid command has been send and cannot be parsed.")
        
        # remove the first command tag as we validated it as the queue command
        del command_tags[0]
        
        if (not command_tags[0].startswith("-")):
            raise SyntaxError("Invalid command syntax! Please retry.")
        
        indencies_of_tags = [i for i, x in enumerate(command_tags) if x.startswith("-")]
        
        i = 0
        for index in indencies_of_tags:
            if (command_tags[index] not in command_tag_functions.keys):
                raise SyntaxError("Invalid command tag! Please retry.")
            
            # This will call the appropriate command tag function and supply it will all the data attached to the tag
            command_tag_data = command_tags[index + 1:] if i == len(indencies_of_tags - 1) else command_tags[index + 1:indencies_of_tags[i + 1]]
            command_tag_functions[command_tags[index]](command_tag_data)
            
            i += 1

    # Initialization Variables
    maps: list = [] # Maps data loaded in from JSON data file
    queue_maps: list = [] # Maps being queued for competitve match

    # Constants
    QUEUE_COMMAND = "!csbotqueue"
    ADD_TAG = "-add"
    REMOVE_TAG = "-remove"
    RANDOM_TAG = "-random"
    