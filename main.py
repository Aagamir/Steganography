import numpy as np
import matplotlib.pyplot as plt
import stgsnek
import stgfile


def read_image(url):
    image = plt.imread(url)
    print(image.shape)
    print(image.dtype)
    plt.imshow(image[:, :, 0]%2)
    plt.colorbar()
    plt.show()

image = plt.imread("rafał.jpg")
ImageEncoded = stgsnek.encode(image, "Dzień dobry państu, z tej strony Remigiusz Maciaszek, co mam na czole, co mam na czole, twoją starą mam na czole")

stgfile.save_encoded_image(ImageEncoded, "rafał")


stgsnek.decode_utf8(stgfile.load_encoded_image("rafał"))
