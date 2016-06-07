from skimage import feature
from scipy.stats import itemfreq

class LocalBinaryPatterns:
  def __init__(self, num_of_points, radius):
    self.num_of_points = num_of_points
    self.radius = radius

  def compute(self, image):
    lbp = feature.local_binary_pattern(image, self.num_of_points,
            self.radius, method = "uniform")

    #Calculating and normalizing the histogram
    x = itemfreq(lbp.ravel())
    hist = x[:, 1]/sum(x[:, 1])

    return hist

