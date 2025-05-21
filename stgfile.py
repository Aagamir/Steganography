from PIL import Image
import numpy as np

class ImageHandler:
    def __new__(cls, image=None, file_name=None):
        if image is not None and not isinstance(image, np.ndarray):
            raise TypeError("Image must be a numpy array")
        if file_name is not None and not isinstance(file_name, str):
            raise TypeError("File name must be a string")
        return super().__new__(cls)
    
    @staticmethod
    def save_encoded_image(image, file_name):
        if not isinstance(image, np.ndarray):
            raise TypeError("Image must be a numpy array")
        if not isinstance(file_name, str):
            raise TypeError("File name must be a string")
            
        path = f"img/{file_name}.png"
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        img = Image.fromarray(image)
        img.save(path)
    
    @staticmethod
    def load_encoded_image(file_name):
        if not isinstance(file_name, str):
            raise TypeError("File name must be a string")
            
        path = f"img/{file_name}.png"
        return np.array(Image.open(path))