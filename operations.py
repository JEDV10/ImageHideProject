import numpy as np
from tkinter import filedialog


def imagePathFinder(path):
    '''
    Obtain path to the main image
    '''
    image = filedialog.askopenfilename(title="Open", initialdir="C:", filetypes=(("Images", "*.png"), ("All Files", "*.*")))
    path.set(image)