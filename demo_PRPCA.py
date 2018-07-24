# -*- coding: utf-8 -*-
# Panoramic Robust PCA demo in Python.
# Written by Steve Lee
# 
# Algorithm originally created and written in MatLab
# by Chen Gao
# chengao@umich.edu
#
# June 18, 2018

# Necessary Libraries.

import os
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
import math
import imageio
import boto3
from PIL import Image


# Custom Class.

from PRPCA_RGB import PRPCA_RGB

###############################################################

# Helper Functions.

# Downloads raw video data from S3 bucket. 
def downloadVideoDataFromS3Named(rawVideoName, rawVideoPath):
	# Download the file.
	# Connecting to S3.
	# Do not hard code credentials
	# boto3.client not available if there are spaces.
	client = boto3.client("s3", aws_access_key_id="AKIAIXW57FAC5P2E3ILA", aws_secret_access_key="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")
	client.download_file("vsp-userfiles-mobilehub-602139379", "userData/" + rawVideoName, rawVideoPath + "/" + rawVideoName)

	# Store at the given video path.

def downloadParameterDataFromS3(parameterDataName, parameterDataPath):
	client = boto3.client("s3", aws_access_key_id="AKIAIXW57FAC5P2E3ILA", aws_secret_access_key="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")
	client.download_file("vsp-userfiles-mobilehub-602139379", "userData/" + parameterDataName, parameterDataPath + "/" + parameterDataName)

def parseDownloadedParameterData():
	return "Hello"


###############################################################

# Input Variables.

# If 'useRawVideo' is set to True, it uses 'rawVideoPath',
# which involves separating the video into frames. Otherwise,
# the pre-separated video frames will be used, which are located
# at the path indicated by 'videoFramesPath'.
useRawVideo = True
rawVideoName = "PRPCA_RAW.mov"
rawVideoPath = "." #"./Data/newData/Test/PRPCA_RAW.mov"
videoFramesPath = "." #"." #"./Data/newData/Test" #"./Data/tennis"
parameterDataName = "PRPCA_parameters.txt"
parameterDataPath = "."
resultOutputPath = "."
	# # Between 0.0 -> 1.0. 1.0 is original image size.
	# percentageToResizeTo = 0.23 # 0.5 is too slow for python, takes about 15 mins, but 0.39 or 0.43 gives decent results.
getVideoDataFromS3 = True
# Needs to be less than or equal to the numberOfVideoFrames.
numberOfFramesToUse = 25 # This may be changed based on how many frames are retreived from the video.
getParameterDataFromS3 = False


###############################################################

# Downloading video data from S3 bucket if specified.
if (getVideoDataFromS3):
	downloadVideoDataFromS3Named(rawVideoName, rawVideoPath)

# Separates given video at rawVideoPath into frames if
# 'useRawVideo' is set to True.
if (useRawVideo):
	from VideoToFrames import separateVideoIntoFrames
	separateVideoIntoFrames(rawVideoPath, rawVideoName, 3, videoFramesPath)

# Getting the parameter data from S3 bucket if specified.
if (getParameterDataFromS3):
	parsedData = downloadParameterDataFromS3(parameterDataName, parameterDataPath)


###############################################################

# Below does L + S RGB.

# Getting the list of frames' names and sorting them.
fileNames = os.listdir(videoFramesPath + "/")

# Getting and saving each of the frame data using the
# list of frames' names.
videoFrameNames = []
for fileName in fileNames:
	if fileName.endswith('.jpg'):
		videoFrameNames.append(fileName)
# Sorting the videoFrameNames, because time to time,
# the frames get read in randomly, which affects the
# whole program.
videoFrameNames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print(videoFrameNames)
# Getting the total number of video frames.
numberOfVideoFrames = len(videoFrameNames)

# Deciding how many frames to actually use based on number of total video frames.
# If the user specified number frames is less than the total number of frames, use
# specified number of frames. Else, use max number of available frames.
if (numberOfFramesToUse > numberOfVideoFrames):
	numberOfFramesToUse = numberOfVideoFrames

# Getting the width and height of the video using the
# first frame of the video.
firstFrame = imread(videoFramesPath + "/" + videoFrameNames[0])

# Keep in mind that the width of the video is usually shorter
# when it is in a landscape.
height = len(firstFrame)
width = len(firstFrame[0])
# Calculate the ideal video frame size based on the recommended values.
recommendedWidth = 427.0
multiplier = 1.0
if (width > recommendedWidth):
	multiplier = recommendedWidth / width

newHeight = math.floor(float(height * multiplier))
newWidth = math.floor(float(width * multiplier))
print("Width",newWidth)
print("Height",newHeight)

# Initializing the 4-D Matrix with 0s.
RGBCount = 3
# The MovMat is a 4-D array/Matrix that has the dimension of
# height * width * 3 * # of frames.
MovMat = [[[[0 for x in range(newHeight)] for y in range(newWidth)] for m in range(RGBCount)] for z in range(numberOfFramesToUse)]

# Goes through every single frame and sets it to the MovMat. Starts from frame0.jpg.
for i in range(numberOfFramesToUse):
	# Getting the specific frame and saving in the 4-D array.
	frame = imread(videoFramesPath + "/" + videoFrameNames[i])
	# cv2.resize doesn't do im2double automatically so normalizing needs to be done later.
	MovMat[i] = cv2.resize(frame, None, fx=multiplier, fy=multiplier)


# Arvin. Julia. Calilng Julia.rpca. Julia optimization, precompiling, which makes it faster. Registering do it in python, part after it, use Julia, which precompilation, there is a way to do it. 
# Julia is pretty easy. Figure out inefficient

# RGB PRPCA
# Getting the return value and saving them.
instance = PRPCA_RGB()
L_RPCA = instance.PRPCA_RGB_Main(MovMat)
#RPCA_image, L, S, L_RPCA, S_RPCA = instance.PRPCA_RGB_Main(MovMat)

print("FINAL",len(L_RPCA))
images = []
# Create Gif.
for frameCount in range(numberOfFramesToUse):
	frameData = L_RPCA[:,:,:,frameCount]
	image = numpy.array(Image.fromarray((frameData * 255).astype(numpy.uint8)))
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "L_RPCA.gif", images, duration=0.08)

# Upload gif to the S3.
client = boto3.client("s3", aws_access_key_id="AKIAIXW57FAC5P2E3ILA", aws_secret_access_key="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")
client.upload_file(resultOutputPath + "/" + "L_RPCA.gif", "vsp-userfiles-mobilehub-602139379", "userData/PRPCA_Finished.gif")


# Showing the results visually.
# Panorama
# plt.imshow(RPCA_image)
# plt.show()

# Play results

# Play results in original ratio


