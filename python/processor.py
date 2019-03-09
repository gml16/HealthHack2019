import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def process_image(filename):
    image = np.array(Image.open(filename))
    print(image.shape, image.dtype)
    empty_img = np.zeros_like(image)
    RED, GREEN, BLUE = (2, 1, 0)
    reds = image[:, :, RED]
    greens = image[:, :, GREEN]
    blues = image[:, :, BLUE]
    #mask = (greens < 35) | (reds > greens) | (blues > greens)
    #mask = (greens > 100) & (reds > 100) & (blues > 100)
    mask = (greens < 150) | (reds < 150) | (blues < 150)
    image[mask] = (0, 0, 0, 255)
    plt.imshow(image)
    plt.savefig(filename + "test2.PNG")
    #image[mask] = (0, 255, 0, 255)
    #print(image)
    return filename
