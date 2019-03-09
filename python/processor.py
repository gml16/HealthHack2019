import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def process_image(filename):
    image = np.array(Image.open(filename))
    image = lips_canny(image)
    plt.imshow(image)
    plt.savefig(filename + "test2.PNG")
    #image[mask] = (0, 255, 0, 255)
    #print(image)
    return filename

def lips_canny(image):
    bilateral_filtered_image = cv2.bilateralFilter(image, 5, 175, 175)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    cv2.imshow('Edge', edge_detected_image)
    return edge_detected_image

def analyse_lips(image):
    RED, GREEN, BLUE = (2, 1, 0)
    reds = image[:, :, RED]
    greens = image[:, :, GREEN]
    blues = image[:, :, BLUE]
    #mask = (greens < 35) | (reds > greens) | (blues > greens)
    #mask = (greens > 100) & (reds > 100) & (blues > 100)
    average = image.mean(axis=0).mean(axis=0)

    pixels = np.float32(image.reshape(-1, 4))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    print(palette)


    mask = (greens < average[0]) | (reds < average[1]) | (blues < average[2])
    image[mask] = (0, 0, 0, 255)
    return image
