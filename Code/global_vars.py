class locations:
    def __init__(self):
        self.val = {}

class openings:
    def __init__(self):
        self.val = 0

class absolute_room_num():
    def __init__(self):
        self.val = 1

class rng():
    def __init__(self):
        self.val = {'Random Room Spawn': 0.3,        # The chances of a new door to spawn
                    'Entrance Lock': 0.2,            # The chances that you cannot head back the way you came from
                    'Suddenly Secret Door': 0.5}     # The chances that a door that should lead to another room is locked from this side

class player():
    # The max value of something is the highest it can go
    def __init__(self):
        self.maxHealth  = self.topHealth  = self.curHealth  = 100 
        self.maxStamina = self.topStamina = self.curStamina = 100 
        self.maxMagic   = self.topMagic   = self.curMagic   = 100
    
    

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

OPENINGS = openings()
ABSOLUTE_ROOM_NUM = absolute_room_num()
LOCATIONS = locations()
RNG = rng()
COLOR_WHEEL = color_wheel()

# PROGRAM INFO
TITLE = "Averkorf Dungeon"
CREATOR = "George"
PLATFORM = "Python 3"


def reset_global_vars():
    ABSOLUTE_ROOM_NUM.val = 1
    LOCATIONS.val = {}  
    OPENINGS.val = 0
