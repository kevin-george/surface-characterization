from phase_stretch_transform import PhaseStretchTransform
from classifier import Classifier
import os
import cv2
from sklearn.cross_validation import train_test_split

def run_iteration(iteration, hash_map):
    pst = PhaseStretchTransform()
    data = []
    labels = []

    #Finding all images
    images = [os.path.join(root, name) for root, dirs, files in os.walk("../training_images")
            for name in files if name.endswith((".jpeg", ".jpg"))]

    #Spliting it into training and testing groups
    training, testing = train_test_split(images, test_size = 0.25)

    #Training Phase
    for imagePath in training:
      #Load the image, convert it to grayscale, and compute LBP
      image = cv2.imread(imagePath)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      if imagePath in hash_map:
        hist = hash_map[imagePath]
      else:
        hist = pst.compute(gray)
        hash_map[imagePath] = hist

      print str(iteration) + " DEBUG(Training): Computed PST Histogram for " + imagePath

      #Extract the label from the image path, then update the label and data lists
      labels.append(imagePath.split("/")[-2])
      data.append(hist)

    #Train classifier
    classifier = Classifier("Chi-Squared")
    print "\n\n" + str(iteration) + " DEBUG: Training Classifier"
    classifier.train(data, labels)
    print "\n\n" + str(iteration) + " DEBUG: Trained Classifier\n\n"

    #Testing Phase
    data = []
    labels = []
    for imagePath in testing:
      #Load the image, convert to grayscale, describe it and classify it
      image = cv2.imread(imagePath)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      if imagePath in hash_map:
        hist = hash_map[imagePath]
      else:
        hist = pst.compute(gray)
        hash_map[imagePath] = hist

      print str(iteration) + " DEBUG(Testing): Computed PST Histogram for " + imagePath

      data.append(hist)
      labels.append(imagePath.split("/")[-2])

    print "\n\n" + str(iteration) + " DEBUG: Forming predictions"
    predictions = classifier.predict(data)
    counter = 0
    print "\n\n" + str(iteration) + " DEBUG: Printing predictions\n\n"
    for index, prediction in enumerate(predictions):
        print "Name -> " + testing[index] + " Actual -> " + labels[index] + " Prediction -> " + prediction
        if labels[index] == prediction:
            counter = counter + 1

    accuracy = (float(counter)/float(len(predictions))) * 100.0
    print "\n\n" + str(iteration) + " The Classifier Accuracy was " + str(accuracy) + "%"

    return accuracy
