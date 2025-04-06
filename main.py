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
    utf8_bytes = character.encode('utf-8')
    bits = []
    for byte in utf8_bytes:
        bits += [int(b) for b in format(byte, '08b')]
    #x = [int(x) for x in bin(ord(character))[2:]]
    #x = [0]*(7-len(x)) + x #Dla polskich znaków będzie 9-len(x)
    #return x
    return bits

def get_bin_str(string):
    ret = []
    for character in string:
        ret += get_bin_char(character)
    ret += [0]*8
    return ret

def encode(image, string, starting_point=0):
    x = get_bin_str(string)
    x = np.array(x, dtype=np.uint8)

    imageRound = image.copy()
    imageRound = image - image%2
    imageRound = imageRound.flatten()
    imageRound[starting_point:x.size] += x
    
    if x.size > imageRound.size:
        raise ValueError("Obraz jest za mały, żeby zakodowac cały tekst")

    return np.reshape(imageRound, image.shape)

def decode(image, read_every_n_bits=8, start_point=0):
    #places = np.array([2**(6-i) for i in range(7)])
    imageDecoded = image.flatten()
    n = read_every_n_bits
    i = start_point
    still_reading = True
    string = ""
    byte_buffer = []
    while still_reading:
        byte = imageDecoded[i:i+n]%2
        byte_val = int("".join(map(str, byte)), 2)
        if byte_val == 0:
            still_reading = False
        else: 
            byte_buffer.append(byte_val)

            try:
                char = bytes(byte_buffer).decode("utf-8")
                string += char
                byte_buffer = []
            except UnicodeDecodeError:
                pass
        i+=8
    print(string)
    return string

        #character = imageDecoded[i:i+n]%2
        #character = np.sum(places*character)
        #if character == 0:
        #    still_reading = False
        #else:
        #    string += chr(character)
        #i += 7
    #print(string)
    #return(string)

#ReadImage("Python\\Projekt\\test.jpg")
#read_image("test.jpg")

image = plt.imread("test.jpg")
ImageEncoded = encode(image, "Ala ma kotą,!/ i żółwia")

decode(ImageEncoded)
