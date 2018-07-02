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

img = imread("Data/newData/Test_Grace/frame1.jpg") #, cv2.IMREAD_GRAYSCALE)

print(img)


normImage = cv2.normalize(img.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

plt.imshow(normImage)
plt.show()

width = len(img)
height = len(img[0])
print("height", height)
print("width", width)

# # Float could affect the surf and othe things so check on them.
# newWidth = float(width * 0.5)
# newHeight = float(height * 0.5)
# print("newheight", newHeight)
# print("newwidth", newWidth)

# # Resizing the 
# # img = transform.resize(img, (newWidth, newHeight))
# img = cv2.resize(img, None, fx=0.5, fy=0.5)


# # For some reason this works.
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # gray = rgb2gray(img)

# #gray = numpy.float32(gray)
# surf = cv2.xfeatures2d.SURF_create()
# # #points = cv2.cornerHarris(gray,2,3,0.04)
# # # Not sure why, but the values of the points found differs from the matlab and the python.
# # # For instance, matlab finds 2209 points where as the python finds 2977 points.
# # # The dimension are the same though. For points, it's n * 1 and for features it's n * 64.
# # # This is the extract features function.
# points, features = surf.detectAndCompute(img, None)
# featureImage = cv2.drawKeypoints(gray, points, None)

#print(points[0].size)

#

# plt.imshow(featureImage)
# plt.show()

# tform = matplotlib.transforms.Affine2D(numpy.eye(3))
# M = numpy.array(tform)
# M = cv2.getPerspectiveTransform(gray, img)
M = numpy.array([[ 1.00421832, 2.25010209 * 10**-3, -1.34915050],[ 1.07836005 * 10**-3, 1.00230697, -3.14733685 * 10**-1],[ 9.30398327 * 10**-6, 4.26840446 * 10**-6, 1.00000000]])
M = numpy.array([[ 1.00352805, 1.56851240 * 10**-2, -300],[ 2.13974387 * 10**-3, 1.00792381, -300],[ 1.05903669 * 10**-4, 3.37836527 * 20**-4, 1.00000000]])
M = numpy.float32(M)

#([[1.0748, 0.0117, 7.8756 * 10**(-5)], [-0.0037, 1.0383, 2.8427* 10**(-5)], [-77.8843, -0.3584, 0.9957]])

# ([[1.0748, -0.0037, -77.8843], [0.0117, 1.0383, -0.3584], [7.8756**-5, 2.8427**-5, 0.9957]])
#([[1.0572, 0.0060, -75.9097], [0.0018, 1.0431, 0.7612], [4.0147**-5, 6.3568**-5, 0.9977]])
#([[1.0572, 0.0018, 4.0147**-5], [0.0060, 1.0431, 6.3568**-5], [-75.9097, 0.7612, 0.9977]])

#print(M)

print(M)

# Don't worry about the x position.
pt1 = numpy.array([0,0,1])
pt2 = numpy.array([0,width,1])
pt3 = numpy.array([height,width,1])
pt4 = numpy.array([height,0,1])

print(pt1)
print(pt2)
print(pt3)
print(pt4)

# Had problem because the width and the height were mixed up in the x and y coordinates matrix, which gave weird values. It's now fixed.
pt1 = numpy.matmul(M, pt1)
pt2 = numpy.matmul(M, pt2)
pt3 = numpy.matmul(M, pt3)
pt4 = numpy.matmul(M, pt4)



print(pt1)
print(pt2)
print(pt3)
print(pt4)


newWidth = abs((pt1[0] / 1) - (pt3[0] / 1.22613900))
newHeight = abs((771.57) - (-300))

print(newWidth)
print(newHeight)

# Changing height.
translateMatrix = [[1, 0, 300], [ 0, 1, 300],[0, 0, 1]]

# OG
plt.imshow(img)
plt.show()

# non translated
warp = cv2.warpPerspective(img, M, (int(newWidth), int(newHeight)))
#x, y, z, h = cv2.boundingRect(warp)

plt.imshow(warp)
plt.show()

# Translated 
M = numpy.matmul(translateMatrix, M)
warp = cv2.warpPerspective(img, M, (int(newWidth), int(newHeight)))
#x, y, z, h = cv2.boundingRect(warp)

plt.imshow(warp)
plt.show()



#warpedImage = cv2.warpPerspective(numpy.ones(len(img)), M, (1561, 678))
#print(warpedImage)

#plt.imshow(warp)

# result = surf.detect(gray, None)
#dst = cv2.dilate(img, None)

#print(len(features[0]))
#print(len(points))

#plt.imshow(warp, extent=[-92.6526, 1.6827 * 10**3, -258.0739, 622.4175]) #cmap="gray")
#plt.show()
