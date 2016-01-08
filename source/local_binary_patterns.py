from skimage import feature
import numpy
import cv2
import paths
from sklearn.svm import LinearSVC

numPoints = 24
radius = 8
eps = 1e-7

data = []
labels = []

#First train linear SVM using training images
training_images = paths.list_images("../training_images")
for imagePath in training_images:
	#Load the image, convert it to grayscale, and describe it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lbp = feature.local_binary_pattern(gray, numPoints, radius, method = "uniform")
        (hist, _) = numpy.histogram(lbp.ravel(), bins = numpy.arange(0, numPoints + 2), range = (0, numPoints + 1))

        #Normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)

        #Extract the label from the image path, then update the label and data lists
	labels.append(imagePath.split("/")[-2])
	data.append(hist)

model = LinearSVC(C = 100.0, random_state = 42)
model.fit(data, labels)

#Now loop through the test images to test model
testing_images = paths.list_images("../testing_images")
for imagePath in testing_images:
	#Load the image, convert to grayscale, describe it and classify it
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	lbp = feature.local_binary_pattern(gray, numPoints, radius, method = "uniform")
        (hist, _) = numpy.histogram(lbp.ravel(), bins = numpy.arange(0, numPoints + 2), range = (0, numPoints + 1))

        #Normalize the histogram
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)

        prediction = model.predict(hist)[0]

	#Display the image and the prediction
	cv2.putText(image, prediction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
