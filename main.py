import numpy as np
import matplotlib.pyplot as plt
from IPython.display import IFrame


def read_image(url):
    image = plt.imread(url)
    print(image.shape)
    print(image.dtype)
    plt.imshow(image[:, :, 0]%2)
    plt.colorbar()
    plt.show()

def get_bin_char(character):
    x = [int(x) for x in bin(ord(character))[2:]]
    x = [0]*(7-len(x)) + x #Dla polskich znaków będzie 9-len(x)
    return x

def get_bin_str(string):
    ret = []
    for character in string:
        ret += get_bin_char(character)
    ret += [0]*7
    return ret

def encode(image, string):
    x = get_bin_str(string)
    x = np.array(x, dtype=np.uint8)

    imageRound = image.copy()
    imageRound = image - image%2
    imageRound = imageRound.flatten()
    imageRound[0:x.size] += x
    
    if x.size > imageRound.size:
        raise ValueError("Obraz jest za mały, żeby zakodowac cały tekst")

    return np.reshape(imageRound, image.shape)

def decode(image, read_every_n_bits = 7, start_point = 0):
    places = np.array([2**(6-i) for i in range(7)])
    imageDecoded = image.flatten()
    n = read_every_n_bits
    i = start_point
    still_reading = True
    string = ""
    while still_reading:
        character = imageDecoded[i:i+n]%2
        character = np.sum(places*character)
        if character == 0:
            still_reading = False
        else:
            string += chr(character)
        i += 7
    print(string)
    return(string)

#ReadImage("Python\\Projekt\\test.jpg")
#read_image("test.jpg")

image = plt.imread("test.jpg")
ImageEncoded = encode(image, "Ala ma kotą")

decode(ImageEncoded)
