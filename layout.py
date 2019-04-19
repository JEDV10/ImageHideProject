from tkinter import *
from tkinter import messagebox
import operations as op

'''
Main class. It implements the main layout of the application.
Each functionality use one or several functions from "operations.py" module.
'''

# ----- Graphic Interface -----
root = Tk()

# ----- Options Bar -----
barMenu = Menu(root)
root.config(menu=barMenu, width=300, height=300)
# File menu
fileMenu = Menu(barMenu, tearoff = 0)
fileMenu.add_command(label="Save")
fileMenu.add_command(label="Save As...")
fileMenu.add_command(label="Clear")
fileMenu.add_separator()
fileMenu.add_command(label="Exit")
# App menu
appMenu = Menu(barMenu, tearoff = 0)
appMenu.add_command(label="Hide text")
appMenu.add_command(label="Recover text")
# Help menu
helpMenu = Menu(barMenu, tearoff = 0)
helpMenu.add_command(label="Help")
helpMenu.add_command(label="About")

barMenu.add_cascade(label="File", menu=fileMenu)
barMenu.add_cascade(label="App", menu=appMenu)
barMenu.add_cascade(label="Help", menu=helpMenu)


root.mainloop()