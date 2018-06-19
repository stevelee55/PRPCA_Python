#
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
# print(img)
# print(img[0][0][0])
width = len(img)
height = len(img[0])
newWidth = width * 0.5
newHeight = height * 0.5

# Initializing the 4-D Matrix with 0 values.
# Apparently the matrix is width * height * 3 * # of frames of the video.
mys = 3
MovMat = [[[[0 for x in range(width)] for y in range(height)] for m in range(mys)] for z in range(numberOfVideoFrames)]

# This is 0-Indexed Matrix. Goes through every single
# frame and sets it to the MovMat.
for i in range(numberOfVideoFrames):
	# Getting the specific frame and saving in the 4-D array.
	img = imread("./Data/tennis/" + videoFrames[i])
	MovMat[i] = transform.resize(img, (newWidth, newHeight))

	#Description
	#example
	#B = imresize(A,scale) returns image B that is scale times the size of A. The input image A can be a grayscale, RGB, or binary image. If A has more than two dimensions, imresize only resizes the first two dimensions. If scale is in the range [0, 1], B is smaller than A. If scale is greater than 1, B is larger than A. By default, imresize uses bicubic interpolation.


# These are used to present and show the imported image.
# print(img)
# plt.imshow(img)
# plt.show()


# RGB PRPCA
# Getting the return value and saving them.
	#[RPCA_image, L, S, L_RPCA, S_RPCA] = PRPCA_RGB(MovMat)

# Showing the results visually.

# Panorama

# Play results

# Play results in original ratio


