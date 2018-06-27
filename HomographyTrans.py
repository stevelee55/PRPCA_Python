import numpy
import struct
from skimage.color import rgb2gray
import cv2
import matplotlib.transforms

class HomographyTrans(object):


	# Function that parses struct field
	# Function that parses struct field
	def parseField(self, stats, field, default):
		# Value to return from the function.
		val = None
		# Checking if the field/key exists in the "stats" struct.
		# "hasattr" already exists in python.
		if hasattr(stats, field):
			val = getattr(stats, field)
		else:
			val = default
		return val

	# Parsing inputs.
	def parseInputs(self, otps):
		# Checking to see if opts and var exists and then creating something.
		opts = struct

		# I think isRGB is boolearn return type so I changed the third paramter from
		# 1 to "True".
		isRGB = parseField(opts, "isRGB", 0)
		method = parseField(opts, "method", "numeric")
		T = parseField(opts, "T", 1)

	# Initializer for the this class' instance.
	def __init__(self):
		print("HomographyTrans is created!")


	def HomographyTrans_Main(self, movmat, opts):
		# Parsing and getting and storing the opts values.
		isRGB, method, T = parseInputs(opts)

		# In the matlab code, it checks to see if there is a "prior T", but it's not being used so
		# here I am trying to write it without it.

		# Reading in the first frame.
		if (!isRGB):
			# I put 2 instead of 3 because python is 0-indexed.
			numOfFrames = movmat.shape[2]
			# Get only the first frame. This is probably because when
			# the video is not RGB, then it is only 3-D.
			imgB = movmat[0]
		else:
			# Not exactly sure what this returns but just going by the website: http://mathesaurus.sourceforge.net/matlab-numpy.html
			numOfFrames = movmat.shape[3]
			# Get only the first frame's gray color(?)
			imgB = rgb2gray(movmat[0])

		# Extract features points in the first frame.
		# Use SURF first and then try to use others.
		# Creating Surf object.
		surf = cv2.xfeatures2d.SURF_create()
		# Key poitns and descriptors(?) https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html#surf-in-opencv
		# Not sure why, but the values of the points found differs from the matlab and the python.
		# For instance, matlab finds 2209 points where as the python finds 2977 points.
		# The dimension are the same though. For points, it's n * 1 and for features it's n * 64.
		# This is the extract features function.
		points, features = surf.detectAndCompute(imgB, None)
		featureImage = cv2.drawKeypoints(imgB, points, None)
		# Creating 1-D matrix of tforms. Based on the matlab outputs, seems like affin2d and projective2d results are the same.
		# I think the only difference is that the object type is different.
		tforms = [0 for x in range(numOfFrames)]
		tforms[numOfFrames - 1] = matplotlib.transforms.Affine2D(numpy.eye(3))

		# Repeating the above for every frame.
		# Starting from the index 1 because the first frame has already been processed.
		for n in range(1, numOfFrames):
			pointsPrevious = points
			featuresPrevious = features

			# Reading in the next frame.
			if (!isRGB):
				imgB = movmat[0]
			else:
				imgB = rgb2gray(movmat[0])

	# Temporary till figuring everyhing out.
			points, features = points, features = surf.detectAndCompute(imgB)
			indexPairs = match




