from datetime import datetime
import hashlib
import base64

class DateCipher:
    def __new__(cls, custom_date=None):
        instance = super().__new__(cls)
        instance.date_format = "%Y-%m-%d"
        if custom_date:
            try:
                datetime.strptime(custom_date, instance.date_format)
                instance.date_key = custom_date
            except ValueError:
                raise ValueError(f"Data musi być w formacie {instance.date_format} (np. 2025-06-04)")
        else:
            instance.date_key = datetime.now().strftime(instance.date_format)
        return instance
    
    def get_date_key(self):
        """Zwraca datę używaną jako klucz"""
        return self.date_key
    
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
        
        # Zamieniamy na bity i zapisujemy jako base64 dla łatwego zapisu
        encrypted_bytes = ''.join(encrypted).encode('utf-8')
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    
    def decrypt(self, encrypted_message):
        """Deszyfrowanie wiadomości"""
        # Dekodujemy z base64 na bity a potem do stringa
        encrypted_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
        encrypted_str = encrypted_bytes.decode('utf-8')
        # Do odszywrowania używamy tej samej logiki co do szyfrowania
        key = self._generate_key()
        decrypted = []
        for i, char in enumerate(encrypted_str):
            key_part = ord(key[i % len(key)])
            decrypted_char = chr(ord(char) ^ key_part)
            decrypted.append(decrypted_char)
        return ''.join(decrypted)