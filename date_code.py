from datetime import datetime
import hashlib

class DateCipher:
    def __new__(cls, custom_date=None):
        instance = super().__new__(cls)
        
        # Inicjalizacja atrybutów instancji
        instance.date_format = "%Y-%m-%d %H:%M:%S"
        instance.date_key = custom_date or datetime.now().strftime(instance.date_format)
        
        return instance
    
    def _generate_key(self):
        """Generuje klucz szyfrujący na podstawie daty"""
        hash_object = hashlib.sha256(self.date_key.encode())
        return hash_object.hexdigest()
    
    def encrypt(self, message):
        """Szyfrowanie wiadomości"""
        if not isinstance(message, str):
            raise TypeError("Wiadomość musi być ciągiem znaków")
            
        key = self._generate_key()
        encrypted = []
        
        for i, char in enumerate(message):
            key_part = ord(key[i % len(key)])
            encrypted_char = chr(ord(char) ^ key_part)
            encrypted.append(encrypted_char)
        
        return ''.join(encrypted)
    
    def decrypt(self, encrypted_message):
        """Deszyfrowanie wiadomości"""
        return self.encrypt(encrypted_message)  # XOR jest odwracalny tym samym kluczem