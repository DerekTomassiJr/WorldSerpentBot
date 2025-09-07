from enum import Enum

class CSMapPool(Enum):
    active_duty = 0
    reserve = 1
    community = 2
    hostage = 3
    unknown = 255

class CSMapOriginalGame(Enum):
    counter_strike_beta = 0
    counter_strike = 1
    counter_strike_go = 2
    counter_strike_2 = 3
    unknown = 255

class CSMapScenario(Enum):
    defuse = 0
    hostage = 1
    unknown = 255