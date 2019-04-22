import math
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from PIL import Image
import numpy as np
from skimage import io


# ----- Variables -----
head_string = "@$€*XIII*€$@"
end_string = "#&Íkarvs&#"


# ----- Menu Operations -----
def imagePathFinder(path):
    """
    Obtain path to the main image
    """
    image = filedialog.askopenfilename(title="Open", initialdir="C:",
                                       filetypes=(("Images", "*.png"), ("All Files", "*.*")))
    path.set(image)


def deleteFields(inputImagePath, charCounter, textBlock):
    """
    Erase all data in each input field
    """
    inputImagePath.set("")
    charCounter.set("")
    textBlock.delete(1.0, END)


def exitApp(root):
    """
    Check that the user really wants to quit.
    In that case, destroy root
    """
    decision = messagebox.askquestion("Exit", "Do you want to exit?")
    if decision == "yes":
        root.destroy()


def obtainDateString():
    """
    Return string with current date in specific YYYY-MM-DD_HH.mm.SS format
    """
    now = datetime.now()
    date_format = "%Y-%m-%d_%H.%M.%S"
    return now.strftime(date_format)


def saveText(text):
    """
    Save text in "Text" widget.
    Creates a ".txt" file
    """
    date_string = obtainDateString()
    filename = filedialog.asksaveasfilename(initialfile= "ImageHide_text_"+date_string+".txt",
                                            defaultextension=".txt", title="Select file", initialdir="C:",
                                            filetypes=(("Text File", "*.txt"), ("All Files", "*.*")))
    try:
        f = open(filename, 'w')
        f.write(text)
        f.close()
        messagebox.showinfo("Info", "Text file saved correctly.")
    except FileNotFoundError:
        pass


def saveImage(initial_image_path, image):
    """
    Save new image with hidden message.
    Creates a ".png" file
    """
    date_string = obtainDateString()
    filename = filedialog.asksaveasfilename(initialfile="ImageHide_image_" + date_string + ".png",
                                            defaultextension=".png", title="Select file",
                                            initialdir=initial_image_path,
                                            filetypes=(("Images", "*.png"), ("All Files", "*.*")))
    image_uint8 = np.array(image, dtype=np.uint8) # Take care of this line. uint8 can convert 254 in 255.
    io.imsave(filename, image_uint8)
    messagebox.showinfo("Info", "Modified image saved correctly.")


def saveImage_old(initial_image_path, image):
    """
    Save new image with hidden message.
    Creates a ".png" file
    """
    date_string = obtainDateString()
    filename = filedialog.asksaveasfilename(initialfile="ImageHide_image_" + date_string + ".png",
                                            defaultextension=".png", title="Select file",
                                            initialdir=initial_image_path,
                                            filetypes=(("Images", "*.png"), ("All Files", "*.*")))
    image.save(filename)
    messagebox.showinfo("Info", "Modified image saved correctly.")


def helpMenu():
    """
    Help panel with instructions to use each functionality
    """
    messagebox.showinfo("Help",
    '''
    How to use main functionalities:
    
    - Hide Text: It allows you to hide text inside an image.
        1) Choose your image using "Select Image" button.
        2) Write your text on the "Text" block.
        3) Save the new image with the "Hide Text" button.
        
    - Recover Text: It allows you to recover the hidden text.
        1) Select the modified image with "Recover Text".
        2) Save your text as ".txt" using "File -> Save Text".
    ''')


def aboutMenu():
    """
    About panel with informations about the version
    """
    messagebox.showinfo("Help",
    '''Version:
    v0.2 (April 21, 2019)
    
Author:
    J. Enrique Domínguez
    (je.dominguez.vidal@gmail.com)
    ''')


def updateCharCounter(textBlock, charCounter, image_path, charLabel):
    if (image_path == ""):
        charCounter.set("0/0 (0)")
        textBlock.delete(1.0, END)
        messagebox.showwarning("Warning", "Select a valid image file before write.")
    else:
        # ----- Calculate max text length allowed -----
        image = io.imread(image_path)
        image_size = image.size
        char_limit = min(10, int(((image_size/16)/2)-len(head_string)-len(end_string)))
        size_text = len(textBlock.get("1.0", 'end-1c'))
        # ----- Check text is not longer than max length
        if (size_text >= char_limit):
            text = textBlock.get("1.0", 'end-1c')
            textBlock.delete(1.0, END)
            textBlock.insert(END, text[0:char_limit])
            size_text = len(textBlock.get("1.0", 'end-1c')) # As textBlock has just changed, must recalculate
            charLabel.config(fg="red")
        else:
            charLabel.config(fg="black")

        charCounter.set( str(size_text)+"/"+str(char_limit)+" ("+str(char_limit-size_text)+")" )



# ----- Hide Text Operations -----
def obtainAsciiRepresentation(char):
    """
    Return ASCII representation of given char
    """
    return ord(char)

def obtainBinaryRepresentation(num):
    """
    Return binary representation of given number (16 bits format)
    """
    return bin(num)[2:].zfill(16)

def changeLSB(byte, new_bit):
    """
    Change LSB of given byte
    """
    return byte[:-1] + str(new_bit)

def binaryToDecimal(binary):
    """
    Return decimal representation of given binary number
    """
    return int(binary, 2)

def changeColor(original_color, bit):
    """
    Change LSB of given byte
    """
    binary_color = obtainBinaryRepresentation(original_color)
    mod_color = changeLSB(binary_color, bit)
    return binaryToDecimal(mod_color)

def obtainBitsList(text):
    """
    Return list with each bit of each byte of each ASCII representation of given text
    """
    list = []
    for char in text:
        ascii_representation = obtainAsciiRepresentation(char)
        binary_representation = obtainBinaryRepresentation(ascii_representation)
        for bit in binary_representation:
            list.append(bit)
    return list

def obtainInitOutputImagePath(original_path):
    """
    Return path to folder where is the original path
    """
    return original_path[:(original_path.rfind("/"))]

def hideText(message, original_image_path):
    """
    Main function to hide text inside images.
    It opens the image at given path, converts the given message to binary and
    modify LSBs of each pixel in the image acording to the binary representation
    of the original message
    """
    try:
        # ----- Read image -----
        original_image = io.imread(original_image_path)
        original_shape = original_image.shape

        # ----- Create array with message -----
        bit_list = obtainBitsList(head_string + message + end_string)
        array_list = np.asarray(bit_list)
        if (len(original_shape) > 2):  # Color image
            array_list_expanded = np.append(array_list, np.zeros(
                ((original_shape[0] * original_shape[1] * original_shape[2])) - len(array_list)))
        else:  # B/W image
            array_list_expanded = np.append(array_list,
                                             np.zeros(((original_shape[0] * original_shape[1])) - len(array_list)))
        array_list_expanded = array_list_expanded.reshape(original_shape).astype(float)
        array_list_expanded = array_list_expanded.astype(int)

        # ----- Obtain modified image -----
        image_hidden = (original_image - (original_image % 2)) # Erase LSB
        image_hidden = image_hidden + array_list_expanded # Add new LSB

        # ----- Save modified image -----
        image_hidden_path = obtainInitOutputImagePath(original_image_path)
        saveImage(image_hidden_path, image_hidden)
    except OSError:
        messagebox.showwarning("Warning", "Select a valid image file. (.png)")
    except ValueError:
        pass


def hideText_old(message, original_image_path):
    """
    Main function to hide text inside images.
    It opens the image at given path, converts the given message to binary and
    modify LSBs of each pixel in the image acording to the binary representation
    of the original message
    """
    try:
        image = Image.open(original_image_path)
        pixels = image.load()

        (columns, rows) = image.size

        list = obtainBitsList(head_string + message + end_string)
        counter = 0
        total_lenght = len(list)
        for x in range(rows):
            for y in range(columns):
                if counter < total_lenght:
                    pixel = pixels[x, y]
                    red = pixel[0]
                    green = pixel[1]
                    blue = pixel[2]

                    if counter < total_lenght:
                        mod_red = changeColor(red, list[counter])
                        counter += 1
                    else:
                        mod_red = red

                    if counter < total_lenght:
                        mod_green = changeColor(green, list[counter])
                        counter += 1
                    else:
                        mod_green = green

                    if counter < total_lenght:
                        mod_blue = changeColor(blue, list[counter])
                        counter += 1
                    else:
                        mod_blue = blue

                    pixels[x, y] = (mod_red, mod_green, mod_blue)
                else:
                    break
            else:
                continue
            break

        if (counter < total_lenght):
            messagebox.showwarning("Warning", "Warning: {} remaining chars."
                  .format(math.floor((total_lenght - counter) / 16)))

        initial_image_path = obtainInitOutputImagePath(original_image_path)
        saveImage_old(initial_image_path, image)
    except OSError:
        messagebox.showwarning("Warning", "Select a valid image file.")


# ----- Recover Text Operations -----
def obtainLSB(byte):
    """
    Obtain LSB of given byte
    """
    return byte[-1]

def charFromAscii(numero):
    """
    Return char representation of given decimal number
    """
    return chr(numero)

def obtainModifiedImagePath():
    """
    Return path to modified image selected by user
    """
    return filedialog.askopenfilename(title="Open", initialdir="C:",
                                         filetypes=(("Images", "*.png"), ("All Files", "*.*")))

def recoverText(textBlock):
    """
    Main function to recover text from images.
    It opens the modified image at given path, extracts LSBs from each pixel and
    reconstruct the message until it finds termination string
    """
    try:
        # ----- Read image -----
        hidden_text_image_path = obtainModifiedImagePath()
        image_recovered = io.imread(hidden_text_image_path)

        # ----- Processing -----
        byte = 0
        message = ""
        counter = 0
        found = False

        info_recovered = image_recovered % 2 # Take LSBs
        info_recoverded_reshaped = info_recovered.ravel()
        for i in range(len(info_recoverded_reshaped)):
            byte = byte * 2 + info_recoverded_reshaped[i]
            counter += 1
            if counter >= 16:
                counter = 0
                message += charFromAscii(byte)
                if (message[-len(head_string):] == head_string):
                    message = ""
                    found = True
                if (message[-len(end_string):] == end_string):
                    message = message[0:len(message) - len(end_string)]
                    break
                byte = 0

        if found:
            textBlock.delete(1.0, END)
            textBlock.insert('1.0', message)
            messagebox.showinfo("Info", "Hidden text recovered correctly.")
        else:
            messagebox.showwarning("Warning", "No hidden text found. Try other image.")
    except AttributeError:
        messagebox.showwarning("Warning", "Select a valid image file.")
    except ValueError:
        pass


def recoverText_old(textBlock):
    """
    Main function to recover text from images.
    It opens the modified image at given path, extracts LSBs from each pixel and
    reconstruct the message until it finds termination string
    """
    try:
        hidden_text_image_path = obtainModifiedImagePath()
        image = Image.open(hidden_text_image_path)
        pixels = image.load()

        (columns, rows) = image.size

        byte = ""
        message = ""
        found = False
        for x in range(rows):
            for y in range(columns):
                pixel = pixels[x, y]
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                byte += obtainLSB(obtainBinaryRepresentation(red))
                if len(byte) >= 16:
                    message += charFromAscii(binaryToDecimal(byte))
                    if (message[-len(head_string):] == head_string):
                        message = ""
                        found = True
                    if (message[-len(end_string):] == end_string):
                        message = message[0:len(message) - len(end_string)]
                        break
                    byte = ""

                byte += obtainLSB(obtainBinaryRepresentation(green))
                if len(byte) >= 16:
                    message += charFromAscii(binaryToDecimal(byte))
                    if (message[-len(head_string):] == head_string):
                        message = ""
                        found = True
                    if (message[-len(end_string):] == end_string):
                        message = message[0:len(message) - len(end_string)]
                        break
                    byte = ""

                byte += obtainLSB(obtainBinaryRepresentation(blue))
                if len(byte) >= 16:
                    message += charFromAscii(binaryToDecimal(byte))
                    if (message[-len(head_string):] == head_string):
                        message = ""
                        found = True
                    if (message[-len(end_string):] == end_string):
                        message = message[0:len(message) - len(end_string)]
                        break
                    byte = ""

            else:
                continue
            break

        if found:
            textBlock.delete(1.0, END)
            textBlock.insert('1.0', message)
            messagebox.showinfo("Info", "Hidden text recovered correctly.")
        else:
            messagebox.showwarning("Warning", "No hidden text found. Try other image.")
    except AttributeError:
        messagebox.showwarning("Warning", "Select a valid image file.")