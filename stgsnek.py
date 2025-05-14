import numpy as np

def get_bin_char(character):
    utf8_bytes = character.encode('utf-8')
    bits = []
    for byte in utf8_bytes:
        bits += [int(b) for b in format(byte, '08b')]
    return bits

def get_bin_str(string):
    ret = []
    for character in string:
        ret += get_bin_char(character)
    ret += [0]*8
    return ret

def encode(image, bin_string, starting_point=0):
    
    x = bin_string
    x = np.array(x, dtype=np.uint8)

    if x.size + starting_point > image.size:
        raise ValueError("Obraz jest za mały, żeby zakodowac cały tekst")


    imageRound = image.copy()
    imageRound = image - image%2
    imageRound = imageRound.flatten()
    imageRound[starting_point:x.size+starting_point] += x
    
   
    return np.reshape(imageRound, image.shape)

def decode_utf8(image, read_every_n_bits=8, start_point=0):
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
    return string


def decode(image, read_every_n_bits=7, start_point=0):
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


# filepath: c:\Users\User\Desktop\Studia\Semestr 2\Python\Projekt\stgsnek.py
def caesar_encode(message, shift):
    encoded_message = ""
    for char in message:
        encoded_message += chr((ord(char) + shift) % 0x110000)  # zakres pełnego Unicode
    return encoded_message

def caesar_decode(message, shift):
    decoded_message = ""
    for char in message:
        decoded_message += chr((ord(char) - shift) % 0x110000)
    return decoded_message
