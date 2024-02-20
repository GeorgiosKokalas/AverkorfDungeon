import os,sys

# Before Importing, we set the workign directory to be that of the script
# Then append the Code folder into our path
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("./Code/")

# Import what we need from the Code section
from Code.global_vars import *
import Code.Class_Room as Room
from Code.interface import run_interface
import Code.Class_Option as Option


def print_txt(fileName):
    fileName = "./txt_folder/" + fileName + ".txt"
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
      
        
def print_locations():
    global LOCATIONS

    message = 'You wip out your catalogous to see these locations: \n'
    counter = 0
    for i in LOCATIONS.val.keys():
        message += f"Room {LOCATIONS.val[i].roomNum} is at {i} \t"
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
        print(f"\nOpenings: {OPENINGS.val}")
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
                ABSOLUTE_ROOM_NUM.val, OPENINGS.val = 1, 0
                LOCATIONS.val = {}
                room = Room.Room(-1, 1, (0,0))
            else:
                print("Waiting for the dungeon to shift while inside it, will likely trap you in there forever.")
                print("Instead of sentencing yourself to a very cruel suicide, you think of other options instead.")
                print("After some consideration you decide that it is best to either move on or exit the dungeon first.")
        else: 
            print("Command not recognized. Try again")
    return False

def main_1():
    global ABSOLUTE_ROOM_NUM, LOCATIONS, OPENINGS

    game = True
    while game:
        screen_clear()
        choice = str(input("AVERKORF DUNGEON\n-[P]lay\n-[I]nfo\n-[Q]uit\nYour Input here: ")).lower()
        if choice == 'p':
            ABSOLUTE_ROOM_NUM.val = 1
            LOCATIONS.val = {}  
            OPENINGS.val = 0
            game = play_game()
        elif choice == 'i':
            screen_clear()
            print_txt("GameLore")
            input('Press Enter to go back to the menu.')
        elif choice == 'q':
            return 0
        else:
            input("Command not recognized. Press enter to try again.")

def print_info():
    backOption = Option.Option("Back to Main Menu", 1, "back")
    quitOption = Option.Option("Quit", 2, "quit")
    OptionsList = [backOption,quitOption]

    selectedOption = run_interface(OptionsList,AsciiArt=0,StatusText="MainMenuInfo")
    match selectedOption.command:
        case "back":
            return True
        case "quit":
            quit()


def main_menu():
    global ABSOLUTE_ROOM_NUM, LOCATIONS, OPENINGS
    playOption = Option.Option("Play", 1, "play")
    loadOption = Option.Option("Load", 2, "load")
    infoOption = Option.Option("Info", 3, "info")
    quitOption = Option.Option("Quit", 4, "quit")
    OptionsList = [playOption, loadOption, infoOption, quitOption]
    
    mainMenuActive = True
    while mainMenuActive:
        selectedOption = run_interface(OptionsList)
        match selectedOption.command:
            case "play":
                print("play")
            case "load":
                print("Load")
            case "info":
                print_info()
            case "quit":
                print("BuBye!")
                mainMenuActive = False


if __name__ == "__main__":
    main_menu()