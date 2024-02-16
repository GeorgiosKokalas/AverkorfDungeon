import tkinter as tk 
import ttkbootstrap as ttkb


def create_menu():
    root = ttkb.Window()

    root.title("Averkorf Dungeon - Python")
    root.geometry("1000x350")

    pan = tk.PanedWindow(root, bd=4, orient='vertical', background = 'red', width = 200)
    pan.pack(side = 'left', fill='both')

    mybutton = ttkb.Button(text = "Click", bootstyle = "primary, outline")
    mybutton.pack(pady= 60)

 

    root.mainloop()

if __name__ == "__main__":
    create_menu()