from local_binary_patterns import LocalBinaryPatterns
from classifier import Classifier
import os
import cv2
from sklearn.cross_validation import train_test_split

#Caputuring the Image
#---To be done---

lbp = LocalBinaryPatterns(24, 8)
data = []
labels = []
#Finding all images
training = [os.path.join(root, name) for root, dirs, files in os.walk("../training_images")
        for name in files if name.endswith((".jpeg", ".jpg"))]

#Training Phase
for imagePath in training:
  #Load the image, convert it to grayscale, and compute LBP
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  hist = lbp.compute(gray)

  #Extract the label from the image path, then update the label and data lists
  labels.append(imagePath.split("/")[-2])
  data.append(hist)


#Train classifier
classifier = Classifier("Chi-Squared")
classifier.train(data, labels)

#Testing Phase
data = []
testing = [os.path.join(root, name) for root, dirs, files in os.walk("../testing_images")
        for name in files if name.endswith((".jpeg", ".jpg"))]

for imagePath in testing:
  #Load the image, convert to grayscale, describe it and classify it
  image = cv2.imread(imagePath)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  hist = lbp.compute(gray)
  data.append(hist)

predictions = classifier.predict(data)
for index, prediction in enumerate(predictions):
    print "Name -> " + testing[index] + " Prediction -> " + prediction
