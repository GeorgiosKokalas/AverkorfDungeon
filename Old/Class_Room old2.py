import random

# from global_vars import *
import Code.global_vars as glb

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

class Room:
    def __init__(self, entry, roomNum, location):
        # Generate a list of nonexistent doors, except for our point of entry
        self._doors = [glb.DOOR_STATUS.NonExistent for i in glb.DIRECTIONS]
        if entry > -1:
            self._doors[entry] = glb.DOOR_STATUS.P_KnownDoor
        
        # Assign the rest of the input in this room
        self.location = location
        self.roomNum = roomNum
        self.nexLoc = []
        for direction in glb.DIRECTIONS:

            # Per direction, add the coordinates of the adjacent room
            xAxis = yAxis = zAxis = 0
            match direction.lower():
                case "north":
                    yAxis += 1
                case "east":
                    xAxis += 1
                case "south":
                    yAxis -= 1
                case "west":
                    xAxis -= 1
                case "up":
                    zAxis += 1
                case "down":
                    zAxis -= 1
            self.nexLoc.append((location[0] + xAxis, location[1] + yAxis, location[2] + zAxis))

            # Not yet designed to handle vertical exploration, so skip for now
            directionIdx = glb.DIRECTIONS.index(direction)
            if directionIdx >= 4:
                continue
            
            # If we are talking about the point of entry decide to block the path or not and do not process further
            if directionIdx == entry:
                if random.random()*100 < glb.RNG.Entrance_Lock:
                    self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                    print('As you venture into the Room, the door you just used closes, revealing a lack of an opening mechanism from this side!')
                continue
            
            # Determine whether or not each direction is going to have a door
            devLocation = self.nexLoc[directionIdx]
            otherDir = find_other_direction(directionIdx)
            if devLocation in glb.CH_LOCATIONS.keys() and glb.CH_LOCATIONS[devLocation].doors[otherDir] == glb.DOOR_STATUS.P_NewDoor:
                if random.random()*100 > glb.RNG.Suddenly_Secret_Door:
                    self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor
                else:
                    self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
            elif random.random()*100 < glb.RNG.Random_Room_Spawn:
                self._doors[directionIdx] = glb.DOOR_STATUS.P_NewDoor
                glb.CH_OPENINGS += 1
        
        if location not in glb.CH_LOCATIONS:
            glb.CH_LOCATIONS[location] = self
        # self.trap = len(list(filter(lambda x: x == 2 or x == 1, self._doors))) == 0 and entry > -1
        # LOCATIONS.val[location] = self


    def __str__(self) -> str:
        message = f"This is Room {self.roomNum} at {self.location}.\n"
        for direction in glb.DIRECTIONS:
            directionIdx = glb.DIRECTIONS.index(direction)
            if self._doors[directionIdx] == glb.DOOR_STATUS.NonExistent:
                if self.nexLoc[directionIdx] in glb.CH_LOCATIONS.keys():
                    message += f"To the {direction} you remember the presence of Room {glb.CH_LOCATIONS[self.nexLoc[directionIdx]].roomNum}, but see no doorway leading to it.\n"
            elif self._doors[directionIdx] > glb.DOOR_STATUS.NonExistent:              
                if self._doors[directionIdx] == glb.DOOR_STATUS.P_KnownDoor:
                    message += f"\tThe room has a door to the {direction}. "
                    message += f"The door leads to Room {glb.CH_LOCATIONS[self.nexLoc[directionIdx]].roomNum}.\n"
                elif self._doors[directionIdx] == glb.DOOR_STATUS.P_NewDoor:
                    message += f"\t{direction.capitalize()}side, you notice a door. "
                    message += f"The door remains unopened, and you don't know where it leads.\n"
            else:
                if self._doors[directionIdx] == glb.DOOR_STATUS.U_NoDoorHandle:
                    message += f"\tTo the {direction}, you know of the presence of a hidden door. "
                    message += f"The door is connected to Room {glb.CH_LOCATIONS[self.nexLoc[directionIdx]].roomNum}, but you cannot open it from this side.\n"
        return message
    

    def update(self):
        for directionIdx in range(len(glb.DIRECTIONS)):
            if self.nexLoc[directionIdx] in glb.CH_LOCATIONS.keys():
                otherIdx = find_other_direction(directionIdx)

                otherDoor = glb.CH_LOCATIONS[self.nexLoc[directionIdx]].doors[otherIdx]
                if otherDoor == glb.DOOR_STATUS.P_KnownDoor:
                    if self._doors[directionIdx] == glb.DOOR_STATUS.NonExistent:
                        self._doors[directionIdx] = glb.DOOR_STATUS.U_NoDoorHandle
                    elif self._doors[directionIdx] == glb.DOOR_STATUS.P_NewDoor:
                        self._doors[directionIdx] = glb.DOOR_STATUS.P_KnownDoor
                        glb.CH_OPENINGS -= 1

            
    
    def go_to(self, DoorChoice):

        if self._doors[DoorChoice] == glb.DOOR_STATUS.NonExistent:
            print("There is no door here.")
            return self.location
        
        elif self._doors[DoorChoice] == glb.DOOR_STATUS.P_NewDoor:
            glb.CH_OPENINGS -= 1
            print(f"You venture on, discovering Room {glb.CH_ABS_ROOM_NUM + 1}")
            glb.CH_ABS_ROOM_NUM += 1
            self._doors[DoorChoice] = glb.DOOR_STATUS.P_KnownDoor
            entry = find_other_direction(DoorChoice)
            Room(entry,glb.CH_ABS_ROOM_NUM, self.nexLoc[DoorChoice])
            return self.nexLoc[DoorChoice]
        
        elif self._doors[DoorChoice] == glb.DOOR_STATUS.P_KnownDoor:
            print(f"You have been here before. This is Room {glb.CH_LOCATIONS[self.nexLoc[DoorChoice]].roomNum}")
            return self.nexLoc[DoorChoice]
        
        elif self._doors[DoorChoice] == glb.DOOR_STATUS.U_NoDoorHandle:
            print("While there is a room on the opposite side of this wall, you are unable to access it from this side.")
            return self.location
        
    
    @property
    def doors(self):
        return self._doors