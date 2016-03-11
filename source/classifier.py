from sklearn.svm import LinearSVC
import cv2
import numpy as np

class Classifier:
  def __init__(self, ctype):
    self.ctype = ctype

  def train(self, data, labels):
    if self.ctype == "SVM":
      self.model = LinearSVC()
      self.model.fit(data, labels)
    elif self.ctype == "Decision":
      print "Unsupported"
    elif self.ctype == "Chi-Squared":
      self.model_data = data
      self.model_labels = labels

  def predict(self, data):
    if self.ctype == "SVM":
      return self.model.predict(data)
    elif self.ctype == "Decision":
      print "Unsupported"
    elif self.ctype == "Chi-Squared":
      predictions = []
      for sample, test_hist in enumerate(data):
        #Storing the first distance by default
        lowest_score = cv2.compareHist(np.array(self.model_data[0], dtype = np.float32),
                np.array(test_hist, dtype = np.float32), method = 1)
        predictions.append(self.model_labels[0])
        #Going through the rest of data
        for index, train_hist in enumerate(self.model_data):
          score = cv2.compareHist(np.array(train_hist, dtype = np.float32),
                np.array(test_hist, dtype = np.float32), method = 1)
          if score < lowest_score:
            lowest_score = score
            predictions[sample] = self.model_labels[index]
      return predictions


