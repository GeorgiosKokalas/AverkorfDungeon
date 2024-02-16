import keyboard

def main():
    print("Press 's' to run the script or 'q' to quit.")
    print(keyboard.read_key())
    # i = 1
    # while True:
    #     key = keyboard.read_key()
    #     if key == 'up':
    #         print("Running script...", i)
    #         i+=1
    #     elif key == 'q':
    #         print("Exiting...")
    #         break

if __name__ == "__main__":
    main()