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
numel = 20

# Initializing the array with 0 values.
w, h = 8, 5;
Matrix = [[0 for x in range(w)] for y in range(h)]

# Gets the list of names of the frames.
contents = os.listdir("directory path")
numberOfElementsInContents = len(contents)

for a in range(numberOfElementsInContents):
	for b in 
	# Getting the specific frame and saving in the 4-D array.
	MovMat = [,,,i]

	w, h = 8, 5;
	Matrix = [[0 for x in range(w)] for y in range(h)]

# Converting the data to double (?)
MovMat = Double(MovMat)
MovMat = MovMat(,,,1,1,35) # This works somehow.

# RGB PRPCA
# Getting the return value and saving them.
[RPCA_image, L, S, L_RPCA, S_RPCA] = PRPCA_RGB(MovMat)

# Showing the results visually.

# Panorama

# Play results

# Play results in original ratio


