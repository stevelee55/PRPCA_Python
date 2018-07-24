import cv2
import math

# Separates the video into frames and saves the frames in the current working
# directory.
def separateVideoIntoFrames(rawVideoPath, rawVideoName, frameRate, videoFramesPath):
	# Getting the video from the given video path.
	capturedVideo = cv2.VideoCapture(rawVideoPath + "/" + rawVideoName)
	# Ideal frameRate is 3.
	#vidcap.set(cv2.CAP_PROP_POS_MSEC,20000)
	isSuccess, frame = capturedVideo.read()

	# Prompts the user if the captured video cannot be read for some reason.
	if (isSuccess):
		# Variables needed for looping through the video frames.
		currentFrameCount = 0
		isSuccess = True
		while isSuccess:
			frameId = capturedVideo.get(1)
			isSuccess, frame = capturedVideo.read()
			if (frameId % math.floor(frameRate) == 0):
				
				# save frame as jpg file
				cv2.imwrite(videoFramesPath + "/frame%d.jpg" % currentFrameCount, frame)
				print("Saved frame #: ", currentFrameCount)
				currentFrameCount += 1

		# Prompts the user when the program is finished converting.
		print("Finished converting video into frames.")
	else:
		print("Error: Specified video cannot be read.")