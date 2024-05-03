import random

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

class Room(Location):
    def __init__(self, entry, roomNum, location):
        # Call the constructor of the parent class
        super().__init__(location, glb.LOCATION_TYPE.Room)
        
        # Generate the class variables
        self.roomNum = roomNum
        self._doors = [glb.DOOR_STATUS.Wall for i in glb.DIRECTIONS]
        if entry > -1:
            self._doors[entry] = glb.DOOR_STATUS.P_KnownDoor
        
        # Work on each workable direction
        for direction in glb.DIRECTIONS:
            # Not yet designed to handle vertical exploration, so skip for now
            directionIdx = glb.DIRECTIONS.index(direction)
            if directionIdx >= 4:
                continue
            
            # If we are talking about the point of entry decide to block the path or not and do not process further
            if directionIdx == entry:
                if random.random()*100 < glb.RNG.EntranceLock:
                    self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                    print('As you venture into the Room, the door you just used closes, revealing a lack of an opening mechanism from this side!')
                continue
            
            # Determine what kind of passage each door has
            workingLoc = self.nexCoords[directionIdx]       # Get a short version of the coordinate of the room adjacent to the direction we work at
            otherDir = find_other_direction(directionIdx)   # Find the direction of the other room we are workign with
            
            # The adjacent location has either been instantiated or not
            if workingLoc in glb.CH_LOCATIONS.keys():
                otherLoc = glb.CH_LOCATIONS[workingLoc]
                if otherLoc.locType == glb.LOCATION_TYPE.Room:
                    self._doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall              # If we have a room, we don't have a standard wall no matter what
                    if otherLoc.doors[otherDir] == glb.DOOR_STATUS.P_NewDoor:           # If we know there is a door from the other side, but it is not opened
                        if random.random()*100 > glb.RNG.SuddenlySecretDoor:            #   either OUR wall has a door we know the passage to,
                            self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor 
                        else:                                                           #   or it is a secret passage openable from the other side
                            self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle  
            else:
                # Determine whether or not the wall will have a room next to it or not
                if random.random()*100 < glb.RNG.RoomNextWall: 
                    if random.random()*100 < glb.RNG.RandomDoorSpawn:
                        self._doors[directionIdx] = glb.DOOR_STATUS.P_NewDoor
                        glb.CH_OPENINGS += 1 
                    else:
                        self.doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall
                else:
                    glb.CH_LOCATIONS[workingLoc] = NonInteractibleSpace(workingLoc)
        
        if location not in glb.CH_LOCATIONS:
            glb.CH_LOCATIONS[location] = self
        # self.trap = len(list(filter(lambda x: x == 2 or x == 1, self._doors))) == 0 and entry > -1
        # LOCATIONS.val[location] = self


    def __str__(self) -> str:
        message = f"This is Room {self.roomNum} at {self.coords}.\n"
        for direction in glb.DIRECTIONS:
            directionIdx = glb.DIRECTIONS.index(direction)
            message += f"\t{direction}: You see "
            match self._doors[directionIdx]:
                case glb.DOOR_STATUS.Wall:
                    message += "a wall. There is nothing there."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and glb.CH_LOCATIONS[self.nexCoords[directionIdx]].locType == glb.LOCATION_TYPE.Room:
                        message += "\033[0;31mERROR\033[0;32m 1\033[0m"
                case glb.DOOR_STATUS.B_ThinWall:
                    message += "a wall. You can hear faint sounds, which should be eminating from the other side."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and glb.CH_LOCATIONS[self.nexCoords[directionIdx]].locType == glb.LOCATION_TYPE.NonInteractibleSpace:
                        message += "\033[0;31mERROR\033[0;32m 2\033[0m"
                
                case glb.DOOR_STATUS.P_KnownDoor:
                    message += f"the door leading to Room {glb.CH_LOCATIONS[self.nexCoords[directionIdx]].roomNum}."
                case glb.DOOR_STATUS.P_NewDoor:
                    message += f"a door, but you are unsure where it leads."
                    if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys() and glb.CH_LOCATIONS[self.nexCoords[directionIdx]].locType == glb.LOCATION_TYPE.NonInteractibleSpace:
                        message += "\033[0;31mERROR\033[0;32m 3\033[0m"

                case glb.DOOR_STATUS.U_NoDoorHandle:
                    message += "what seems to be a wall, but you know it is actually a secret passage. "
                    message += f"Behind this passage lies Room {glb.CH_LOCATIONS[self.nexCoords[directionIdx]].roomNum}. "
                    message += "Unfortunately the passage cannot be opened from this side"
            message += "\n"
        return message
    

    def update(self):
        for directionIdx in range(len(glb.DIRECTIONS)):
            if self.nexCoords[directionIdx] in glb.CH_LOCATIONS.keys():
                otherIdx = find_other_direction(directionIdx)

                match glb.CH_LOCATIONS[self.nexCoords[directionIdx]].locType:
                    case glb.LOCATION_TYPE.Room:
                        otherDoor = glb.CH_LOCATIONS[self.nexCoords[directionIdx]].doors[otherIdx]
                        
                        if self._doors[directionIdx] == glb.DOOR_STATUS.Wall:
                            self._doors[directionIdx] = glb.DOOR_STATUS.B_ThinWall

                        if otherDoor == glb.DOOR_STATUS.P_KnownDoor:
                            if self._doors[directionIdx] == glb.DOOR_STATUS.B_ThinWall:
                                self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                            elif self._doors[directionIdx] == glb.DOOR_STATUS.P_NewDoor:
                                self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor
                                glb.CH_OPENINGS -= 1

                    case glb.LOCATION_TYPE.NonInteractibleSpace:
                        self._doors[directionIdx] = glb.DOOR_STATUS.Wall
            
    
    def go_to(self, DoorChoice):        
        if self._doors[DoorChoice] == glb.DOOR_STATUS.P_NewDoor:
            glb.CH_OPENINGS -= 1
            print(f"You venture on, discovering Room {glb.CH_ABS_ROOM_NUM + 1}")
            glb.CH_ABS_ROOM_NUM += 1
            self._doors[DoorChoice] = glb.DOOR_STATUS.P_KnownDoor
            entry = find_other_direction(DoorChoice)
            Room(entry,glb.CH_ABS_ROOM_NUM, self.nexCoords[DoorChoice])
            return self.nexCoords[DoorChoice]
        
        elif self._doors[DoorChoice] == glb.DOOR_STATUS.P_KnownDoor:
            print(f"You have been here before. This is Room {glb.CH_LOCATIONS[self.nexCoords[DoorChoice]].roomNum}")
            return self.nexCoords[DoorChoice]
        
        return self.coords
        
    
    @property
    def doors(self):
        return self._doors