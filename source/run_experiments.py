from main_lbp_svm import run_iteration
import time

class Timer:
  def __enter__(self):
    self.start = time.clock()
    return self

  def __exit__(self, *args):
    self.end = time.clock()
    self.interval = self.end - self.start

accuracy = 0
hash_map = {}
with Timer() as t:
  for i in range(0, 10):
    accuracy += run_iteration(i, hash_map)

print "\n\n********************************"
print "Average is " + str(accuracy/10.0)
print "Time taken " + str(t.interval) + " sec"
print "********************************"
