import struct
import math
from HomographyTrans import HomographyTrans
from improvedRobustPCA import improvedRobustPCA
import numpy

class PRPCA_RGB(object):

	# Initializer for the this class' instance.
	def __init__(self):
		print("PRPCA_RGB is created!")

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

	# Functions for parsing inputs.
	# 'opts' are the optional data that may or may not exist.
	def parseInputs(self, Y): # (self, Y, opts):
		# Below is the psudo code for the matlab code that I don't think
		# it's necessary. For now, create the opts object in this function
		# and use it and return it instead.
		# if opts and var do not exist
		# 	then opts = struct()
		opts = struct

		# Getting the calcualted LamS and nIters and returning them.
		# the part "1 / sqrt(max(size(Y))" is the one that I could pass in infinity I think. Check on this.
		# "max" is already built in python.
		# Parameter for the LamS: Not sure what this really represents yet.
		# Y dimension.
		Ydimension = numpy.array(Y).shape
		lamSParameter = 1 / math.sqrt(max(Ydimension))
		LamS = self.parseField(opts, "LamS", lamSParameter)
		# The third parameter is "100", but see if it can be changed and see what it affects.
		# It may be like the 35 frame limit, which was to run the code pretty fast by only using the
		# 35 frames.
		nIters = self.parseField(opts, "nIters", 100)

		return LamS, nIters

	def parseInputs2(self): #, opts):
		# Below is the psudo code for the matlab code that I don't think
		# it's necessary. For now, create the opts object in this function
		# and use it and return it instead.
		# if opts and var do not exist
		# 	then opts = struct()
		opts = struct

		# I think isRGB is boolearn return type so I changed the third paramter from
		# 1 to "True".
		isRGB = self.parseField(opts, "isRGB", True)
		method = self.parseField(opts, "method", "numeric")

		return isRGB, method
		
		
	def PRPCA_RGB_Main(self, movmat):

		# Took out varagin{:} since it's matlab notation for "Any arguement"
		isRGB, method = self.parseInputs2()
		# Creating a struct to hold the above-returned values.
		optsHT = struct
		optsHT.isRGB = isRGB
		optsHT.method = method

		# Homography transformation
		homographyTransInstance = HomographyTrans()
		Y, Mask, height, width, T = homographyTransInstance.HomographyTrans_Main(movmat, optsHT)

		# Parse inputs.
		# Took out varagin{:} since it's matlab notation for "Any arguement"
		LamS, nIters = self.parseInputs(Y)

		# Calculating meaningful region for boosting (?)
		
		print(len(Mask[0]))
		print(len(Mask))
		print(len(Y[0]))
		print(len(T))

		# m = numpy.any(Mask, axis=1)
		# print("m:", len(m))
		# # m = any(Mask,2)

		Ytil = []
		Mtil = []

		

		for i in range(len(Mask)):
			for j in range(len(Mask[0])):
				if (Mask[i][j] == int(1)):
					Ytil.append(Y[i])
					Mtil.append(Mask[i])
					break

		# print("Ytil:", len(Ytil))
		# print(Ytil)
		# print("Mtil:", len(Mtil))
		# print(len(Mask))

		# RPCA
		opts = struct
		opts.M = Mtil
		opts.maxIters = nIters
		improvedRobustPCAInstance = improvedRobustPCA()
		Ltil, Stil = improvedRobustPCA(Ytil, 1, LamS, opts)




		return "hello world", [2,3], "yay", "123", 3
