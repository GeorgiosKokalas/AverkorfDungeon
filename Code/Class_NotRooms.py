# from global_vars import *
import Code.global_vars as glb
from Code.Class_Location import Location

# This class represents spaces the player cannot traverse through or interact with
# Is parent of:         -
# Will be parent of:    -
# Is child of:          Location
class NonInteractibleSpace(Location):
    def __init__(self, coords):
        super().__init__(coords)

# This class represents spaces that will be able to be traversed
# Used as a placeholder, for when we don't know what type of location it will be
# Is parent of:         -
# Will be parent of:    Room
# Is child of:          Location
class TraversibleLocation(Location):
    def __init__(self, coords):
        super().__init__(coords)