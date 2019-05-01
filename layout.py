from tkinter import *
from tkinter import messagebox
import operations as op

"""
Main class. It implements the main layout of the application.
Each functionality use one or several functions from "operations.py" module.
"""


def update(event):
    op.updateCharCounter(textBlock, charCounter, inputImagePath.get(), charLabel)


# ----- Graphic Interface -----
root = Tk()
root.title("Image Hide")

# ----- Options Bar -----
barMenu = Menu(root)
root.config(menu=barMenu, width=300, height=300)
# File menu
fileMenu = Menu(barMenu, tearoff=0)
fileMenu.add_command(label="Save Text", command=lambda:op.saveText(textBlock.get("1.0", 'end-1c')))
fileMenu.add_command(label="Clear", command=lambda:op.deleteFields(inputImagePath, charCounter, textBlock, passwordInput))
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=lambda:op.exitApp(root))
# App menu
appMenu = Menu(barMenu, tearoff=0)
appMenu.add_command(label="Hide text", command=lambda:op.hideText(textBlock.get("1.0", 'end-1c'), inputImagePath.get(),
                                                               passwordInput.get()))
appMenu.add_command(label="Recover text", command=lambda:op.recoverText(textBlock, passwordInput.get()))
# Help menu
helpMenu = Menu(barMenu, tearoff=0)
helpMenu.add_command(label="Help", command=lambda:op.helpMenu())
helpMenu.add_command(label="About", command=lambda:op.aboutMenu())

barMenu.add_cascade(label="File", menu=fileMenu)
barMenu.add_cascade(label="App", menu=appMenu)
barMenu.add_cascade(label="Help", menu=helpMenu)


# ----- Input Elements -----
inputImagePath = StringVar(value="")
passwordInput = StringVar(value="")
charCounter = StringVar(value="0/0 (0)")

pathFrame = Frame(root)
pathFrame.pack()

# Image Path and Password
pathLabel = Label(pathFrame, text="Image Path:")
pathLabel.grid(row=0, column=0, sticky="w", padx=10, pady=5)
pathEntry = Entry(pathFrame, textvariable=inputImagePath, width=47)
pathEntry.grid(row=0, column=1, padx=10, pady=5)
pathButton = Button(pathFrame, text="Select Image", command=lambda:op.imagePathFinder(inputImagePath))
pathButton.grid(row=0, column=2, sticky="e", padx=10, pady=5)
passLabel = Label(pathFrame, text="Password:")
passLabel.grid(row=1, column=0, sticky="w", padx=10, pady=5)
passEntry = Entry(pathFrame, textvariable=passwordInput, width=47)
passEntry.config(fg="red", show="*")
passEntry.grid(row=1, column=1, padx=10, pady=5)

textFrame = Frame(root)
textFrame.pack()

# Text
textLabel = Label(textFrame, text="Text:")
textLabel.grid(row=0, column=0, sticky="ne", padx=5, pady=20)
textBlock = Text(textFrame, width=50, height=20)
textBlock.grid(row=0, column=1, padx=10, pady=20)
textBlock.bind("<KeyRelease>", update)
scrollVert = Scrollbar(textFrame, command=textBlock.yview)
scrollVert.grid(row=0, column=2, sticky="nsew")
textBlock.config(yscrollcommand=scrollVert.set)
charLabel = Label(textFrame, textvariable=charCounter)
charLabel.grid(row=1, column=1, sticky="nw", padx=10, pady=5)


# ----- Operation Buttons -----
buttonsFrame = Frame(root)
buttonsFrame.pack()

# Hide
hideButton = Button(buttonsFrame, text="Hide Text", command=lambda:op.hideText(textBlock.get("1.0", 'end-1c'),
                                                                            inputImagePath.get(), passwordInput.get()))
hideButton.grid(row=0, column=0, sticky="e", padx=10, pady=10)
# Recover
recoverButton = Button(buttonsFrame, text="Recover Text", command=lambda:op.recoverText(textBlock, passwordInput.get()))
recoverButton.grid(row=0, column=1, sticky="e", padx=10, pady=10)

root.mainloop()