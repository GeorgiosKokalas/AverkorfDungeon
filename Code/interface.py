import keyboard
import time
import Class_Option as Option
import os

def screen_clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')


def print_option(SingleOption, OptionIdx, SelectedOptionIdx, OptionsLength):
    if OptionIdx == SelectedOptionIdx%OptionsLength:
        print("\033[0;41m" + str(SingleOption) + "\033[0m")
    else:
       print(SingleOption)


def update_interface(OptionsList, SelectedOptionIdx = 0, AsciiArt = 0, StatusText = 0, TxtPointer = True):
    if AsciiArt != 0:
        asciiFile = open( "./ascii/"+AsciiArt+".txt", "r")
        print(asciiFile.read())
        asciiFile.close()
    
    if StatusText !=0:
        print("------------------------------")
        if TxtPointer:
            statusFile = open( "./txt_folder/"+StatusText+".txt", "r")
            print(statusFile.read())
            statusFile.close()
        else:
            print(StatusText)


    print("------------------------------")
    for idx in range(len(OptionsList)):
        print_option(OptionsList[idx], idx, SelectedOptionIdx, len(OptionsList))
    
    # print(SelectedOptionIdx)
    return keyboard.read_key(suppress=True)
    

def run_interface(OptionsList=0, AsciiArt = 0, StatusText = 0, TxtPointer = True) -> Option.Option:
    position = 0
    isInterfaceRunning = True
    while isInterfaceRunning:
        screen_clear()
        key = update_interface(OptionsList,position, AsciiArt, StatusText, TxtPointer)
        match key:
            case "up":
                position -= 1
            case "down":
                position += 1
            case "enter":
                isInterfaceRunning = False
        time.sleep(0.15)
    return OptionsList[position%len(OptionsList)]

if __name__ == "__main__":
    run_interface()