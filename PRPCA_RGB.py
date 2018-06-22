import struct
import math

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
		lamSParameter = 1 / math.sqrt(max(size(Y)))
		LamS = parseField(opts, "LamS", lamSParameter)
		# The third parameter is "100", but see if it can be changed and see what it affects.
		# It may be like the 35 frame limit, which was to run the code pretty fast by only using the
		# 35 frames.
		nIters = parseField(opts, "nIters", 100)

	def parseInputs2(self, opts):
		return "Defautl"
		
		
	def PRPCA_RGB_Woah(movmat):

		# # Homography transformation
		# Y, Mask, height, width, T = HomographyTrans(movmat)

		# # Parse inputs (?)
		# LamS, nIters = parseInputs(Y,)

		# # Calculating meaningful region for boosting (?)
		# m = any(Mask,2)
		# Ytil = Y(m,:)
		# Mtil = Mask(m,:)

		# # RPCA
		# opts.M = Mtil

		return "hello world", [2,3], "yay", "123", 3
