import numpy as np
import matplotlib.pyplot as plt
from IPython.display import IFrame


def ReadImage(url):
    image = plt.imread(url)
    plt.imshow(image)
    plt.show()
    print(image.shape)

ReadImage("Python\\Projekt\\durka.jpg")