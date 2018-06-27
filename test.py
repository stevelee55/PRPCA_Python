# Necessary libraries.
import os
# the code must be run by saying python3.6 <filename>
from imread import imread
import matplotlib.pyplot as plt
from skimage import transform
import cv2
import numpy
from skimage.color import rgb2gray
import matplotlib.transforms

img = imread("Data/newData/frame1.jpg") #, cv2.IMREAD_GRAYSCALE)

width = len(img)
height = len(img[0])
newWidth = int(width * 0.5)
newHeight = int(height * 0.5)

# Resizing the 
# img = transform.resize(img, (newWidth, newHeight))
img = cv2.resize(img, None, fx=0.5, fy=0.5)


# For some reason this works.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#gray = rgb2gray(img)

#gray = numpy.float32(gray)
# surf = cv2.xfeatures2d.SURF_create()
# #points = cv2.cornerHarris(gray,2,3,0.04)
# # Not sure why, but the values of the points found differs from the matlab and the python.
# # For instance, matlab finds 2209 points where as the python finds 2977 points.
# # The dimension are the same though. For points, it's n * 1 and for features it's n * 64.
# # This is the extract features function.
# points, features = surf.detectAndCompute(gray, None)
# featureImage = cv2.drawKeypoints(gray, points, None)

# tform = matplotlib.transforms.Affine2D(numpy.eye(3))
# M = numpy.array(tform)
#M = cv2.getPerspectiveTransform(gray, img)
M = numpy.float32([[1.0748, -0.0037, -77.8843], [0.0117, 1.0383, -0.3584], [7.8756 * 10**(-5), 2.8427* 10**(-5), 0.9957]])

#([[1.0748, 0.0117, 7.8756 * 10**(-5)], [-0.0037, 1.0383, 2.8427* 10**(-5)], [-77.8843, -0.3584, 0.9957]])

# ([[1.0748, -0.0037, -77.8843], [0.0117, 1.0383, -0.3584], [7.8756**-5, 2.8427**-5, 0.9957]])
#([[1.0572, 0.0060, -75.9097], [0.0018, 1.0431, 0.7612], [4.0147**-5, 6.3568**-5, 0.9977]])
#([[1.0572, 0.0018, 4.0147**-5], [0.0060, 1.0431, 6.3568**-5], [-75.9097, 0.7612, 0.9977]])

print(M)

warp = cv2.warpPerspective(img, M, (1561, 678))

plt.imshow(warp)

# result = surf.detect(gray, None)
#dst = cv2.dilate(img, None)

#print(len(features[0]))
#print(len(points))

#plt.imshow(warp, extent=[-92.6526, 1.6827 * 10**3, -258.0739, 622.4175]) #cmap="gray")
plt.show()
