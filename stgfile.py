from PIL import Image
import numpy as np
import os

class FileHandler:
    @staticmethod
    def load_image(file_path):
        """
        Wczytuje obraz z podanej ścieżki i zwraca jako tablice
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Plik {file_path} nie istnieje")
                
            img = Image.open(file_path)
            return np.array(img)
            
        except Exception as e:
            raise IOError(f"Błąd wczytywania obrazu: {str(e)}")

    @staticmethod
    def save_image(image_array, file_path):
        """
        Zapisuje obraz w podanej ścieżki z automatycznym wykrywaniem formatu
        """
        try:
            if not isinstance(image_array, np.ndarray):
                raise TypeError("Obraz musi być tablicą numpy")
                
            img = Image.fromarray(image_array.astype(np.uint8))
            
            # Konwersja dla formatów bez obsługi przezroczystości
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
            elif file_path.lower().endswith('.bmp'):
                img = img.convert('RGB')
            
            img.save(file_path)
            return True
            
        except Exception as e:
            raise IOError(f"Błąd zapisywania obrazu: {str(e)}")

    @staticmethod
    def load_text(file_path, encoding='utf-8'):
        """
        Wczytuje tekst z pliku z określonym kodowaniem
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Plik {file_path} nie istnieje")
                
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content
            
        except Exception as e:
            raise IOError(f"Błąd wczytywania pliku tekstowego: {str(e)}")

    @staticmethod
    def save_text(content, file_path, encoding='utf-8'):
        """
        Zapisuje tekst do pliku z określonym kodowaniem
        """
        try:
            if not isinstance(content, str):
                raise TypeError("Zawartość musi być ciągiem znaków")
                
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
            
        except Exception as e:
            raise IOError(f"Błąd zapisywania pliku tekstowego: {str(e)}")

    @staticmethod
    def get_supported_image_formats():
        """
        Zwraca listę obsługiwanych formatów obrazów
        """
        return {
            'PNG': '.png',
            'JPEG': '.jpg',
            'BMP': '.bmp',
            'TIFF': '.tiff'
        }

    @staticmethod
    def get_supported_text_formats():
        """
        Zwraca listę obsługiwanych formatów tekstowych
        """
        return {
            'Plain Text': '.txt',
            'Markdown': '.md',
            'JSON': '.json'
        }
