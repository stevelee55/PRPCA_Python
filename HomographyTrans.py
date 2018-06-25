import numpy
import struct
from skimage.color import rgb2gray 

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
			# The first frame.
			for i in range(35):
				NewMovMat[i] = MovMat[i]

			# Get only the first one.
			imgB = movmat[0]
		else:
			# Not exactly sure what this returns but just going by the website: http://mathesaurus.sourceforge.net/matlab-numpy.html
			numOfFrames = movmat.shape[3]
			imgB = rgb2gray()