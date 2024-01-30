import tkinter as tk 
import ttkbootstrap as ttkb

root = ttkb.Window(themename="superhero")

root.title("TTK Bootstrap")
root.geometry("1000x350")

mylabel = ttkb.Label(text = "Label1", font=("Helvetica", 28), bootstyle="default")
mylabel.pack(pady = 50)

root.mainloop()
