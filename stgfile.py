from PIL import Image
import numpy as np

def save_encoded_image(image, file_name):
    path = f"img/{file_name}.png"
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    img = Image.fromarray(image)
    img.save(path)

def load_encoded_image(file_name):
    path = f"img/{file_name}.png"
    return np.array(Image.open(path))
