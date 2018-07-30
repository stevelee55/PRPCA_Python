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
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
import math
import imageio
import boto3
from PIL import Image
import smtplib

from skimage import img_as_ubyte

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

emailAddress = "testemailaddress5123@gmail.com"
#Function for sending an email notification.
def sendEmailNofi():
	emailAddress = "testemailaddress5123@gmail.com"
	content = "PRPCA Finished."
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(emailAddress, "Deu04137*")
	server.sendmail(emailAddress, emailAddress, content)
	server.quit()


###############################################################

# Input Variables.

# If 'useRawVideo' is set to True, it uses 'rawVideoPath',
# which involves separating the video into frames. Otherwise,
# the pre-separated video frames will be used, which are located
# at the path indicated by 'videoFramesPath'.
useRawVideo = False
rawVideoName = "PRPCA_RAW.mov"
rawVideoPath = "." #"./Data/newData/Test/PRPCA_RAW.mov"
videoFramesPath = "." #"." #"./Data/newData/Test" #"./Data/tennis"
parameterDataName = "PRPCA_parameters.txt"
parameterDataPath = "."
resultOutputPath = "."
	# # Between 0.0 -> 1.0. 1.0 is original image size.
	# percentageToResizeTo = 0.23 # 0.5 is too slow for python, takes about 15 mins, but 0.39 or 0.43 gives decent results.
getVideoDataFromS3 = False
# Needs to be less than or equal to the numberOfVideoFrames.
numberOfFramesToUse = 35 # This may be changed based on how many frames are retreived from the video.
getParameterDataFromS3 = False


###############################################################

# Downloading video data from S3 bucket if specified.
if (getVideoDataFromS3):
	downloadVideoDataFromS3Named(rawVideoName, rawVideoPath)

# Separates given video at rawVideoPath into frames if
# 'useRawVideo' is set to True.
if (useRawVideo):
	from VideoToFrames import separateVideoIntoFrames
	separateVideoIntoFrames(rawVideoPath, rawVideoName, 2, videoFramesPath)

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
# Returned value is Mat type in opencv.
firstFrame = cv2.imread(videoFramesPath + "/" + videoFrameNames[0])

# Keep in mind that the width of the video is usually shorter
# when it is in a landscape.
imageDimension = firstFrame.shape
height = imageDimension[0]
width = imageDimension[1]
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
RGBDimension = 3
# The MovMat is a 4-D array/Matrix that has the dimension of
# newHeight * newWidth * 3 * # of frames to use.
MovMat = numpy.zeros((newHeight, newWidth, RGBDimension, numberOfFramesToUse), numpy.uint8)

# Goes through every single frame and sets it to the MovMat. Starts from frame0.jpg.
for i in range(numberOfFramesToUse):
	# Getting the specific frame and saving in the 4-D array.
	frame = cv2.imread(videoFramesPath + "/" + videoFrameNames[i])
	# cv2.resize doesn't do im2double automatically so normalizing needs to be done later.
	# Saving in 0 to 255 values, since the homography uses cv2 libraries.
	MovMat[:,:,:,i] = cv2.resize(frame, (newWidth, newHeight))

# LATER
# cv2.imshow("Test Image", cv2.normalize(MovMat[:,:,:,0], alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U, dst=None))

# Arvin. Julia. Calilng Julia.rpca. Julia optimization, precompiling, which makes it faster. Registering do it in python, part after it, use Julia, which precompilation, there is a way to do it. 
# Julia is pretty easy. Figure out inefficient

# RGB PRPCA
# Getting the return value and saving them.
instance = PRPCA_RGB()
RPCA_image, L, S, L_RPCA, S_RPCA = instance.PRPCA_RGB_Main(MovMat)
#RPCA_image, L, S, L_RPCA, S_RPCA = instance.PRPCA_RGB_Main(MovMat)
RPCA_image = img_as_ubyte(RPCA_image)
L = img_as_ubyte(L)
S = img_as_ubyte(S)
L_RPCA = img_as_ubyte(L_RPCA)
S_RPCA = img_as_ubyte(S_RPCA)

# Upload gif to the S3.
client = boto3.client("s3", aws_access_key_id="AKIAIXW57FAC5P2E3ILA", aws_secret_access_key="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")

print("Creating RPCA_image")
plt.imsave("RPCA_image.jpg", RPCA_image)
client.upload_file(resultOutputPath + "/" + "RPCA_image.jpg", "vsp-userfiles-mobilehub-602139379", "userData/RPCA_image.jpg")

print("Creating L gif...")
images = []
# Create Gif for L.
for frameCount in range(numberOfFramesToUse):
	image = L[:,:,:,frameCount]
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "L.gif", images, duration=0.08)
client.upload_file(resultOutputPath + "/" + "L.gif", "vsp-userfiles-mobilehub-602139379", "userData/L.gif")


print("Creating S gif...")
images = []
# Create Gif for S.
for frameCount in range(numberOfFramesToUse):
	image = S[:,:,:,frameCount]
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "S.gif", images, duration=0.08)
client.upload_file(resultOutputPath + "/" + "S.gif", "vsp-userfiles-mobilehub-602139379", "userData/S.gif")

print("Creating L_RPCA gif...")
images = []
# Create Gif for S.
for frameCount in range(numberOfFramesToUse):
	image = L_RPCA[:,:,:,frameCount]
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "L_RPCA.gif", images, duration=0.08)
client.upload_file(resultOutputPath + "/" + "L_RPCA.gif", "vsp-userfiles-mobilehub-602139379", "userData/L_RPCA.gif")

print("Creating Original gif...")
images = []
# Create Gif for S.
for frameCount in range(numberOfFramesToUse):
	image = MovMat[:,:,:,frameCount]
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "OG.gif", images, duration=0.08)
client.upload_file(resultOutputPath + "/" + "OG.gif", "vsp-userfiles-mobilehub-602139379", "userData/OG.gif")

print("Creating S_RPCA gif...")
images = []
# Create Gif for S.
for frameCount in range(numberOfFramesToUse):
	image = numpy.array(S_RPCA)[:,:,:,frameCount]
	images.append(image)#imageio.imread(resultOutputPath + "/" + "frame%d.jpg" % frameCount))

imageio.mimsave(resultOutputPath + "/" + "S_RPCA.gif", images, duration=0.08)
client.upload_file(resultOutputPath + "/" + "S_RPCA.gif", "vsp-userfiles-mobilehub-602139379", "userData/S_RPCA.gif")

sendEmailNofi()
# Showing the results visually.
# Panorama
# plt.imshow(RPCA_image)
# plt.show()

# Play results

# Play results in original ratio


