import random

from global_vars import *

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
        global LOCATIONS, OPENINGS, DIRECTIONS

        self._doors = [DOOR_STATUS.NonExistent for i in DIRECTIONS]
        self.location = location
        if entry > -1:
            self._doors[entry] = DOOR_STATUS.P_KnownDoor
        self.roomNum = roomNum
        self.nexLoc = []
        for direction in DIRECTIONS:
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

            directionIdx = DIRECTIONS.index(direction)
            if directionIdx >= 4:
                continue

            if directionIdx == entry:
                if random.random()*100 < RNG.Entrance_Lock:
                    self._doors[directionIdx] = DOOR_STATUS.U_NoDoorHandle
                    print('As you venture into the Room, the door you just used closes, revealing a lack of an opening mechanism from this side!')
                continue
            
            # chance = random.random()
            if self.nexLoc[directionIdx] in LOCATIONS.val.keys():
                if random.random()*100 > RNG.Suddenly_Secret_Door:
                    self._doors[directionIdx] = DOOR_STATUS.P_KnownDoor
                else:
                    self._doors[directionIdx] = DOOR_STATUS.U_NoDoorHandle
            elif random.random()*100 < RNG.Random_Room_Spawn:
                self._doors[directionIdx] = DOOR_STATUS.P_NewDoor
                OPENINGS.val += 1
        
        # self.trap = len(list(filter(lambda x: x == 2 or x == 1, self._doors))) == 0 and entry > -1
        # LOCATIONS.val[location] = self


    def __str__(self) -> str:
        global LOCATIONS, DIRECTIONS

        message = f"This is Room {self.roomNum} at {self.location}. {self.nexLoc}\n"
        message += f"{self._doors}\n"
        # directions = ["north", "east", "south", "west"]
        for direction in DIRECTIONS:
            directionIdx = DIRECTIONS.index(direction)
            if self._doors == DOOR_STATUS.NonExistent:
                if self.nexLoc[directionIdx] in LOCATIONS.val.keys():
                    message += f"To the {direction} you remember the presence of Room {LOCATIONS.val[self.nexLoc[directionIdx]].roomNum}, but see no doorway leading to it.\n"
            elif self._doors[directionIdx] > DOOR_STATUS.NonExistent:              
                if self._doors[directionIdx] == DOOR_STATUS.P_KnownDoor:
                    message += f"\tThe room has a door to the {direction}. "
                    message += f"The door leads to Room {LOCATIONS.val[self.nexLoc[directionIdx]].roomNum}.\n"
                elif self._doors[directionIdx] == DOOR_STATUS.P_NewDoor:
                    message += f"\t{direction.capitalize()}side, you notice a door. "
                    message += f"The door remains unopened, and you don't know where it leads.\n"
            else:
                # input(str(self._doors[directionIdx])+ "   "+str(DOOR_STATUS.U_NoDoorHandle)+"    "+str(self._doors[directionIdx] == DOOR_STATUS.U_NoDoorHandle))
                if self._doors[directionIdx] == DOOR_STATUS.U_NoDoorHandle:
                    message += f"\tTo the {direction}, you know of the presence of a hidden door. "
                    message += f"The door is connected to Room {LOCATIONS.val[self.nexLoc[directionIdx]].roomNum}, but you cannot open it from this side.\n"
        return message
    

    def update(self):
        global LOCATIONS, OPENINGS

        for directionIdx in range(len(DIRECTIONS)):
            if self.nexLoc[directionIdx] in LOCATIONS.val.keys():
                otherIdx = find_other_direction(directionIdx)

                otherDoor = LOCATIONS.val[self.nexLoc[directionIdx]].doors[otherIdx]
                if otherDoor == DOOR_STATUS.P_KnownDoor:
                    if self._doors[directionIdx] == DOOR_STATUS.NonExistent:
                        self._doors[directionIdx] = DOOR_STATUS.U_NoDoorHandle
                    elif self._doors[directionIdx] == DOOR_STATUS.P_NewDoor:
                        self._doors[directionIdx] = DOOR_STATUS.P_KnownDoor
                        OPENINGS.val -= 1

            
    
    def go_to(self, DoorChoice) -> (int, int, int):
        global LOCATIONS, CURRENT_LOCATION, ABSOLUTE_ROOM_NUM, OPENINGS

        if self._doors[DoorChoice] == DOOR_STATUS.NonExistent:
            print("There is no door here.")
            return self.location
        
        elif self._doors[DoorChoice] == DOOR_STATUS.P_NewDoor:
            OPENINGS.val -= 1
            print(f"You venture on, discovering Room {ABSOLUTE_ROOM_NUM.val + 1}")
            ABSOLUTE_ROOM_NUM.val += 1
            self._doors[DoorChoice] = DOOR_STATUS.P_KnownDoor
            entry = find_other_direction(DoorChoice)
            LOCATIONS.val[self.nexLoc[DoorChoice]] = Room(entry,ABSOLUTE_ROOM_NUM.val, self.nexLoc[DoorChoice])
            return self.nexLoc[DoorChoice]
        
        elif self._doors[DoorChoice] == DOOR_STATUS.P_KnownDoor:
            print(f"You have been here before. This is Room {LOCATIONS.val[self.nexLoc[DoorChoice]].roomNum}")
            return self.nexLoc[DoorChoice]
        
        elif self._doors[DoorChoice] == DOOR_STATUS.U_NoDoorHandle:
            print("While there is a room on the opposite side of this wall, you are unable to access it from this side.")
            return self.location
        
    
    @property
    def doors(self):
        return self._doors