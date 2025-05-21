class CaesarCipher:
    def __new__(cls, message=None, shift=None):
        if message is not None and not isinstance(message, str):
            raise TypeError("Wiadomość musi być ciągiem znaków")
        if shift is not None and not isinstance(shift, int):
            raise TypeError("Przesunięcie musi być liczbą całkowitą")
            
        return super().__new__(cls)
    
    @staticmethod
    def encode(message, shift):
        if not isinstance(message, str):
            raise TypeError("Wiadomość musi być ciągiem znaków")
        if not isinstance(shift, int):
            raise TypeError("Przesunięcie musi być liczbą całkowitą")
            
        encoded_message = ""
        for char in message:
            encoded_message += chr((ord(char) + shift) % 0x110000)  # zakres pełnego Unicode
        return encoded_message

    @staticmethod
    def decode(message, shift):
        if not isinstance(message, str):
            raise TypeError("Wiadomość musi być ciągiem znaków")
        if not isinstance(shift, int):
            raise TypeError("Przesunięcie musi być liczbą całkowitą")
            
        decoded_message = ""
        for char in message:
            decoded_message += chr((ord(char) - shift) % 0x110000)
        return decoded_message
    
