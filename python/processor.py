from copy import deepcopy
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def process_image(filenames):

    images = [cv2.resize(np.array(Image.open(filename)),(300,300)) for filename in filenames]

    fragment = 50

    # Remove sides for dark and white patch detection.
    images[2] = images[2][fragment:-fragment,fragment:-fragment]
    images[3] = images[3][fragment:-fragment,fragment:-fragment]

    # Setup baseline healthy flags. 
    flags = "0000"
    flags[1] = fit_ellipse(filenames[1])
    print("WARNING: Updated flag %s" % flags)
    flags[2] = analyse(images[2], "tongue_patch")
    print("WARNING: Updated flag %s" % flags)
    flags[3] = analyse(images[3], "gums")
    print("WARNING: Updated flag %s" % flags)

    # t_patch = analyse(images[2], "tongue_patch")
    # g_patch = analyse(images[3], "gums")
    # plt.imshow(t_patch)
    # plt.show()
    # plt.imshow(g_patch)
    # plt.show()

    return flag

def fit_ellipse(filename):
    image = cv2.imread(filename)
    image = cv2.resize(image, (300,300))

    bilateral_filtered_image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)

    imgray = cv2.cvtColor(bilateral_filtered_image,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Edge', imgray)
    # cv2.waitKey(0)

    ret,thresh = cv2.threshold(imgray,175,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    # cv2.imshow('Edge', image)
    # cv2.waitKey(0)

    max_cnt = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(max_cnt)
    ellipse_pnts = cv2.ellipse2Poly( (int(ellipse[0][0]),int(ellipse[0][1]) ) ,( int(ellipse[1][0]),int(ellipse[1][1]) ),int(ellipse[2]),0,360,1)
    comp = cv2.matchShapes(max_cnt,ellipse_pnts,1,0.0)
    flag = "1"
    for p in ellipse_pnts:
        if p[0]>0 and p[0] < 200 and p[1]>0 and p[1] < 200:
            image[p[0], p[1]]=[0,0,255]
        else:
            flag = "0"
    # cv2.imshow('Edge', image)
    # cv2.waitKey(0)
    return flag


def analyse(image, _type):
    RED, GREEN, BLUE = (2, 1, 0)
    reds = image[:, :, RED]
    greens = image[:, :, GREEN]
    blues = image[:, :, BLUE]
    average = image.mean(axis=0).mean(axis=0)
    pixels = np.float32(image.reshape(-1, 4))

    masks = {
        "lips": (greens < average[0]) | (reds < average[1]) | (blues < average[2]),
        "tongue_patch": (greens < 130) | (blues < 130) | (reds < 130),
        "gums": (greens > 100) | (blues > 100) | (reds > 100)
    }

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    mask = masks[_type]
    image[~mask] = (255, 0, 0, 255)
    
    return flag(image, _type)

    return image

# Checks if the image presents substancial symptoms.
def flag(image, _type):

    # Set conditions

    # Go through the image and calculate how much of it is in the ROI
    size = image.shape[0] * image.shape[1]
    roi = image[:,:,0]
    r = 0
    for row in roi:
        for p in row:
            if p == 255:
                r += 1
    part = (r / size) * 100

    if (_type == "gums"):
        # Be extremely sensible as small dark patches are never good.
        print("There are %.2f%% of cancer places" % (part))
        return "1" if part > 5 else "0"    

    elif (_type == "tongue_patch"):
        # Be more leenient for white patches.
        print("There are %.2f%% of white places" % (part))
        return "1" if part > 12 else "0"    
    else:
        # Cold sore case - TODO
        pass
