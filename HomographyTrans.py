import numpy
import struct
from skimage.color import rgb2gray
import cv2
import matplotlib.transforms
import matplotlib.pyplot as plt
import time
import math

class HomographyTrans(object):

	# Function that finds x and y limits of the panaroma.
	def outputLimits(tform, ):
		print("")

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
	def parseInputs(self, opts):
		# Checking to see if opts and var exists and then creating something.
		opts = struct
		# I think isRGB is boolearn return type so I changed the third paramter from
		# 1 to "True".
		isRGB = self.parseField(opts, "isRGB", 0)
		method = self.parseField(opts, "method", "numeric")
		T = self.parseField(opts, "T", 1)

		return isRGB, method, T

	# Initializer for the this class' instance.
	def __init__(self):
		print("HomographyTrans is created!")


	def HomographyTrans_Main(self, movmat, opts):
		# Global Variables

		# Parsing and getting and storing the opts values.
		isRGB, method, T = self.parseInputs(opts)

		# In the matlab code, it checks to see if there is a "prior T", but it's not being used so
		# here I am trying to write it without it.

		# Reading in the first frame.
		if (not isRGB):
			# I put 2 instead of 3 because python is 0-indexed.
			numOfFrames = len(movmat) #movmat.shape[3] ?
			# Get only the first frame. This is probably because when
			# the video is not RGB, then it is only 3-D.
			imgB = movmat[0]
		else:
			# Not exactly sure what this returns but just going by the website: http://mathesaurus.sourceforge.net/matlab-numpy.html
			numOfFrames = len(movmat)
			# Get only the first frame's gray color(?)
			imgB = cv2.cvtColor(movmat[0], cv2.COLOR_BGR2GRAY) # Surf only works with this.

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

		#featureImage = cv2.drawKeypoints(imgB, points, None)
		# Creating 1-D matrix of tforms. Based on the matlab outputs, seems like affin2d and projective2d results are the same.
		# I think the only difference is that the object type is different.
		tformObject = matplotlib.transforms.Affine2D(numpy.eye(3))
		tforms = [tformObject for x in range(numOfFrames)]

		# Repeating the above for every frame.
		# Starting from the index 1 because the first frame has already been processed.
		for n in range(1, numOfFrames):
			pointsPrevious = points
			featuresPrevious = features

			# Reading in the next frame.
			if (not isRGB):
				imgB = movmat[n]
			else:
				imgB = cv2.cvtColor(movmat[n], cv2.COLOR_BGR2GRAY)

			points, features = surf.detectAndCompute(imgB, None)
			# create BFMatcher object for feature matching.
			bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=True)
			# This means that queryIdx is features, and trainIdx is featuresPrevious.
			# https://stackoverflow.com/questions/13318853/opencv-drawmatches-queryidx-and-trainidx/34380383
			indexPairs = bf.match(features, featuresPrevious)
			# Should be for looped.
			# indexPairs[i].queryIdx gives index of points that were matched.
			matchedPoints = [points[indexPairs[i].queryIdx] for i in range(len(indexPairs))]
			numpyArrayMatchedPoints = numpy.array([matchedPoints[i].pt for i in range(len(matchedPoints))])
			# matchedPoints have the KeyPoint objects, which an be accesesd by index and .pt.
			# print(matchedPoints[0].pt)
			matchedPointsPrev = [pointsPrevious[indexPairs[i].trainIdx] for i in range(len(indexPairs))]
			numpyArrayMatchedPointsPrev = numpy.array([matchedPointsPrev[i].pt for i in range(len(matchedPointsPrev))])
			# Estimating geometric transform.
			# Not sure what the Affine = Bool does.
			estimatePair, status = cv2.findHomography(numpyArrayMatchedPoints, numpyArrayMatchedPointsPrev,cv2.RANSAC,5.0) #cv2.estimateRigidTransform(numpyArrayMatchedPoints, numpyArrayMatchedPointsPrev, True)
			#print(estimatePair)
			#print(status)
			# first = [estimatePair[0][0], estimatePair[1][0], 91.59]
			# second = [estimatePair[0][1], estimatePair[1][1], -0.63]
			# third = [estimatePair[0][2], estimatePair[1][2], 0.9896]
			tforms[n] = estimatePair #[estimatePair[0], estimatePair[1], numpy.array([0,0,1])]
			# Estimate transform from frame A to frame B, and fit as an s-R-t
			tforms[n] = numpy.matmul(tforms[n-1], tforms[n])


		# Getting the centerImageId.
	# For now, set it to the half of the frame.
		centerImageId = math.floor(numOfFrames / 2)



		# This affects at which angle the panaroma is gonna be happening.
		Tinv = numpy.linalg.inv(tforms[centerImageId])

		# Centering the registered images for a specific image.		
		for i in range(numOfFrames):
			# Recalculating the transformation matrix.
			tforms[i] = numpy.matmul(Tinv, tforms[i])
			# This is to get the frame move within the positive coordinates.
			# pos-x makes it go right, pos-y makes it go down.
			x_offset = 300
			y_offset = 50
			translateMatrix = [[1, 0, x_offset], [ 0, 1, y_offset],[0, 0, 1]]
			tforms[i] = numpy.matmul(translateMatrix, tforms[i])

			imgB = movmat[i]
			M = numpy.float32(tforms[i])
			warp = cv2.warpPerspective(imgB, M, (1000, 500))
			plt.imshow(warp)
			plt.show()

		print("hello", tforms[0])
		print(tforms[34])

		# Skipping getting hte sizes for the panorama view since it has to be figured out.

		height = 500
		width = 1000 
		Y = []
		Mask = []

		for i in range(len(tforms)):
			if not isRGB:
				imgB = movmat[i]
				M = numpy.float32(tforms[i])
				warpedImage = cv2.warpPerspective(imgB, M, (width, height))
				# Column of Y are the frames and each row is pixels. Matlab says it's "vectorized"...?
				Y[i] = warpedImage
				# Getting the mask.
				mask = cv2.warpPerspective(numpy.ones(len(imgB)), M, (width, height))
				for z in range(len(mask)):
					for j in range(len(mask[z])):
						for k in range(len(mask[z][j])):
							if (mask[z][j][k] != 0):
								mask[z][j][k] = 1
				Mask[i] = mask

		T = tforms

		return Y, Mask, height, width, T

	#imgB = cv2.cvtColor(movmat[i], cv2.COLOR_BGR2GRAY)
	# imgB = movmat[i]
	# # This matters.
	# tforms[i] = numpy.matmul(Tinv, tforms[i])
	# M = numpy.float32(tforms[i])
	# warp = cv2.warpPerspective(imgB, M, (799, 288))
	# plt.imshow(warp)
	# plt.show()





