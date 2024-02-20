import random

from global_vars import *

class Room:
    def __init__(self, entry, roomNum, location):
        global LOCATIONS, OPENINGS, RNG

        self.doors = [0,0,0,0]
        self.location = location
        if entry > -1:
            self.doors[entry] = 2
        self.roomNum = roomNum
        self.nexLoc = []
        for i in range(4):
            if i == 0:
                self.nexLoc.append((location[0], location[1] + 1))
            elif i == 1:
                self.nexLoc.append((location[0] + 1, location[1]))
            elif i == 2:
                self.nexLoc.append((location[0], location[1] - 1))
            elif i == 3:
                self.nexLoc.append((location[0] - 1, location[1]))

            chance = random.random()
            if i == entry:
                if chance < RNG.val['Entrance Lock']:
                    self.doors[i] = 3
                    print('As you venture into the Room, the door you just used closes, revealing a lack of an opening mechanism from this side!')
                continue
            
            chance = random.random()
            if self.nexLoc[i] in LOCATIONS.val.keys():
                if chance > RNG.val['Suddenly Secret Door']:
                    self.doors[i] = 2
                else:
                    self.doors[i] = 3
            elif chance < RNG.val['Random Room Spawn']:
                self.doors[i] = 1
                OPENINGS.val += 1
        
        self.trap = len(list(filter(lambda x: x == 2 or x == 1, self.doors))) == 0 and entry > -1

        
        LOCATIONS.val[location] = self


    def __str__(self) -> str:
        global LOCATIONS

        message = f"This is Room {self.roomNum}\n"
        directions = ["north", "east", "south", "west"]
        for idx in range(4):
            if self.doors == 0:
                if self.nexLoc[idx] in LOCATIONS.val.keys():
                    message += f"To the {directions[idx]} you remember the presence of Room {LOCATIONS.val[self.nexLoc[idx]].roomNum}, but see no doorway leading to it.\n"
            elif self.doors[idx] > 0:              
                if self.doors[idx] == 2:
                    message += f"\tThe room has a door to the {directions[idx]}. "
                    message += f"The door is leads to Room {LOCATIONS.val[self.nexLoc[idx]].roomNum}.\n"
                elif self.doors[idx] == 3:
                    message += f"\tTo the {directions[idx]}, you know of the presence of a hidden door. "
                    message += f"The door is connected to Room {LOCATIONS.val[self.nexLoc[idx]].roomNum}, but you cannot open it from this side.\n"
                else:
                    message += f"\t{directions[idx].capitalize()}side, you notice a door. "
                    message += f"The door remains unopened, and you don't know where it leads.\n"
        return message
    

    def update(self):
        global LOCATIONS, OPENINGS

        for idx in range(4):
            if self.nexLoc[idx] in LOCATIONS.val.keys():
                otherIdx = idx - 2
                if otherIdx < 0:
                    otherIdx = idx + 2
                
                otherDoor = LOCATIONS.val[self.nexLoc[idx]].doors[otherIdx]
                if otherDoor == 2:
                    if self.doors[idx] == 0:
                        self.doors[idx] = 3
                    elif self.doors[idx] == 1:
                        self.doors[idx] = 2
                        OPENINGS.val -= 1

            
    
    def go_to(self, doorChoice):
        global LOCATIONS

        doorNum = 'nesw'.index(doorChoice)

        if self.doors[doorNum] == 0:
            print("There is no door here.")
            return self
        elif self.doors[doorNum] == 1:
            global ABSOLUTE_ROOM_NUM, OPENINGS

            OPENINGS.val -= 1
            print(f"You venture on, discovering Room {ABSOLUTE_ROOM_NUM.val + 1}")
            ABSOLUTE_ROOM_NUM.val += 1
            self.doors[doorNum] = 2
            entry = doorNum - 2
            if entry < 0:
                entry = doorNum + 2
            return Room(entry,ABSOLUTE_ROOM_NUM.val, self.nexLoc[doorNum])
        elif self.doors[doorNum] == 2:
            print(f"You have been here before. This is Room {LOCATIONS.val[self.nexLoc[doorNum]].roomNum}")
            return LOCATIONS.val[self.nexLoc[doorNum]]
        elif self.doors[doorNum] == 3:
            print("While there is a room on the opposite side of this wall, you are unable to access it from this side.")
            return self