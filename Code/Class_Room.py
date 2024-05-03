import random, time

# from global_vars import *
import Code.global_vars as glb
from Code.Class_Location import Location
from Code.Class_NotRooms import *

# Function that finds the door opposite to the current one
def find_other_direction(CurrentDirection) -> int:
    match CurrentDirection:
        case 0:
            return 2
        case 1:
            return 3
        case 2: 
            return 0
        case 3:
            return 1
        case 4:
            return 5
        case 5:
            return 4
        case _:
            return ValueError("Wrong CurrentDirection value")

class Room(TraversibleLocation):
    def __init__(self, entry, roomNum, location):
        # Call the constructor of the parent class
        super().__init__(location)
        
        # Generate the class variables
        self.roomNum = roomNum
        self._doors = [glb.DOOR_STATUS.Wall for i in glb.DIRECTIONS]
        if entry > -1:
            self._doors[entry] = glb.DOOR_STATUS.P_KnownDoor
        # Work on each workable direction
        for direction in glb.DIRECTIONS:
            # Generate a new seed for RNG, because I want to
            time.sleep(random.random()/random.randint(50,70))
            random.seed()

            # Not yet designed to handle vertical exploration, so skip for now
            directionIdx = glb.DIRECTIONS.index(direction)
            if directionIdx >= 4:
                continue
            
            # If we are talking about the point of entry decide to block the path or not and do not process further
            if directionIdx == entry:
                if random.random()*100 < glb.RNG.EntranceLock:
                    self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                continue
            
            # Determine what kind of passage each door has
            workingLoc = self.nexCoords[directionIdx]       # Get a short version of the coordinate of the room adjacent to the direction we work at
            otherDir = find_other_direction(directionIdx)   # Find the direction of the other room we are workign with
            
            # The adjacent location has either been instantiated or not
            if workingLoc in glb.CH_LOCATIONS.keys():
                otherLoc = glb.CH_LOCATIONS[workingLoc]
                if isinstance(otherLoc, TraversibleLocation):
                    self._doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall              # If we have a room, we don't have a standard wall no matter what

                    # Account for the next location being a room with a door to us
                    # Or see if a door should spawn regardless (Works both in generic locations and Room)
                    
                    # Work per type of location (maybe not short, but clearer)
                    if isinstance(otherLoc, Room):
                        if otherLoc.doors[otherDir] == glb.DOOR_STATUS.P_NewDoor:
                            # either make the door not open from this side or make it know where it leads
                            ifCond =  random.random()*100 < glb.RNG.SuddenlySecretDoor
                            self._doors[directionIdx] = \
                                glb.DOOR_STATUS.U_NoDoorHandle if ifCond else glb.DOOR_STATUS.P_KnownDoor
                        elif otherLoc.doors[otherDir] == glb.DOOR_STATUS.P_KnownDoor:   # DEBUG
                            raise Exception('The door to here should not be known')     # DEBUG
                        elif otherLoc.doors[otherDir] == glb.DOOR_STATUS.B_ThinWall:
                            # either create a door from this side or keep the wall as is
                            ifCond = random.random()*100 < glb.RNG.RandomDoorSpawn
                            self._doors[directionIdx] = \
                                glb.DOOR_STATUS.P_KnownDoor if ifCond else self._doors[directionIdx]
                    else:
                        if random.random()*100 < glb.RNG.RandomDoorSpawn:
                            self._doors[directionIdx] = glb.DOOR_STATUS.P_NewDoor

            else:
                # If there is to be a location beyond this wall allocate a TraversibleLocation
                # Otherwise allocate a NonInteractibleSpace
                if random.random()*100 < glb.RNG.RoomNextWall: 
                    glb.CH_LOCATIONS[workingLoc] = TraversibleLocation(workingLoc)

                    # There may be a small door leading to the next room or not
                    if random.random()*100 < glb.RNG.RandomDoorSpawn:
                        self._doors[directionIdx] = glb.DOOR_STATUS.P_NewDoor
                        glb.CH_OPENINGS += 1 
                    else:
                        self.doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall
                else:
                    glb.CH_LOCATIONS[workingLoc] = NonInteractibleSpace(workingLoc)
        
        # If this coordinate is not logged as a Room in the LOCATIONS or at all, enter it.
        if (location not in glb.CH_LOCATIONS) or (not isinstance(glb.CH_LOCATIONS[location], Room)) or (glb.CH_LOCATIONS[location].roomNum != roomNum):
            glb.CH_LOCATIONS[location] = self


    def __str__(self) -> str:
        # Generate some responce lists to shorten the text
        wallDir = ["a wall" for i in range(4)] + ["the ceiling", "the floor"]
        doorDir = ["door" for i in range(4)] + ["trapdoor" for i in range(2)]

        # Generate a message
        message = f"This is Room {self.roomNum} at {self.coords}.\n"

        # Work on each direction individually
        for direction in glb.DIRECTIONS:
            directionIdx = glb.DIRECTIONS.index(direction)
            message += f"\t{direction}: You see "

            # per case of door type have a specific responce.
            match self._doors[directionIdx]:
                case glb.DOOR_STATUS.Wall:
                    message += wallDir[directionIdx] + ". You cannot notice any passageway leading out of the room."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], Room):
                        message += "\033[0;31mERROR\033[0;32m 1\033[0m"
                case glb.DOOR_STATUS.B_ThinWall:
                    message += wallDir[directionIdx] + ". You can hear faint sounds, which should be eminating from the other side."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], NonInteractibleSpace):
                        message += "\033[0;31mERROR\033[0;32m 2\033[0m"
                
                case glb.DOOR_STATUS.P_KnownDoor:
                    message += doorDir[directionIdx] + f"leading to Room {glb.CH_LOCATIONS[self.nexCoords[directionIdx]].roomNum}."
                case glb.DOOR_STATUS.P_NewDoor:
                    message += doorDir[directionIdx] + f", but you are unsure where it leads."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], NonInteractibleSpace):
                        message += "\033[0;31mERROR\033[0;32m 3\033[0m"

                case glb.DOOR_STATUS.U_NoDoorHandle:
                    message + "what at first glance seems to be " + wallDir[directionIdx] + "."
                    message += " However, you know about a " + doorDir[directionIdx] 
                    message += f" leading to Room {glb.CH_LOCATIONS[self.nexCoords[directionIdx]].roomNum}. "
                    message += "Unfortunately this side of the " + doorDir[directionIdx]
                    message += " has no functional opening mechanism, and cannot be used."
            message += "\n"
        return message
    

    def update(self):
        # Update each direction separately
        for directionIdx in range(len(glb.DIRECTIONS)):
            # We need to update only if there is a location next door
            if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys():
                otherIdx = find_other_direction(directionIdx)    # Get the index of the door list from the other room

                if isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], TraversibleLocation):                    
                    if self._doors[directionIdx] == glb.DOOR_STATUS.Wall:
                        self._doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall

                    # If we are not dealing with an established room do some quick computations and leave
                    if not isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], Room):
                        continue
                    
                    otherDoor = glb.CH_LOCATIONS[self.nexCoords[directionIdx]].doors[otherIdx]   # store the type of door from the other room for easy workings
                    
                    # If the value of the door from the next room to here is above 0, then we need to acc
                    if otherDoor > 0:
                        # If we had a ThinWall, the presence of another door makes it a one-way passage
                        if self._doors[directionIdx] == glb.DOOR_STATUS.B_ThinWall:
                            self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                        # If this door is somehow unknown, then we need to account for us knowing the next room
                        elif self._doors[directionIdx] == glb.DOOR_STATUS.P_NewDoor:
                            self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor
                            glb.CH_OPENINGS -= 1

                elif isinstance(glb.CH_LOCATIONS[self.nexCoords[directionIdx]], NonInteractibleSpace):
                        # If next door is a non-interactible space, then we can only have a Wall
                        self._doors[directionIdx] = glb.DOOR_STATUS.Wall
            
    # Function to help us transition to the next room
    # If the location is eligible for entering, then return the coordinates of the new location
    # If not return the current coordinates
    def go_to(self, DoorChoice):        
        # A new door means we create a new room and return its location
        if self._doors[DoorChoice] == glb.DOOR_STATUS.P_NewDoor:
            # Generate a small safeguard to prevent from generating a room in a bad location
            ifCond = not isinstance(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]], Room) and \
                     not isinstance(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]], NonInteractibleSpace)
            if ifCond:
                glb.CH_OPENINGS -= 1                                        # Update some global metrics
                glb.CH_ABS_ROOM_NUM += 1
                self._doors[DoorChoice] = glb.DOOR_STATUS.P_KnownDoor       # Change this door to a known one
                entry = find_other_direction(DoorChoice)                    # Generate an appropriate entry for the other room
                Room(entry,glb.CH_ABS_ROOM_NUM, self.nexCoords[DoorChoice]) # Generate a new Room
                return self.nexCoords[DoorChoice]                           # Return the coordinates of the new Room
            
            # Toss Errors in case the next room is not an empty location
            elif isinstance(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]], Room):
                msg  = "\033[0;41mDEBUG ERROR: Attempted to overwrite a room with a new room\033[0m\n"
                msg += "\033[1;37mSource of error Room go_to() method. New Door leading to pre-made room\033[0m\n"
                msg += "Direction: " + str(DoorChoice) + ".\n Room attempted to create: " + str(glb.CH_ABS_ROOM_NUM+1) + ".\n"
                msg += "Current Room Coordinates: " + str(self.coords) + "| Obscuring Room Coordinates: " + str(self.nexCoords[DoorChoice]) + ".\n"
                msg += "Room attempted to overwrite: " + str(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]].roomNum) + ".\n"
                msg += "Opposing Room Door Status facing to this location: " + \
                    str(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]].doors[find_other_direction(DoorChoice)]) + ".\n"
                raise Exception(msg)
            elif isinstance(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]], NonInteractibleSpace):
                msg  = "\033[0;41mDEBUG ERROR: Attempted to overwrite a Non-Traversible Location with a new room\033[0m\n"
                msg += "\033[1;37mSource of error Room go_to() method. New Door leading to Non-Traversible Location\033[0m\n"
                msg += "Direction: " + str(DoorChoice) + ".\n Room attempted to create: " + str(glb.CH_ABS_ROOM_NUM+1) + ".\n"
                msg += "Current Room Coordinates: " + str(self.coords) + "| Non-Traversible Location Coordinates: " + str(self.nexCoords[DoorChoice]) + ".\n"
                raise Exception(msg)
        
        elif self._doors[DoorChoice] == glb.DOOR_STATUS.P_KnownDoor:
            if isinstance(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]], Room):
                print(f"You have been here before. This is Room {glb.CH_LOCATIONS[self.nexCoords[DoorChoice]].roomNum}")
                return self.nexCoords[DoorChoice]
            
            # Toss Errors in case we are not pointed to a Room
            else:
                msg  = "\033[0;41mDEBUG ERROR: Attempted to enter a room where there was none\033[0m\n"
                msg += "\033[1;37mSource of error Room go_to() method. Known Door leading to a non-room locale\033[0m\n"
                msg += "Direction: " + str(DoorChoice) + ".\n Type of Location attempted to enter: " + str(type(glb.CH_LOCATIONS[self.nexCoords[DoorChoice]])) + ".\n"
                msg += "Current Room Coordinates: " + str(self.coords) + "| Wanted Direction Coordinates: " + str(self.nexCoords[DoorChoice]) + ".\n"
                raise Exception(msg)
            
        return self.coords
        
    
    @property
    def doors(self):
        return self._doors