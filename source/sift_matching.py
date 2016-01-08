import cv2
import numpy
from matplotlib import pyplot as plt

# Load an color image in grayscale
img1 = cv2.imread('2_left.png', 0)
img2 = cv2.imread('2_right.png', 0)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)


# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k = 2)

# BFMatcher with default params
#bf = cv2.BFMatcher()
#matches = bf.knnMatch(des1, des2, k = 2)

# Apply ratio test
good = [] #Stores all the matching points
pts1 = []
pts2 = []

for m,n in matches:
  if m.distance < 0.8*n.distance:
    good.append(m)
    pts1.append(kp1[m.trainIdx].pt)
    pts2.append(kp2[m.queryIdx].pt)

pts1 = numpy.int32(pts1)
pts2 = numpy.int32(pts2)
F, mask = cv2.findEssentialMat(pts1, pts2, 12.0, cv2.LMEDS)

# cv2.drawMatchesKnn expects list of lists as matches.
# img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags = 2)

#plt.imshow(img3),plt.show()
