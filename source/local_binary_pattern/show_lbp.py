from local_binary_patterns import LocalBinaryPatterns
import os
import cv2
import matplotlib.pyplot as plt
from skimage import feature

lbp = LocalBinaryPatterns(24, 8)
data = []

#Finding all images
images = [os.path.join(root, name) for root, dirs, files in os.walk("../images")
        for name in files if name.endswith((".jpeg", ".jpg"))]

#Training Phase
for imagePath in images:
  #Load the image, convert it to grayscale, and compute LBP
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  lbp = feature.local_binary_pattern(gray, 24, 8, method = "uniform")
  cv2.imshow("LBP", lbp)
  cv2.waitKey(0)

  #Plotting histogram if needed
  #plt.bar(bin_edges[:-1], hist, width = 1)
  #plt.xlim(min(bin_edges), max(bin_edges))
  #plt.show()
