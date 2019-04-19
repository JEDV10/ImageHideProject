import numpy as np
from tkinter import *
from tkinter import filedialog


def imagePathFinder(path):
    '''
    Obtain path to the main image
    '''
    image = filedialog.askopenfilename(title="Open", initialdir="C:", filetypes=(("Images", "*.png"), ("All Files", "*.*")))
    path.set(image)


def deleteFields(inputImagePath, charCounter, textBlock):
    '''
    Erase all data in each input field
    '''
    inputImagePath.set("")
    charCounter.set("")
    textBlock.delete(1.0, END)


