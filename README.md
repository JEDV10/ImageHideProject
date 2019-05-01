# ImageHideProject
App in Python (3.x) for hiding text inside images.

## Getting Started
It uses _NumPy_ and _scikit-image_ in order to modify LSB of each pixel hiding a text previously coded in UTF-16.
It also uses _Crypto_ to encrypt and decrypt the message (SHA-256).

Graphic Interface created using _Tkinter_

### Prerequisites
Project created on Windows.

_NumPy_, _scikit-image_, _Crypto_ and _Tkinter_ libraries are necessary (_Tkinter_ library comes in default with every Python installation).
Installation using "pip":
```
pip install numpy
pip install scikit-image
pip install pycrypto
```
Installation in anaconda environment:
```
conda install numpy
conda install -c conda-forge scikit-image
conda install -c anaconda pycrypto
```

## Running the tests
How to use main functionalities:

    - Hide Text: It allows you to hide text inside an image.
        1) Choose your image using "Select Image" button.
        2) Type the password that you want (or leave it blank if you do not want any password).
        3) Write your text on the "Text" block.
        4) Save the new image with the "Hide Text" button.
        
    - Recover Text: It allows you to recover the hidden text.
        1) Type the correct password (it can be blank).
        2) Select the modified image with "Recover Text".
        3) Save your text as ".txt" using "File -> Save Text".

## Authors
* **J. Enrique Domínguez** - (je.dominguez.vidal@gmail.com)

## License
This project is licensed under GNU License.