from copy import deepcopy
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# from skimage import data, color
# from skimage.transform import hough_circle, hough_circle_peaks
# from skimage.feature import canny
# from skimage.draw import circle_perimeter
# from skimage.util import img_as_ubyte


# # Load picture and detect edges
# image = data.load("/Users/remiuzel/Documents/Scolarité/2016-2020 Imperial College London/2018-2019 3nd Year JMC/HealthHack2019/diagnostic_uploads/syphilis1.png")[:,:,0]
# cv2.imshow('Edge', image)
# cv2.waitKey(0)
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
# cv2.imshow('Edge', image)
# cv2.waitKey(0)
# image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)
# cv2.imshow('Edge', image)
# cv2.waitKey(0)
# image = img_as_ubyte(image)[:,:,0]
# cv2.imshow('Edge', image)
# cv2.waitKey(0)
# edges = canny(image, sigma=3, low_threshold=10, high_threshold=50)


# # Detect two radii
# hough_radii = np.arange(20, 35, 2)
# hough_res = hough_circle(edges, hough_radii)

# # Select the most prominent 5 circles
# accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
#                                            total_num_peaks=3)

# # Draw them
# fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
# image = color.gray2rgb(image)
# for center_y, center_x, radius in zip(cy, cx, radii):
#     circy, circx = circle_perimeter(center_y, center_x, radius)
#     image[circy, circx] = (220, 20, 20)

# ax.imshow(image, cmap=plt.cm.gray)
# plt.show()


def process_image(filename, _type):
    image = np.array(Image.open(filename))
    # image = lips_canny(image)
    fragment = 50
    image = cv2.resize(image,(300,300))[fragment:-fragment,fragment:-fragment]

    # image = lips_canny(image)
    image = analyse(image, _type)
    plt.imshow(image)
    plt.show()
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

def analyse(image, _type):
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

    mask = get_mask(_type, greens, reds, blues, average)
    image[~mask] = (255, 0, 0, 255)
    
    return image

def get_mask(_type, greens, reds, blues, average):
    if (_type == "lips"): # TODO - DETECT OVAL INSTEAD OF APPLYING MASK
        mask = (greens < average[0]) | (reds < average[1]) | (blues < average[2])
    if (_type == "tongue_patch"):
        mask = (greens < 130) | (blues < 130) | (reds < 130)
    if (_type == "tongue_ulcer"): # TODO - DETECT OVAL INSTEAD OF APPLYING MASK
        mask = (greens < 130) | (blues < 130) | (reds < 130)
    if (_type == "gums"):
        mask = (greens > 100) | (blues > 100) | (reds > 100)
    return mask
