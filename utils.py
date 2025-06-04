import re
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from stgsnek import Steganography

def display_image(img, canvas):
    try:
        if not isinstance(img, Image.Image):
            raise TypeError("Nieprawidłowy typ obrazu")
        
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10:
            return

        ratio = min(canvas_width/img.width, canvas_height/img.height)
        new_size = (int(img.width*ratio), int(img.height*ratio))
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img)
        
        canvas.image = photo
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, anchor="center", image=photo)
    except Exception as e:
        messagebox.showerror("Błąd wyświetlania", str(e))

def detect_algorithm(text):
    detectors = [
        (r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", "Date Cipher"),
        (r"^[^\x00-\x7F]+", "Caesar"),
        (r"^[A-F0-9]{64}:", "AES"),
        (r"^\d+,\d+", "RSA")
    ]
    
    for pattern, algo in detectors:
        if re.match(pattern, text):
            return algo
    return None