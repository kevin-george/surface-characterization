from skimage import feature
import numpy

class LocalBinaryPatterns:
  def __init__(self, num_of_points, radius):
    self.num_of_points = num_of_points
    self.radius = radius

  def compute(self, image, eps = 1e-7):
    lbp = feature.local_binary_pattern(image, self.num_of_points, self.radius, method = "uniform")
    (hist, bin_edges) = numpy.histogram(lbp.ravel(), bins = numpy.arange(0, self.num_of_points + 2), range = (0, self.num_of_points + 1))

    #Normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + eps)

    return hist, bin_edges

