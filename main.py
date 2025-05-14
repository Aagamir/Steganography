import numpy as np
import matplotlib.pyplot as plt
import stgsnek
import stgfile

# mode = input("Co chcesz zrobić?\n1 - Zaszyfrować plik\n2 - Odszyfrować plik\n3 - Wyjść\n")


# if mode == "1":
#     input_image = str(input("Podaj nazwę pliku bez rozszerzenia w którym chcesz zakodować wiadomość:\n"))
#     print(input_image)
#     message = str(input("Podaj wiadomość którą chcesz zakodować w obrazie:\n"))
#     image = plt.imread("img\\"+input_image+".jpg")
#     print(image[0], "\n")
#     ImageEncoded = stgsnek.encode(image, stgsnek.get_bin_str(message))
#     print("Obrazek po zakodowaniu:\n")
#     print(ImageEncoded[0])

#     stgfile.save_encoded_image(ImageEncoded, input_image)
# elif mode == "2":
#     input_image = str(input("Podaj nazwę pliku bez rozszerzenia który chcesz odszyfrować:\n"))
#     print("Wiadomość ukryta w obrazie to:\n")
#     decoded = stgsnek.decode_utf8(stgfile.load_encoded_image(input_image))
# elif mode == "3":
#     exit()

message = "Wiadomość testowa"
image = (plt.imread("img\\test.jpg") * 255).astype(np.uint8)
MessageEncoded = stgsnek.caesar_encode(message, 3)
BinaryMessage = stgsnek.get_bin_str(MessageEncoded)
ImageEncoded = stgsnek.encode(image, BinaryMessage)
stgfile.save_encoded_image(ImageEncoded, "test2") 
print("Wiadomośc po zaszyfrowaniu:\n")
print(MessageEncoded)  
print("Ukryta wiadomość w obrazie to:\n")
decoded = stgsnek.decode_utf8(stgfile.load_encoded_image("test2"))
print(decoded)
print("Po odszyfrowaniu:\n")
print(stgsnek.caesar_decode(decoded, 3))

