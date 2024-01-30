import random
import os

from global_vars import *
import Room
OPENINGS = 0
ABSOLUTE_ROOM_NUM = 1
LOCATIONS = {}
RANDOM_MODS = {'Random Room Spawn': 0.3,        # The chances of a new door to spawn
               'Entrance Lock': 0.3,            # The chances that you cannot head back the way you came from
               'Suddenly Secret Door': 0.5}     # The chances that a door that should lead to another room is locked from this side

# Doors: Up, Right, Down, Left
# Door Signs: 0-> absent, 1-> closed, 2-> opened, 3-> opennable from other side only
class Room:
    def __init__(self, entry, roomNum, location):
        global LOCATIONS, OPENINGS, RANDOM_MODS

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
                if chance < RANDOM_MODS['Entrance Lock']:
                    self.doors[i] = 3
                    print('As you venture into the Room, the door you just used closes, revealing a lack of an opening mechanism from this side!')
                continue
            
            chance = random.random()
            if self.nexLoc[i] in LOCATIONS.keys():
                if chance > RANDOM_MODS['Suddenly Secret Door']:
                    self.doors[i] = 2
                else:
                    self.doors[i] = 3
            elif chance < RANDOM_MODS['Random Room Spawn']:
                self.doors[i] = 1
                OPENINGS += 1
        
        self.trap = len(list(filter(lambda x: x == 2 or x == 1, self.doors))) == 0 and entry > -1

        
        LOCATIONS[location] = self


    def __str__(self) -> str:
        global LOCATIONS

        message = f"This is Room {self.roomNum}\n"
        directions = ["north", "east", "south", "west"]
        for idx in range(4):
            if self.doors == 0:
                if self.nexLoc[idx] in LOCATIONS.keys():
                    message += f"To the {directions[idx]} you remember the presence of Room {LOCATIONS[self.nexLoc[idx]].roomNum}, but see no doorway leading to it.\n"
            elif self.doors[idx] > 0:              
                if self.doors[idx] == 2:
                    message += f"\tThe room has a door to the {directions[idx]}. "
                    message += f"The door is leads to Room {LOCATIONS[self.nexLoc[idx]].roomNum}.\n"
                elif self.doors[idx] == 3:
                    message += f"\tTo the {directions[idx]}, you know of the presence of a hidden door. "
                    message += f"The door is connected to Room {LOCATIONS[self.nexLoc[idx]].roomNum}, but you cannot open it from this side.\n"
                else:
                    message += f"\t{directions[idx].capitalize()}side, you notice a door. "
                    message += f"The door remains unopened, and you don't know where it leads.\n"
        return message
    

    def update(self):
        global LOCATIONS, OPENINGS

        for idx in range(4):
            if self.nexLoc[idx] in LOCATIONS.keys():
                otherIdx = idx - 2
                if otherIdx < 0:
                    otherIdx = idx + 2
                
                otherDoor = LOCATIONS[self.nexLoc[idx]].doors[otherIdx]
                if otherDoor == 2:
                    if self.doors[idx] == 0:
                        self.doors[idx] = 3
                    elif self.doors[idx] == 1:
                        self.doors[idx] = 2
                        OPENINGS -= 1

            
    
    def go_to(self, doorChoice):
        global LOCATIONS

        doorNum = 'nesw'.index(doorChoice)

        if self.doors[doorNum] == 0:
            print("There is no door here.")
            return self
        elif self.doors[doorNum] == 1:
            global ABSOLUTE_ROOM_NUM, OPENINGS

            OPENINGS -= 1
            print(f"You venture on, discovering Room {ABSOLUTE_ROOM_NUM + 1}")
            ABSOLUTE_ROOM_NUM += 1
            self.doors[doorNum] = 2
            entry = doorNum - 2
            return Room(entry,ABSOLUTE_ROOM_NUM, self.nexLoc[doorNum])
        elif self.doors[doorNum] == 2:
            print(f"You have been here before. This is Room {LOCATIONS[self.nexLoc[doorNum]].roomNum}")
            return LOCATIONS[self.nexLoc[doorNum]]
        elif self.doors[doorNum] == 3:
            print("While there is a room on the opposite side of this wall, you are unable to access it from this side.")
            return self

def print_txt(fileName):
    fileName = "./Averkorf_txt/" + fileName + ".txt"
    file = open(fileName, "r")
    print(file.read())
    file.close()

def screen_clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')
        
def print_help():
    print("Here is a list of available commands")
    print("[H]elp\t\tList this menu")
    print("[R]oom\t\tList current room information")
    print("[L]ist\t\t List all rooms located")
    print("[M]ove\t\tGo to door in a specified direction:")
    print("\t\t[mN]orth")
    print("\t\t[mE]ast")
    print("\t\t[mS]outh")
    print("\t\t[mW]est")
    print("[W]ait\t\tIf the dungeon is too hard today, exit and come again tomorrow.")
    print("[G]ive up\t\tThis pursuit is getting pointless.")
    print("[Q]uit Game") 

def print_information():
    print('TREASURE HUNTERS')
    print('----------------')
    print('You are an adventurer, who has just entered the treasure dungeon.')
    print('Your goal, for reasons known only to you is to find treasure beyond all rational thought.')
    print('Legend says that the dungeon rewards only those who can navigate 100 unique rooms of the dungeon, and come out alive to tell the tale.')
    print('Legend also says that the dungeon is cursed and evershifting, its architecture changing every day.')
    print('There are tales of warriors who have entered and never foudn their way out, their corpses unseen to this day within this ever evolving structure.')
    print('Find the treasure, get out, be rich.')
    print('If you feel that today the dungeon is feeling cruel just come back tomorrow')
    input('Press Enter to go back to the menu.')

def print_locations():
    global LOCATIONS

    message = 'You wip out your catalogous to see these locations: \n'
    counter = 0
    for i in LOCATIONS.keys():
        message += f"Room {LOCATIONS[i].roomNum} is at {i} \t"
        counter += 1
        if counter == 7:
            counter = 0
            message += '\n'
    print(message)
        


def play_game() -> bool:
    global OPENINGS, LOCATIONS, ABSOLUTE_ROOM_NUM

    play = True
    input("You start in Room 1. Location: 0,0. Press Enter to continue.")
    room = Room.Room(-1, 1, (0,0))
    while play:
        print(f"\nOpenings: {OPENINGS}")
        room.update()
        if room.trap:
            print("You realize that this room has no exit and that you are trapped.")
            print("To your horror, you realise, that you will be added to the list of sould that lost their lives here.")
            print("There is nothing to do, but to wait a slow, torturous and isolated death.")
            input("Press Enter to go to the main menu")
            return True

        choice = str(input("Choose option (h for help): ")).lower()
        if choice == 'h':
            print_txt("HelpListCommands")
        elif choice == 'r':
            print(room)
        elif len(choice) > 1 and choice[0] == 'm':
            try:
                doorChoice = choice[1].lower()
                if doorChoice in 'news':
                    room = room.go_to(doorChoice)
                else:
                    print('Wrong moving direction.')
            except Exception as error:
                print(error)
                print("Incorrect moving input.")
                continue
        elif choice == 'l':
            print_locations()
        elif choice == 'q':
            play = False
        elif choice == 'g':
            if room.roomNum == 1:
                print_txt("E2LeaveDungeon")
                input("Press Enter to return to the main menu")
            else:
                print('You have given up hope. You wander aimlessly around the dungeon as you await your inevitable starvation.')
                input("Press Enter to return to the main menu")
            return True
        elif choice == 'w':
            if room.roomNum == 1:
                print_txt("WaitForReshuffle")
                ABSOLUTE_ROOM_NUM, OPENINGS = 1, 0
                LOCATIONS = {}
                room = Room.Room(-1, 1, (0,0))
            else:
                print("Waiting for the dungeon to shift while inside it, will likely trap you in there forever.")
                print("Instead of sentencing yourself to a very cruel suicide, you think of other options instead.")
                print("After some consideration you decide that it is best to either move on or exit the dungeon first.")
        else: 
            print("Command not recognized. Try again")
    return False

def main():
    global ABSOLUTE_ROOM_NUM, LOCATIONS, OPENINGS

    game = True
    while game:
        screen_clear()
        choice = str(input("AVERKORF DUNGEON\n-[P]lay\n-[I]nfo\n-[Q]uit\nYour Input here: ")).lower()
        if choice == 'p':
            ABSOLUTE_ROOM_NUM = 1
            LOCATIONS = {}  
            OPENINGS = 0
            game = play_game()
        elif choice == 'i':
            screen_clear()
            print_txt("GameLore")
            input('Press Enter to go back to the menu.')
        elif choice == 'q':
            return 0
        else:
            input("Command not recognized. Press enter to try again.")


if __name__ == "__main__":
    main()