'''
@name    sharpness_calc.py
@brief   Calculates the sharpness of a set of images
@author  Russell Wong, 2017
'''

import sys, os, math, cv2
import numpy as np
from matplotlib import pyplot as plt

import img_util

DEFAULT_IMG_DIR = 'RTImg/'


'''
@name       loadImages
@brief      Retrieves all images from a folder and loads them into black-and-white matrices
@param[in]  folder: String representing path to folder containing images
@return     images: List of black-and-white images
@return     distances: List of focus distances corresponding to each image
'''
def loadImages(folder=DEFAULT_IMG_DIR):
    images = []
    distances = []
    for file in os.listdir(folder):
        img = img_util.readImageBW(os.path.join(folder, file))
        if img is not None:
            images.append(img)
            distances.append(int(file[9:13]))
            print file
    return images, distances


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


'''
@name       getPoints
@brief      Finds (focus distance, sharpness) data points for a set of images
@param[in]  subject_name: The subject name to search for
@param[in]  show_images: Whether to display image derivatives using matplotlib 
@return     points: List of 2-tuples representing (x,y) coordinates 
'''
def getPoints(subject_name='111', show_images=False):
    images, distances = loadImages(folder=DEFAULT_IMG_DIR+subject_name)
    derivative_imgs, sharpness_vals = getSharpness(images)
    for i, img in enumerate(derivative_imgs):
        if show_images:
            img_util.plot(img, 'IMAGE', cmap='gray')
        img_util.saveImageBW('img_' + str(i) + '.png', img)    
        print 'Sharpness for img %d: %f' % (i, sharpness_vals[i])
    return zip(distances, sharpness_vals)


#######################
###  Main Function  ###
#######################
if __name__ == '__main__':
    subject_name='001'
    if len(sys.argv) >= 2:
        subject_name = sys.argv[1]
    points = getPoints(subject_name=subject_name, show_images=False)
    print points
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    img_util.plotPoints(x, y, "Points")
    sys.exit()