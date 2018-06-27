# Necessary libraries.
import os
# the code must be run by saying python3.6 <filename>
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
from skimage.color import rgb2gray

img = imread("Data/tennis/00000.jpg") #, cv2.IMREAD_GRAYSCALE)

width = len(img)
height = len(img[0])
newWidth = float(width * 0.5)
newHeight = float(height * 0.5)

# Resizing the 
# img = transform.resize(img, (newWidth, newHeight))
img = cv2.resize(img, None, fx=0.5, fy=0.5)

# For some reason this works.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#gray = rgb2gray(img)

#gray = numpy.float32(gray)
surf = cv2.xfeatures2d.SURF_create()
#points = cv2.cornerHarris(gray,2,3,0.04)
# Not sure why, but the values of the points found differs from the matlab and the python.
# For instance, matlab finds 2209 points where as the python finds 2977 points.
# The dimension are the same though. For points, it's n * 1 and for features it's n * 64.
# This is the extract features function.
points, features = surf.detectAndCompute(gray, None)
featureImage = cv2.drawKeypoints(gray, points, None)

# result = surf.detect(gray, None)
#dst = cv2.dilate(img, None)

#print(len(features[0]))
print(len(points))

plt.imshow(featureImage,cmap="gray")
plt.show()
