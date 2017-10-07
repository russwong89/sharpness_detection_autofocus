'''
@name    sharpness_calc.py
@brief   Calculates the sharpness of a set of images
@author  Russell Wong, 2017
'''

import sys, os, math, cv2
import numpy as np
from matplotlib import pyplot as plt

import img_util

DEFAULT_IMG_DIR = 'img/'


'''
@name       loadImages
@brief      Retrieves all images from a folder and loads them into black-and-white matrices
@param[in]  folder: String representing path to folder containing images
@return     images: List of black-and-white images
'''
def loadImages(folder=DEFAULT_IMG_DIR):
    images = []
    for file in os.listdir(folder):
        img = img_util.readImageBW(os.path.join(folder, file))
        if img is not None:
            images.append(img)
    return images


'''
@name       getSharpness
@brief      Calculates the derivative in the x direction of images in a list and
            finds the sharpness given by the L2-Norm of the matrix
@param[in]  images: A list of grayscale images
@return     derivative_imgs: A list of images containing all image derivatives
@return     sharpness_vals: A list of floats containing all calculated sharpness values
'''
def getSharpness(images):
    sharpness_vals = []
    derivative_imgs = []
    for img in images:
        derivative = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
        derivative_imgs.append(derivative)
        sharpness_vals.append(cv2.norm(derivative))
    return derivative_imgs, sharpness_vals


#######################
###  Main Function  ###
#######################
if __name__ == '__main__':
    images = loadImages()
    derivative_imgs, sharpness_vals = getSharpness(images)
    for i, img in enumerate(derivative_imgs):
        img_util.plot(img, 'IMAGE', cmap='gray')
        img_util.saveImageBW('img_' + str(i) + '.png', img)    
        print 'Sharpness for img %d: %f' % (i, sharpness_vals[i])
        