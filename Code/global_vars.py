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

OPENINGS = openings()
ABSOLUTE_ROOM_NUM = absolute_room_num()
LOCATIONS = locations()
RNG = rng()