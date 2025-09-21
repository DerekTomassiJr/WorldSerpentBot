import random
import string
import json
import os
from CSBotFiles import cs_map
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
            print(f"JSON Data:\n{data}")
            self.map_factory(data["maps"][0])
        
        self.active = True
        print("CS Bot Queue Activated!")

    def map_factory(self, map_data):
        print("Starting Map Factory!")
        print(f"Map Data:\n{map_data}")
        print(f"Map Data Length: {len(list(map_data.keys()))}")

        for map in map_data.keys():
            map_name: string = map
            map_pool: CSMapPool = map_data[map_name]["map_pool"]
            map_original_game: CSMapOriginalGame = map_data[map_name]["original_game"]
            map_scenario: CSMapScenario = map_data[map_name]["scenario"]
            map_object = cs_map.cs_map(map_name, map_pool, map_original_game, map_scenario)
            
            print(map_object.to_string())
            self.maps.append(map_object)
            
    def process_add_tag(self, tag_attributes):
        raise NotImplementedError("This is an upcoming feature that has not been implemented yet.")
        
    def process_remove_tag(self, tag_attributes):
        raise NotImplementedError("This is an upcoming feature that has not been implemented yet.")
        
    def process_random_tag(self, tag_attributes):
        if (len(tag_attributes) > 1):
            raise ValueError("Invalid random tag value! Random tag should only have 1 attribute.")
        
        if (not tag_attributes[0].isdigit()):
            raise ValueError("Invalid random tag attribute! Random can only have a number provided as an attribute.")
        
        for i in range(int(tag_attributes[0])):
            random_map = self.maps[random.randint(0, len(self.maps) - 1)]
            print(f"Random Map #{i + 1}: {random_map.map_name}")
            
            if (random_map in self.queue_maps):
                i -= 1
                continue
            
            self.queue_maps.append(random_map)
            
        queue_to_string = "The following maps have been added to the queue:\n"
        for map in self.queue_maps:
            queue_to_string += f"• {map.map_name}\n"
            
        return queue_to_string
            
    def process_roll_tag(self, tag_attributes):
        if (len(tag_attributes > 0)):
            raise ValueError("Roll does not take tag atrributes! Resend the command with no attributes.")
        
        if (len(self.queue_maps == 0)):
            raise ValueError("Current queue pool is empty! Add maps to your queue pool to roll a random map.")
        
        if (self.chosen_map != None):
            raise ValueError("Chosen map clean up was not done properly! Dev needs to address this immediately!")
        
        chosen_map = random.choice(self.queue_maps)
        self.queue_maps.remove(self.chosen_map)
        
        return f"---Map Rolled---\n{chosen_map.to_string()}"
        
    
    def command_parser(self, command):
        return_string = ""
        
        for map in self.maps:
            print (f"Map:\n{map.to_string()}")
        
        command_tag_functions: dict = {
            self.ADD_TAG: self.process_add_tag,
            self.REMOVE_TAG: self.process_remove_tag,
            self.RANDOM_TAG: self.process_random_tag,
            self.ROLL_TAG: self.process_roll_tag
        }
        
        command_tags: list = command.split()

        if (command_tags[0] != self.QUEUE_COMMAND or len(command_tags) < 2):
            raise ValueError("Invalid command has been send and cannot be parsed.")
        
        # remove the first command tag as we validated it as the queue command
        del command_tags[0]
        
        if (not command_tags[0].startswith("-")):
            raise SyntaxError("Invalid command syntax! Please retry.")
        
        indencies_of_tags = [i for i, x in enumerate(command_tags) if x.startswith("-")]
        
        i = 0
        for index in indencies_of_tags:
            if (command_tags[index] not in command_tag_functions):
                raise SyntaxError("Invalid command tag! Please retry.")
            
            # This will call the appropriate command tag function and supply it will all the data attached to the tag
            command_tag_attributes = command_tags[(index + 1):] if i == (len(indencies_of_tags) - 1) else command_tags[(index + 1):indencies_of_tags[i + 1]]
            
            #for debugging purposes only
            print(f"Command Tag Attributes: {command_tag_attributes}")
            
            return_string += command_tag_functions[command_tags[index]](command_tag_attributes)
            
            i += 1
        
        if not return_string == "":
            return return_string
        
        return "Invalid Operation Occurred in cs_bot_queue.command_parser()."

    # Initialization Variables
    maps: list = [] # Maps data loaded in from JSON data file
    queue_maps: list = [] # Maps being queued for competitve match
    active = False # Flag to show if the object initialized properly

    # Constants
    QUEUE_COMMAND = "!csbotqueue"
    ADD_TAG = "-add"
    REMOVE_TAG = "-remove"
    RANDOM_TAG = "-random"
    ROLL_TAG = "-roll"
    