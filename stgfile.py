import skimage.io

def save_encoded_image(image, file_name):
    file_name = "img\\"+str(file_name)+".png"
    skimage.io.imsave(file_name, image)

def load_encoded_image(file_name):
    return skimage.io.imread("img\\"+ file_name+".png")