# -*- coding: utf-8 -*-
# Panoramic Robust PCA demo in Python.
# Written by Steve Lee
# 
# Algorithm originally created and written in MatLab
# by Chen Gao
# chengao@umich.edu
#
# June 18, 2018

# Necessary Libraries.

import os
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
import math
import imageio



# Need to put a method to get the data from S3 Bucket.
# This could be done by seeing if the flag is set to S3,
# and if it is set to S3, then call the S3 first to
# download the frames or the video and then call the rest
# of the functions.



# Custom Class.

from PRPCA_RGB import PRPCA_RGB


# Input Variables.

# If 'useRawVideo' is set to True, it uses 'rawVideoPath',
# which involves separating the video into frames. Otherwise,
# the pre-separated video frames will be used, which are located
# at the path indicated by 'videoFramesPath'.
useRawVideo = False
rawVideoPath = "./Data/newData/Test/moving.MOV"
videoFramesPath = "./Data/tennis"
# Between 0.0 -> 1.0. 1.0 is original image size.
percentageToResizeTo = 0.50 # 0.5 is too slow for python, takes about 15 mins, but 0.39 or 0.43 gives decent results.
# Needs to be less than or equal to the numberOfVideoFrames.
numberOfFramesToUse = 35 # For now, 35 is ideal.


# Helper Functions.

# Separates given video at rawVideoPath into frames if
# 'useRawVideo' is set to True.
if (useRawVideo):
	from VideoToFrames import separateVideoIntoFrames
	separateVideoIntoFrames(rawVideoPath, 3, videoFramesPath)


# Below does L + S RGB.

# Getting the list of frames' names and sorting them.
fileNames = os.listdir(videoFramesPath)

# Getting and saving each of the frame data using the
# list of frames' names.
videoFrameNames = []
for fileName in fileNames:
	if fileName.endswith('.jpg'):
		videoFrameNames.append(fileName)
# Sorting the videoFrameNames, because time to time,
# the frames get read in randomly, which affects the
# whole program.
videoFrameNames.sort()
# Getting the total number of video frames.
numberOfVideoFrames = len(videoFrameNames)

# Getting the width and height of the video using the
# first frame of the video.
firstFrame = imread(videoFramesPath + "/" + videoFrameNames[0])
# Keep in mind that the width of the video is usually shorter
# when it is in a landscape.
height = len(firstFrame)
width = len(firstFrame[0])
newHeight = math.floor(float(height * percentageToResizeTo))
newWidth = math.floor(float(width * percentageToResizeTo))

# Initializing the 4-D Matrix with 0s.
RGBCount = 3
# The MovMat is a 4-D array/Matrix that has the dimension of
# height * width * 3 * # of frames.
MovMat = [[[[0 for x in range(newHeight)] for y in range(newWidth)] for m in range(RGBCount)] for z in range(numberOfFramesToUse)]

# Goes through every single frame and sets it to the MovMat.
for i in range(numberOfFramesToUse):
	# Getting the specific frame and saving in the 4-D array.
	frame = imread(videoFramesPath + "/" + videoFrameNames[i]) #newData/CorruptedClip/" + "frame" + str(i + 1) + ".jpg")
	# The interesting thing about this code is that when it resizes, it does the "im2double" automatically.
	# Still quiet don't understand why "im2double" is needed in the Matlab code.
	# One thing to keep in mind that the pixel values are differ by very little when the values are compared.
	#For instance, 0.24117647 0.4372549  0.68431373 is for python, 0.2392, 0.4353, 0.6824 in matlab.
	# In the Matlab code, the function imresize changes the values dramatically, but it is later fixed
	#by the im2double.
	# cv2.resize doesn't do im2double automatically so normalizing needs to be done later.
	MovMat[i] = cv2.resize(frame, None, fx=percentageToResizeTo, fy=percentageToResizeTo)

	#Description
	#example
	#B = imresize(A,scale) returns image B that is scale times the size of A. The input image A can be a grayscale, RGB, or binary image. If A has more than two dimensions, imresize only resizes the first two dimensions. If scale is in the range [0, 1], B is smaller than A. If scale is greater than 1, B is larger than A. By default, imresize uses bicubic interpolation.



#Getting the certain number of frames for the computation.

# Arvin. Julia. Calilng Julia.rpca. Julia optimization, precompiling, which makes it faster. Registering do it in python, part after it, use Julia, which precompilation, there is a way to do it. 
# Julia is pretty easy. Figure out inefficient

# Email the results to him. 
# NewMovMat = [[[[0 for x in range(height)] for y in range(width)] for m in range(RGB)] for z in range(numberOfFramesToUse)]
# for i in range(numberOfFramesToUse):
# 	NewMovMat[i] = MovMat[i]
#Size should be 35.
#print(len(NewMovMat))

# These are used to present and show the imported image.
#plt.imshow(img)
#plt.show()

# RGB PRPCA
# Getting the return value and saving them.
instance = PRPCA_RGB()
L_RPCA = instance.PRPCA_RGB_Main(MovMat)
#RPCA_image, L, S, L_RPCA, S_RPCA = instance.PRPCA_RGB_Main(MovMat)

print("FINAL",len(L_RPCA))
images = []
# Create Gif.
for frameCount in range(35):
	images.append(imageio.imread("./Data/newData/Test/frame%d.jpg" % frameCount))

imageio.mimsave("L_RPCA.gif", images, duration=0.05)


# Showing the results visually.
# Panorama
# plt.imshow(RPCA_image)
# plt.show()

# Play results

# Play results in original ratio


