# -*- coding: utf-8 -*-
# Panoramic Robust PCA demo in Python.
# Written by Steve Lee
# 
# Algorithm originally created and written in MatLab
# by Chen Gao
# chengao@umich.edu
#
# June 18, 2018

# Necessary libraries.
import os
# the code must be run by saying python3.6 <filename>
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy

# Classes
from PRPCA_RGB import PRPCA_RGB

#######################################################
# Function Definitions
def HomographyTrans(movmat):
	return Y, Mask, height, width, T

####### PRPCA_RGB
instance = PRPCA_RGB()
#instance.parseInputs(2,3)


#######################################################

# L + S RGB

# Load Data

# Accessing the local data (frames) at a speicifc path
# resizing it by 0.5, and storing them in a 4-D array.
# The 4-D array/Matrix is actually:
# "MovMat is a height * width * 3 * #frame video matrix"
# Is it * because it's RGB?

# Gets the list of names of the frames along with the
# number of total frames.
contents = os.listdir("./Data/tennis")
contents.sort()
# Getting only the ones that have the certain extension.
# In this case, only .jpg
videoFrames = []
for content in contents:
	if content.endswith('.jpg'):
		videoFrames.append(content)

numberOfVideoFrames = len(videoFrames)

# Getting the new width and height for the video frame.
img = imread("Data/tennis/00000.jpg")
# Shorter. i.e: 480
height = len(img)
# Longer. i.e: 854
width = len(img[0])
percentage = 0.5
newHeight = float(height * percentage)
newWidth = float(width * percentage)

# Initializing the 4-D Matrix with 0 values.
# Apparently the matrix is height * width * 3 * # of frames of the video.
RGB = 3
MovMat = [[[[0 for x in range(height)] for y in range(width)] for m in range(RGB)] for z in range(numberOfVideoFrames)]

# This is 0-Indexed Matrix. Goes through every single
# frame and sets it to the MovMat.
for i in range(numberOfVideoFrames):
	# Getting the specific frame and saving in the 4-D array.
	img = imread("./Data/tennis/" + videoFrames[i]) #newData/CorruptedClip/" + "frame" + str(i + 1) + ".jpg")
	# The interesting thing about this code is that when it resizes, it does the "im2double" automatically.
	# Still quiet don't understand why "im2double" is needed in the Matlab code.
	# One thing to keep in mind that the pixel values are differ by very little when the values are compared.
	#For instance, 0.24117647 0.4372549  0.68431373 is for python, 0.2392, 0.4353, 0.6824 in matlab.
	# In the Matlab code, the function imresize changes the values dramatically, but it is later fixed
	#by the im2double.
	# cv2.resize doesn't do im2double automatically so normalizing needs to be done later.
	MovMat[i] = cv2.resize(img, None, fx=percentage, fy=percentage)

	#Description
	#example
	#B = imresize(A,scale) returns image B that is scale times the size of A. The input image A can be a grayscale, RGB, or binary image. If A has more than two dimensions, imresize only resizes the first two dimensions. If scale is in the range [0, 1], B is smaller than A. If scale is greater than 1, B is larger than A. By default, imresize uses bicubic interpolation.


# Needs to be less than or equal to the numberOfVideoFrames.
numberOfFramesToUse = 35
#Getting the certain number of frames for the computation.

# Arvin. Julia. Calilng Julia.rpca. Julia optimization, precompiling, which makes it faster. Registering do it in python, part after it, use Julia, which precompilation, there is a way to do it. 
# Julia is pretty easy. Figure out inefficient

# Email the results to him. 
NewMovMat = [[[[0 for x in range(height)] for y in range(width)] for m in range(RGB)] for z in range(numberOfFramesToUse)]
for i in range(numberOfFramesToUse):
	NewMovMat[i] = MovMat[i]
#Size should be 35.
#print(len(NewMovMat))

# These are used to present and show the imported image.
#plt.imshow(img)
#plt.show()

# RGB PRPCA
# Getting the return value and saving them.
RPCA_image, L, S, L_RPCA, S_RPCA = instance.PRPCA_RGB_Main(NewMovMat)


# Showing the results visually.
# Panorama
# plt.imshow(RPCA_image)
# plt.show()

# Play results

# Play results in original ratio


