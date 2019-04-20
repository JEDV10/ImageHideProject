import math
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image


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


# ----- Hide Text Operations -----
end_string = "#&Ícaro&#"

def obtainAsciiRepresentation(char):
    """
    Return ASCII representation of given char
    """
    return ord(char)

def obtainBinaryRepresentation(num):
    """
    Return binary representation of given number (8 bits format)
    """
    return bin(num)[2:].zfill(8)

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

def hideText(message, original_image_path, output_image_path="C:/Users/EQUIPO/ImageHideProject.png"):
    """
    Main function to hide text inside images.
    It opens the image at given path, converts the given message to binary and
    modify LSBs of each pixel in the image acording to the binary representation
    of the original message
    """
    print("Hiding message...")
    print(original_image_path)
    print(type(original_image_path))
    print(message)
    print(type(message))
    image = Image.open(original_image_path)
    pixels = image.load()

    (columns, rows) = image.size

    list = obtainBitsList(message + end_string)
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

    if counter >= total_lenght:
        print("Message hidden correctly.")
    else:
        print("Warning: {} remaining chars."
              .format(math.floor((total_lenght - counter) / 8)))

    image.save(output_image_path)


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

def recoverText(textBlock, hidden_text_image_path):
    """
    Main function to recover text from images.
    It opens the modified image at given path, extracts LSBs from each pixel and
    reconstruct the message until it finds termination string
    """
    print("Recovering message...")
    image = Image.open(hidden_text_image_path)
    print(hidden_text_image_path)
    print(type(hidden_text_image_path))
    pixels = image.load()

    (columns, rows) = image.size

    byte = ""
    message = ""
    for x in range(rows):
        for y in range(columns):
            pixel = pixels[x, y]
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            byte += obtainLSB(obtainBinaryRepresentation(red))
            if len(byte) >= 8:
                message += charFromAscii(binaryToDecimal(byte))
                if (message[-9:] == end_string):
                    message = message[0:len(message) - 9]
                    break
                byte = ""

            byte += obtainLSB(obtainBinaryRepresentation(green))
            if len(byte) >= 8:
                message += charFromAscii(binaryToDecimal(byte))
                if (message[-9:] == end_string):
                    message = message[0:len(message) - 9]
                    break
                byte = ""

            byte += obtainLSB(obtainBinaryRepresentation(blue))
            if len(byte) >= 8:
                message += charFromAscii(binaryToDecimal(byte))
                if (message[-9:] == end_string):
                    message = message[0:len(message) - 9]
                    break
                byte = ""

        else:
            continue
        break
    print(message)
    textBlock.delete(1.0, END)
    textBlock.insert('1.0', message)