from enum import IntEnum
from Code.Class_Player import Player

class color_wheel():
    def __init__(self):
        self.val = {}
        self.val["RESET"]           = "\033[0m"
        self.val["BLACK"]           = "\033[0;30m"
        self.val["RED"]             = "\033[0;31m"
        self.val["GREEN"]           = "\033[0;32m"
        self.val["YELLOW"]          = "\033[0;33m"
        self.val["BLUE"]            = "\033[0;34m"
        self.val["PURPLE"]          = "\033[0;35m"
        self.val["CYAN"]            = "\033[0;36m"
        self.val["WHITE"]           = "\033[0;37m"
        self.val["GRAY"]            = "\033[0;38m"
        self.val["DARK_GRAY"]       = "\033[1;30m"
        self.val["BOLD_RED"]        = "\033[1;31m"
        self.val["BOLD_GREEN"]      = "\033[1;32m"
        self.val["BOLD_YELLOW"]     = "\033[1;33m"
        self.val["BOLD_BLUE"]       = "\033[1;34m"
        self.val["BOLD_PURPLE"]     = "\033[1;35m"
        self.val["BOLD_CYAN"]       = "\033[1;36m"
        self.val["BOLD_WHITE"]      = "\033[1;37m"
        self.val["BOLD_GRAY"]       = "\033[1;38m"

# ENUMS
# Wall -> 0
# Available passages -> Positives
# Unavailable Passages -> Negatives
#   Unlockable Passages -> Divisible by 1000
#   
class DOOR_STATUS(IntEnum):
    # Wall
    Wall = 0
    # Passable doors
    P_NewDoor = 2
    P_KnownDoor = 3 
    # Unopenable doors
    U_NoDoorHandle = -1
    U_CollapsedDoor = -2
    # Barricaded doors
    B_LockedDoor = -1000
    B_BreakableDoor = -2000
    B_ThinWall = -3000
    B_CrackedWall = -4000
    
class RNG(IntEnum):
    RandomDoorSpawn = 70      # The chances of a new door to spawn
    EntranceLock = 20         # The chances that you cannot head back the way you came from
    SuddenlySecretDoor = 50   # The chances that a door that should lead to another room is locked from this side
    RoomNextWall = 80         # The chances that behind a wall, you have a room instead of solid rock

# class LOCATION_TYPE(IntEnum):
#     Room = 1
#     NonInteractibleSpace = 2


# Create all global variables, should be called only once
def create_globals():
    global CH_ABS_ROOM_NUM, CH_LOCATIONS, CH_OPENINGS, CH_CUR_LOCATION, CH_PLAYER
    global DIRECTIONS
    CH_ABS_ROOM_NUM = 0
    CH_LOCATIONS = {}
    CH_OPENINGS = 0
    CH_CUR_LOCATION = (0,0,0)
    CH_PLAYER = Player()

    DIRECTIONS = ["North", "East", "South", "West", "Upwards", "Downwards"]

# Reset all global variables (used for a New Game)
def reset_globals():
    global CH_ABS_ROOM_NUM, CH_LOCATIONS, CH_OPENINGS, CH_CUR_LOCATION, CH_PLAYER
    CH_ABS_ROOM_NUM= 0
    CH_LOCATIONS = {}  
    CH_OPENINGS = 0
    CH_CUR_LOCATION = (0,0,0)
    CH_PLAYER = Player()



# PROGRAM INFO
TITLE = "Averkorf Dungeon"
CREATOR = "George"
PLATFORM = "Python 3"
