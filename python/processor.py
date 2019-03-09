import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def process_image(filename):
    image = np.array(Image.open(filename))
    # image = lips_canny(image)
    image = cv2.resize(image,(300,300))

    image = lips_canny(image)
    plt.imshow(image)
    #plt.savefig(filename + "test2.PNG")
    return filename

def lips_canny(image):
    image = image[: , :, :3]
    # = cv2.bilateralFilter(image, 5, 150, 150)
    bilateral_filtered_image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)
    cv2.imshow('Edge', bilateral_filtered_image)
    cv2.waitKey(0)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 30, 35)
    cv2.imshow('Edge', edge_detected_image)
    cv2.waitKey(0)
    gray = cv2.cvtColor(edge_detected_image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    #c = plt.Circle((circles[0,0, 0],circles[0,0,1]), circles[0,0,2])
    #cv2.circle(img, center, radius
    print(circles)
    return edge_detected_image

def analyse(image):
    RED, GREEN, BLUE = (2, 1, 0)
    reds = image[:, :, RED]
    greens = image[:, :, GREEN]
    blues = image[:, :, BLUE]
    average = image.mean(axis=0).mean(axis=0)

    pixels = np.float32(image.reshape(-1, 4))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    print(palette)

    mask = get_mask("tongue_patches", greens, reds, blues, average)

    image[mask] = (0, 0, 0, 255)
    return image

def get_mask(t, greens, reds, blues, average):
    if (t == "lips"):
        mask = (greens < average[0]) | (reds < average[1]) | (blues < average[2])
    if (t == "tongue_patches"):
        mask = (greens < 140) | (blues < 140)
    return mask
