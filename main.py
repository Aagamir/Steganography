import numpy as np
import matplotlib.pyplot as plt
import stgsnek
import stgfile

mode = input("Co chcesz zrobić?\n1 - Zaszyfrować plik\n2 - Odszyfrować plik\n")

if mode == "1":
    input_image = str(input("Podaj nazwę pliku bez rozszerzenia w którym chcesz zakodować wiadomość:\n"))
    print(input_image)
    message = str(input("Podaj wiadomość którą chcesz zakodować w obrazie:\n"))
    image = plt.imread("img\\"+input_image+".jpg")
    print(image[0], "\n")
    ImageEncoded = stgsnek.encode(image, message)
    print(ImageEncoded[0])

    stgfile.save_encoded_image(ImageEncoded, input_image)
elif mode == "2":
    input_image = str(input("Podaj nazwę pliku bez rozszerzenia który chcesz odszyfrować:\n"))
    print("Wiadomość ukryta w obrazie to:\n")
    decoded = stgsnek.decode_utf8(stgfile.load_encoded_image(input_image))
