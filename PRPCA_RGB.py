import struct
import math
from HomographyTrans import HomographyTrans
from improvedRobustPCA import improvedRobustPCA
from adjustLS2_RGB import adjustLS2_RGB_Main
import numpy
import matplotlib.pyplot as plt
from pano2RGBMovie import pano2RGBMovie_Main
import boto3

# print("VERSION", boto3.__version__)

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

class PRPCA_RGB(object):

	# Temporary AWS bucket upload.
	def S3_Upload_Image(self, image):
		# Do not hard code credentials
		# boto3.client not available if there are spaces.
		client = boto3.client("s3", aws_access_key_id="AKIAIXW57FAC5P2E3ILA", aws_secret_access_key="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")
		client.upload_file("L.jpg", "vsp-userfiles-mobilehub-602139379", "L.jpg")

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

	#import pdb; pdb.set_trace()


		# Homography transformation
		homographyTransInstance = HomographyTrans()
		Y, Mask, height, width, T = homographyTransInstance.HomographyTrans_Main(movmat, optsHT)

		# Parse inputs.
		# Took out varagin{:} since it's matlab notation for "Any arguement"
		LamS, nIters = self.parseInputs(Y)

		# Calculating meaningful region for boosting (?)
		
		# print(len(Mask[0]))
		# print(len(Mask))
		# print(len(Y[0]))
		# print(len(T))

		# m = numpy.any(Mask, axis=1)
		# print("m:", len(m))
		# # m = any(Mask,2)

		# Debugger.
	#import pdb; pdb.set_trace()

		Ytil = []
		Mtil = []
		m = []


		added = False

		for h in range(len(Mask)):
			for w in range(len(Mask[0])):
				# print("Checking",Mask[i][j])
				# This replicates any by allowing any value that is only 1.
				if (Mask[h][w] != 0):
					Ytil.append(Y[h])
					Mtil.append(Mask[h])
					# print("i",i)
					m.append(1)
					added = True
					break
			if (not added):
				m.append(0)
			else:
				added = False

		# print("Ytil:", len(Ytil))
		#print("Ytil",Ytil)
		# print("Mtil:", len(Mtil))
		# print(len(Mask))

	#import pdb; pdb.set_trace()

		# RPCA
		opts = struct
		opts.M = Mtil
		opts.maxIters = nIters
		improvedRobustPCAInstance = improvedRobustPCA()
		# r should be 0 since it's later used to reference a value and matlab is referring to the index 1 (matlab) value.
		Ltil, Stil = improvedRobustPCAInstance.improvedRobustPCA_Main(Ytil, 0, LamS, opts)

		#import pdb; pdb.set_trace()

	#import pdb; pdb.set_trace()
		# print("Ltil",Ltil)
		# print("Stil",Stil)

		# print(":)")
		# Embedding.
		Y = numpy.array(Y)
		Lhat = numpy.zeros(Y.shape)
		counter = 0
		# Adding back into the original dimensions.
		# Lhat[m][:] = Ltil.
		for i in range(len(m)):
			if (m[i] == 1):
				Lhat[i] = Ltil[counter]
				counter+=1
		Shat = numpy.zeros(Y.shape)
		counter = 0
		# Adding back into the original dimensions.
		# Lhat[m][:] = Ltil.
		for i in range(len(m)):
			if (m[i] == 1):
				Shat[i] = Stil[counter]
				counter+=1


		#Check for nan here


		#import pdb; pdb.set_trace()
		shape = (height, width, 3, len(movmat))
		# # print(shape)
		L_RPCA = numpy.reshape(Lhat, shape,order="F")
		# print(L_RPCA.shape)
		# print(L_RPCA)
		S_RPCA = numpy.reshape(Shat, shape,order="F")
		# print(S_RPCA.shape)
		# print(S_RPCA)
		M = numpy.reshape(Mask, shape,order="F")

		L_RPCA, S_RPCA = adjustLS2_RGB_Main(L_RPCA, S_RPCA, M)

		#import pdb; pdb.set_trace()

		# # Seems like I have to convery the image back to [0..255] range?
		imageeee = L_RPCA[:,:,:,0]
		# plt.imshow(imageeee)
		plt.imsave("L.jpg", imageeee)
		# plt.show()

		self.S3_Upload_Image("L.jpg")
		

		imageeee = S_RPCA[:,:,:,0]
		#plt.imshow(imageeee)
		#plt.savefig("S.jpg")

		# (L_RPCA, Mask, height, width, size(MovMat,4), size(MovMat));

		MovMatLen = 35
		pano2RGBMovie_Main(L_RPCA, Mask, height, width, MovMatLen,numpy.array(movmat).shape)



		return "hello world", [2,3], "yay", "123", 3





