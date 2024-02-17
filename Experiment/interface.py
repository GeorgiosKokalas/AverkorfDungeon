import keyboard
import time


def print_option(SingleOption, OptionIdx, SelectedOptionIdx):
    if OptionIdx == SelectedOptionIdx:
        print("\033[0;41m")

    print(SingleOption)

    if OptionIdx == SelectedOptionIdx:
        print("\033[0m")



def update_interface(OptionsList, SelectedOptionIdx = 0, AsciiArt = 0, StatusText = 0):
    if AsciiArt != 0:
        print(AsciiArt)
    
    if StatusText !=0:
        print("------------------------------")
        print(StatusText)

    print("------------------------------")
    for idx in range(len(OptionsList)):
        print_option(OptionsList, idx, SelectedOptionIdx)

    

    
    


def main():
    print("Press 's' to run the script or 'q' to quit.")
    print(keyboard.read_key())
    i = 1
    while True:
        key = keyboard.read_key()
        if key == 'up':
            print("Running script...", i)
            i+=1
        elif key == 'q':
            print("Exiting...")
            break
        time.sleep(0.5)

if __name__ == "__main__":
    main()