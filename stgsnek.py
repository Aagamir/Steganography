import numpy as np
from datetime import datetime

class Steganography:
    def __new__(cls, image=None, text=None, shift=None):
        if image is not None and not isinstance(image, np.ndarray):
            raise TypeError("Obraz musi być tablicą numpy")
        if text is not None and not isinstance(text, str):
            raise TypeError("Tekst musi być ciągiem znaków")
        if shift is not None and not isinstance(shift, int):
            raise TypeError("Przesunięcie musi być liczbą całkowitą")
        
        return super().__new__(cls)
    
    @staticmethod
    def get_bin_char(character):
        if not isinstance(character, str) or len(character) != 1:
            raise ValueError("Oczekiwano pojedynczego znaku")
            
        utf8_bytes = character.encode('utf-8')
        bits = []
        for byte in utf8_bytes:
            bits += [int(b) for b in format(byte, '08b')]
        return bits

    @staticmethod
    def get_bin_str(string):
        if not isinstance(string, str):
            raise TypeError("Oczekiwano ciągu znaków")
            
        ret = []
        for character in string:
            ret += Steganography.get_bin_char(character)
        ret += [0]*8  # Dodajemy znacznik końca
        return ret

    @staticmethod
    def encode(image, bin_string, starting_point=0):
        if not isinstance(image, np.ndarray):
            raise TypeError("Obraz musi być tablicą numpy")
        if not isinstance(bin_string, (list, np.ndarray)):
            raise TypeError("Ciąg bitów musi być listą lub tablicą numpy")
        if not isinstance(starting_point, int) or starting_point < 0:
            raise ValueError("Punkt startowy musi być nieujemną liczbą całkowitą")
            
        x = np.array(bin_string, dtype=np.uint8)

        if x.size + starting_point > image.size:
            raise ValueError("Obraz jest za mały, żeby zakodować cały tekst")

        image_round = image.copy()
        image_round = image - image % 2
        image_round = image_round.flatten()
        image_round[starting_point:x.size+starting_point] += x
       
        return np.reshape(image_round, image.shape), datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def decode_utf8(image, read_every_n_bits=8, start_point=0):
        if not isinstance(image, np.ndarray):
            raise TypeError("Obraz musi być tablicą numpy")
        if not isinstance(read_every_n_bits, int) or read_every_n_bits <= 0:
            raise ValueError("Liczba bitów do odczytu musi być dodatnią liczbą całkowitą")
        if not isinstance(start_point, int) or start_point < 0:
            raise ValueError("Punkt startowy musi być nieujemną liczbą całkowitą")
            
        image_decoded = image.flatten()
        n = read_every_n_bits
        i = start_point
        still_reading = True
        string = ""
        byte_buffer = []
        
        while still_reading:
            byte = image_decoded[i:i+n] % 2
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
            i += 8
        return string

    @staticmethod
    def decode(image, read_every_n_bits=7, start_point=0):
        if not isinstance(image, np.ndarray):
            raise TypeError("Obraz musi być tablicą numpy")
        if not isinstance(read_every_n_bits, int) or read_every_n_bits <= 0:
            raise ValueError("Liczba bitów do odczytu musi być dodatnią liczbą całkowitą")
        if not isinstance(start_point, int) or start_point < 0:
            raise ValueError("Punkt startowy musi być nieujemną liczbą całkowitą")
            
        places = np.array([2**(6-i) for i in range(7)])
        image_decoded = image.flatten()
        n = read_every_n_bits
        i = start_point
        still_reading = True
        string = ""
        
        while still_reading:
            character = image_decoded[i:i+n] % 2
            character = np.sum(places * character)
            if character == 0:
                still_reading = False
            else:
                string += chr(character)
            i += 7
        return string
    
    @staticmethod
    def show_picture_capacity(image):
        if not isinstance(image, np.ndarray):
            raise TypeError("Obraz musi być tablicą numpy")
            
        image = image.flatten()
        return image.size // 8, image.size  #Rozmiar w bajtach (znakach) i bitach
    
    @staticmethod
    def message_character_count(message):
        if not isinstance(message, str):
            raise TypeError("Wiadomość musi być ciągiem znaków")
            
        return  len(message), len(message) * 8  # Rozmiar w bajtach (znakach) i bitach
