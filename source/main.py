from local_binary_patterns import LocalBinaryPatterns
from classifier import Classifier
import os
import cv2
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt

#Caputuring the Image
#---To be done---

lbp = LocalBinaryPatterns(24, 50)
data = []
labels = []

images = [os.path.join(root, name) for root, dirs, files in os.walk("../training_images") for name in files if name.endswith((".jpeg", ".jpg"))]
training, testing = train_test_split(images, test_size = 5)

#Training Phase
for imagePath in training:
	#Load the image, convert it to grayscale, and compute LBP
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  hist,bin_edges = lbp.compute(gray)

  #Plotting histogram if needed
  #plt.bar(bin_edges[:-1], hist, width = 1)
  #plt.xlim(min(bin_edges), max(bin_edges))
  #plt.show()

  #Extract the label from the image path, then update the label and data lists
  labels.append(imagePath.split("/")[-2])
  data.append(hist)

#Train classifier
classifier = Classifier("SVM")
classifier.train(data, labels)

#Testing Phase
for imagePath in testing:
	#Load the image, convert to grayscale, describe it and classify it
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  hist = lbp.compute(gray)

  prediction = classifier.predict(hist)
  print "The image was "+ str(imagePath) + " And the prediction is -> " + str(prediction)
