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

###

# L + S RGB

# Load Data

# Accessing the local data (frames) at a speicifc path
# resizing it by 0.5, and storing them in a 4-D array.
# The 4-D array/Matrix is actually:
# "MovMat is a height * width * 3 * #frame video matrix"

# Gets the list of names of the frames along with the
# number of total frames.
contents = os.listdir("./Data/tennis")
numberOfElementsInContents = len(contents)

# Initializing the array with 0 values.
w, h, z = 1, 1, 3;
MovMat = [[[0 for x in range(w)] for y in range(h)] for z in range(z)]

# This is 0-Indexed Matrix. Goes through every single
# frame and sets it to the MovMat.
for a in range(numberOfElementsInContents):
	# Getting the specific frame and saving in the 4-D array.
	print(MovMat[2][0][0])

#Description
#example
#B = imresize(A,scale) returns image B that is scale times the size of A. The input image A can be a grayscale, RGB, or binary image. If A has more than two dimensions, imresize only resizes the first two dimensions. If scale is in the range [0, 1], B is smaller than A. If scale is greater than 1, B is larger than A. By default, imresize uses bicubic interpolation.

#	A(:,:,3) =
 #    5     5     5
 #    5     5     5
 #    5     5     5


	#MovMat = Double(MovMat)
	#MovMat = MovMat(,,,1,1,35) # This works somehow.

# RGB PRPCA
# Getting the return value and saving them.
	#[RPCA_image, L, S, L_RPCA, S_RPCA] = PRPCA_RGB(MovMat)

# Showing the results visually.

# Panorama

# Play results

# Play results in original ratio


