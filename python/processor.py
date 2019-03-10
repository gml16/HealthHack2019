from copy import deepcopy
import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(filename, _type):
    image = cv2.imread(filename)
    # image = lips_canny(image)
    fragment = 50
    image = cv2.resize(image,(300,300))

    res = fit_ellipse(image)
    return res

def fit_ellipse(image):
    bilateral_filtered_image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)
    #cv2.imshow('Edge', bilateral_filtered_image)
    #cv2.waitKey(0)

    '''
    filtered = cv2.convertScaleAbs(bilateral_filtered_image, alpha=1.5)
    cv2.imshow('Edge', filtered)
    cv2.waitKey(0)
    '''

    imgray = cv2.cvtColor(bilateral_filtered_image,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Edge', imgray)
    cv2.waitKey(0)

    ret,thresh = cv2.threshold(imgray,175,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    cv2.imshow('Edge', image)
    cv2.waitKey(0)

    max_cnt = max(contours, key=cv2.contourArea)
    ellipse = cv2.fitEllipse(max_cnt)
    ellipse_pnts = cv2.ellipse2Poly( (int(ellipse[0][0]),int(ellipse[0][1]) ) ,( int(ellipse[1][0]),int(ellipse[1][1]) ),int(ellipse[2]),0,360,1)
    comp = cv2.matchShapes(max_cnt,ellipse_pnts,1,0.0)
    res = 1
    for p in ellipse_pnts:
        if p[0]>0 and p[0] < 200 and p[1]>0 and p[1] < 200:
            image[p[0], p[1]]=[0,0,255]
        else:
            res = 0
    cv2.imshow('Edge', image)
    cv2.waitKey(0)
    return res

def find_contours(image):

    bilateral_filtered_image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)
    cv2.imshow('Edge', bilateral_filtered_image)
    cv2.waitKey(0)

    imgray = cv2.cvtColor(bilateral_filtered_image,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Edge', imgray)
    cv2.waitKey(0)
    ret,thresh = cv2.threshold(imgray,150,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    cv2.imshow('Edge', image)
    cv2.waitKey(0)

def lips_canny(image):
    image = image[: , :, :3]
    # = cv2.bilateralFilter(image, 5, 150, 150)
    bilateral_filtered_image = cv2.fastNlMeansDenoisingColored(image,None,15,10,7,21)
    cv2.imshow('Edge', bilateral_filtered_image)
    cv2.waitKey(0)
    edges = cv2.Canny(bilateral_filtered_image, 54, 56)
    cv2.imshow('Edge', edges)
    cv2.waitKey(0)


    '''
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 0.5, 100)
    print(circles)
    cv2.imshow('Edge', circles)
    cv2.waitKey(0)
    '''

    '''
    #imgray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Edge', imgray)
    #cv2.waitKey(0)
    ret,thresh = cv2.threshold(edges,127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('Edge', im2)
    cv2.waitKey(0)
    '''


    '''

    cv2.drawContours(edges, contours, -1, (0,255,0), 3)
    cv2.imshow('Edge', edges)
    cv2.waitKey(0)
    '''
    return image

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
