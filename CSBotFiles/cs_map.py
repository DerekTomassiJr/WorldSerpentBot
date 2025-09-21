import string
from enumerations import CSMapPool
from enumerations import CSMapOriginalGame
from enumerations import CSMapScenario

class cs_map():
    def __init__(self, map_name, map_pool, original_game, scenario):
        self.map_name = map_name
        self.map_pool = map_pool
        self.original_game = original_game
        self.scenario = scenario

    def to_string(self):
        return f"{self.map_name}:\nMap Pool: {CSMapPool(self.map_pool).name}\nOriginal Game: {CSMapOriginalGame(self.original_game).name}\nScenario: {CSMapScenario(self.scenario).name}"

    # Initialization Variables
    map_name: string = None # The map name
    map_pool: CSMapPool =  CSMapPool.unknown # The map pool the map belongs to
    original_game: CSMapOriginalGame = CSMapOriginalGame.unknown # The game in which the map debuted
    scenario: CSMapScenario = CSMapScenario.unknown # The scanario of the map 