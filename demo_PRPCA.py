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
numberOfElementsInContents = len(contents)
img = imread("Data/tennis/00000.jpg")
# Getting the new width and height for the video frame.
newWidth = len(img) * 0.5
newHeight = len(img[0]) * 0.5
img = transform.resize(img, (newWidth, newHeight))

# These are used to present and show the imported image.
# print(img)
# plt.imshow(img)
# plt.show()

# Initializing the 4-D Matrix with 0 values.
# Apparently the matrix is width * height * 3 * # of frames of the video.
numberOfVideoFrames = numberOfElementsInContents
width = 20
height = 5
mys = 3
MovMat = [[[[0 for x in range(width)] for y in range(height)] for m in range(mys)] for z in range(numberOfVideoFrames)]

	#Checking to see if the MovMat is initizlied correctly.
counter = 0

	# for z in range(numberOfVideoFrames):
	# 	for y in range(height):
	# 		for x in range(width):
	# 			counter+=1

	# print(counter)

# This is 0-Indexed Matrix. Goes through every single
# frame and sets it to the MovMat.
for a in range(numberOfElementsInContents):
	# Getting the specific frame and saving in the 4-D array.
	#print(MovMat[2][0][0])
	counter+=1

	#Description
	#example
	#B = imresize(A,scale) returns image B that is scale times the size of A. The input image A can be a grayscale, RGB, or binary image. If A has more than two dimensions, imresize only resizes the first two dimensions. If scale is in the range [0, 1], B is smaller than A. If scale is greater than 1, B is larger than A. By default, imresize uses bicubic interpolation.




# RGB PRPCA
# Getting the return value and saving them.
	#[RPCA_image, L, S, L_RPCA, S_RPCA] = PRPCA_RGB(MovMat)

# Showing the results visually.

# Panorama

# Play results

# Play results in original ratio


