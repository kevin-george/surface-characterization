from sklearn.svm import LinearSVC

class Classifier:
  def __init__(self, ctype):
    self.ctype = ctype

  def train(self, data, labels):
    if self.ctype == "SVM":
      self.model = LinearSVC(C=1.0)
      self.model.fit(data, labels)
    else if self.ctype == "Decision":
      print "Unsupported"

  def predict(self, hist):
    if self.ctype == "SVM":
      return self.model.predict(hist)[0]
    else if self.ctype == "Decision":
      print "Unsupported"
    else:
      return None
