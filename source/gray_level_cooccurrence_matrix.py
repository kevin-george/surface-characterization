from skimage import feature
from scipy.stats import itemfreq

class GrayLevelCooccurenceMatrix:
  def __init__(self, distance, angle):
    self.distance.append(distance)
    self.angle.append(angle)

  def compute(self, image):
    glcm = feature.greycomatrix(image, self.distance, self.angle, 256,
            symmetric = True, normed = True)

    #Calculating and normalizing the histogram
    x = itemfreq(glcm.ravel())
    hist = x[:, 1]/sum(x[:, 1])

    return hist
