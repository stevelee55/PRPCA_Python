import cv2
import math
print(cv2.__version__)

vidcap = cv2.VideoCapture("test.MOV")
frameRate = 2
#vidcap.set(cv2.CAP_PROP_POS_MSEC,20000)
success,image = vidcap.read()
count = 0
frameNumberCount = 0
success = True
while success:
	frameId = vidcap.get(1)
	success,image = vidcap.read()
	if (frameId % math.floor(frameRate) == 0):
		frameNumberCount += 1
		cv2.imwrite("frame%d.jpg" % frameNumberCount, image)     # save frame as JPEG file
		print ("Read a new frame: ", success)
		
	count += 1