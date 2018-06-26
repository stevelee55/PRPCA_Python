# Necessary libraries.
import os
# the code must be run by saying python3.6 <filename>
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
from skimage.color import rgb2gray

img = imread("Data/tennis/00000.jpg", cv2.IMREAD_GRAYSCALE)

width = len(img)
height = len(img[0])
newWidth = float(width * 0.5)
newHeight = float(height * 0.5)

#img = transform.resize(img, (newWidth, newHeight))

#gray = rgb2gray(img)

#gray = numpy.float32(gray)
surf = cv2.xfeatures2d.SURF_create()
#points = cv2.cornerHarris(gray,2,3,0.04)
points, features = surf.detectAndCompute(img, None)

featureImage = cv2.drawKeypoints(img, points, None)

# result = surf.detect(gray, None)
#dst = cv2.dilate(img, None)

print(len(features))

plt.imshow(featureImage)
plt.show()
