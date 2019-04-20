from tkinter import *
from tkinter import messagebox
import operations as op

"""
Main class. It implements the main layout of the application.
Each functionality use one or several functions from "operations.py" module.
"""


def update(event):
    charCounter.set(str(len(textBlock.get("1.0", 'end-1c'))))


# ----- Graphic Interface -----
root = Tk()
root.title("Image Hide App")

# ----- Options Bar -----
barMenu = Menu(root)
root.config(menu=barMenu, width=300, height=300)
# File menu
fileMenu = Menu(barMenu, tearoff=0)
fileMenu.add_command(label="Save Image")
fileMenu.add_command(label="Save Text")
fileMenu.add_command(label="Clear", command=lambda:op.deleteFields(inputImagePath, charCounter, textBlock))
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=lambda:op.exitApp(root))
# App menu
appMenu = Menu(barMenu, tearoff=0)
appMenu.add_command(label="Hide text")
appMenu.add_command(label="Recover text")
# Help menu
helpMenu = Menu(barMenu, tearoff=0)
helpMenu.add_command(label="Help")
helpMenu.add_command(label="About")

barMenu.add_cascade(label="File", menu=fileMenu)
barMenu.add_cascade(label="App", menu=appMenu)
barMenu.add_cascade(label="Help", menu=helpMenu)


# ----- Input Elements -----
inputImagePath = StringVar()
charCounter = StringVar()

pathFrame = Frame(root)
pathFrame.pack()

# Image Path
pathLabel = Label(pathFrame, text="Image Path:")
pathLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)
pathEntry = Entry(pathFrame, textvariable=inputImagePath, width=47)
pathEntry.grid(row=0, column=1, padx=10, pady=10)
pathButton = Button(pathFrame, text="Select Image", command=lambda:op.imagePathFinder(inputImagePath))
pathButton.grid(row=0, column=2, sticky="e", padx=10, pady=10)

textFrame = Frame(root)
textFrame.pack()

# Text
textLabel = Label(textFrame, text="Text:")
textLabel.grid(row=0, column=0, sticky="ne", padx=5, pady=10)
textBlock = Text(textFrame, width=50, height=10)
textBlock.grid(row=0, column=1, padx=10, pady=10)
textBlock.bind("<KeyRelease>", update)
scrollVert = Scrollbar(textFrame, command=textBlock.yview)
scrollVert.grid(row=0, column=2, sticky="nsew")
textBlock.config(yscrollcommand=scrollVert.set)
charLabel = Label(textFrame, textvariable=charCounter)
charLabel.grid(row=1, column=0, sticky="ne", padx=10, pady=10)


# ----- Operation Buttons -----
buttonsFrame = Frame(root)
buttonsFrame.pack()

# Hide
hideButton = Button(buttonsFrame, text="Hide Text", command=lambda:op.hideText(textBlock.get("1.0", 'end-1c'), inputImagePath.get()))
hideButton.grid(row=0, column=0, sticky="e", padx=10, pady=10)
# Recover
recoverButton = Button(buttonsFrame, text="Recover Text", command=lambda:op.recoverText("C:/Users/EQUIPO/ImageHideProject.png"))
recoverButton.grid(row=0, column=1, sticky="e", padx=10, pady=10)



root.mainloop()